#Working version-works with limited functionality on macOS and linux
import time
errorlist=[]
loadfailed=False
elm_missing=False
try:
    import numpy as np
except ImportError:
    errorlist.append('numpy')
try:
    import pygame as pg
except:
    errorlist.append('pygame')
from math import sin, cos, fabs, pow, sqrt, pi, ceil
from time import sleep
from threading import Thread
import os
try:
    import pyaudio
except ImportError:
    errorlist.append('pyaudio')
import sys
try:
    from XInput import *
except ImportError:
    errorlist.append('XInput-python')
except IOError:
    loadfailed=True
import socket
try:
    from elm import *
    from elm import plugins
except ImportError:
    errorlist.append('ELM327-emulator')
try:
    from winreg import *
except:
    REG_SZ=0
    REG_DWORD=0
    def SetValueEx(a, b, c, d, e):
        pass
try:
    from tkinter import messagebox
    tkinter_available=True
except:
    tkinter_available=False
if len(errorlist)>0:
    if tkinter_available:
        if ('numpy' in errorlist) or ('pygame' in errorlist) or ('pyaudio' in errorlist):
            messagebox.showerror('Critical Error', 'Module '+str(errorlist)+' is missing or damaged, some of which are core modules. Reinstall each module with:\npip install module\nThis program will now close.')
            sys.exit(1)
        elif ('ELM327-emulator' in errorlist):
            elm_missing=True
            if 'XInput-python' in errorlist: 
                messagebox.showwarning('Warning', 'Module [ELM327-emulator, XInput-python] is missing or damaged. Reinstall each module with:\npip install module\nController support and OBD emulation will be disabled.')
                def get_connected():
                    return (False, False, False, False)
                def set_vibration(a, b, c):
                    pass
            else:
                messagebox.showwarning('Warning', 'Module ELM327-emulator is missing or damaged. Reinstall with:\npip install ELM327-emulator\nOBD emulation will be disabled.')
        else:
            messagebox.showwarning('Warning', 'Module XInput-python is missing or damaged. Reinstall with:\npip install XInput-python\nController support will be disabled.')
            def get_connected():
                return (False, False, False, False)
            def set_vibration(a, b, c):
                pass
elif loadfailed:
    messagebox.showwarning('Warning', 'XInput failed to load. Controller support will be disabled.')
    def get_connected():
        return (False, False, False, False)
    def set_vibration(a, b, c):
        pass
if not elm_missing:
    emulator=elm.Elm()
    emulator.net_port=35000
    emulator.scenario='car'
    r=Thread(target=emulator.run)
    r.daemon=True
    r.start()
else:
    class Elm:
        def __init__(self):
            self.answer={}
    emulator=Elm()
stream=None
DATA_OUT_FORMAT = [
    {'size': 4,'type': 'int32','name': 'IsRaceOn'},
    {'size': 4,'type': 'float','name': 'EngineMaxRpm'},
    {'size': 4,'type': 'float','name': 'EngineIdleRpm'},
    {'size': 4,'type': 'float','name': 'CurrentEngineRpm'},
    {'size': 4,'type': 'float','name': 'Speed'},
    {'size': 1,'type': 'uint8@normalize255to1','name': 'Throttle'},
    {'size': 1,'type': 'uint8@normalize255to1','name': 'Brake'},
    {'size': 1,'type': 'uint8','name': 'Gear'},
    {'size': 1,'type': 'uint8@normalize255to1','name': 'Steer'}]
audio_device=None
r.daemon=True
r.start()
def sine_wave_note(frequency, duration):
    '''
    Creates audio buffer representing a sine-wave
    frequency: Hz
    duration: seconds
    '''
    global sample_rate
    elements = math.ceil(duration * sample_rate)
    timesteps = np.linspace(start=0, stop=duration, num=elements, endpoint=False)
    return np.sin(frequency * timesteps * 2 * np.pi)

def sawtooth_wave_note(frequency, duration):
    '''
    Creates audio buffer representing a sine-wave
    frequency: Hz
    duration: seconds
    '''
    global sample_rate
    elements = math.ceil(duration * sample_rate)
    timesteps = np.linspace(start=0, stop=duration, num=elements, endpoint=False)
    print(timesteps)
    timesteps = timesteps.tolist()
    timesteps = [1-((x * frequency * 2 * np.pi)%1) for x in timesteps]
    timesteps = np.array(timesteps)
    return frequency * timesteps * 2 * np.pi

def random_wave_note(frequency, duration):
    '''
    Creates audio buffer representing a sine-wave
    frequency: Hz
    duration: seconds
    '''
    global sample_rate
    elements = math.ceil(duration * sample_rate)
    timesteps = np.linspace(start=0, stop=duration, num=elements, endpoint=False)
    return np.array([float(x%1)-1 for x in range(len(timesteps))])

def silence(duration):
    '''
    Creates audio buffer representing silence
    duration: seconds
    '''
    global sample_rate
    elements = math.ceil(duration * sample_rate)
    return np.zeros(elements)

def v_twin_90_deg():
    '''Suzuki SV650/SV1000, Yamaha MT-07'''
    return Engine(
        idle_rpm=1000,
        limiter_rpm=10500,
        strokes=4,
        cylinders=2,
        timing=[270, 450],
        fire_snd=_fire_snd,
        between_fire_snd=silence(1)
    )

def v_twin_60_deg():
    return Engine(
        idle_rpm=1100,
        limiter_rpm=10500,
        strokes=4,
        cylinders=2,
        timing=[300, 420],        fire_snd=_fire_snd,
        between_fire_snd=silence(1)
    )

def v_twin_45_deg():
    return Engine(
        idle_rpm=800,
        limiter_rpm=7000,
        strokes=4,
        cylinders=2,
        timing=[315, 405],
        fire_snd=_fire_snd,
        between_fire_snd=silence(1)
    )

def inline_4():
    return Engine(
        idle_rpm=800,
        limiter_rpm=7800,
        strokes=4,
        cylinders=4,
        timing=[180, 180, 180, 180],
        fire_snd=_fire_snd,
        between_fire_snd=silence(1)
    )

def inline_7():
    return Engine(
        idle_rpm=800,
        limiter_rpm=7800,
        strokes=4,
        cylinders=7,
        timing=[103, 103, 103, 103, 103, 103, 102],
        fire_snd=_fire_snd,
        between_fire_snd=silence(1)
    )

def inline_6():
    return Engine(
        idle_rpm=800,
        limiter_rpm=7800,
        strokes=4,
        cylinders=6,
        timing=[120, 120, 120, 120, 120, 120],
        fire_snd=_fire_snd,
        between_fire_snd=silence(1)
    )
def v_8_LR():
    return Engine(
        idle_rpm=800,
        limiter_rpm=7000,
        strokes=4,
        cylinders=8,
        timing=[90]*8,
        fire_snd=_fire_snd,
        between_fire_snd=silence(1)
    )

def v_8_LS():
    return Engine(
        idle_rpm=600,
        limiter_rpm=7000,
        strokes=4,
        cylinders=8,
        timing=[180, 270, 180, 90, 180, 270, 180, 90],
        fire_snd=_fire_snd,
        between_fire_snd=silence(1)
    )

def v_8_FP():
    return Engine(
        idle_rpm=800,
        limiter_rpm=7000,
        strokes=4,
        cylinders=8,
        timing=[180]*8,
        fire_snd=_fire_snd,
        between_fire_snd=silence(1)
    )

def v_8_FP_TVR():
    return Engine(
        idle_rpm=800,
        limiter_rpm=7000,
        strokes=4,
        cylinders=8,
        timing=[75]*8,
        fire_snd=_fire_snd,
        between_fire_snd=silence(1)
    )

def w_16():
    return Engine(
        idle_rpm=800,
        limiter_rpm=7000,
        strokes=4,
        cylinders=16,
        timing=[27, 90-27, 27, 180-117, 27, 270-207, 27, 360-297, 27, 90-27, 27, 180-117, 27, 270-207, 27, 360-297],
        #timing=[180, 270, 180, 90],
        fire_snd=_fire_snd,
        between_fire_snd=silence(1)
    )

def inline_9():
    return Engine(
        idle_rpm=800,
        limiter_rpm=7000,
        strokes=4,
        cylinders=9,
        timing=[80]*9,
        fire_snd=_fire_snd,
        between_fire_snd=silence(1)
    )

