# Blog: Music Analysis Tool

**Patrick Ferry**

## Setting up

My first aim was to gather some songs to play around with and see how they read and what kind of information they hold. 
I wrote  a small script using PyTube and ffmpeg which takes a youtube url and downloads a song and converts it into WAV 
format. I am aware that these songs may not be of the best quality but they should be enough to begin with. I created a 
jupyter notebook for my code playground. I also created a Latex file for holding any research and formulae that I would 
like to refer back to. 

## Initial research
I began researching for guides on techniques for achieving some of my goals. The first thing I looked into was finding 
the BPM(beats per minute) or tempo of a song. This lead me onto the term 'Onset Detection'. I began searching for this 
term and I found multiple papers on the topic. I began to read them but I realised that a lot of the terms were things
I had not heard before. The papers fell under the tags of 'digital signal processing' and 'music information retrieval' 
so I began to search for these terms and information on them to get a better understanding of what I was reading. 
#### The Scientist and Engineer's Guide to Digital Signal Processing
'The Scientist and Engineer's Guide to Digital Signal Processing' by Steven W. Smith was a book I discovered while I 
was researching. I found a small section of it online and then found out that we have a copy of it in the DCU library so
I went got a loan of it. The only real thing I knew about signal processing before this book was the basic idea of the 
Fourier Transform but I understood a lot more after reading a few chapters of this book. I did not understand all of it
perfectly of course but I understood more of the terms that I had read in papers earlier.

#### The International Society of Music Information Retrieval ([ISMIR](http://ismir.net/))
I found this forum while researching and it contains information on different aspects of music information retrieval as
well as datasets and educational resources. I expect this to be a handy find as I progress. I have already began to look
through some of the papers that are mentioned.

## First attempt
I decided to revisit the idea of onset detection and how it works. Onset detection is when you look for the beginning of
notes. One of the most basic ways to do this is by looking at the energy increase from frame to frame in an audio 
waveform, where a frame is a set number of samples. There are some issues with this basic technique because if new notes
are quieter than previous notes and just have less energy because of the instrument they are played on causing this 
method to miss a lot of onsets and be quite inaccurate.

A more steady technique seems to be using spectral energy from a short time Fourier transform of the waveform. I am 
planning on implementing this myself but as I am still trying to understand how it works I have decided to use a python
called Librosa. Librosa has a function for finding the onsets of an input by using this technique. I have been using 
this library to play around with the output and see if I am going down the right path with this plan.

![onset](https://gitlab.computing.dcu.ie/ferryp2/2019-ca400-ferryp2/raw/master/docs/blog/images/onset.png)


Onset detection and initial melody tracking. Librosa

## New Findings
Muellers book and

## Frequency Binning

## Monophonic pitch tracking

## F0 Tracking using salience

### Problems with phase vocoder 

## Setting up flask

## Segmentation 

## Teaching Drums

## Testing

## My Fifth Blog Entry

This week, I learned how to include
[images](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet#images)
in my blog.

![cat](https://gitlab.computing.dcu.ie/sblott/2018-ca400-XXXX/raw/master/docs/blog/images/cat.jpg)

Here are the instructions:

- Add the image to your repo (probably using the `images` sub-directory here).
  The cat example above is in `./images/cat.jpg`.

- Commit that and push it to your repo.

- On Gitlab, navigate to your new image and click *Raw*.  You get the raw URL of your image.  Copy that URL.

- Add your image to this document using the following format:

    <pre>![alternative text](URL)</pre>

See the example [here](https://gitlab.computing.dcu.ie/sblott/2018-ca400-XXXX/raw/master/docs/blog/blog.md).

You can also mention other users (like me: @sblott).

## Including Code

Raw text:
```
Mary had a little lamb,
it's fleece was white as snow.
```

Syntax highlighting is also possible; for example...

Python:
```python
i = 0
while i < len(s):
   # So something.
   i = i + 1
```

Java:
```java
for (i=0; i<s.length(); i+=1) {
   // Do something.
}
```

Coffeescript:
```coffeescript
i = 0
while i < s.length
   # So something.
   i = i + 1
```

## Instructions

Once you've understood this sample, replace it with your own blog.
