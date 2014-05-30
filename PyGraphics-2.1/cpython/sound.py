# This library is a modified extract from PyGraphics developed at the
#University of Toronto
# Aug 2010: fixed envelope for stereo sounds; further restructuring
# May 2011: module is only one file now

'''The Sample classes that support the Sound class and allow manipulation
of individual sample values.'''

class MonoSample(object):
    '''A sample in a single-channeled Sound with a value.'''
    
    def __init__(self, samp_array, i):
        '''Create a MonoSample object at index i from numpy array object 
        samp_array, which has access to the Sound's buffer.'''
        
        # negative indices are supported
        if -len(samp_array) <= i <= len(samp_array) - 1:    
            self.samp_array = samp_array
            self.index = i
        else:
            raise IndexError('Sample index out of bounds.')


    def __str__(self):
        '''Return a str with index and value information.'''
        
        return "Sample at " + str(self.index) + " with value " \
                 + str(self.get_value())
    

    def set_value(self, v):
        '''Set this Sample's value to v.'''
        
        if type(v) != int:
            raise TypeError("int expected")
        else:
            self.samp_array[self.index] = v


    def get_value(self):
        '''Return this Sample's value.'''
        
        return int(self.samp_array[self.index])


    def get_index(self):
        '''Return this Sample's index.'''
        
        return self.index
    
    def __cmp__ (self, other):
        return cmp(self.samp_array[self.index], other.samp_array[other.index])
        
        
class StereoSample(object):
    '''A sample in a two-channeled Sound with a left and a right value.'''

    
    def __init__(self, samp_array, i):
        '''Create a StereoSample object at index i from numpy array object 
        samp_array, which has access to the Sound's buffer.'''
       
        # negative indices are supported
        if -len(samp_array) <= i <= len(samp_array) - 1:    
            self.samp_array = samp_array
            self.index = i
        else:
            raise IndexError('Sample index out of bounds.')


    def __str__(self):
        '''Return a str with index and value information.'''
        
        return "Sample at " + str(self.index) + " with left value " \
                 + str(self.get_left()) + " and right value " + \
                 str(self.get_right())

    
    def set_values(self, left, right):
        '''Set this StereoSample's left value to left and 
        right value to right.'''
        
        if type(left) != int or type(right) != int:
            raise TypeError("int expected")
        else:
            self.samp_array[self.index] = [left, right]
    

    def get_values(self):        
        '''Return this StereoSample's left and right values as a tuple 
        (left, right) of two ints.'''
        
        return (self.samp_array[self.index, 0], self.samp_array[self.index, 1])

    
    def set_left(self, v):
        '''Set this StereoSample's left value to v.'''
        
        if type(v) != int:
            raise TypeError("int expected")
        else:
            self.samp_array[self.index, 0] = v


    def set_right(self, v):
        '''Set this StereoSample's right value to v.'''
        
        if type(v) != int:
            raise TypeError("int expected")
        else:
            self.samp_array[self.index, 1] = v
        
        
    def get_left(self):
        '''Return this StereoSample's left value.'''

        return int(self.get_values()[0])
    
    
    def get_right(self):
        '''Return this StereoSample's right value.'''

        return int(self.get_values()[1])


    def get_index(self):
        '''Return this Sample's index.'''
        
        return self.index
        
def __cmp__ (self, other):
  '''The bigger sample is the one with the biggest sample in any channel'''
  
  self_max = max(self.get_values())
  other_max = max(other.get_values())
  return max (self_max, other_max)


'''The Sound class and helper functions. This currently supports only 
uncompressed .wav files. For best quality use .wav files with sampling
rates of either 22050 or 44100. The default number of channels,
sampling rate, encoding, and buffering can be changed through the call
to init_sound at the end of this file.'''

import math
import numpy
import pygame
import wave
import sndhdr
import os

####################------------------------------------------------------------
## Defaults and Globals
####################------------------------------------------------------------

