import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "python"))
from readrinex import get_eph, readrinex


def test_readrinex_success():
    mock_data = MagicMock()
    with patch("readrinex.gr.load", return_value=mock_data):
        result = readrinex("test.19n")
        unittest.TestCase().assertIsNotNone(result)


def test_readrinex_error():
    with patch("readrinex.gr.load", side_effect=Exception("Error")):
        result = readrinex("bad.19n")
        unittest.TestCase().assertIsNone(result)


def test_get_eph_all():
    mock_data = MagicMock()
    result = get_eph(mock_data)
    unittest.TestCase().assertEqual(result, mock_data)


def test_get_eph_specific():
    mock_data = MagicMock()
    mock_data.sel.return_value.dropna.return_value = mock_data
    result = get_eph(mock_data, "G01")
    unittest.TestCase().assertIsNotNone(result)
