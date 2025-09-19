import pytest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'python'))
from readrinex import readrinex, get_eph


def test_readrinex_success():
    mock_data = MagicMock()
    with patch('readrinex.gr.load', return_value=mock_data):
        result = readrinex('test.19n')
        assert result is not None


def test_readrinex_error():
    with patch('readrinex.gr.load', side_effect=Exception("Error")):
        result = readrinex('bad.19n')
        assert result is None


def test_get_eph_all():
    mock_data = MagicMock()
    result = get_eph(mock_data)
    assert result == mock_data


def test_get_eph_specific():
    mock_data = MagicMock()
    mock_data.sel.return_value.dropna.return_value = mock_data
    result = get_eph(mock_data, 'G01')
    assert result is not None
