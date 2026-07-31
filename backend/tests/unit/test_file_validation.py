"""
Unit tests for file validator and storage manager utilities.
"""

import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from app.utils.file_validation import validate_resume_file


def test_validate_pdf_file():
    mock_file = MagicMock()
    mock_file.filename = "my_resume.pdf"
    mock_file.content_type = "application/pdf"

    filename, ext = validate_resume_file(mock_file)
    assert filename == "my_resume.pdf"
    assert ext == "pdf"


def test_validate_docx_file():
    mock_file = MagicMock()
    mock_file.filename = "my_resume.docx"
    mock_file.content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    filename, ext = validate_resume_file(mock_file)
    assert filename == "my_resume.docx"
    assert ext == "docx"


def test_invalid_extension_raises_400():
    mock_file = MagicMock()
    mock_file.filename = "malicious_script.exe"
    mock_file.content_type = "application/x-msdownload"

    with pytest.raises(HTTPException) as exc_info:
        validate_resume_file(mock_file)
    assert exc_info.value.status_code == 400
    assert "Invalid file type" in exc_info.value.detail