def inline_1():
    return Engine(
        idle_rpm=800,
        limiter_rpm=7000,
        strokes=4,
        cylinders=1,
        timing=[720],
        fire_snd=_fire_snd,
        between_fire_snd=silence(1)
    )

def inline_7_4_3():
    return Engine(
        idle_rpm=800,
        limiter_rpm=9000,
        strokes=4,
        cylinders=7,
        timing=[180, 90, 180, 270]+[240]*3,
        fire_snd=_fire_snd,
        between_fire_snd=silence(1)
    )

def inline_16():
    whynot=16
    return Engine(
        idle_rpm=800,
        limiter_rpm=7000,
        strokes=4,
        cylinders=whynot,
        timing=[720/whynot]*whynot,
        fire_snd=_fire_snd,
        between_fire_snd=silence(1)
    )

def inline_5():
    whynot=5
    return Engine(
        idle_rpm=800,
        limiter_rpm=9000,
        strokes=4,
        cylinders=whynot,
        timing=[720/whynot]*whynot,
        fire_snd=_fire_snd,
        between_fire_snd=silence(1)
    )

def inline_any():
    whynot=5
    return Engine(
        idle_rpm=800,
        limiter_rpm=9000,
        strokes=4,
        cylinders=whynot,
        timing=[720/whynot]*whynot,
        fire_snd=_fire_snd,
        between_fire_snd=silence(1)
    )

def inline_5_crossplane():
    whynot=5
    return Engine(
        idle_rpm=800,
        limiter_rpm=9000,
        strokes=4,
        cylinders=whynot,
        timing=[180, 90, 180, 90, 180],
        fire_snd=_fire_snd,
        between_fire_snd=silence(1)
    )

def inline_4_uneven_firing():
    whynot=4
    mini = 170
    maxi = 190
    return Engine(
        idle_rpm=800,
        limiter_rpm=7800,
        strokes=4,
        cylinders=whynot,
        timing=[rd.uniform(mini, maxi), rd.uniform(mini, maxi), rd.uniform(mini, maxi), rd.uniform(mini, maxi)],
        fire_snd=_fire_snd,
        between_fire_snd=silence(1)
    )

def boxer_4_crossplane_custom(rando=[0]*4):  #wrx
    whynot=4
    because=180
    #because=rando
    return Engine(
        idle_rpm=750,
        limiter_rpm=6700,
        strokes=4,
        cylinders=whynot,
        timing=[because, 360-because]*2,
        #timing = [180, 270, 180, 90],
        fire_snd=_fire_snd,
        between_fire_snd=silence(1),
        unequal=rando
    )

def boxer_4_half():
    whynot=2
    return Engine(
        idle_rpm=800,
        limiter_rpm=6700,
        strokes=4,
        cylinders=whynot,
        timing=[180, 720-180],
        fire_snd=_fire_snd,
        between_fire_snd=silence(1)
    )

def random():
    #whynot=rd.choice([4, 8, 16])
    whynot=4
    print(whynot)
    randlist = []
    for i in range(whynot):
        rando = randrange(int(360/5/whynot), int(1440/5/whynot))*5
    randlist = [randrange(int(360/5/whynot), int(1440/5/whynot))*5 for x in range(whynot)]
    print(randlist)
    return Engine(
        idle_rpm=800,
        limiter_rpm=9000,
        strokes=4,
        cylinders=whynot,
        timing=randlist,
        fire_snd=_fire_snd,
        between_fire_snd=silence(1)
    )

def v_four_90_deg():
    return Engine(
        idle_rpm=1100,
        limiter_rpm=16500,
        strokes=4,
        cylinders=4,
        timing=[180, 90, 180, 270],
        fire_snd=_fire_snd,
        between_fire_snd=silence(1)
    )

def fake_rotary_2rotor():
    difference = 60
    return Engine(
        idle_rpm=800,
        limiter_rpm=8300,
        strokes=2,
        cylinders=2,
        #timing=[90, 720-90],
        timing = [difference, 720-difference],
        fire_snd=_fire_snd,
        between_fire_snd=silence(1)
    )

def inline_4_1_spark_plug_disconnected():
    return Engine(
        idle_rpm=800,
        limiter_rpm=7800,
        strokes=4,
        cylinders=3,
        timing=[180, 360, 180],
        fire_snd=_fire_snd,
        between_fire_snd=silence(1)
    )

def V_12(rando=[0]*12):
    return Engine(
        idle_rpm=800,
        limiter_rpm=9000,
        strokes=4,
        cylinders=12,
        timing=[60]*12,
        fire_snd=_fire_snd,
        between_fire_snd=silence(1),
        unequal=rando
    )

class Stopwatch:
        def __init__(self):
                self.start_time=time.time()
        def reset(self):
                self.start_time=time.time()
        def get_time(self):
                return time.time()-self.start_time
'''Basic simulation of engine for purposes of audio generation'''
sample_rate = 44100
max_16bit = 2**(16-1)-1  # 32,767

# added by omar
sound_merge_method = "average"  # max or average

import math
import numpy as np
import pyaudio

class AudioDevice:
    def __init__(self):
        self._pyaudio = pyaudio.PyAudio()

    def close(self):
        self._pyaudio.terminate()

    def play_stream(self, callback):
        global sample_rate
        def callback_wrapped(in_data, frame_count, time_info, status_flags):
            return (callback(frame_count), pyaudio.paContinue)

        return self._pyaudio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=sample_rate,
            output=True,
            stream_callback=callback_wrapped
        )

def concat(bufs):
    return np.hstack(bufs)

def overlay(bufs):
    assert type(bufs) == list and len(bufs), 'bufs must be a non-empty list'
    assert all(len(bufs[0]) == len(buf) for buf in bufs), 'All buffers must have the same length'

    bufs = [np.copy(buf) for buf in bufs]
    for buf in bufs:
        #print(buf)
        buf / len(bufs)

    out_buf = np.sum(bufs, axis=0)
    normalize_volume(out_buf)

    return out_buf

def pad_with_zeros(buf, num_zeros):
    if num_zeros == 0:
        return buf

    return concat([
        buf,
        np.zeros(num_zeros)
    ])

def normalize_volume(buf, loudest_sample=None):
    '''Makes the loudest sample in the buffer use the max_16bit volume. No clipping'''
    buf *= np.int32(max_16bit / (loudest_sample or find_loudest_sample(buf)))

def exponential_volume_dropoff(buf, duration, base):
    global sample_rate
    num_samples = math.ceil(duration * sample_rate)
    zeros_required = len(buf) - num_samples

    unpadded_curve = base / np.logspace(1, 10, num=num_samples, base=base)
    dropoff_curve = pad_with_zeros(unpadded_curve, zeros_required)

    buf *= dropoff_curve

def find_loudest_sample(buf):
    return np.max(np.abs(buf))

def aslice(buf, duration):
    '''Take slice of audio buffers based on the duration of sound required'''
    global sample_rate
    if duration <= 0:
        return []
    num_samples = math.ceil(duration * sample_rate)
    return buf[:num_samples]

def in_playback_format(buf):
    return buf.astype(np.int16)

import math
import numpy as np

def _convert_timing_format(timing):
    # Convert timing format from standard format to our internal format.
    # Standard format: each element is the number of crankshaft degrees that cylinder should wait
    #   to fire after the _previous_ cylinder fires
    # Internal format: each element is the number of crankshaft degrees that cylinder should wait
    #   to fire after the _first_ cylinder fires
    timing[0] = 0 # we automatically wait for crank to finish rotation before coming back to first cylinder
    for i in range(1, len(timing)):
        timing[i] += timing[i-1]