SOUND_FORMATS = ['.wav']
DEFAULT_SAMP_RATE = None
DEFAULT_ENCODING = None
DEFAULT_CHANNELS = None
DEFAULT_BUFFERING = None
SND_INITIALIZED = False
AUDIO_ENCODINGS = { 8 : numpy.uint8,   # unsigned 8-bit
     16 : numpy.uint16, # unsigned 16-bit
     -8 : numpy.int8,   # signed 8-bit
     -16 : numpy.int16  # signed 16-bit
     }

####################------------------------------------------------------------
## Initializer
####################------------------------------------------------------------

def init_sound(samp_rate=22050, encoding=-16, channels=1):
    '''Initialize this module. Must be done before any sounds are created.'''    
    
    global SND_INITIALIZED, DEFAULT_SAMP_RATE, DEFAULT_ENCODING, \
    DEFAULT_CHANNELS, DEFAULT_BUFFERING
            
    if not SND_INITIALIZED:
        DEFAULT_SAMP_RATE = samp_rate
        DEFAULT_ENCODING = encoding
        DEFAULT_CHANNELS = channels
        DEFAULT_BUFFERING = 3072
        pygame.mixer.pre_init(DEFAULT_SAMP_RATE, 
                              DEFAULT_ENCODING, 
                              DEFAULT_CHANNELS, 
                              DEFAULT_BUFFERING)
        pygame.mixer.init()
        SND_INITIALIZED = True
    else:
        raise Exception('Sound has already been initialized!')

####################------------------------------------------------------------
## Sound class
####################------------------------------------------------------------


