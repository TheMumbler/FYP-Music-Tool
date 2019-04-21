from pytube import YouTube
import subprocess
# TODO: Make proper functions of below
# TODO: READ INPUT (URL)
link = input()

# yt = YouTube("https://www.youtube.com/watch?v=mTwoMGCtPT8")
yt = YouTube("https://www.youtube.com/watch?v=ziAqB9nb_To")

# yt = YouTube("https://www.youtube.com/watch?v=LSwXh1Y5thY")

# TODO: DOWNLOAD SONG

print(yt.streams.all())
t = yt.streams.filter(only_audio=True).all()
print(t)
title = yt.title
print(title)
t[0].download()
print("ffmpeg -i \"" + title + ".mp4\" \"" + title + ".wav\"")
# TODO: CONVERT SONG
subprocess.call("ffmpeg -i \"" + title + ".mp4\" -ac 1 \"" + "tycho2.wav\"")

# ffmpeg -i my_video.mp4 -c copy -map 0:a output_audio.mp4
# TODO: REMOVE OLD SONG