class Engine:
    def __init__(self, idle_rpm, limiter_rpm, strokes, cylinders, timing, fire_snd, between_fire_snd, unequal=[]):
        '''
        Note: all sounds used will be concatenated to suit engine run speed.
        Make sure there's excess audio data available in the buffer.

        idle_rpm: engine speed at idle
        limiter_rpm: engine speed at rev limiter
        strokes: number of strokes in full engine cycle, must be 2 or 4 (new: 3 for rotary)
        cylinders: number of cylinders in engine
        timing: array where each element is the number of crankshaft degrees that cylinder should wait
          to fire after the previous cylinder fires. See engine_factory.py for examples
        fire_snd: sound engine should make when a cylinder fires
        between_fire_snd: sound engine should make between cylinders firing
        '''
        global sample_rate
        # Audio library will request a specific number of samples, but we can't simulate partial engine
        # revolutions, so we buffer whatever we have left over. We start with some zero samples to stop
        # the pop as the audio device opens.
        self._audio_buffer = np.zeros([256])

        self._rpm = idle_rpm
        self.idle_rpm = idle_rpm
        self.limiter_rpm = limiter_rpm

        #assert strokes in (2, 4), 'strokes not in (2, 4), see docstring'
        self.strokes = strokes

        assert cylinders > 0, 'cylinders <= 0'
        self.cylinders = cylinders

        assert len(timing) == cylinders, 'len(timing) != cylinders, see docstring'
        self.timing = timing
        _convert_timing_format(self.timing)

        assert type(fire_snd) == np.ndarray and \
               type(between_fire_snd) == np.ndarray, \
            'Sounds should be passed in as numpy.ndarray buffers'
        assert len(fire_snd) >= sample_rate * 1 and \
               len(between_fire_snd) >= sample_rate * 1, \
            'Ensure all audio buffers contain at least 1 second of data, see docstring'
        self.fire_snd = fire_snd
        self.between_fire_snd = between_fire_snd
        
        #added by omar
        if not unequal:
            unequal = [0]*cylinders
        self.unequal = unequal

        self.unequalmore = []
        self.previousms = 0

    def _gen_audio_one_engine_cycle(self):
        global sound_merge_method
        # Calculate durations of fire and between fire events
        strokes_per_min = self._rpm * 2 # revolution of crankshaft is 2 strokes
        strokes_per_sec = strokes_per_min / 60
        sec_between_fires = self.strokes / strokes_per_sec
        fire_duration = sec_between_fires / self.strokes # when exhaust valve is open
        between_fire_duration = sec_between_fires / self.strokes * (self.strokes-1) # when exhaust valve is closed

        # Generate audio buffers for all of the cylinders individually
        bufs = []
        bufsunequal = []
        fire_snd = aslice(self.fire_snd, fire_duration)
        for cylinder in range(0, self.cylinders):
            unequalms = (
                self.unequal[cylinder]/1000  # unequal converted from milliseconds to seconds
                if self.unequal[cylinder] > 0  # if unequal set
                #else self.unequal[cylinder]  # else 0
                else 0
            )
            #unequalms = min(unequalms, (self.timing[cylinder] / 180) * 2 / strokes_per_sec)
            before_fire_duration = (self.timing[cylinder] / 180) / strokes_per_sec# + unequalms # 180 degrees crankshaft rotation per stroke
            before_fire_snd = aslice(self.between_fire_snd, before_fire_duration+unequalms)
            after_fire_duration = between_fire_duration - before_fire_duration # - unequalms
            after_fire_snd = aslice(self.between_fire_snd, after_fire_duration)
            #print(len(audio_tools.concat([before_fire_snd, fire_snd, after_fire_snd])))
            if len(self.unequalmore):
                bufsunequal.append(np.array(self.unequalmore))
            if unequalms:  # if unequal parameter set for cylinder
                #print("unequal")
                bufs.append(  # add to buffer
                    np.array(  # make array
                        [0]*len(  # a tring of 0s the length of
                            concat(
                                [
                                    aslice(
                                        self.between_fire_snd,
                                        before_fire_duration
                                    ),  # silence as long as before_fire_duration (in seconds)
                                    fire_snd,
                                    after_fire_snd
                                ]  # complete combustion sound including before and after
                            )
                        )
                    )
                )
                #if self.previousms != unequalms:  # unequal ms different from previous cylinder
                before_fire_snd = aslice(
                    self.between_fire_snd, # silence
                    before_fire_duration + unequalms# - self.previousms  # current duration plus difference between unequals
                )  # make interval before sound smaller
                bufsunequal.append(
                    concat(
                        [before_fire_snd, fire_snd, after_fire_snd]  # combustion + silence
                    )
                )  # add generated combustion to unequal buffer
                self.previousms = unequalms  # make current unequalms the new previousms
            else:
                #forgot what this was for, probly before separate buffers
                """if self.unequaldelay > len(audio_tools.concat([before_fire_snd, fire_snd, after_fire_snd])):

                    self.unequaldelay -= len(audio_tools.concat([before_fire_snd, fire_snd, after_fire_snd]))
                else:
                    bufsunequal.append(
                        np.array(  # make numpy array of
                            [0]*(  # a list of 0s with the amount of 0s equal to
                                len(  # the length of
                                    audio_tools.slice(self.between_fire_snd, self.unequaldelay)  # silence as long as unequal offset
                                ) 
                                - 
                                len(
                                    audio_tools.concat([before_fire_snd, fire_snd, after_fire_snd])
                                )
                            )
                        )
                    )"""
                bufsunequal.append(
                    np.array(
                        [0]*len(
                            concat(
                                [before_fire_snd, fire_snd, after_fire_snd]  # combustion + silence
                            )
                        )
                    )
                )  # add silence to unequal buffer
                bufs.append(
                    concat(
                        [before_fire_snd, fire_snd, after_fire_snd]  # combustion + silence
                    )
                )  # add combustion package to equal buffer

        # combine both lists
        #print(len(bufs))
        #print("nextone")
        #print(len(bufsunequal))
        #bufs = list(np.maximum(bufs, bufsunequal))
        # Make sure all buffers are the same length (may be off by 1 because of rounding issues)
        
        max_buf_len = len(max(bufs, key=len))
        bufs = [pad_with_zeros(buf, max_buf_len-len(buf)) for buf in bufs]
        
        # same thing as before but with unequal buffer

        max_buf_len_unequal = len(max(bufsunequal, key=len))
        #print(max_buf_len)
        #might not be good idea with unequal, since that's how the unequalness is made
        bufsunequal = [pad_with_zeros(buf, max_buf_len_unequal-len(buf)) for buf in bufsunequal]

        # Combine all the cylinder sounds
        engine_snd = overlay(bufs)  # not sure
        engine_snd_unequal = overlay(bufsunequal)  # not sure
        #print(len(engine_snd), len(engine_snd_unequal))
        if sum(engine_snd_unequal) > 0:  # if unequal buffer contains anything
            if sound_merge_method == "average":  # average of both buffers
                engine_snd = np.mean([engine_snd, engine_snd_unequal[:len(engine_snd)]], axis=0)
            elif sound_merge_method == "max":  # maximum values of both buffers
                engine_snd = np.maximum(engine_snd, engine_snd_unequal[:len(engine_snd)])
        if len(engine_snd_unequal) > len(engine_snd):  # if unequal buffer is longer than 
            self.unequalmore = engine_snd_unequal[len(engine_snd):]
        return in_playback_format(engine_snd)

    def gen_audio(self, num_samples):
        '''Return `num_samples` audio samples representing the engine running'''
        # If we already have enough samples buffered, just return those
        if num_samples < len(self._audio_buffer):
            buf = self._audio_buffer[:num_samples]
            self._audio_buffer = self._audio_buffer[num_samples:]
            return buf

        # Generate new samples. If we still don't have enough, loop what we generated
        engine_snd = self._gen_audio_one_engine_cycle()
        while len(self._audio_buffer) + len(engine_snd) < num_samples:
            engine_snd = concat([engine_snd, engine_snd]) # this is unlikely to run more than once

        # Take from the buffer first, and use new samples to make up the difference
        # Leftover new samples become the audio buffer for the next run
        num_new_samples = num_samples - len(self._audio_buffer)
        buf = concat([self._audio_buffer, engine_snd[:num_new_samples]])
        #assert len(buf) == num_samples, (f'${num_samples} requested, but ${len(buf)} samples provided, from ' +
            #f'${len(self._audio_buffer)} buffered samples and ${num_new_samples} new samples')
        self._audio_buffer = engine_snd[num_new_samples:]
        return buf
    def specific_rpm(self, speed):  # TODO
        self._rpm=speed