class Sound(object):
    '''A Sound class as a wrapper for the pygame.mixer.Sound object.'''
        
    def __init__(self, filename=None, samples=None, seconds=None, sound=None):
        '''Create a Sound.
                
        Requires one of:
        - named str argument filename (with .wav extension), 
                e.g. Sound(filename='sound.wav')
        - named int argument samples, e.g. Sound(samples=2000)
        - named int argument seconds, e.g. Sound(seconds=10) 
        - named pygame.mixer.Sound argument sound, 
                e.g. Sound(sound=pygame.mixer.Sound)
        
        Filename takes precedence over samples, which takes precedence 
        over seconds, which in turn takes precedence over sound.'''
        
        if not SND_INITIALIZED:
            raise Exception('Sound is not initialized. Run init_sound() first.')
        
        self.player = None
        self.channels = DEFAULT_CHANNELS
        self.samp_rate = DEFAULT_SAMP_RATE
        self.numpy_encoding = AUDIO_ENCODINGS[DEFAULT_ENCODING]
        self.encoding = DEFAULT_ENCODING
        self.set_filename(filename)
        
        if filename != None:
            snd = load_pygame_sound(filename)
            
        elif samples != None:
            snd = create_pygame_sound(samples)
            
        elif seconds != None:
            samples = int(seconds * self.samp_rate)
            snd = create_pygame_sound(samples)
            
        elif sound != None:
            snd = sound
            
        else:
            raise TypeError("No arguments were given to the Sound constructor.")
                    
        self.set_samples(snd)
            
    def __eq__ (self, snd):
        if self.get_channels() == snd.get_channels():
            return numpy.all (self.samples == snd.samples)
        else:
            raise ValueError('Sound snd must have same number of channels.')
        
    def __str__(self):
        '''Return the number of Samples in this Sound as a str.'''
        
        return "Sound of length " + str(len(self))


    def __iter__(self):
        '''Return this Sound's Samples from start to finish.'''
        
        if self.channels == 1:
            for i in range(len(self)):
                yield MonoSample(self.samples, i)
        elif self.channels == 2:
            for i in range(len(self)):
                yield StereoSample(self.samples, i)
                

    def __len__(self):
        '''Return the number of Samples in this Sound.'''
        
        return len(self.samples)


    def __add__(self, snd):
        '''Return a Sound object with this Sound followed by Sound snd.'''
        
        new = self.copy()
        new.append(snd)
        return new


    def __mul__(self, num):
        '''Return a Sound object with this Sound repeated num times.'''
        
        new = self.copy()
        for time in range(int(num) - 1):
            new.append(self)
        return new


    def set_samples(self, pygame_snd):
        '''Set this Sound's samples array and pygame object.'''
        
        # self.samples is a numpy array object (either 1D or 2D depending on the
        # number of channels). This object allows access to specific samples
        # in the buffer.
        self.samples = pygame_to_sample_array(pygame_snd)        
        self.pygame_sound = pygame_snd
        
        
    def get_pygame_sound(self):
        '''Return this Sound's pygame Sound object.'''
        
        return self.pygame_sound


    def copy(self):
        '''Return a deep copy of this Sound.'''
        
        samples = self.samples.copy()
        new_pygame_snd =  sample_array_to_pygame(samples)
        return Sound(sound=new_pygame_snd)


    def append_silence(self, s):
        '''Append s samples of silence to each of this Sound's channels.'''
        
        if self.channels == 1:
            silence_array = numpy.zeros(s, self.numpy_encoding)
        else:
            silence_array = numpy.zeros((s, 2), self.numpy_encoding)
        pygame_silence =  sample_array_to_pygame(silence_array)
        self.append(Sound(sound=pygame_silence))


    def append(self, snd):
        '''Append Sound snd to this Sound. Requires that snd has same number of
        channels as this Sound.'''
        
        self.insert (snd, len(self))
    
    
    def insert(self, snd, i):
        '''Insert Sound snd at index i. Requires that snd has same number of
        channels as this Sound. Negative indices are supported.'''

        if self.get_channels() == snd.get_channels() == 1:
            first_chunk = self.samples[:i]
            second_chunk = self.samples[i:]
            new_samples = numpy.concatenate((first_chunk, 
                                             snd.samples, 
                                             second_chunk))
            self.samples = new_samples
            self.pygame_sound = sample_array_to_pygame(new_samples)
        elif self.get_channels() == snd.get_channels() == 2:
            first_chunk = self.samples[:i, :]
            second_chunk = self.samples[i:, :]
            new_samples = numpy.concatenate((first_chunk, 
                                        snd.samples, 
                                        second_chunk))            
            self.samples = new_samples
            self.pygame_sound = sample_array_to_pygame(new_samples)
        else:
            raise ValueError("Sound snd must have same number of channels.")


    def crop(self, first, last):
        '''Crop this Sound so that all Samples before int first and 
        after int last are removed. Cannot crop to a single sample. 
        Negative indices are supported'''

        first = first % len(self)
        last = last % len(self)        
        self.samples = self.samples[first:last + 1]
        self.pygame_sound = sample_array_to_pygame(self.samples)



    def normalize(self):
        '''Maximize the amplitude of this Sound's wave. This will increase
        the volume of the Sound.'''
        
        maximum = self.samples.max()
        minimum = self.samples.min()
        factor = min(32767.0/maximum, 32767.0/abs(minimum))        
        self.samples *= factor      
    
    

    def play(self, first=0, last=-1):
        '''Play this Sound from sample index first to last. As default play
        the entire Sound.'''
        
        self.player = self.copy()
        self.player.crop(first, last)        
        self.player.pygame_sound.play()


    def stop(self):
        '''Stop playing this Sound.'''
        
        if self.player:
            self.player.get_pygame_sound().stop()
        

    def get_sampling_rate(self):
        '''Return the number of Samples this Sound plays per second.'''

        return self.samp_rate


    def get_sample(self, i):
        '''Return this Sound's Sample object at index i. Negative indices are
        supported.'''

        if self.channels == 1:
            return MonoSample(self.samples, i)
        elif self.channels == 2:
            return StereoSample(self.samples, i)

    
    def get_max(self):
        '''Return this Sound's highest sample value. If this Sound is stereo
        return the absolute highest for both channels.'''
        
        return self.samples.max()
        
        
    def get_min(self):
        '''Return this Sound's lowest sample value. If this Sound is stereo
        return the absolute lowest for both channels.'''
        
        return self.samples.min()


    def get_channels(self):
        '''Return the number of channels in this Sound.'''
        
        return self.channels
    

    def set_filename(self, filename=None):
        '''Set this Sound's filename to filename. If filename is None 
        set this Sound's filename to the empty string.'''
        
        if filename != None:
            self.filename = filename
        else:
            self.filename = ''
    
    
    def get_filename(self):
        '''Return this Sound's filename.'''

        return self.filename
        
        
    def save_as(self, filename):
        '''Save this Sound to filename filename and set its filename.'''
        
        ext = os.path.splitext(filename)[-1]
        if ext in SOUND_FORMATS or ext in [e.upper() for e in SOUND_FORMATS]:
            self.set_filename(filename=filename)
            wav = wave.open(filename, 'w')
            wav.setnchannels(self.get_channels())
            
            # calculate the number of bytes for this sound
            fmtbytes = (abs(self.encoding) & 0xff) >> 3
            wav.setsampwidth(fmtbytes)
            
            wav.setframerate(self.get_sampling_rate())
            wav.setnframes(len(self))
            wav.writeframes(self.pygame_sound.get_buffer().raw)
            wav.close()
        else:
            raise ValueError("%s is not one of the supported file formats." \
                             % ext)        
        
        
    def save(self):
        '''Save this Sound to its filename. If an extension is not specified
        the default is .wav.'''
 
        filename = os.path.splitext(self.get_filename())[0]
        ext = os.path.splitext(self.get_filename())[-1]
        if ext == '':
            self.save_as(filename + '.wav')
        else:
            self.save_as(self.get_filename())
        
        
