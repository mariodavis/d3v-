from __future__ import annotations
from pathlib import Path
from typing import Union
from PyPDF2 import PdfReader, PdfWriter

PDFPath = Union[str, Path]


def encrypt_pdf(input_path: PDFPath, output_path: PDFPath, password: str) -> Path:
    """
    Encrypts a PDF file with a password and saves it to output_path.
    Returns the path to the encrypted file.
    """
    in_path = Path(input_path)
    out_path = Path(output_path)

    reader = PdfReader(in_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(password)

    with out_path.open("wb") as f:
        writer.write(f)

    return out_path


def encrypt_with_suffix(input_path: PDFPath, password: str, suffix: str = "_encrypted") -> Path:
    """
    Creates an encrypted copy next to the original file.
    Example:
    secret.pdf → secret_encrypted.pdf
    """
    in_path = Path(input_path)
    output_path = in_path.with_name(f"{in_path.stem}{suffix}{in_path.suffix}")
    return encrypt_pdf(in_path, output_path, password)


if __name__ == "__main__":
    pdf_file = "/home/kali/Downloads/P3.pdf"     
    pdf_password = "pythontoday"

    encrypted_path = encrypt_with_suffix(pdf_file, pdf_password)
    print(f"Encrypted file created: {encrypted_path}")