_fire_snd = sine_wave_note(frequency=160, duration=1)
normalize_volume(_fire_snd)
exponential_volume_dropoff(_fire_snd, duration=0.06, base=5)
def get_resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
def collide_with_walls(walls, current_x, current_y, future_x, future_y):
    for wall in walls:
        if fabs(current_x - wall.x3) < 3000:
            denominator = (current_x - future_x) * (wall.y3 - wall.y4) - \
                (current_y - future_y) * (wall.x3 - wall.x4)

            if denominator != 0:
                t = ((current_x - wall.x3) * (wall.y3 - wall.y4) -
                     (current_y - wall.y3) * (wall.x3 - wall.x4)) / denominator
                u = ((current_x - wall.x3) * (current_y - future_y) -
                     (current_y - wall.y3) * (current_x - future_x)) / denominator
                if 0 < t < 1 and 0 < u < 1:
                    return True
    return False
class Ray:
    def __init__(self, angle):
        self.angle = angle
        self.color = pg.Color("yellow")
        self.width = 1

    def cast(self, position, walls):
        self.x1 = position[0]
        self.y1 = position[1]
        self.x2 = self.x1 + cos(self.angle)
        self.y2 = self.y1 + sin(self.angle)

        min_distance = 10e8
        self.texture = 0

        for wall in walls:
            denominator = (self.x1 - self.x2) * (wall.y3 - wall.y4) - (self.y1 - self.y2) * (wall.x3 - wall.x4)
            if denominator == 0:
                t, u = 0, 0
            else:
                t = ((self.x1 - wall.x3) * (wall.y3 - wall.y4) - (self.y1 - wall.y3) * (wall.x3 - wall.x4)) / denominator
                u = ((self.x1 - wall.x3) * (self.y1 - self.y2) - (self.y1 - wall.y3) * (self.x1 - self.x2)) / denominator

            if t > 0 and 0 < u < 1: 
                x2 = self.x1 + t * (self.x2 - self.x1)
                y2 = self.y1 + t * (self.y2 - self.y1)
                distance = pow(x2 - self.x1, 2) + pow(y2 - self.y1, 2)

                if distance < min_distance:
                    self.texture = (u // 0.001) % 100
                    min_distance = distance
                    self.x2 = x2
                    self.y2 = y2

        return sqrt(min_distance)

    def render(self, screen):
        pg.draw.line(screen, self.color, (self.x1, self.y1), (self.x2, self.y2), self.width)
class Progress:
    def __init__(self, car, track, screen_width, screen_height):
        self.car = car
        self.track = track

        self.width = screen_width / 30
        self.height = screen_height / 2

        self.image = pg.transform.smoothscale(pg.image.load(get_resource_path("sprites/checkerboard.png")), (self.width, self.height / 10)).convert()

        self.x = screen_width - 3 * self.width / 2
        self.y = (screen_height - self.height) / 2

        self.outer_rect = pg.Rect(self.x - 4, self.y - 4, self.width + 8, self.height + 8)
        self.outer_color = pg.Color(32, 32, 32)
        self.inner_color = pg.Color("#1f51ff")

    def render(self, screen):
        length = (self.car.x / self.track.final_x) * self.height
        inner_rect = pg.Rect(self.x, self.y + self.height - length, self.width, length)
        pg.draw.rect(screen, self.outer_color, self.outer_rect)
        pg.draw.rect(screen, self.inner_color, inner_rect)
        screen.blit(self.image, (self.x, self.y))
class Sound:
    def __init__(self):
        self.state = "starting"
        
        pg.mixer.init()
        self.brake_sound = pg.mixer.Sound(get_resource_path("sounds/brake.mp3"))        
        self.crash_sound = pg.mixer.Sound(get_resource_path("sounds/crash.mp3"))
        self.scratch_sound = pg.mixer.Sound(get_resource_path("sounds/scratch.wav"))
        self.finish_sound = pg.mixer.Sound(get_resource_path("sounds/finish.wav"))
    def stop_sound(self):
        try:
            if self.state == "accelerate" or self.state == "decelerate":
                pg.mixer.music.stop()
            elif self.state == "brake":
                self.brake_sound.stop()
            elif self.state == "crash":
                self.crash_sound.stop()
            pg.mixer.pause()
        except:
            pass

    def play_brake(self):
        state_changed = False

        if self.state == "accelerate" or self.state == "decelerate":
            pg.mixer.music.stop()
            state_changed = True
        if self.state == "top":
            state_changed = True

        if state_changed:
            self.state = "brake"
            self.brake_sound.play()

    def play_crash(self):
        state_changed = False

        if self.state == "idle":
            state_changed = True
        elif self.state == "brake":
            self.brake_sound.stop()
            state_changed = True
        elif self.state == "top":
            state_changed = True
        elif self.state == "accelerate" or self.state == "decelerate":
            pg.mixer.music.stop()
            state_changed = True

        if state_changed:
            self.state = "crash"
            self.crash_sound.play()

    def play_scratch(self):
        pass

    def play_finish(self):
        pg.mixer.music.stop()
        if self.state == "brake":
            self.brake_sound.stop()        

        self.finish_sound.play()
        sleep(1)
class Minimap:
    def __init__(self, car, track, screen_width, screen_height):
        self.car = car
        self.track = track

        self.radius = screen_width / 12
        self.x = 3 * self.radius / 2
        self.y = screen_height - 3 * self.radius / 2

        self.road_length = self.radius / 6
        self.car_rect = pg.Rect(self.x - 4, self.y - 4, 8, 8)

        self.background_color = pg.Color("black")
        self.road_color = pg.Color(128, 128, 128)
        self.player_color = pg.Color("red")

    def get_position(self):
        for i in range(0, len(self.track.walls), 2):
            if self.track.walls[i].x3 < self.car.x < self.track.walls[i].x4:
                return i
        return 0

    def render(self, screen):
        pg.draw.circle(screen, self.background_color, (self.x, self.y), self.radius)

        car_position = self.get_position()

        # obtain track around car
        track_angles = []
        for offset in range(-10, 12, 2):
            track_position = int((car_position + offset) / 2)
            if 0 < track_position < len(self.track.track_curvature):
                track_angles.append(self.track.track_curvature[track_position])
            else:
                track_angles.append(None)

        front_x, front_y = self.x, self.y - self.road_length / 2
        back_x, back_y = self.x, self.y + self.road_length / 2
        pg.draw.line(screen, self.road_color, (front_x, front_y), (back_x, back_y), 3)

        current_x, current_y = front_x, front_y
        next_x, next_y = 0, 0
        running_angle = 0

        # render track in front of car
        for i in range(6, 11):
            angle = track_angles[i]
            if angle is not None:
                next_x, next_y = current_x + self.road_length * sin(running_angle + angle), current_y - self.road_length * cos(running_angle + angle)
                pg.draw.line(screen, self.road_color, (current_x, current_y), (next_x, next_y), 3)
                current_x, current_y = next_x, next_y
                running_angle += angle
        
        current_x, current_y = back_x, back_y
        next_x, next_y = 0, 0
        running_angle = 0

        # render track behind car
        for i in range(4, -1, -1):
            angle = track_angles[i]
            if angle is not None:
                next_x, next_y = current_x + self.road_length * sin(running_angle + angle), current_y + self.road_length * cos(running_angle + angle)
                pg.draw.line(screen, self.road_color, (current_x, current_y), (next_x, next_y), 3)
                current_x, current_y = next_x, next_y
                running_angle += angle

        pg.draw.rect(screen, self.player_color, self.car_rect)
class Car:
    def __init__(self, x, y, look_angle, screen_width, screen_height):
        self.x = x
        self.y = y
        self.look_angle = np.deg2rad(look_angle)

        car_width = screen_width / 3
        car_height = screen_height / 4
        self.image = pg.transform.smoothscale(
            pg.image.load(get_resource_path("sprites/car.png")), (car_width, car_height)).convert_alpha()

        self.screen_x = screen_width / 2 - car_width / 2
        self.screen_y = 5 * screen_height / 6 - car_height / 2

        self.speed = 0
        self.rpm=0
        self.gear=0
        self.top_speed = 284
        self.reverse_speed = 5
        self.acceleration = 1

        self.deceleration = 0.33
        self.braking = 3

        self.turn_speed = np.deg2rad(1)
        self.front_distance = 300
        self.side_distance = 32
        self.collide_front = False
        self.collide_back = False
        self.collide_left = False
        self.collide_right = False

        self.wall_behind = False
        self.collide_x = 0
        self.collide_y = 0

        self.sound = Sound()
        self.sound.state='idle'
    def update(self, acc, steering, walls):
        if acc>0 and not self.collide_front:
            if self.gear==1 and self.speed<110*acc:
                self.speed+=acc*self.acceleration
            if self.gear==2 and self.speed<150*acc:
                self.speed+=0.9*acc*self.acceleration
            if self.gear==3 and self.speed<200*acc:
                self.speed+=0.6*acc*self.acceleration
            if self.gear==4 and self.speed<250*acc:
                self.speed+=0.4*acc*self.acceleration
            if self.gear==5 and self.speed<270*acc:
                self.speed+=0.2*acc*self.acceleration
            if self.gear==6 and self.speed<320*acc:
                self.speed+=0.08*acc*self.acceleration
            if self.gear==7 and self.speed<360*acc:
                self.speed+=0.03*acc*self.acceleration
            if self.speed > self.top_speed:
                self.speed = self.top_speed
            if self.speed>self.top_speed*acc:
                if self.speed / self.top_speed > 0.66:
                    self.speed -= 3 * self.deceleration
                elif self.speed / self.top_speed > 0.33:
                    self.speed -= 2 * self.deceleration
                self.speed -= self.deceleration
                state_changed=False
                if not self.sound.state=='decelerate':
                    state_changed==True
                self.sound.state='decelerate'
            else:
                state_changed=False
                if not self.sound.state=='accelerate':
                    state_changed==True
                self.sound.state='accelerate'
            self.x += self.speed * cos(self.look_angle)
            self.y += self.speed * sin(self.look_angle)
        if acc<0:
            if self.speed == 0 and not self.collide_back:
                self.x -= self.reverse_speed * cos(self.look_angle)
                self.y -= self.reverse_speed * sin(self.look_angle)
            elif self.speed > 0 and not self.collide_front:
                self.sound.play_brake()
                self.speed -= self.braking*abs(acc)
                if self.speed < 0:
                    self.speed = 0
                self.x += self.speed * cos(self.look_angle)
                self.y += self.speed * sin(self.look_angle)
        if steering<0:
            if self.speed > 0 and not self.collide_front and not self.collide_left:
                self.look_angle -= self.turn_speed * (1.5 - self.speed / self.top_speed)*abs(steering)
            elif self.speed == 0 and acc<0 and not self.collide_back and not self.collide_right:
                self.look_angle += self.turn_speed*abs(steering)
        if steering>0:
            if self.speed > 0 and not self.collide_front and not self.collide_right:
                self.look_angle += self.turn_speed * (1.5 - self.speed / self.top_speed)*steering
            elif self.speed == 0 and acc<0 and not self.collide_back and not self.collide_left:
                self.look_angle -= self.turn_speed*steering
        if acc==0 and self.speed > 0 and not self.collide_front and not self.collide_left and not self.collide_right:
            if self.speed / self.top_speed > 0.66:
                self.speed -= 3 * self.deceleration
            elif self.speed / self.top_speed > 0.33:
                self.speed -= 2 * self.deceleration
            self.speed -= self.deceleration
            if self.speed < 0:
                self.speed = 0
            self.x += self.speed * cos(self.look_angle)
            self.y += self.speed * sin(self.look_angle)
        if self.speed>255:
            emulator.answer['SPEED'] = '<exec>ECU_R_ADDR_E + " 04 41 0D %.4X" % int(255)</exec><writeln />'
        else:
            emulator.answer['SPEED'] = '<exec>ECU_R_ADDR_E + " 04 41 0D %.4X" % int('+str(self.speed)+')</exec><writeln />'
        emulator.answer['RPM'] = '<exec>ECU_R_ADDR_E + " 04 41 0C %.4X" % int(4 * '+str(self.rpm)+')</exec><writeln />'
        if collide_with_walls(
            walls,
            self.x + self.front_distance * cos(self.look_angle),
            self.y + self.front_distance * sin(self.look_angle),
            self.x + (self.front_distance + self.speed + self.acceleration) * cos(self.look_angle),
            self.y + (self.front_distance + self.speed + self.acceleration) * sin(self.look_angle)
        ):
            if not self.collide_front:
                w=Thread(target=crash_vibration)
                w.daemon=True
                w.start()
            self.collide_front = True
            self.sound.play_crash()
            self.collide_speed = self.speed
            self.speed = 0
            if self.speed==0:
                self.gear=1

            self.collide_x = self.x + self.front_distance * cos(self.look_angle)
            self.collide_y = self.y + self.front_distance * sin(self.look_angle)
        else:
            if self.x + self.front_distance * cos(self.look_angle) != self.collide_x or self.y + self.front_distance * sin(self.look_angle) != self.collide_y:
                self.collide_front = False

        if collide_with_walls(
            walls,
            self.x + self.front_distance * cos(self.look_angle),
            self.y + self.front_distance * sin(self.look_angle),
            self.x + (self.front_distance - self.reverse_speed) *
            cos(self.look_angle),
            self.y + (self.front_distance - self.reverse_speed) *
            sin(self.look_angle)
        ):
            if not self.collide_back:
                w=Thread(target=crash_vibration)
                w.daemon=True
                w.start()
            self.collide_back = True
            self.sound.play_crash()
        else:
            self.collide_back = False

        if collide_with_walls(
            walls,
            self.x + self.front_distance * cos(self.look_angle),
            self.y + self.front_distance * sin(self.look_angle),
            self.x + self.front_distance *
                cos(self.look_angle) + self.side_distance *
            cos(self.look_angle - np.pi / 2),
            self.y + self.front_distance *
                sin(self.look_angle) + self.side_distance *
            sin(self.look_angle - np.pi / 2)
        ):
            self.sound.play_scratch()
            if not self.collide_left:
                w=Thread(target=crash_vibration)
                w.daemon=True
                w.start()
            self.collide_left = True
        else:
            self.collide_left = False

        if collide_with_walls(
            walls,
            self.x + self.front_distance * cos(self.look_angle),
            self.y + self.front_distance * sin(self.look_angle),
            self.x + self.front_distance *
                cos(self.look_angle) + self.side_distance *
            cos(self.look_angle + np.pi / 2),
            self.y + self.front_distance *
                sin(self.look_angle) + self.side_distance *
            sin(self.look_angle + np.pi / 2)
        ):
            self.sound.play_scratch()
            if not self.collide_right:
                w=Thread(target=crash_vibration)
                w.daemon=True
                w.start()
            self.collide_right = True
        else:
            self.collide_right = False

        if collide_with_walls(
            walls,
            self.x,
            self.y,
            self.x + self.front_distance * cos(self.look_angle),
            self.y + self.front_distance * sin(self.look_angle)
        ):
            self.wall_behind = True
        else:
            self.wall_behind = False

        if self.x < 0:
            self.x = 0  

    def render(self, screen):
        screen.blit(self.image, (self.screen_x, self.screen_y))

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.speed = 0
        self.look_angle = 0
class Speedometer:
    def __init__(self, car, screen_width, screen_height):
        self.car = car

        speedometer_width = screen_width / 4
        speedometer_height = screen_height / 4

        self.image = pg.transform.smoothscale(pg.image.load(
            get_resource_path("sprites/speedometer.png")), (speedometer_width, speedometer_height)).convert_alpha()

        self.screen_x = screen_width - (speedometer_width)
        self.screen_y = screen_height - (speedometer_height)
        self.needle_x = screen_width - (speedometer_width / 2)
        self.needle_y = screen_height - 20
        self.needle_length = speedometer_height / 1.7
        self.needle_color = pg.Color("#1f51ff")

    def render(self, screen):
        screen.blit(self.image, (self.screen_x, self.screen_y))
        angle = pi*self.car.rpm / 10000
        tip_x = self.needle_x - self.needle_length * cos(angle)
        tip_y = self.needle_y - self.needle_length * sin(angle)
        pg.draw.line(screen, self.needle_color, (self.needle_x, self.needle_y), (tip_x, tip_y), 3)
def blit_text(surface, text, pos, font, color):
    words = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0] 
    max_width, _ = surface.get_size()
    max_width = max_width / 2

    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]
                y += word_height
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0] 
        y += word_height
