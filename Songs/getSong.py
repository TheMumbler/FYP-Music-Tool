from pytube import YouTube
# import subprocess

# yt = YouTube("https://www.youtube.com/watch?v=mTwoMGCtPT8")
yt = YouTube("https://www.youtube.com/watch?v=mTwoMGCtPT8")

print(yt.streams.all())
t  = yt.streams.filter(only_audio=True).all()
title = yt.title
t[0].download()

