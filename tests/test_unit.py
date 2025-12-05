import pytest
import sys
import os

from clasificador_logic import (
    normalizar_unicode,
    normalize_filename,
    get_filename_without_extension,
    sanitize_folder_name,
    find_column_name
)

class TestClasificadorLogic:
    
    def test_normalizar_unicode(self):
        # Test basic string
        assert normalizar_unicode("hola") == "hola"
        # Test unicode composition (n + ~ = ñ)
        n_tilde_composed = "\u00F1" # ñ
        n_tilde_decomposed = "\u006E\u0303" # n + ~
        assert normalizar_unicode(n_tilde_decomposed) == n_tilde_composed
        
    def test_normalize_filename(self):
        # Test lowercase and trim
        assert normalize_filename("  FILE.pdf  ") == "file.pdf"
        # Test accents removal
        assert normalize_filename("Camión.pdf") == "camion.pdf"
        # Test multiple spaces
        assert normalize_filename("file  name.pdf") == "file name.pdf"
        # Test unicode normalization in filename
        assert normalize_filename("A\u0301rbol.pdf") == "arbol.pdf"

    def test_get_filename_without_extension(self):
        assert get_filename_without_extension("file.pdf") == "file"
        assert get_filename_without_extension("archive.tar.gz") == "archive.tar"
        assert get_filename_without_extension("simple") == "simple"
        assert get_filename_without_extension("") == ""

    def test_sanitize_folder_name(self):
        assert sanitize_folder_name("Folder Name") == "Folder_Name"
        assert sanitize_folder_name("A & B") == "A_and_B"
        assert sanitize_folder_name("Invalid/Chars:*?") == "InvalidChars"
        
    def test_find_column_name(self):
        headers = ["File Name", "Area", "Date"]
        
        # Exact match (case insensitive)
        assert find_column_name(headers, ["file name"]) == "File Name"
        
        # Partial match
        assert find_column_name(headers, ["file"]) == "File Name"
        
        # No match
        assert find_column_name(headers, ["NonExistent"]) is None
