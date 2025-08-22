from pathlib import PosixPath

import pytest


@pytest.fixture(autouse=True)
def temp_media_root(tmp_path: PosixPath, settings):
    temp_dir = tmp_path / "media"
    temp_dir.mkdir()
    settings.MEDIA_ROOT = str(temp_dir)
    yield