####################------------------------------------------------------------
## Note class
####################------------------------------------------------------------


class Note(Sound):
    '''A Note class to create different notes of the C scale. Inherits from Sound,
    does everything Sounds do, and can be combined with Sounds.'''
    
    # These are in Hz. 
    frequencies = {'C' : 261.63,
                   'D' : 293.66,
                   'E' : 329.63,
                   'F' : 349.23,
                   'G' : 392,
                   'A' : 440,
                   'B' : 493.88}
    
    default_amp = 5000
    
    def __init__(self, note, s, octave=0):
        '''Create a Note s samples long with the frequency according to 
        str note. The following are acceptable arguments for note, starting 
        at middle C:
            
        'C', 'D', 'E', 'F', 'G', 'A', and 'B'
            
        To raise or lower an octave specify the argument octave as a
        positive or negative int. Positive to raise by that many octaves
        and negative to lower by that many.'''

        
        if not SND_INITIALIZED:
            raise Exception('Sound is not initialized. Run init_sound() first.')
        
        self.channels = DEFAULT_CHANNELS
        self.samp_rate = DEFAULT_SAMP_RATE
        self.numpy_encoding = AUDIO_ENCODINGS[DEFAULT_ENCODING]
        self.encoding = DEFAULT_ENCODING        
        self.set_filename(None)

        if octave < 0: 
            freq = self.frequencies[note] / (2 ** abs(octave))
        else:
            freq = self.frequencies[note] * (2 ** octave)
        
        snd = create_sine_wave(int(freq), self.default_amp, s)
        self.set_samples(snd)
                
        
####################------------------------------------------------------------
## Helper functions
####################------------------------------------------------------------


def load_pygame_sound(filepath):
    '''Return a pygame Sound object from the file at str filepath. If 
    that file is not a .wav or is corrupt in some way raise a TypeError.'''
    
    # Check if the file exists
    if not os.access(filepath, os.F_OK):
        raise Exception("This file does not exist.")
    
    # Check if it is a .wav file
    if sndhdr.what(filepath):
        assert sndhdr.what(filepath)[0] == 'wav', "The file is not a .wav file"
    
    # Check the compression. Wave_read.getcomptype() will raise an Error if it is
    # compressed.
    wav = wave.open(filepath, 'r')
    try:
        wav.getcomptype()
    except:
        raise TypeError("This .wav file is compressed.")
    wav.close()
    
    return pygame.mixer.Sound(filepath)