import random
import numpy as np
class Track:
    def __init__(self, max_distance, road_width):
        self.max_distance = max_distance
        self.road_width = road_width

        self.wall_segment_length = 2000
        self.front_load_distance = 8000
        self.back_load_distance = 4000

        self.track_curvature = []
        self.walls = []

        self.current_angle = 0
        self.current_distance = 0

        self.build_bluprint()
        self.build_track()

    def build_bluprint(self):
        self.track_curvature = []

        any_direction = [
            self.straight_track, self.straight_track,
            self.gradual_left_turn, self.gradual_left_turn,
            self.sharp_left_turn, self.sharp_right_turn,
            self.tight_left_turn, self.tight_right_turn
        ]
        left_direction = [
            self.gradual_left_turn, self.gradual_left_turn,
            self.sharp_left_turn, self.tight_left_turn
        ]
        right_direction = [
            self.gradual_right_turn, self.gradual_left_turn,
            self.sharp_right_turn, self.tight_right_turn
        ]

        while self.current_distance < self.max_distance:
            if fabs(self.current_angle) < np.pi / 4:
                next_section = random.choice(any_direction)
                next_section()
            elif self.current_angle <= -np.pi / 4:
                next_section = random.choice(right_direction)
                next_section()
            elif self.current_angle >= np.pi / 4:
                next_section = random.choice(left_direction)
                next_section()

    def straight_track(self):
        self.track_curvature += [0 for _ in range(random.randint(2, 4))]

    def gradual_left_turn(self):
        self.track_curvature += [-0.1, -0.1, -0.1, -0.1, -0.1]
        self.current_distance += 5 * self.wall_segment_length
        self.current_angle -= 0.5

    def gradual_right_turn(self):
        self.track_curvature += [0.1, 0.1, 0.1, 0.1, 0.1]
        self.current_distance += 5 * self.wall_segment_length
        self.current_angle += 0.5

    def sharp_left_turn(self):
        self.track_curvature += [-0.3, -0.3, -0.3]
        self.current_distance += 3 * self.wall_segment_length
        self.current_angle -= 0.9

    def sharp_right_turn(self):
        self.track_curvature += [0.3, 0.3, 0.3]
        self.current_distance += 3 * self.wall_segment_length
        self.current_angle += 0.9

    def tight_left_turn(self):
        self.track_curvature += [-0.2, -0.2, -0.2, -0.2]
        self.current_distance += 4 * self.wall_segment_length
        self.current_angle -= 0.8

    def tight_right_turn(self):
        self.track_curvature += [0.2, 0.2, 0.2, 0.2]
        self.current_distance += 4 * self.wall_segment_length
        self.current_angle += 0.8

    def smooth_hairpin(self):
        if random() > 0.5:
            self.gradual_left_turn()
            self.gradual_right_turn()
        else:
            self.gradual_right_turn()
            self.gradual_left_turn()

    def build_track(self):
        self.walls.append(Wall(0, 0, 0, self.road_width))
        self.walls.append(Wall(0, 0, self.wall_segment_length, 0))
        self.walls.append(
            Wall(0, self.road_width, self.wall_segment_length, self.road_width))

        self.current_angle = 0
        for angle in self.track_curvature:
            self.current_angle += angle
            x3 = self.walls[-2].x4
            y3 = self.walls[-2].y4
            x4 = x3 + self.wall_segment_length * cos(self.current_angle)
            y4 = y3 + self.wall_segment_length * sin(self.current_angle)
            self.walls.append(Wall(x3, y3, x4, y4))

            horizontal_width = self.road_width * \
                sin(self.current_angle + np.pi / 2)
            vertical_width = self.road_width * \
                cos(self.current_angle + np.pi / 2)
            self.walls.append(Wall(
                self.walls[-2].x4, self.walls[-2].y4, x4 + vertical_width, y4 + horizontal_width))

        self.final_x = self.walls[-1].x4

    def load_walls(self, car_position):
        visible_walls = []

        for wall in self.walls:
            if -self.back_load_distance < wall.x3 - car_position < self.front_load_distance:
                visible_walls.append(wall)
        return visible_walls
