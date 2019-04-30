from pytube import YouTube
import subprocess
import os
from werkzeug import secure_filename
# TODO: Make proper functions of below
# TODO: READ INPUT (URL)
# link = input()

# yt = YouTube("https://www.youtube.com/watch?v=mTwoMGCtPT8")
# yt = YouTube("https://www.youtube.com/watch?v=ziAqB9nb_To")
yt = YouTube("https://www.youtube.com/watch?v=JBp7iBfy_8M")

# yt = YouTube("https://www.youtube.com/watch?v=3X9LvC9WkkQ")

# TODO: DOWNLOAD SONG

# print(yt.streams.all())
# t = yt.streams.filter(only_audio=True).all()
t = yt.streams.filter(file_extension='mp4').all()
# t = yt.streams.all()
# t = yt.get('mp4', '480p')
print(t)
title = yt.title
print(title)
fname = "test"  #  secure_filename(title.replace(".", ""))
print(fname)
print(fname, "THIS IS THE FILE")
t[0].download(filename=fname)
# TODO: CONVERT SONG
subprocess.call("ffmpeg -i \"" + fname + ".mp4\" -ac 1 -f wav \"" + "drumbeat1.wav\"")
# os.remove(fname + ".mp4")
# ffmpeg -i my_video.mp4 -c copy -map 0:a output_audio.mp4
# TODO: REMOVE OLD SONG


