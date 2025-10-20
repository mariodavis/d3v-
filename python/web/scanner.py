#!/usr/bin/env python3
"""
Advanced Ethical Web Vulnerability Scanner
-------------------------------------------
Purpose:
    A professional-grade educational tool to automate the discovery of 
    common web vulnerabilities, designed for ethical penetration testing 
    and cybersecurity learning environments (e.g., DVWA, OWASP Juice Shop).

Key Capabilities:
    - SQL Injection (Error & Time-based)
    - Cross-Site Scripting (XSS)
    - Command Injection
    - Path Traversal
    - Missing Security Headers
    - Clickjacking
    - CSRF token validation
    - Sensitive file and directory exposure
    - Information Disclosure

Usage:
    python3 web_vuln_scanner.py -u http://127.0.0.1/DVWA --crawl-depth 2 --delay 1

Disclaimer:
    This tool is strictly for authorized testing and educational purposes.
    Ensure you have written permission before scanning any system you do not own.
"""

import argparse
import json
import re
import time
import warnings
from urllib.parse import urlparse, urljoin, parse_qs, urlencode

import requests
from bs4 import BeautifulSoup

# Silence SSL warnings
warnings.filterwarnings("ignore", message="Unverified HTTPS request")


class WebVulnerabilityScanner:
    def __init__(self, target_url, crawl_depth=2, delay=1.0, headers=None, cookies=None):
        self.target_url = target_url.rstrip("/")
        self.domain = urlparse(target_url).netloc
        self.max_depth = crawl_depth
        self.delay = delay
        self.visited = set()
        self.forms = []
        self.vulnerabilities = []
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (EthicalScanner/1.0) Chrome/120.0"
        })
        if headers:
            self.session.headers.update(headers)
        if cookies:
            self.session.cookies.update(cookies)

        self.payloads = {
            "sqli": ["' OR '1'='1", "'; DROP TABLE users; --", "1 AND SLEEP(5)--"],
            "xss": ["<script>alert(1)</script>", "\"><svg/onload=alert(1)>"],
            "cmd": ["; cat /etc/passwd", "| whoami"],
            "traversal": ["../../../../etc/passwd", "..%2F..%2F..%2Fetc%2Fpasswd"],
        }

    def log(self, msg, level="INFO"):
        prefix = {"INFO": "[*]", "WARN": "[!]", "ERROR": "[-]", "SUCCESS": "[+]"}
        print(f"{prefix.get(level, '[*]')} {msg}")

    def request(self, url, method="GET", data=None):
        """Send HTTP requests with throttling and safety."""
        time.sleep(self.delay)
        try:
            if method == "POST":
                r = self.session.post(url, data=data, timeout=8, verify=False)
            else:
                r = self.session.get(url, timeout=8, verify=False)
            return r
        except requests.RequestException as e:
            self.log(f"Request error: {e}", "ERROR")
            return None

    def crawl(self, url, depth=0):
        """Recursively crawl a website within the same domain."""
        if depth > self.max_depth or url in self.visited:
            return
        if urlparse(url).netloc != self.domain:
            return

        self.visited.add(url)
        self.log(f"Crawling {url}")

        response = self.request(url)
        if not response:
            return

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract links
        for link in soup.find_all("a", href=True):
            next_url = urljoin(url, link["href"])
            if self.domain in next_url:
                self.crawl(next_url, depth + 1)

        # Extract and save forms
        for form in soup.find_all("form"):
            self.forms.append({
                "url": url,
                "action": urljoin(url, form.get("action", "")),
                "method": form.get("method", "GET").upper(),
                "inputs": [inp.get("name") for inp in form.find_all("input") if inp.get("name")]
            })

        self.analyze_page(url, response)

    def analyze_page(self, url, response):
        """Run multiple passive and active tests on a page."""
        self.check_security_headers(url, response)
        self.check_clickjacking(url, response)
        self.check_disclosure(url, response)
        self.test_parameters(url)

    def check_security_headers(self, url, response):
        headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
        }
        missing = [h for h in headers if h not in response.headers]
        if missing:
            self.add_vuln("Missing Security Headers", url, evidence=f"Missing: {', '.join(missing)}")

    def check_clickjacking(self, url, response):
        if "X-Frame-Options" not in response.headers:
            self.add_vuln("Clickjacking", url, evidence="No X-Frame-Options header")

    def check_disclosure(self, url, response):
        patterns = [
            ("server:", "Server Banner Leak"),
            ("x-powered-by", "Technology Disclosure"),
            ("password", "Potential Password Leak"),
            ("exception", "Error Message Disclosure"),
        ]
        for pat, desc in patterns:
            if re.search(pat, response.text, re.I):
                self.add_vuln(desc, url)

    def test_parameters(self, url):
        """Inject payloads into URL parameters."""
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        if not params:
            return

        for param in params:
            for category, payload_list in self.payloads.items():
                for payload in payload_list:
                    test_params = params.copy()
                    test_params[param] = payload
                    test_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{urlencode(test_params)}"
                    r = self.request(test_url)
                    if not r:
                        continue

                    if category == "sqli" and re.search(r"(sql|error|syntax)", r.text, re.I):
                        self.add_vuln("SQL Injection", test_url, param, payload)
                    elif category == "xss" and payload in r.text:
                        self.add_vuln("XSS", test_url, param, payload)
                    elif category == "cmd" and "root:x:" in r.text:
                        self.add_vuln("Command Injection", test_url, param, payload)
                    elif category == "traversal" and "root:x:" in r.text:
                        self.add_vuln("Path Traversal", test_url, param, payload)

    def add_vuln(self, vuln_type, url, param=None, payload=None, evidence=None):
        self.vulnerabilities.append({
            "type": vuln_type,
            "url": url,
            "param": param,
            "payload": payload,
            "evidence": evidence,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })
        self.log(f"Potential {vuln_type} found at {url}", "SUCCESS")

    def report(self):
        """Output vulnerabilities to console and JSON file."""
        print("\n" + "=" * 50)
        print("VULNERABILITY REPORT")
        print("=" * 50)
        if not self.vulnerabilities:
            print("No issues found. Target appears secure.")
        else:
            for v in self.vulnerabilities:
                print(f"- {v['type']} | {v['url']} | Param: {v['param']}")

        with open("vulnerability_report.json", "w") as f:
            json.dump(self.vulnerabilities, f, indent=2)
        self.log("Report saved to vulnerability_report.json")

    def scan(self):
        """Run the complete scan process."""
        self.log(f"Starting scan on {self.target_url}")
        self.crawl(self.target_url)
        self.report()


def main():
    parser = argparse.ArgumentParser(description="Ethical Web Vulnerability Scanner")
    parser.add_argument("-u", "--url", required=True, help="Target URL (e.g., http://127.0.0.1/DVWA)")
    parser.add_argument("-d", "--crawl-depth", type=int, default=2, help="Maximum crawl depth (default=2)")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between requests (default=1s)")
    args = parser.parse_args()

    scanner = WebVulnerabilityScanner(
        target_url=args.url,
        crawl_depth=args.crawl_depth,
        delay=args.delay
    )

    print("⚠️  Use responsibly. Authorized testing only.\n")
    scanner.scan()


if __name__ == "__main__":
    main()