def start_menu():
    global address, port
    pg.init()
    screen = pg.display.set_mode((800, 600))
    screen_width, screen_height = pg.display.get_surface().get_size()
    pg.display.set_caption("Car Racing 3D v0.5.1 (c) sserver")
    clock = pg.time.Clock()
    title_font = pg.font.SysFont(None, 48)
    text_font = pg.font.SysFont(None, 36)

    bg_color = pg.Color(48, 48, 48)
    font_color = pg.Color("white")
    emulator.answer['RPM'] = '<exec>ECU_R_ADDR_E + " 04 41 0C %.4X" % int(4 * 0)</exec><writeln />'
    emulator.answer['SPEED'] = '<exec>ECU_R_ADDR_E + " 04 41 0D %.4X" % int(4 * 0)</exec><writeln />'
    title_text = title_font.render("Car Racing 3D v0.5.1 (c) sserver", True, font_color)
    title_rect = title_text.get_rect(center=(screen_width / 2, 18))

    left_text =  "CONTROLS:\n\
Use RT/LT/LS or arrows to drive the car\n\
Press R or START to restart\n\
RevHeadz OBD IP: Run ipconfig to view\n\
For controller users, press SELECT to select option then START to choose. Selection will be shown on the title bar.\n\
IMPORTANT: If unresponsive, click on the game window. Collision detection is a bit buggy. Keyboard controls are ignored if a controller is connected.\n\
ABOUT:\n\
Developed by sserver224\nmywebsite1324.neocities.org"
    
    button_1 = pg.image.load(get_resource_path("buttons/button_1.png"))
    button_2 = pg.image.load(get_resource_path("buttons/button_2.png"))
    button_3 = pg.image.load(get_resource_path("buttons/button_3.png"))
    button_4 = pg.image.load(get_resource_path("buttons/button_4.png"))
    selection=1
    running = True
    DATA_OUT_FORMAT[0]['value']=0
    DATA_OUT_FORMAT[1]['value']=8000
    DATA_OUT_FORMAT[2]['value']=750
    DATA_OUT_FORMAT[3]['value']=0
    DATA_OUT_FORMAT[4]['value']=0
    DATA_OUT_FORMAT[5]['value']=0
    DATA_OUT_FORMAT[6]['value']=0
    DATA_OUT_FORMAT[7]['value']=0
    pg.display.set_icon(pg.image.load(get_resource_path("sprites/car.ico")))
    pg.display.set_caption("Car Racing 3D v0.5.1 (c) sserver - Currently selected: 3 mi")
    while running:
        clock.tick(30)
        sock.sendto(bytes(str(DATA_OUT_FORMAT), "utf-8"), (address, port))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pg.mouse.get_pos()

                if 500 < mouse_x < 700:
                    if 100 < mouse_y < 200:
                        return 5
                    elif 225 < mouse_y < 325:
                        return 10
                    elif 350 < mouse_y < 450:
                        return 15
                    elif 475 < mouse_y < 575:
                        return 20
            
        screen.fill(bg_color)

        screen.blit(title_text, title_rect)
        blit_text(screen, left_text, (1, 100), text_font, font_color)
        screen.blit(button_1, (500, 100))
        screen.blit(button_2, (500, 225))
        screen.blit(button_3, (500, 350))
        screen.blit(button_4, (500, 475))
        if get_connected()[0]:
            if get_button_values(get_state(0))['BACK']:
                selection+=1
                if selection>4:
                    selection=1
                pg.display.set_caption("Car Racing 3D v0.5.1 (c) sserver - Currently selected: "+str(selection*3)+" mi")
                while get_button_values(get_state(0))['BACK']:
                    pass
            if get_button_values(get_state(0))['START']:
                return selection*5
        pg.display.flip()
    set_vibration(0, 0, 0)
    pg.quit()
    return None
class Wall:
    def __init__(self, x3, y3, x4, y4):
        self.x3 = x3
        self.y3 = y3
        self.x4 = x4
        self.y4 = y4

        self.color = pg.Color("blue")
        self.width = 5

    def render(self, screen):
        pg.draw.line(screen, self.color, (self.x3, self.y3), (self.x4, self.y4), self.width)
def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

def generate_rays(look_angle, fov, screen_width, res):
    return [Ray(angle) for angle in np.arange(look_angle - fov / 2, look_angle + fov / 2, fov * res / screen_width)]