def create_pygame_sound(s):
    '''Return a pygame sound object with s number of silent samples.'''

    if DEFAULT_CHANNELS == 1:
        
        # numpy.zeros returns an array object with all 0s in the
        # specified encoding. In sound terms, this is silence.
        sample_array = numpy.zeros(s, AUDIO_ENCODINGS[DEFAULT_ENCODING])
    else:
        sample_array = numpy.zeros((s, 2), AUDIO_ENCODINGS[DEFAULT_ENCODING])
    return sample_array_to_pygame(sample_array)


def create_sine_wave(hz, amp, samp):
    '''Return a pygame sound samp samples long in the form of a sine wave 
    with frequency hz and amplitude amp in the range [0, 32767].'''
    
    # Default frequency is in samples per second
    samples_per_second = float(DEFAULT_SAMP_RATE)
    
    # Hz are periods per second
    seconds_per_period = 1.0 / hz
    samples_per_period = samples_per_second * seconds_per_period
    if DEFAULT_CHANNELS == 1:
        samples = numpy.array(range(samp), 
                              numpy.float)
    else:
        samples = numpy.array([range(samp), range(samp)], 
                              numpy.float)
        samples = samples.transpose()
    
    # For each value in the array multiply it by 2 pi, divide by the 
    # samples per period, take the sin, and multiply the resulting
    # value by the amplitude.
    samples = numpy.sin((samples * 2.0 * math.pi) / samples_per_period) * amp
    envelope (samples, DEFAULT_CHANNELS)
    
    # Convert the array back into one with the appropriate encoding
    
    samples = numpy.array(samples, AUDIO_ENCODINGS[DEFAULT_ENCODING])
    
    return sample_array_to_pygame(samples)

def envelope (samples, channels):
    '''Add an envelope to numpy array samples to prevent clicking.'''    
    
    attack = 800
    if len(samples) < 3 * attack:
        attack = int(len(samples) * 0.05)
    line1 = numpy.linspace (0, 1, attack * channels)
    line2 = numpy.ones (len(samples) * channels - 2 * attack * channels)
    line3 = numpy.linspace (1, 0, attack * channels)
    envelope = numpy.concatenate ((line1, line2, line3))
    if channels == 2:
        envelope.shape = (len(envelope) / 2, 2)
    samples *= envelope




def pygame_to_sample_array(pygame_snd):
    '''Return a numpy array object, which allows direct access to specific
    sample values in the buffer of the pygame.mixer.Sound object pygame_snd.'''
     
    data = pygame_snd.get_buffer()
    
    # Create a numpy array from the buffer with the default encoding
    array = numpy.frombuffer(data, AUDIO_ENCODINGS[DEFAULT_ENCODING])
    
    # If there are two channels make the array object 2D
    if DEFAULT_CHANNELS == 2:        
        array.shape = (len(array) / 2, 2)
    return array


def sample_array_to_pygame(samp_array):
    '''Return a new pygame.mixer.Sound object from a numpy array object 
    samp_array. Requires that samp_array is an appropriate 1D or 2D shape.'''

    shape = samp_array.shape
    
    # Check if array has the right shape
    if DEFAULT_CHANNELS == 1:
        if len (shape) != 1:
            raise ValueError("Array must be 1-dimensional for mono sound")
    else:
        if len (shape) != 2:
            raise ValueError("Array must be 2-dimensional for stereo sound")
        elif shape[1] != DEFAULT_CHANNELS:
            raise ValueError("Array depth must match number of sound channels")
    
    return pygame.mixer.Sound(samp_array)    

####################------------------------------------------------------------
## Global Sound Functions
####################------------------------------------------------------------


