from pytube import YouTube
# import subprocess

# TODO: READ INPUT (URL)


def progress_function(stream, chunk, file_handle, bytes_remaining):
    print(round((1 - bytes_remaining / video.filesize) * 100, 3), '% done...')


# yt = YouTube("https://www.youtube.com/watch?v=mTwoMGCtPT8")
yt = YouTube("https://www.youtube.com/watch?v=LSwXh1Y5thY")  # on_progress_callback=progress_function

# TODO: DOWNLOAD SONG


# TODO: CONVERT SONG

print(yt.streams.all())
t = yt.streams.filter(only_audio=True).all()
print(t)
title = yt.title
t[0].download()

# TODO: REMOVE OLD SONG


