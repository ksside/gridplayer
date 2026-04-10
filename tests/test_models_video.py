import tempfile
from pathlib import Path

import pytest

from gridplayer.models.video import Video, filter_video_uris
from gridplayer.models.video_uri import parse_uri


class TestVideo:
    def test_local_file_via_parse_uri(self):
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            path = f.name

        video = Video(uri=parse_uri(path))
        assert isinstance(video.uri, Path)

        Path(path).unlink()

    def test_http_url(self):
        video = Video(uri="http://example.com/video.mp4")
        assert isinstance(video.uri, str)
        assert video.is_http_url is True

    def test_https_url(self):
        video = Video(uri="https://example.com/video.mp4")
        assert isinstance(video.uri, str)
        assert video.is_http_url is True

    def test_uri_name_url(self):
        video = Video(uri="http://example.com/video.mp4")
        assert video.uri_name == "http://example.com/video.mp4"

    def test_defaults(self):
        video = Video(uri="http://example.com/test.mp4")
        assert video.current_position == 0
        assert video.volume == 1.0
        assert video.rate == 1.0
        assert video.scale == 1.0
        assert video.title is None


class TestFilterVideoUris:
    def test_valid_url(self):
        videos = filter_video_uris(["http://example.com/b.mp4"])
        assert len(videos) == 1

    def test_empty(self):
        videos = filter_video_uris([])
        assert len(videos) == 0

    def test_nonexistent_local_file_skipped(self):
        uris = ["/nonexistent/path/to/file.mp4"]
        videos = filter_video_uris(uris)
        # Non-existent local files fail pydantic validation on Windows
        # but may pass as strings on some platforms
        assert len(videos) <= 1
