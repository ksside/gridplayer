import pytest

from gridplayer.models.playlist import Playlist, _parse_video_params, _parse_video_paths


class TestPlaylistParse:
    def test_parse_minimal(self):
        txt = "#GRIDPLAYER\n/video/test.mp4\n"
        playlist = Playlist.parse(txt)

        assert playlist.videos is not None
        assert len(playlist.videos) == 1
        assert str(playlist.videos[0].uri) == "/video/test.mp4"

    def test_parse_multiple_videos(self):
        txt = "#GRIDPLAYER\n/video/a.mp4\n/video/b.mp4\n/video/c.mp4\n"
        playlist = Playlist.parse(txt)

        assert len(playlist.videos) == 3

    def test_parse_invalid_format(self):
        txt = "NOT_A_PLAYLIST\n/video/test.mp4\n"

        with pytest.raises(ValueError, match="Playlist format is not valid"):
            Playlist.parse(txt)

    def test_parse_empty_lines_ignored(self):
        txt = "#GRIDPLAYER\n\n/video/test.mp4\n\n"
        playlist = Playlist.parse(txt)

        assert len(playlist.videos) == 1

    def test_parse_with_video_params(self):
        txt = (
            '#GRIDPLAYER\n'
            '#V0:{"current_position":5000,"is_paused":true}\n'
            '/video/test.mp4\n'
        )
        playlist = Playlist.parse(txt)

        assert playlist.videos[0].current_position == 5000
        assert playlist.videos[0].is_paused is True

    def test_parse_with_playlist_params(self):
        txt = (
            '#GRIDPLAYER\n'
            '#P:{"shuffle_on_load":true}\n'
            '/video/test.mp4\n'
        )
        playlist = Playlist.parse(txt)

        assert playlist.shuffle_on_load is True


class TestPlaylistDumps:
    def test_dumps_roundtrip(self):
        txt = "#GRIDPLAYER\n/video/test.mp4\n"
        playlist = Playlist.parse(txt)
        dumped = playlist.dumps()

        assert dumped.startswith("#GRIDPLAYER\n")
        assert "/video/test.mp4" in dumped

    def test_dumps_multiple_videos(self):
        txt = "#GRIDPLAYER\n/video/a.mp4\n/video/b.mp4\n"
        playlist = Playlist.parse(txt)
        dumped = playlist.dumps()

        assert "/video/a.mp4" in dumped
        assert "/video/b.mp4" in dumped


class TestParseHelpers:
    def test_parse_video_paths(self):
        lines = ["#GRIDPLAYER", "#V0:{}", "/video/a.mp4", "/video/b.mp4"]
        paths = _parse_video_paths(lines)

        assert paths == ["/video/a.mp4", "/video/b.mp4"]

    def test_parse_video_params(self):
        lines = ["#GRIDPLAYER", '#V0:{"current_position":1000}', "/video/a.mp4"]
        params = _parse_video_params(lines)

        assert 0 in params
        assert params[0]["current_position"] == 1000

    def test_parse_video_params_multiple(self):
        lines = [
            "#GRIDPLAYER",
            '#V0:{"is_paused":true}',
            '#V1:{"is_paused":false}',
            "/a.mp4",
            "/b.mp4",
        ]
        params = _parse_video_params(lines)

        assert params[0]["is_paused"] is True
        assert params[1]["is_paused"] is False
