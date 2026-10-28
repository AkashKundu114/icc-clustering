"""Unit tests for scripts/verify_refs.py with mocked API calls."""
import json
import os
import sys
from unittest.mock import MagicMock, patch
import pytest

# Ensure scripts directory is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
import verify_refs as vr


def test_norm_and_sim():
    assert vr.norm("Hello, World!--") == "hello world"
    assert vr.sim("Machine Learning", "Machine Learning") == 1.0
    assert vr.sim("Machine Learning", "Deep Learning") < 0.9


def test_compare_matching_entry_ok():
    entry = {
        "title": "Fast Clustering with Anchor Guidance",
        "author": "Feiping Nie and Jing Xue and Dingyuan Yu and Xuelong Li",
        "year": "2024",
        "volume": "46",
        "pages": "1898--1912",
        "journal": "IEEE Transactions on Pattern Analysis and Machine Intelligence",
    }
    api_rec = {
        "title": "Fast Clustering With Anchor Guidance",
        "authors": ["Nie", "Xue", "Yu", "Li"],
        "year": 2024,
        "volume": "46",
        "pages": "1898-1912",
        "venue": "IEEE Transactions on Pattern Analysis and Machine Intelligence",
        "source": "crossref",
        "doi": "10.1109/TPAMI.2023.3318603",
    }
    flags = vr.compare(entry, api_rec)
    assert flags == []
    assert not (vr.HARD & set(flags))


def test_compare_wrong_volume_mismatch():
    entry = {
        "title": "RFAG: Random forest clustering based on anchor graph",
        "author": "Jinyu Li and Congyu Wang and Mingjing Du",
        "year": "2026",
        "volume": "172",
        "pages": "112997",
        "journal": "Pattern Recognition",
    }
    api_rec = {
        "title": "RFAG: Random forest clustering based on anchor graph",
        "authors": ["Li", "Wang", "Du"],
        "year": 2026,
        "volume": "174",
        "pages": "112997",
        "venue": "Pattern Recognition",
        "source": "crossref",
    }
    flags = vr.compare(entry, api_rec)
    assert "VOLUME" in flags
    assert bool(vr.HARD & set(flags))


def test_compare_wrong_first_author_mismatch():
    entry = {
        "title": "Sample Paper Title",
        "author": "John Doe and Jane Smith",
        "year": "2020",
    }
    api_rec = {
        "title": "Sample Paper Title",
        "authors": ["Smith", "Doe"],
        "year": 2020,
        "volume": None,
        "pages": None,
        "venue": "",
        "source": "crossref",
    }
    flags = vr.compare(entry, api_rec)
    assert "FIRST_AUTHOR" in flags
    assert bool(vr.HARD & set(flags))


def test_compare_arxiv_published_version_exists():
    entry = {
        "title": "Preprint Paper Title",
        "author": "Author One and Author Two",
        "year": "2023",
        "journal": "arXiv",
    }
    api_rec = {
        "title": "Preprint Paper Title",
        "authors": ["One", "Two"],
        "year": 2023,
        "volume": None,
        "pages": None,
        "venue": "arXiv",
        "source": "arxiv",
        "doi": "10.1016/j.jcp.2024.1000",
        "journal_ref": "J. Comput. Phys. 2024",
    }
    flags = vr.compare(entry, api_rec)
    assert "PUBLISHED_VERSION_EXISTS" in flags
    # PUBLISHED_VERSION_EXISTS is a warning, not in HARD
    assert not (vr.HARD & set(flags))


def test_crossref_by_doi_mocked():
    mock_payload = {
        "message": {
            "title": ["Fast Clustering with Anchor Guidance"],
            "author": [
                {"family": "Nie"},
                {"family": "Xue"},
                {"family": "Yu"},
                {"family": "Li"},
            ],
            "container-title": ["IEEE Transactions on Pattern Analysis and Machine Intelligence"],
            "issued": {"date-parts": [[2024]]},
            "volume": "46",
            "page": "1898-1912",
            "DOI": "10.1109/TPAMI.2023.3318603",
            "type": "journal-article",
        }
    }
    with patch("requests.get") as mock_get:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = mock_payload
        mock_get.return_value = mock_resp

        rec = vr.crossref_by_doi("10.1109/TPAMI.2023.3318603")
        assert rec is not None
        assert rec["title"] == "Fast Clustering with Anchor Guidance"
        assert rec["year"] == 2024
        assert rec["volume"] == "46"
        assert rec["pages"] == "1898-1912"


def test_arxiv_rec_mocked():
    xml_data = """<?xml version="1.0" encoding="UTF-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom" xmlns:ax="http://arxiv.org/schemas/atom">
      <entry>
        <title>CoHiRF: Hierarchical Consensus for Interpretable Clustering Beyond Scalability Limits</title>
        <author><name>Katia Meziani</name></author>
        <author><name>Bruno Belucci</name></author>
        <published>2025-02-01T00:00:00Z</published>
      </entry>
    </feed>
    """
    with patch("requests.get") as mock_get:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = xml_data
        mock_get.return_value = mock_resp

        rec = vr.arxiv_rec("2502.00380")
        assert rec is not None
        assert "CoHiRF" in rec["title"]
        assert rec["authors"] == ["Meziani", "Belucci"]
        assert rec["year"] == 2025


def test_main_pipeline_with_mock(tmp_path):
    # Test main pipeline handling OK, MANUAL, MISMATCH, NOT_FOUND, CHECK_ID
    bib_content = """
@article{paper_ok,
  author = {Alice Smith},
  title = {Paper Alpha},
  year = {2022},
  volume = {10},
  doi = {10.1000/alpha}
}
@article{paper_manual,
  author = {Bob Jones},
  title = {Paper Beta Technical Report},
  year = {1985}
}
"""
    bib_file = tmp_path / "test.bib"
    bib_file.write_text(bib_content, encoding="utf-8")

    manual_csv = tmp_path / "manual.csv"
    manual_csv.write_text("key,url,verified_by,date\npaper_manual,http://example.com,manual,2026-10-28\n", encoding="utf-8")

    out_csv = tmp_path / "report.csv"

    mock_rec = {
        "title": "Paper Alpha",
        "authors": ["Smith"],
        "year": 2022,
        "volume": "10",
        "issue": None,
        "pages": None,
        "venue": "",
        "source": "crossref",
        "doi": "10.1000/alpha",
        "type": "journal-article",
    }

    with patch("verify_refs.crossref_by_doi", return_value=mock_rec):
        test_args = ["verify_refs.py", str(bib_file), "--out", str(out_csv), "--manual", str(manual_csv)]
        with patch.object(sys, "argv", test_args):
            vr.main()

    assert os.path.exists(out_csv)
    with open(out_csv, encoding="utf-8") as f:
        content = f.read()
    assert "paper_ok,doi,OK" in content
    assert "paper_manual,manual,MANUAL" in content
