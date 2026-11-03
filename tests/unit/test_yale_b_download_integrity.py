"""Offline tests for Yale B download completeness and safe replacement."""

import io

import numpy as np
import pytest
import scipy.io as sio

from icc.datasets.image import _download_file, download_yale_b


def _valid_mat_bytes() -> bytes:
    buffer = io.BytesIO()
    sio.savemat(
        buffer,
        {
            "fea": np.zeros((2414, 1024), dtype=np.uint8),
            "gnd": np.zeros((2414, 1), dtype=np.uint8),
        },
        do_compression=True,
    )
    return buffer.getvalue()


class _FakeResponse(io.BytesIO):
    def __init__(self, body: bytes, content_length: int):
        super().__init__(body)
        self.headers = {"Content-Length": str(content_length)}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()


def test_download_writes_only_valid_mat_atomically(tmp_path, monkeypatch):
    payload = _valid_mat_bytes()
    monkeypatch.setattr(
        "urllib.request.urlopen",
        lambda *args, **kwargs: _FakeResponse(payload, len(payload)),
    )
    dest = tmp_path / "YaleB_32x32.mat"
    _download_file("http://example.invalid/yale.mat", str(dest))
    assert dest.exists()
    mat = sio.loadmat(dest, variable_names=["fea", "gnd"])
    assert mat["fea"].shape == (2414, 1024)
    assert mat["gnd"].size == 2414
    assert not (tmp_path / "YaleB_32x32.mat.part").exists()


def test_truncated_download_does_not_create_or_replace_target(tmp_path, monkeypatch):
    payload = _valid_mat_bytes()
    dest = tmp_path / "YaleB_32x32.mat"
    original = b"preserve-existing-file"
    dest.write_bytes(original)
    monkeypatch.setattr(
        "urllib.request.urlopen",
        lambda *args, **kwargs: _FakeResponse(payload[:-32], len(payload)),
    )
    with pytest.raises(OSError, match="Incomplete Yale B download"):
        _download_file("http://example.invalid/yale.mat", str(dest))
    assert dest.read_bytes() == original
    assert not (tmp_path / "YaleB_32x32.mat.part").exists()


def test_existing_corrupt_file_is_not_accepted_or_silently_replaced(tmp_path):
    dest = tmp_path / "YaleB_32x32.mat"
    original = b"truncated MATLAB data"
    dest.write_bytes(original)
    with pytest.raises(RuntimeError, match="Existing Yale B file is incomplete or invalid"):
        download_yale_b(raw_dir=str(tmp_path))
    assert dest.read_bytes() == original