def play_game(track_distance):
    global port, address, stream, audio_device
    def gear_up():
        car.gear+=1
        if car.gear==2:
            while car.rpm>car.speed*58+750:
                car.rpm-=231
        if car.gear==3:
            while car.rpm>car.speed*40.3+750:
                car.rpm-=231
        if car.gear==4:
            while car.rpm>car.speed*32.6+750:
                car.rpm-=231
        if car.gear==5:
            while car.rpm>car.speed*27.4+750:
                car.rpm-=231
        if car.gear==6:
            while car.rpm>car.speed*24.2+750:
                car.rpm-=231
        if car.gear==7:
            while car.rpm>car.speed*21.3+750:
                car.rpm-=231
    def gear_down():
        car.gear-=1
        if car.gear==2:
            while car.rpm<car.speed*58+750:
                    car.rpm+=231
        if car.gear==3:
            while car.rpm<car.speed*40.3+750:
                    car.rpm+=231
        if car.gear==4:
            while car.rpm<car.speed*32.6+750:
                    car.rpm+=231
        if car.gear==5:
            while car.rpm<car.speed*27.4+750:
                    car.rpm+=231
        if car.gear==6:
            while car.rpm<car.speed*21.3+750:
                    car.rpm+=231
        if car.gear==1:
            while car.rpm<car.speed*95+750:
                    car.rpm+=231
    # initialize pygame
    pg.init()
    screen = pg.display.set_mode((1280, 720), pg.SCALED)
    screen_width, screen_height = pg.display.get_surface().get_size()
    pg.display.set_caption("Car Racing 3D v0.5.1 (c) sserver")
    clock = pg.time.Clock()
    font = pg.font.SysFont(None, 36)
    # critical settings
    fov = np.deg2rad(60)
    height_scale = 100000
    shader_exponent = 2
    res = 1
    fps = 48
    road_width = 400
    # static elements
    bg_color = pg.Color(21, 1, 3)
    font_color = pg.Color("white")
    road_color = pg.Color(48, 48, 48)
    road_rect = pg.Rect(0, screen_height / 2, screen_width, screen_height / 2)
    title_text = font.render("Car Racing 3D v0.5.1 (c) sserver", True, font_color)
    title_rect = title_text.get_rect(center=(screen_width / 2, 18))

    # load objects
    car = Car(0, road_width / 2, 0, screen_width, screen_height)
    car.rpm=750
    engine = boxer_4_crossplane_custom([1, 1, 0, 0])
    audio_device = AudioDevice()
    stream = audio_device.play_stream(engine.gen_audio)
    speedometer = Speedometer(car, screen_width, screen_height)
    track = Track(track_distance * 20000, road_width)
    rays = generate_rays(car.look_angle, fov, screen_width, res)
    walls = track.load_walls(car.x)
    progress_bar = Progress(car, track, screen_width, screen_height)
    minimap = Minimap(car, track, screen_width, screen_height)
    skyline = pg.transform.smoothscale(pg.image.load(get_resource_path("sprites/skyline.jpg")), (screen_width, screen_height / 2)).convert()
    skyline_turn_sensitivity = 200
    # dynamic loader of walls
    load_walls = pg.USEREVENT + 1
    pg.time.set_timer(load_walls, 1000)
    DATA_OUT_FORMAT[0]['value']=1
    # timers and controls
    race_timer = None
    timer_started = False
    acc=0
    steering=0
    running = True
    # main loop
    while running:
        clock.tick(fps)
        screen.fill(bg_color)
        skyline_x = -skyline_turn_sensitivity * car.look_angle
        screen.blit(skyline, (skyline_x, 0))
        if skyline_x > 0:
            screen.blit(skyline, (skyline_x - screen_width, 0))
        elif skyline_x < 0:
            screen.blit(skyline, (skyline_x + screen_width, 0))
        pg.draw.rect(screen, road_color, road_rect)
        if get_connected()[0]:
            gas=get_trigger_values(get_state(0))[1]
            brake=get_trigger_values(get_state(0))[0]
            if gas>0 and brake==0:
                acc=gas
            elif brake>0:
                acc=-1*brake
            else:
                acc=0
            if acc>0:
                set_vibration(0, max(0, acc*(max(0, (50*acc)-car.speed)/(50*acc))), max(0, acc*(max(0, (50*acc)-car.speed)/(50*acc))))
            elif acc<0:
                if car.speed>20:
                    set_vibration(0, 1.0, 1.0)
                else:
                    set_vibration(0, max(0, -1*acc*(max(0, car.speed)/20)/2), max(0, -1*acc*(max(0, car.speed)/20)))
            else:
                set_vibration(0, 0, 0)
            if get_button_values(get_state(0))['BACK']:
                car.sound.stop_sound()
                emulator.answer['RPM'] = '<exec>ECU_R_ADDR_E + " 04 41 0C %.4X" % int(4 * 0)</exec><writeln />'
                emulator.answer['SPEED'] = '<exec>ECU_R_ADDR_E + " 04 41 0D %.4X" % int(4 * 0)</exec><writeln />'
                car.speed=0
                DATA_OUT_FORMAT[0]['value']=0
                DATA_OUT_FORMAT[1]['value']=8000
                DATA_OUT_FORMAT[2]['value']=750
                DATA_OUT_FORMAT[3]['value']=0
                DATA_OUT_FORMAT[4]['value']=0
                DATA_OUT_FORMAT[5]['value']=0
                DATA_OUT_FORMAT[6]['value']=0
                DATA_OUT_FORMAT[7]['value']=0
                car.rpm=0
                car.gear=0
                stream.close()
                audio_device.close()
                set_vibration(0, 0, 0)
                running = False
                emulator.answer['RPM'] = '<exec>ECU_R_ADDR_E + " 04 41 0C %.4X" % int(4 * 0)</exec><writeln />'
                emulator.answer['SPEED'] = '<exec>ECU_R_ADDR_E + " 04 41 0D %.4X" % int(4 * 0)</exec><writeln />'
            if get_button_values(get_state(0))['START']:
                car.reset(0, road_width / 2)
                timer_started = False
                walls = track.load_walls(car.x)
                rays = generate_rays(car.look_angle, fov, screen_width, res)
            steering=get_thumb_values(get_state(0))[0][0]
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit_program()
            if event.type == pg.KEYDOWN and not get_connected()[0]:
                if event.key == pg.K_ESCAPE:
                    emulator.answer['RPM'] = '<exec>ECU_R_ADDR_E + " 04 41 0C %.4X" % int(4 * 0)</exec><writeln />'
                    emulator.answer['SPEED'] = '<exec>ECU_R_ADDR_E + " 04 41 0D %.4X" % int(4 * 0)</exec><writeln />'
                    car.speed=0
                    DATA_OUT_FORMAT[0]['value']=0
                    DATA_OUT_FORMAT[1]['value']=8000
                    DATA_OUT_FORMAT[2]['value']=750
                    DATA_OUT_FORMAT[3]['value']=0
                    DATA_OUT_FORMAT[4]['value']=0
                    DATA_OUT_FORMAT[5]['value']=0
                    DATA_OUT_FORMAT[6]['value']=0
                    DATA_OUT_FORMAT[7]['value']=0
                    car.rpm=0
                    car.gear=0
                    stream.close()
                    audio_device.close()
                    set_vibration(0, 0, 0)
                    running = False
                if event.key == pg.K_UP:
                    acc=1
                if event.key == pg.K_DOWN:
                    acc=-1
                if event.key == pg.K_LEFT:
                    steering=-1
                if event.key == pg.K_RIGHT:
                    steering=1
                if event.key == pg.K_r:
                    # restart track
                    car.reset(0, road_width / 2)
                    timer_started = False
                    walls = track.load_walls(car.x)
                    rays = generate_rays(car.look_angle, fov, screen_width, res)
            if event.type == pg.KEYUP and not get_connected()[0]:
                if event.key == pg.K_UP:
                    acc=0
                if event.key == pg.K_DOWN:
                    acc=0
                if event.key == pg.K_LEFT:
                    steering=0
                if event.key == pg.K_RIGHT:
                    steering=0
            if event.type == load_walls:
                walls = track.load_walls(car.x)

                if clock.get_fps() < 24:
                    # automatically lower graphics if fps is low
                    res += 1
                    rays = generate_rays(car.look_angle, fov, screen_width, res)
        engine.specific_rpm(car.rpm)
        DATA_OUT_FORMAT[3]['value']=car.rpm
        DATA_OUT_FORMAT[4]['value']=car.speed
        if acc>0:
            DATA_OUT_FORMAT[5]['value']=acc
            DATA_OUT_FORMAT[6]['value']=0
        elif acc<0:
            DATA_OUT_FORMAT[5]['value']=0
            DATA_OUT_FORMAT[6]['value']=abs(acc)
        else:
            DATA_OUT_FORMAT[5]['value']=0
            DATA_OUT_FORMAT[6]['value']=0
        DATA_OUT_FORMAT[7]['value']=car.gear
        DATA_OUT_FORMAT[8]['value']=steering
        car.update(acc, steering, walls)
        if car.gear==0:
            if acc>0:
                car.rpm+=415*acc
            if car.rpm>750:
                car.rpm-=97
        if car.gear==1:
            car.rpm=car.speed*95+750
        if car.gear==2:
            car.rpm=car.speed*58+750
        if car.gear==3:
            car.rpm=car.speed*40.3+750
        if car.gear==4:
            car.rpm=car.speed*32.6+750
        if car.gear==5:
            car.rpm=car.speed*27.4+750
        if car.gear==6:
            car.rpm=car.speed*24.2+750
        if car.gear==7:
            car.rpm=car.speed*21.3+750
        if acc<0 and car.rpm>750:
            car.rpm-=100
        if car.rpm<750:
            car.rpm=750
        if car.rpm>10000:
            car.rpm=10000
        if acc==1:
            if car.gear==2 and car.speed<82:
                gear_down()
            if car.gear==3 and car.speed<134:
                gear_down()
            if car.gear==4 and car.speed<193:
                gear_down()
            if car.gear==5 and car.speed<238:
                gear_down()
            if car.gear==6 and car.speed<283:
                gear_down()
            if car.gear==7 and car.speed<321:
                gear_down()
        if acc<=0:
            if car.rpm>3800:
                if car.rpm<4000 and car.gear>0:
                    gear_down()
            if car.rpm<1200 and car.gear>0:
                gear_down()
        if (acc>0 and ((car.rpm>8500*acc) and car.rpm>2000) and car.gear<7) or (acc>0 and car.gear==0):
            gear_up()
        if acc>0:
            if not timer_started:
                race_timer = time.time()
                timer_started = True
        # check if race finished
        if car.x > track.final_x:
            emulator.answer['RPM'] = '<exec>ECU_R_ADDR_E + " 04 41 0C %.4X" % int(4 * 0)</exec><writeln />'
            emulator.answer['SPEED'] = '<exec>ECU_R_ADDR_E + " 04 41 0D %.4X" % int(4 * 0)</exec><writeln />'
            car.speed=0
            DATA_OUT_FORMAT[0]['value']=0
            DATA_OUT_FORMAT[1]['value']=8000
            DATA_OUT_FORMAT[2]['value']=750
            DATA_OUT_FORMAT[3]['value']=0
            DATA_OUT_FORMAT[4]['value']=0
            DATA_OUT_FORMAT[5]['value']=0
            DATA_OUT_FORMAT[6]['value']=0
            DATA_OUT_FORMAT[7]['value']=0
            car.rpm=0
            car.gear=0
            stream.close()
            audio_device.close()
            set_vibration(0, 0, 0)
            car.sound.play_finish()
            set_vibration(0, 0, 0)
            pg.quit()
            running = False
            set_vibration(0, 0, 0)
            return (time.time() - race_timer)
        
        # ray casting
        if (steering!=0) and (car.speed > 0 or acc<0):
            rays = generate_rays(car.look_angle, fov, screen_width, res)

        distances = np.zeros(len(rays), float)
        for i, ray in enumerate(rays):
            distances[i] = ray.cast((car.x, car.y), walls)

        # rendering walls
        for x, distance in enumerate(distances):
            height = height_scale / distance
            if height > screen_height:
                height = screen_height
            texture = translate(rays[x].texture * 2, 0, 200, 32, 64)
            raw_color = translate(height ** shader_exponent, 0, screen_height ** shader_exponent, 100, 200)
            pg.draw.line(screen, [raw_color, texture, 0], (x * res, (screen_height - height) / 2), (x * res, (screen_height + height) / 2), res)
        
        # rendering car
        if not car.wall_behind:
            car.render(screen)

        # rendering UI elements 
        speedometer.render(screen)
        progress_bar.render(screen)
        minimap.render(screen)

        # rendering text
        fps_display = font.render("FPS: " + str(int(clock.get_fps())), True, font_color)
        gear_display=font.render("Gear: "+str(car.gear), True, font_color)
        speed_display=font.render("MPH: "+str(round(car.speed*0.621371)), True, font_color)
        screen.blit(fps_display, (0, 0))
        screen.blit(speed_display, (1040, 500))
        screen.blit(gear_display, (1040, 470))
        screen.blit(title_text, title_rect)

        if timer_started:
            time_display = font.render(str(round(time.time() - race_timer, 2)), True, font_color)
            screen.blit(time_display, (screen_width - 100, 0))
        
        pg.display.flip()
