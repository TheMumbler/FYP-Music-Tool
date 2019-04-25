from src.site.apps import my_validators


def test_youtube_regex1():
    assert my_validators.check_url("https://www.youtube.com/watch?v=0AegLCRZZvU")


def test_youtube_regex2():
    assert my_validators.check_url("http://www.youtube.com/v/-wtIMTCHWuI?version=3&autohide=1")


def test_youtube_regex3():
    assert my_validators.check_url("http://youtu.be/-wtIMTCHWuI")


def test_youtube_regex4():
    assert my_validators.check_url("http://www.youtube.com/oembed?url=http%3A//www.youtube.com/watch?v%3D-wtIMTCHWuI&format=json")


def test_youtube_regex5():
    assert my_validators.check_url("youtube.com") == False


def test_youtube_regex6():
    assert my_validators.check_url("youtube.com/oembed?url=http%3A//www.youtube.com/watch?v%3D-wtIMTCHWuI&format=json")


def test_youtube_regex6():
    assert my_validators.check_url("google.com/oembed?url=http%3A") == False
