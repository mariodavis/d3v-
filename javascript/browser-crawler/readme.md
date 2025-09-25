## How to use
Open the website you want to test.

Open DevTools → Console (F12 or Ctrl+Shift+I).

Paste the entire script above into the console and hit Enter.

You’ll see:

✅ Site Enumerator loaded. Try:
   await __siteCrawler.lightScan()
   await __siteCrawler.fullScan()
   await __siteCrawler.bruteScan()


##  Run one of the helper scans:

await __siteCrawler.lightScan() → quick scan, no download.

await __siteCrawler.fullScan() → deeper scan, follows sitemap, downloads JSON.

await __siteCrawler.bruteScan() → quick scan + tries common hidden paths.

Check your downloads folder for results (site-enum-<host>-<timestamp>.json).