def crash_vibration():
        set_vibration(0, 1.0, 1.0)
        time.sleep(0.2)
        set_vibration(0, 0, 0)
def exit_program():
    pg.quit()
    set_vibration(0, 0, 0)
    DATA_OUT_FORMAT[0]['value']=0
    DATA_OUT_FORMAT[1]['value']=0
    DATA_OUT_FORMAT[2]['value']=0
    DATA_OUT_FORMAT[3]['value']=0
    DATA_OUT_FORMAT[4]['value']=0
    DATA_OUT_FORMAT[5]['value']=0
    DATA_OUT_FORMAT[6]['value']=0
    DATA_OUT_FORMAT[7]['value']=0
    emulator.answer['RPM'] = '<exec>ECU_R_ADDR_E + " 04 41 0C %.4X" % int(4 * 0)</exec><writeln />'
    emulator.answer['SPEED'] = '<exec>ECU_R_ADDR_E + " 04 41 0D %.4X" % int(4 * 0)</exec><writeln />'
    os._exit(0)
if __name__ == "__main__":
    emulator.answer['RPM'] = '<exec>ECU_R_ADDR_E + " 04 41 0C %.4X" % int(4 * 0)</exec><writeln />'
    emulator.answer['SPEED'] = '<exec>ECU_R_ADDR_E + " 04 41 0D %.4X" % int(4 * 0)</exec><writeln />'
    CreateKeyEx(OpenKey(HKEY_CURRENT_USER, 'Software', reserved=0, access=KEY_ALL_ACCESS), 'sserver\Car Racing 3D', reserved=0)
    if get_connected()[0]:
        set_vibration(0, 0, 0)
    try:
        port=QueryValueEx(OpenKey(OpenKey(OpenKey(HKEY_CURRENT_USER, 'Software', reserved=0, access=KEY_ALL_ACCESS), 'sserver', reserved=0, access=KEY_ALL_ACCESS), 'Car Racing 3D', reserved=0, access=KEY_ALL_ACCESS), 'Port')[0]
        address=QueryValueEx(OpenKey(OpenKey(OpenKey(HKEY_CURRENT_USER, 'Software', reserved=0, access=KEY_ALL_ACCESS), 'sserver', reserved=0, access=KEY_ALL_ACCESS), 'Car Racing 3D', reserved=0, access=KEY_ALL_ACCESS), 'UDPAddr')[0]
    except OSError:
        port=9999
        address='0.0.0.0'
        SetValueEx(OpenKey(OpenKey(OpenKey(HKEY_CURRENT_USER, 'Software', reserved=0, access=KEY_ALL_ACCESS), 'sserver', reserved=0, access=KEY_ALL_ACCESS), 'Car Racing 3D', reserved=0, access=KEY_ALL_ACCESS), 'Port', 0, REG_DWORD, 9999)
        SetValueEx(OpenKey(OpenKey(OpenKey(HKEY_CURRENT_USER, 'Software', reserved=0, access=KEY_ALL_ACCESS), 'sserver', reserved=0, access=KEY_ALL_ACCESS), 'Car Racing 3D', reserved=0, access=KEY_ALL_ACCESS), 'UDPAddr', 0, REG_SZ, '0.0.0.0')
    hostname=socket.gethostname()
    IP=socket.gethostbyname(hostname)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        import pyi_splash
        pyi_splash.update_text('UI Loaded ...')
        pyi_splash.close()
    except:
        pass
    while True:
        length = start_menu()
        if length == 0 or length is None:
            break
        play_game(length)