def load_sound(filename):
    '''Return the Sound at file filename. Requires: file is an uncompressed
    .wav file.'''

    return Sound(filename=filename)


def create_sound(samp):
    '''Return a silent Sound samp samples long.'''

    return Sound(samples=samp)


def create_note(note, samp, octave=0): 
    '''Return a Sound samp samples long with the frequency according to 
    str note. The following are acceptable arguments for note, starting 
    at middle C:
        
    'C', 'D', 'E', 'F', 'G', 'A', and 'B'
        
    To raise or lower an octave specify the argument octave as a
    positive or negative int. Positive to raise by that many octaves
    and negative to lower by that many.'''

    return Note(note, samp, octave=octave)


def get_samples(snd):
    '''Return a list of Samples in Sound snd.'''

    return [samp for samp in snd]


def get_max_sample(snd):
    '''Return Sound snd's highest sample value. If snd is stereo
    return the absolute highest for both channels.'''

    return snd.get_max()
    
    
def get_min_sample(snd):
    '''Return Sound snd's lowest sample value. If snd is stereo
    return the absolute lowest for both channels.'''
    
    return snd.get_min()
    

def concatenate(snd1, snd2):
    '''Return a new Sound object with Sound snd1 followed by Sound snd2.'''
    
    return snd1 + snd2


def append_silence(snd, samp):
    '''Append samp samples of silence onto Sound snd.'''
    
    snd.append_silence(samp)

def append(snd1, snd2):
    '''Append snd2 to snd1.'''

    snd1.append (snd2)
    
def crop_sound(snd, first, last):
    '''Crop snd Sound so that all Samples before int first and 
    after int last are removed. Cannot crop to a single sample. 
    Negative indices are supported.'''

    snd.crop(first, last)
    

def insert(snd1, snd2, i):
    '''Insert Sound snd2 in Sound snd1 at index i.'''
    
    snd1.insert(snd2, i)


def play(snd):
    '''Play Sound snd from beginning to end.'''

    snd.play()


def play_in_range(snd, first, last):
    '''Play Sound snd from index first to last.'''
    
    snd.play(first, last)

def save_as (snd, filename):
    '''Save sound snd to filename.'''
    
    snd.save_as (filename)
    
def stop(snd):
    '''Stop playing Sound snd.'''
    
    snd.stop()
    
    
def get_sampling_rate(snd):
    '''Return the Sound snd's sampling rate.'''

    return snd.get_sampling_rate()


def get_sample(snd, i):
    '''Return Sound snd's Sample object at index i.'''

    return snd.get_sample(i)

####################------------------------------------------------------------
## Global Sample Functions
####################------------------------------------------------------------

def get_index(samp):
    '''Return Sample samp's index.'''
    
    return samp.get_index()


def set_value(mono_samp, v):
    '''Set MonoSample mono_samp's value to v.'''

    mono_samp.set_value(v)


def get_value(mono_samp):
    '''Return MonoSample mono_samp's value.'''

    return mono_samp.get_value()


def set_values(stereo_samp, left, right):
    '''Set StereoSample stereo_samp's left value to left and 
    right value to right.'''

    stereo_samp.set_values(left, right)


def get_values(stereo_samp):
    '''Return StereoSample stereo_samp's values in a tuple, (left, right).'''

    return stereo_samp.get_values()


def set_left(stereo_samp, v):
    '''Set StereoSample stereo_samp's left value to v.'''

    stereo_samp.set_left(v)


def get_left(stereo_samp):
    '''Return StereoSample stereo_samp's left value.'''
    
    return stereo_samp.get_left()


def set_right(stereo_samp, v):
    '''Set StereoSample stereo_samp's right value to v.'''

    stereo_samp.set_right(v)


def get_right(stereo_samp):
    '''Return StereoSample stereo_samp's right value.'''

    return stereo_samp.get_right()

def copy(obj):
    '''Return a deep copy of sound obj.'''
    
    return obj.copy()


init_sound(samp_rate=44100, channels=2)

