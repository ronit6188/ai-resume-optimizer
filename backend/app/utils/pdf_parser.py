"""Utility to extract plain text from a PDF file using pdfminer.six.

The function returns a string (Unicode) with the extracted text. It works on the
binary PDF data stored in the database or the uploaded file stream.
"""

from __future__ import annotations

import io
from typing import Union

from pdfminer.high_level import extract_text


def extract_text_from_pdf(data: Union[bytes, io.BytesIO]) -> str:
    """Extract UTF‑8 text from a PDF.

    * `data` can be a `bytes` object (from DB) or a `BytesIO` (uploaded file).
    * Returns an empty string on failure – callers should handle the case.
    """
    if isinstance(data, bytes):
        stream = io.BytesIO(data)
    else:
        stream = data
    try:
        text = extract_text(stream)
        return text.strip()
    except Exception as exc:
        # In production you would log the error – we keep it simple here.
        return ""
