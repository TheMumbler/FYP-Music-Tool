# Blog: Music Analysis Tool

**Patrick Ferry**

## Setting up - 12/12/2018

My first aim was to gather some songs to play around with and see how they read and what kind of information they hold. 
I wrote  a small script using PyTube and ffmpeg which takes a youtube url and downloads a song and converts it into WAV 
format. I am aware that these songs may not be of the best quality but they should be enough to begin with. I created a 
jupyter notebook for my code playground. I also created a Latex file for holding any research and formulae that I would 
like to refer back to. 

## Initial research - 22/01/2019
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

## First attempt at tracking - 28/02/2019
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

I have been using Librosa to find the onsets and then I would fourier transform a section of the audio signal at that 
point and look for peaks using a function in SciPy called find_peaks. I noticed that there was a lot more spikes than 
I was expecting and it took me a while to realised why. This is when I learned about windowing. Window in signal 
processing are used a section of a wave you are trying to analyse. The aim of a window is to have the segment of audio 
in this case begin around or at zero so to focus on the content in the middle. The most popular type of window seems to
be the Hann window. A window can be applied to a signal by element-wise multiplication.

Segment of audio wave      |  Hann Window              | Segment after windowing   |
:-------------------------:|:-------------------------:|:-------------------------:|
![wave_no_window](https://gitlab.computing.dcu.ie/ferryp2/2019-ca400-ferryp2/raw/master/docs/blog/images/nowindow.png)  |  ![hann_window](https://gitlab.computing.dcu.ie/ferryp2/2019-ca400-ferryp2/raw/master/docs/blog/images/window.png)  | ![wave_with_window](https://gitlab.computing.dcu.ie/ferryp2/2019-ca400-ferryp2/raw/master/docs/blog/images/applied_window.png)|

After applying this technique I noticed it was much easier to pick out the correct peaks from the output of the fourier 
transforms. 

## New Findings - 15/03/2019
This week I came across a new book 'Fundamentals of Music Processing: Audio, Analysis, Algorithms, Applications' by 
Meinard Müller. It was mentioned in the ISMIR edcuational resources. It is an amalgamation of many papers on different
aspects of music information retrieval and also begins by going over fourier transforms and spectrogram representations.
There is also a chapter called "Musically Informed Audio Decomposition" with a section on melody extraction. After reading 
this I realised that my initial technique of using onset detection and finding the most prominent frequency was not very
effective. As onset detection is not perfect building on top of it by just picking peaks would end up being very inaccurate.


### Short time fourier transforms 
Müller's book suggests that a better approach is to create a spectrogram representation of the audio I am planning to 
transcribe. I decided to use SciPy's short time fourier transform function for this and using matplotlibs pcolormesh 
function to display the spectrogram. It can be hard to see some most of the energy in a spectrogram which is why I used 
a logged compression function to make the lower energies easier to see. The following images are the first five seconds 
of Fur Elise by Beethoven.


Without Log compression    |  With Log Compression     |
:-------------------------:|:-------------------------:|
![spectrogram w/o logging](https://gitlab.computing.dcu.ie/ferryp2/2019-ca400-ferryp2/raw/master/docs/blog/images/spec_no_log.png)  |  ![spectrogram with logging](https://gitlab.computing.dcu.ie/ferryp2/2019-ca400-ferryp2/raw/master/docs/blog/images/spec_log.png)  |

As you can see it is much clearly after applying the log compression function. You also notice that most of the energy 
is on the bottom of the spectrogram, this is because many notes the frequency of many musical notes are quite low. The 
distance between notes from lower to higher logarithmically increases and doubles every octave (12 semitones). For 
examples A<sub>4</sub> is usually tuned to a frequency of 440 making A<sub>5</sub> 880. This clumps alot of the information
together which is why I tried frequency binning.

### Frequency Binning
The spectrogram above has 4096 bins as I used an FFT length of 8192 when creating it. These bins correspond to different
frequencies from 0hz to the 22khz (Nyquist Frequency). So what I did was created a function for getting the real frequency
coefficient of a bin and then. 

```python
def freq_coef(index, sr, nfft):
    return index * (sr/nfft)
```
As I plan to output as a midi file to decided to transform my current spectrogram into a variation of a spectrogram with
only 128 frequency bins. Each of these bins represents a semitone or midi note. To do this I took the frequency coefficient
of each current bin and converted it over using the following function which finds it's relative midi note.

```math
Bin(w) = \lfloor{12\cdot log_2(\frac{w}{440}}) + 69.5 \rfloor
```



### Monophonic pitch tracking 
I tried binning all of the frequencies and then getting the highest value in each frame to find the most prevalent note.
This managed to get some of the correct notes but because I was only looking for the max it only finds one even if there 
are no present.  

Single Highest Notes| 
:-------------------------:|
![monophonic notes](https://gitlab.computing.dcu.ie/ferryp2/2019-ca400-ferryp2/raw/master/docs/blog/images/monophonic.png)  |




## Teaching Drums - 25/04/2019
This week I found a [blog](https://medium.com/@sdoshi579/classification-of-music-into-different-genres-using-keras-82ab5339efe0) 
in which they try to create a neural network that can classify music genres. The features they used were very similar to mine 
so I used this blog as a guide for creating mine
