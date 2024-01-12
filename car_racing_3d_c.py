import math
import time
from XInput import *
import engine
from engine.events import *
from engine.operators import *
from engine.types import *
from threading import Thread
from elm import *
from elm import plugins
import numpy as np
import pyaudio
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
eng=None
@sprite('Stage')
class Stage(Target):
    """Sprite Stage"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = 0
        self._ypos = 0
        self._direction = 90
        self.shown = True
        self.pen = Pen(self)

        self.costume = Costumes(
           0, 100, "None", [
            {
                'name': "backdrop1",
                'path': "8872c041882aeb77e2c551a5f7a4f561.png",
                'center': (480, 360),
                'scale': 2
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "pop",
                'path': "83a9787d4cb6f3b7632b4ddfebf74367.wav"
            }
        ])

        self.var_horizon_x = 0
        self.var_speed = 0
        self.var_car_x = 0
        self.var_road_ang = 0
        self.var_car_sx = 0
        self.var_MPH = 0
        self.var_SOUND_TICK = 0
        self.var_SOUND_ID = 0
        self.var_SOUND_ = 0
        self.var_IsAccellerating = 0
        self.var_tick = 104
        self.var_car_slide = 0
        self.var_LapTime = "00:00.00"
        self.var_LastLap = ""
        self.var_engine = 0
        self.var_DMODE = 2
        self.var_RPM = 750
        self.var_gear = 0
        self.var_ON = 1
        self.var_OIL = "-6.175615574477433e-16"
        self.var_DURABILITY = -54
        self.var_CHANGE = 0
        self.var_GEAR = 1
        self.var_KMH = 0
        self.var_MaxRpm = 7500
        self.var_FUEL = 0
        self.var_Gearbox = 0
        self.var_EngineOnOff = 1
        self.var_EngineFailure = 0
        self.var_Gear = "N"
        self.var_Failures = "None"
        self.var_EngineType = "V8"
        self.var_Turbopressure = 85
        self.var_DynoToggle = 0
        self.var_time_hold = 0.307
        self.var_touchinggrass = 0
        self.var_steering = 0
        self.var_gas = 0
        self.var_brake = 0
        self.var_RPMangle = 0
        self.var_SongName = 0

        self.list_Grass1 = List(
            [-178, -178, -174, -174, -170, -170, -166, -166, -162, -162, -158, -158, -154, -154, -150, -150, -146, -146, -142, -142, -138, -138, -134, -134, -130, -130, -126, -126, -122, -122, -18, -18, -14, -14, -10, -10, -6, -6, -2, -2, 2, 2, 6, 6, 10, 10, 30, 30, 34, 34, 38, 38, 50, 50]
        )
        self.list_Grass2 = List(
            [-118, -118, -114, -114, -110, -110, -106, -106, -102, -102, -98, -98, -94, -94, -90, -90, -86, -86, -82, -82, -78, -78, -74, -74, -70, -70, -66, -66, -62, -62, -58, -58, -54, -54, -50, -50, -46, -46, -42, -42, -38, -38, -34, -34, -30, -30, -26, -26, -22, -22, 14, 14, 18, 18, 22, 22, 26, 26, 42, 42, 46, 46, 54, 54, 58, 58]
        )
        self.list_Grass1X = List(
            [-549.5999999999999, 549.5999999999999, -544.8, 544.8, -540, 540, -535.2, 535.2, -530.4, 530.4, -525.6, 525.6, -520.8, 520.8, -516, 516, -511.2, 511.2, -506.4, 506.4, -501.59999999999997, 501.59999999999997, -496.79999999999995, 496.79999999999995, -492.00000000000006, 492.00000000000006, -487.2, 487.2, -482.4, 482.4, -357.6, 357.6, -352.8, 352.8, -348, 348, -343.2, 343.2, -338.4, 338.4, -333.6, 333.6, -328.8, 328.8, -324, 324, -300, 300, -295.2, 295.2, -290.4, 290.4, -276, 276]
        )
        self.list_Grass2X = List(
            [-477.6, 477.6, -472.8, 472.8, -468, 468, -463.20000000000005, 463.20000000000005, -458.4, 458.4, -453.6, 453.6, -448.8, 448.8, -444, 444, -439.2, 439.2, -434.4, 434.4, -429.6, 429.6, -424.8, 424.8, -420, 420, -415.20000000000005, 415.20000000000005, -410.4, 410.4, -405.6, 405.6, -400.79999999999995, 400.79999999999995, -396, 396, -391.2, 391.2, -386.4, 386.4, -381.6, 381.6, -376.8, 376.8, -372, 372, -367.2, 367.2, -362.4, 362.4, -319.20000000000005, 319.20000000000005, -314.4, 314.4, -309.6, 309.6, -304.8, 304.8, -285.6, 285.6, -280.8, 280.8, -271.2, 271.2, -266.4, 266.4]
        )
        self.list_CarsX = List(
            [-99]
        )
        self.list_CarsY = List(
            [565.9999999999994]
        )
        self.list_CarsPX = List(
            [-21.779999999999998, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        )
        self.list_CarsPY = List(
            [-999, -999, -999, -999, -999, -999, -999, -999, -999, -999]
        )
        self.list_track_x = List(
            [-107, -107, -107, -107, -107, -107, -107, -107, -107, -107, -107, -106.47664043757057, -105.25794700351908, -101.51188106935996, -95.3552663161034, -86.69501227825901, -76.81812887230764, -66.91544818489194, -59.60191116870024, -53.17403507183485, -47.15588484031437, -41.137734608793885, -35.119584377273405, -28.96296962401682, -22.80635487076024, -16.649740117503654, -10.49312536424707, -4.474975132726589, 1.543175098793892, 7.561325330314373, 13.579475561834856, 19.597625793355338, 25.615776024875817, 31.633926256396293, 37.65207648791677, 43.67022671943725, 49.68837695095773, 55.70652718247821, 61.29845621718568, 65.20576750207842, 65.90333223951967, 64.33898758911737, 62.08947704567872, 58.02211061492072, 52.43018158021325, 45.73887551662467, 37.16720250960354, 27.96215397507914, 18.30289571218846, 8.340948731271004, -1.6346917713272386, -10.021397450781482, -13.767463384940603, -14.116458351965614, -13.941934287592783, -13.767410223219953, -13.592886158847122, -13.418362094474292, -13.24383803010146, -13.06931396572863, -12.8947899013558, -12.72026583698297, -12.54574177261014, -14.282223549279452, -17.86590304473246, -24.02251779798905, -32.50299875955331, -42.28447476689136, -52.27838303708232, -61.188448278966, -68.00843187959099, -70.93214892681836, -70.93214892681836, -70.75762486244552, -70.58310079807269, -70.40857673369986, -70.23405266932703, -70.0595286049542, -69.88500454058136, -69.71048047620853, -69.5359564118357, -69.36143234746287, -69.18690828309003, -69.0123842187172, -68.48902465628777, -66.75254287961846, -63.332341446361774, -57.59657708285131, -49.8251174682816, -40.68966289185559, -30.908186884517537, -21.03130347856616, -11.03130347856616, -1.0313034785661586, 8.894158037847061, 18.597115300607022, 27.93291956557904, 37.06837414200505, 45.89785007059432, 54.644047141988274, 63.30430117983266, 71.59467690538308, 79.78619734827299, 87.5576569628427, 96.69311153926871, 106.61857305568194, 114.81009349857186, 118.55615943273098, 116.64806947896554, 112.26435801107476, 104.83290975630082, 99.09714539279037, 101.17626230096796, 105.87097792882687, 109.45465742427989, 107.37554051610228, 99.94409226132834, 92.06398472526112, 84.18387718919391, 76.3037696531267, 68.42366211705948, 60.54355458099226, 52.66344704492504, 44.783339508857814, 36.90323197279059, 29.02312443672337, 21.14301690065615, 13.262909364588928, 5.382801828521707, -2.4973057075455145, -10.377413243612736, -18.363768344085663, -27.024022381930045, -36.90090578788142, -46.60386305064139, -55.08434401220565, -58.830409946364774, -59.00493401073762, -53.558543660587354, -46.01144785835963, -38.13134032229242, -30.2512327862252, -22.371125250157988, -14.491017714090772, -6.610910178023559, 1.2691973580436553, 9.14930489411087, 15.70989518401594, 18.46626874218593, 15.376098798436455, 6.240644222010449, -3.7349962805877936, -13.710636783186036, -23.68627728578428, -33.661917788382524, -43.63755829098076, -53.485635821102846, -63.098252780486035, -72.30330131501044, -80.49482175790035, -87.31480535852533, -92.9067343932328, -98.05711514233336, -102.44082661022414, -104.86004556622082, -105.38340512865028, -105.73240009567527, -106.08139506270028, -106.43039002972527, -106.7793849967503, -106.95390906112314, -107.128433125496, -107.128433125496, -107.128433125496, -107.128433125496, -107.128433125496]
        )
        self.list_track_y = List(
            [68, 78, 88, 98, 108, 118, 128, 138, 148, 158, 168, 177.9862953475457, 187.91175686395897, 197.1835954096268, 205.063702945694, 210.063702945694, 211.6280475960963, 210.2363165864957, 203.4163329858707, 195.75588855468092, 187.769533454208, 179.78317835373505, 171.79682325326212, 163.9167157171949, 156.0366081811277, 148.15650064506048, 140.27639310899326, 132.29003800852033, 124.3036829080474, 116.31732780757446, 108.33097270710152, 100.3446176066286, 92.35826250615564, 84.37190740568272, 76.38555230520979, 68.39919720473685, 60.41284210426392, 52.42648700379099, 44.13611127824058, 34.931062743716176, 24.955422241117933, 15.078538835166556, 5.334838187314203, -3.800616389111807, -12.090992114662226, -19.52244036943617, -24.672821118536714, -28.580132403429452, -31.168322854454654, -32.03988028193124, -31.34231554448999, -25.89592519433972, -16.62408664867185, -6.630178378480892, 3.3682985730830204, 13.366775524646933, 23.365252476210845, 33.36372942777476, 43.36220637933867, 53.36068333090259, 63.359160282466505, 73.35763723403042, 83.35611418559434, 93.20419171571642, 102.53999598068845, 110.42010351675565, 115.71929615908768, 117.79841306726529, 117.44941810024024, 112.90951310284478, 105.59597608665308, 96.03292852702272, 86.03292852702273, 76.03445157545882, 66.0359746238949, 56.037497672330986, 46.03902072076707, 36.040543769203154, 26.04206681763924, 16.04358986607533, 6.045112914511417, -3.953364037052495, -13.951840988616407, -23.95031794018032, -33.93661328772606, -43.784690817848144, -53.181617025707226, -61.37313746859714, -67.66634137909551, -71.73370780985351, -73.81282471803111, -75.37716936843341, -75.37716936843341, -75.37716936843341, -74.15847593438194, -71.73925697838526, -68.15557748293226, -64.08821105217426, -59.39349542431535, -54.54539922185197, -49.54539922185197, -43.953470187144504, -38.21770582363404, -31.924501913135664, -27.85713548237766, -29.075828916429135, -34.81159327993959, -44.08343182560746, -53.8997036600841, -62.88764412307577, -69.57895018666436, -77.77047062955428, -87.55194663689234, -96.3814225654816, -105.71722683045364, -115.49870283779168, -122.19000890138028, -128.34662365463686, -134.50323840789343, -140.65985316115, -146.8164679144066, -152.97308266766316, -159.12969742091974, -165.28631217417632, -171.4429269274329, -177.59954168068947, -183.75615643394605, -189.91277118720265, -196.0693859404592, -202.22600069371575, -208.38261544697235, -214.40076567849283, -219.40076567849283, -220.96511032889515, -218.54589137289847, -213.2466987305664, -203.97486018489855, -193.97638323333464, -185.5896775538804, -179.02908726397533, -172.87247251071875, -166.71585775746215, -160.5592430042056, -154.40262825094902, -148.24601349769245, -142.08939874443587, -135.9327839911793, -128.38568818895158, -118.7730712295684, -109.26250606661684, -105.19513963585884, -104.4975748984176, -103.80001016097634, -103.10244542353507, -102.40488068609385, -101.70731594865258, -99.97083417198328, -97.21446061381327, -93.30714932892056, -87.5713849654101, -80.2578479492184, -71.96747222366798, -63.395799216646864, -54.40785875365519, -44.704901490895224, -34.71860614334949, -24.724697873158533, -14.730789602967576, -4.736881332776619, 5.257026937414338, 15.25550388897825, 25.25398084054216, 35.25398084054216, 45.25398084054216, 55.25398084054216, 65.25398084054217]
        )
        self.list_track_a = List(
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 7, 22, 38, 60, 81, 98, 133, 140, 143, 143, 143, 142, 142, 142, 142, 143, 143, 143, 143, 143, 143, 143, 143, 143, 143, 143, 146, 157, 176, 189, 193, 204, 214, 222, 239, 247, 255, 265, 274, 303, 338, 358, 361, 361, 361, 361, 361, 361, 361, 361, 361, 350, 339, 322, 302, 282, 268, 243, 223, 197, 180, 179, 179, 179, 179, 179, 179, 179, 179, 179, 179, 179, 177, 170, 160, 145, 129, 114, 102, 99, 90, 90, 83, 76, 69, 66, 62, 61, 60, 56, 55, 51, 66, 97, 125, 158, 191, 206, 228, 215, 168, 152, 159, 192, 228, 232, 232, 232, 232, 232, 232, 232, 232, 232, 232, 232, 232, 232, 232, 232, 232, 261, 284, 302, 338, 359, 393, 409, 412, 412, 412, 412, 412, 412, 412, 401, 376, 342, 294, 274, 274, 274, 274, 274, 280, 286, 293, 305, 317, 326, 329, 334, 346, 357, 358, 358, 358, 358, 359, 359, 360, 360, 360, 360]
        )
        self.list_track_sx = List(
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 15, 15, 22, 22, 22, 23, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 15, 15, 15, 10, 10, 10, 10, 8, 8, 8, 15, 30, 35, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, -11, -11, -20, -20, -20, -20, -20, -20, -20, -20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, -7, -10, -15, -16, -15, -12, -10, -6, -6, -6, -6, -6, -6, -4, -3, -2, -2, -2, -2, 15, 33, 33, 33, 33, 15, 0, -20, -45, -33, 0, 28, 40, 28, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 23, 25, 27, 30, 30, 15, 0, 0, 0, 0, 0, 0, 0, -11, -25, -34, -48, -20, 0, 0, 0, 0, 6, 7, 8, 9, 9, 9, 9, 9, 10, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        )
        self.list_BarTempo = StaticList(
            []
        )
        self.list_letters = StaticList(
            ["O", "O", ":", "O", "O", ".", "O", "O"]
        )

        self.sprite.layer = 0




@sprite('Game')
class SpriteGame(Target):
    """Sprite Game"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = 0
        self._ypos = -120
        self._direction = 90
        self.shown = True
        self.pen = Pen(self)

        self.costume = Costumes(
           0, 200, "all around", [
            {
                'name': "red1",
                'path': "11cc2ed9a8813dbccee85c82a69eade4.png",
                'center': (34, 49),
                'scale': 2
            },
            {
                'name': "red2",
                'path': "ef4eb6c99d144e6c45b1c53cfcdec01e.png",
                'center': (37, 49),
                'scale': 2
            },
            {
                'name': "red3",
                'path': "205390231a9ae8f0b29f41572c0b87ef.png",
                'center': (42, 49),
                'scale': 2
            },
            {
                'name': "red4",
                'path': "ead4cadfbbafcb594f11158bb0683824.png",
                'center': (46, 49),
                'scale': 2
            },
            {
                'name': "red5",
                'path': "056a876515a57dd585dd1b86f32534aa.png",
                'center': (64, 48),
                'scale': 2
            },
            {
                'name': "red6",
                'path': "722e23c53f4c4a1c7d6b5864953c2154.png",
                'center': (82, 50),
                'scale': 2
            },
            {
                'name': "red7",
                'path': "d93eb02a226d3cf547332b38630a5953.png",
                'center': (76, 50),
                'scale': 2
            },
            {
                'name': "red8",
                'path': "618dde7a35f15d55c4096644590572ea.png",
                'center': (64, 52),
                'scale': 2
            },
            {
                'name': "red9",
                'path': "e214d7e1546dab7ec6bf784f71809c84.png",
                'center': (48, 51),
                'scale': 2
            },
            {
                'name': "red10",
                'path': "c5fa1ec7a21d17a1292a3f24edb7eb29.png",
                'center': (41, 50),
                'scale': 2
            },
            {
                'name': "red11",
                'path': "580fa326e6c7a408474b84968195512a.png",
                'center': (40, 50),
                'scale': 2
            },
            {
                'name': "red12",
                'path': "c4fde8db8a7ffc273899e98a1827138a.png",
                'center': (36, 48),
                'scale': 2
            },
            {
                'name': "red13",
                'path': "db564c5ca44c71bb4b922d0470811a65.png",
                'center': (36, 48),
                'scale': 2
            },
            {
                'name': "red14",
                'path': "c89da2eab3f03af0f75e1dd3767c6d73.png",
                'center': (40, 48),
                'scale': 2
            },
            {
                'name': "red15",
                'path': "77a366ed7321b587899aa3dbac008743.png",
                'center': (47, 50),
                'scale': 2
            },
            {
                'name': "red16",
                'path': "64dac25e8a89ea1599010a3e3bf2bcf1.png",
                'center': (53, 50),
                'scale': 2
            },
            {
                'name': "red17",
                'path': "7a054fa91dc9804b0acd21e206e90492.png",
                'center': (73, 52),
                'scale': 2
            },
            {
                'name': "red18",
                'path': "3e91795165d382dc87a69cb53ff97a6c.png",
                'center': (88, 51),
                'scale': 2
            },
            {
                'name': "red19",
                'path': "bf69af3e887494737aa419ac5e498379.png",
                'center': (86, 50),
                'scale': 2
            },
            {
                'name': "red20",
                'path': "836bc0cab6c4a6255b742cb0c63e8edf.png",
                'center': (71, 51),
                'scale': 2
            },
            {
                'name': "red21",
                'path': "497cc94ab39b6bbe7bda69021e805472.png",
                'center': (56, 48),
                'scale': 2
            },
            {
                'name': "red22",
                'path': "f7a31ee8a14bedeec4ce61c59b3b5d32.png",
                'center': (47, 49),
                'scale': 2
            },
            {
                'name': "red23",
                'path': "e953e19acdaad7ec999c462083e6f97c.png",
                'center': (43, 49),
                'scale': 2
            },
            {
                'name': "red24",
                'path': "f2cbd2f6f5251c3b9542605bfb3834b7.png",
                'center': (40, 49),
                'scale': 2
            },
            {
                'name': "explosion",
                'path': "1f31f66bc7126673d4ab9c140e786822-fallback.png",
                'center': (47, 58),
                'scale': 1
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "acc1",
                'path': "490c6e05e5d75f9d57fe1e1b49f371eb.wav"
            },
            {
                'name': "acc2",
                'path': "bc17de5e29d83a3d929541f45372c32a.wav"
            },
            {
                'name': "acc3",
                'path': "ccae7ec5458f6cb504a97b52e432b854.wav"
            },
            {
                'name': "crash",
                'path': "6e86b21cf446048cde40293d3e49a3de.wav"
            }
        ])

        self.var_y = 0
        self.var_i = 0
        self.var_psp = 846.8444444444442
        self.var_yy = 62
        self.var_z = 454.54545454545456
        self.var_x1 = -266.4
        self.var_x2 = 266.4
        self.var_t = 0
        self.var_road_target = 0
        self.var_road_time = 90
        self.var_nextCarY = 565.9999999999994
        self.var_nextCar = 1
        self.var_debug = -122
        self.var_ecsp = 10.399999999999979
        self.var_ects = 18
        self.var_NextLapY = 70400
        self.var_LapTicks = 0

        self.list_RoadLag = List(
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        )

        self.sprite.layer = 15

    @on_green_flag
    async def green_flag(self, util):
        await self.my_Init(util, )
        global eng
        self.shown = True
        eng = v_8_LS()
        audio_device = AudioDevice()
        stream = audio_device.play_stream(eng.gen_audio)
        self.front_layer(util)
        self.gotoxy(0, -120)
        await util.send_broadcast_wait("create clones")
        self.var_y = 0
        util.sprites.stage.var_car_x = 0
        util.sprites.stage.var_car_sx = 0
        self.var_road_time = 90
        util.sprites.stage.var_road_ang = 0
        self.var_road_target = 0
        util.sprites.stage.var_speed = 0
        util.sprites.stage.list_CarsY[toint(self.var_nextCar)] = 20
        self.var_ecsp = 0
        self.var_ects = 18
        util.sprites.stage.var_tick = 0
        self.var_NextLapY = (400 * len(util.sprites.stage.list_track_x))
        while True:
            await self.my_UpdateTimers(util, )
            self.var_y += util.sprites.stage.var_speed
            self.var_i = self.list_RoadLag[1]
            self.list_RoadLag.delete(1)
            self.list_RoadLag.append(util.sprites.stage.var_road_ang)
            util.sprites.stage.var_horizon_x += (util.sprites.stage.var_speed * div(self.var_i, -50))
            util.sprites.stage.var_car_x += (util.sprites.stage.var_speed * div(self.var_i, -75))
            await self.my_Keys(util, )
            util.sprites.stage.var_MPH = abs(toint((util.sprites.stage.var_speed * 7)))
            await self.my_UpdateCars(util, )
            await self.my_RoadUpdate(util, )
            await self.my_tick(util, )
            await util.send_broadcast_wait("tick")

            await self.yield_()

    @warp
    async def my_Keys(self, util, ):
        util.sprites.stage.var_car_x += (div(util.sprites.stage.var_speed, 4) * (util.sprites.stage.var_car_sx * div(15, (util.sprites.stage.var_speed + 10))))
        if gt(abs(util.sprites.stage.var_speed), 0.01):
            if lt(util.sprites.stage.var_steering, 0):
                util.sprites.stage.var_car_sx += (0.4 * util.sprites.stage.var_steering)
            else:
                if (gt(util.sprites.stage.var_car_slide, 0) and lt(util.sprites.stage.var_car_sx, 0)):
                    util.sprites.stage.var_car_sx += 0.2
            if gt(util.sprites.stage.var_steering, 0):
                util.sprites.stage.var_car_sx += (0.4 * util.sprites.stage.var_steering)
            else:
                if (gt(util.sprites.stage.var_car_slide, 0) and gt(util.sprites.stage.var_car_sx, 0)):
                    util.sprites.stage.var_car_sx += -0.2
        if gt(util.sprites.stage.var_car_slide, 0):
            util.sprites.stage.var_car_sx = (util.sprites.stage.var_car_sx * 0.99)
        else:
            util.sprites.stage.var_car_sx = (util.sprites.stage.var_car_sx * 0.96)
        if lt(util.sprites.stage.var_car_sx, -11):
            util.sprites.stage.var_car_sx = -11
        else:
            if gt(util.sprites.stage.var_car_sx, 11):
                util.sprites.stage.var_car_sx = 11
        await self.my_SetCostume(util, ((toint(div(util.sprites.stage.var_car_sx, 2)) % 24) + 1))
        if gt(util.sprites.stage.var_car_slide, 0):
            if (gt(util.sprites.stage.var_speed, 10) and gt(abs(util.sprites.stage.var_car_sx), 4)):
                util.sprites.stage.var_car_slide = 30
            else:
                util.sprites.stage.var_car_slide += -1
        if gt(util.sprites.stage.var_brake, 0):
            util.sprites.stage.var_IsAccellerating = (-1 * util.sprites.stage.var_brake)
            if gt(util.sprites.stage.var_speed, 0):
                util.sprites.stage.var_speed += (-0.27 * abs(util.sprites.stage.var_IsAccellerating))
            else:
                pass
            util.sprites.stage.var_speed = (util.sprites.stage.var_speed * 0.99)
            if (gt(util.sprites.stage.var_speed, 10) and gt(abs(util.sprites.stage.var_car_sx), 2)):
                util.sprites.stage.var_car_slide = 30
        else:
            if (gt(util.sprites.stage.var_gas, 0) and eq(util.sprites.stage.var_CHANGE, 0)):
                util.sprites.stage.var_IsAccellerating = util.sprites.stage.var_gas
                util.sprites.stage.var_speed += (0.22 * util.sprites.stage.var_IsAccellerating)
                util.sprites.stage.var_speed = (util.sprites.stage.var_speed * 0.992)
            else:
                util.sprites.stage.var_IsAccellerating = 0
                util.sprites.stage.var_speed = (util.sprites.stage.var_speed * 0.995)
        if gt(abs(util.sprites.stage.var_car_x), 106):
            if gt(abs(util.sprites.stage.var_car_x), 132):
                util.sprites.stage.var_touchinggrass = 1
                util.sprites.stage.var_speed = (util.sprites.stage.var_speed * 0.98)
            else:
                util.sprites.stage.var_speed = (util.sprites.stage.var_speed * 0.995)
                util.sprites.stage.var_touchinggrass = 0
        else:
            util.sprites.stage.var_touchinggrass = 0

    @warp
    async def my_tick(self, util, ):
        util.sprites.stage.list_Grass1.delete_all()
        util.sprites.stage.list_Grass2.delete_all()
        util.sprites.stage.list_Grass1X.delete_all()
        util.sprites.stage.list_Grass2X.delete_all()
        self.var_i = (util.sprites.stage.var_road_ang * 0.0001)
        self.var_yy = -178
        self.var_nextCar = 1
        util.sprites.stage.list_CarsPY[toint(self.var_nextCar)] = -999
        util.sprites.stage.list_CarsY[toint(self.var_nextCar)] = (tonum(util.sprites.stage.list_CarsY[toint(self.var_nextCar)]) + self.var_ecsp)
        self.var_nextCarY = util.sprites.stage.list_CarsY[toint(self.var_nextCar)]
        for _ in range(60):
            self.var_z = (div(-100, (self.var_yy - 80)) * 100)
            self.var_t = ((tonum(self.var_i) * (self.var_z * self.var_z)) - util.sprites.stage.var_car_x)
            self.var_x1 = (tonum(self.var_t) - 120)
            self.var_x2 = (tonum(self.var_t) + 120)
            self.var_x1 = (div(self.var_x1, div(self.var_z, 100)) - 240)
            self.var_x2 = (div(self.var_x2, div(self.var_z, 100)) + 240)
            if gt((self.var_y + self.var_z), self.var_nextCarY):
                util.sprites.stage.list_CarsPX[toint(self.var_nextCar)] = div((tonum(util.sprites.stage.list_CarsX[toint(self.var_nextCar)]) + tonum(self.var_t)), div(self.var_z, 100))
                util.sprites.stage.list_CarsPY[toint(self.var_nextCar)] = self.var_yy
                self.var_nextCarY = 999999
            if lt(((self.var_z + self.var_y) % 100), 50):
                util.sprites.stage.list_Grass1.append(self.var_yy)
                if gt(self.var_x1, 0):
                    util.sprites.stage.list_Grass1X.append(0)
                else:
                    util.sprites.stage.list_Grass1X.append(self.var_x1)
                util.sprites.stage.list_Grass1.append(self.var_yy)
                if lt(self.var_x2, 0):
                    util.sprites.stage.list_Grass1X.append(0)
                else:
                    util.sprites.stage.list_Grass1X.append(self.var_x2)
            else:
                util.sprites.stage.list_Grass2.append(self.var_yy)
                if gt(self.var_x1, 0):
                    util.sprites.stage.list_Grass2X.append(0)
                else:
                    util.sprites.stage.list_Grass2X.append(self.var_x1)
                util.sprites.stage.list_Grass2.append(self.var_yy)
                if lt(self.var_x2, 0):
                    util.sprites.stage.list_Grass2X.append(0)
                else:
                    util.sprites.stage.list_Grass2X.append(self.var_x2)
            self.var_yy += 4

    @warp
    async def my_RoadUpdate(self, util, ):
        self.var_road_target = (3 * tonum(util.sprites.stage.list_track_sx[toint(((math.floor(div(self.var_y, 400)) % len(util.sprites.stage.list_track_sx)) + 1))]))
        self.var_t = (3 * tonum(util.sprites.stage.list_track_sx[toint((((math.floor(div(self.var_y, 400)) + 1) % len(util.sprites.stage.list_track_sx)) + 1))]))
        self.var_t = (tonum(self.var_t) - self.var_road_target)
        util.sprites.stage.var_road_ang = (self.var_road_target + ((div(self.var_y, 400) % 1) * tonum(self.var_t)))

    @warp
    async def my_UpdateCars(self, util, ):
        self.var_t = util.sprites.stage.list_CarsY[1]
        if lt(self.var_t, (self.var_y - 600)):
            self.var_ects = pick_rand(10, 21.5)
            self.var_ecsp = pick_rand(10, 21)
            self.var_t = (self.var_y + pick_rand(400, 1500))
            util.sprites.stage.list_CarsY[1] = self.var_t
            util.sprites.stage.list_CarsX[1] = pick_rand(-120, 120)
        else:
            if gt(self.var_t, (self.var_y + 1500)):
                util.sprites.stage.list_CarsY[1] = (self.var_y + 1500)
            else:
                pass
        if lt(self.var_ecsp, self.var_ects):
            self.var_ecsp += 0.1
        else:
            if gt(self.var_ecsp, self.var_ects):
                self.var_ecsp += -0.1
            else:
                pass

    @warp
    async def my_UpdateTimers(self, util, ):
        util.sprites.stage.var_tick += 1
        if eq(self.var_LapTicks, ""):
            if not eq(self.var_y, 0):
                self.var_LapTicks = 1
        else:
            self.var_LapTicks += 1
            util.sprites.stage.var_LapTime = ""
            self.var_i = self.var_LapTicks
            await self.my_AppendTime(util, math.floor((div((tonum(self.var_i) % 30), 30) * 100)), "")
            self.var_i = math.floor(div(self.var_i, 30))
            await self.my_AppendTime(util, (tonum(self.var_i) % 60), ".")
            self.var_i = math.floor(div(self.var_i, 60))
            await self.my_AppendTime(util, self.var_i, ":")
            if gt(self.var_y, self.var_NextLapY):
                util.sprites.stage.var_LastLap = util.sprites.stage.var_LapTime
                self.var_NextLapY += (400 * len(util.sprites.stage.list_track_x))
                self.var_LapTicks = 1
                print(util.sprites.stage.var_LastLap)
                util.send_broadcast("rickroll")

    @warp
    async def my_AppendTime(self, util, arg_num, arg_sep):
        if lt(arg_num, 10):
            util.sprites.stage.var_LapTime = (("0" + str(arg_num)) + (arg_sep + util.sprites.stage.var_LapTime))
        else:
            util.sprites.stage.var_LapTime = (str(arg_num) + (arg_sep + util.sprites.stage.var_LapTime))

    @warp
    async def my_SetCostume(self, util, arg_costume):
        if not eq(arg_costume, self.costume.number):
            self.costume.switch(arg_costume)

    @warp
    async def my_Init(self, util, ):
        self.list_RoadLag.delete_all()
        for _ in range(10):
            self.list_RoadLag.append(0)
        util.sprites.stage.var_LastLap = ""
        util.sprites.stage.var_LapTime = "00:00.00"
        self.var_LapTicks = 0
        util.sprites.stage.var_car_slide = 0
        pass # hide variable

    @on_broadcast('crash')
    async def broadcast_crash(self, util):
        pass

    @on_broadcast('tick')
    async def broadcast_tick(self, util):
        if get_connected()[0]:
            state=get_state(0)
            trigger_values=get_trigger_values(state)
            util.sprites.stage.var_brake, util.sprites.stage.var_gas=trigger_values
            util.sprites.stage.var_steering=get_thumb_values(state)[0][0]
        else:
            if util.inputs["up arrow"]:
                util.sprites.stage.var_gas = 1
            else:
                util.sprites.stage.var_gas = 0
            if util.inputs["down arrow"]:
                util.sprites.stage.var_brake = 1
            else:
                util.sprites.stage.var_brake = 0
            if (util.inputs["left arrow"] and not util.inputs["right arrow"]):
                util.sprites.stage.var_steering = -1
            else:
                if (util.inputs["right arrow"] and not util.inputs["left arrow"]):
                    util.sprites.stage.var_steering = 1
                else:
                    util.sprites.stage.var_steering = 0


@sprite('Sprite2')
class Sprite2(Target):
    """Sprite Sprite2"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = 0
        self._ypos = 0
        self._direction = 90
        self.shown = False
        self.pen = Pen(self)

        self.costume = Costumes(
           1, 100, "all around", [
            {
                'name': "grass1",
                'path': "12e4e3b737f9796599f649a8452c2fdc.png",
                'center': (480, 4),
                'scale': 2
            },
            {
                'name': "grass2",
                'path': "82b25121d43ae02e53a7a2c9b8bd4830.png",
                'center': (480, 4),
                'scale': 2
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "pop",
                'path': "83a9787d4cb6f3b7632b4ddfebf74367.wav"
            }
        ])

        self.var_id = 999
        self.var_x = -999



        self.sprite.layer = 2

    @on_broadcast('create clones')
    async def broadcast_createclones(self, util):
        self.shown = False
        await self.my_createclones(util, )

    @on_broadcast('tick')
    async def broadcast_tick(self, util):
        if eq(self.costume.number, 1):
            if gt(self.var_id, len(util.sprites.stage.list_Grass1)):
                self.var_x = -999
            else:
                self.var_x = util.sprites.stage.list_Grass1X[toint(self.var_id)]
                self.ypos = tonum(util.sprites.stage.list_Grass1[toint(self.var_id)])
        else:
            if gt(self.var_id, len(util.sprites.stage.list_Grass2)):
                self.var_x = -999
            else:
                self.var_x = util.sprites.stage.list_Grass2X[toint(self.var_id)]
                self.ypos = tonum(util.sprites.stage.list_Grass2[toint(self.var_id)])
        if (gt(self.var_x, -477) and lt(self.var_x, 477)):
            self.xpos = tonum(self.var_x)
            self.shown = True
        else:
            self.shown = False

    @warp
    async def my_createclones(self, util, ):
        self.gotoxy(0, 0)
        self.costume.switch("grass1")
        self.var_id = 0
        for _ in range(95):
            self.var_id += 1
            self.create_clone_of(util, "_myself_")
        self.costume.switch("grass2")
        self.var_id = 0
        for _ in range(95):
            self.var_id += 1
            self.create_clone_of(util, "_myself_")
        self.var_id = 999


@sprite('sky')
class Spritesky(Target):
    """Sprite sky"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = -240
        self._ypos = 0
        self._direction = 90
        self.shown = True
        self.pen = Pen(self)

        self.costume = Costumes(
           0, 100, "all around", [
            {
                'name': "sky",
                'path': "fe2f729fae25240bea43edffc158c19e.png",
                'center': (480, 360),
                'scale': 2
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "pop",
                'path': "83a9787d4cb6f3b7632b4ddfebf74367.wav"
            }
        ])





        self.sprite.layer = 1

    @on_green_flag
    async def green_flag(self, util):
        self.change_layer(util, -1000)
        util.sprites.stage.var_horizon_x = 0
        self.gotoxy(-240, 0)
        self.shown = True

    @on_broadcast('tick')
    async def broadcast_tick(self, util):
        self.xpos = ((util.sprites.stage.var_horizon_x % 480) - 240)


@sprite('Other Cars')
class SpriteOtherCars(Target):
    """Sprite Other Cars"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = -21.779999999999998
        self._ypos = 58
        self._direction = 90
        self.shown = False
        self.pen = Pen(self)

        self.costume = Costumes(
           0, 27, "all around", [
            {
                'name': "red1",
                'path': "11cc2ed9a8813dbccee85c82a69eade4.png",
                'center': (34, 49),
                'scale': 2
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "meow",
                'path': "83c36d806dc92327b9e7049a565c6bff.wav"
            }
        ])

        self.var_carID = 1
        self.var_py = -999
        self.var_z = 370.3703703703704



        self.sprite.layer = 3

    @on_broadcast('create clones')
    async def broadcast_createclones(self, util):
        self.shown = False
        self.var_carID = 1

    @on_broadcast('tick')
    async def broadcast_tick(self, util):
        self.var_py = util.sprites.stage.list_CarsPY[toint(self.var_carID)]
        if lt(self.var_py, -177):
            self.shown = False
        else:
            self.gotoxy(tonum(util.sprites.stage.list_CarsPX[toint(self.var_carID)]), tonum(self.var_py))
            self.var_z = (div(-100, (tonum(self.var_py) - 85)) * 100)
            self.costume.size = div(10000, self.var_z)
            self.shown = True

    @on_green_flag
    async def green_flag(self, util):
        self.gotoxy(0, 20)

    @on_broadcast('crash')
    async def broadcast_crash(self, util):
        self.shown = False


@sprite('map')
class Spritemap(Target):
    """Sprite map"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = 150
        self._ypos = 125
        self._direction = 90
        self.shown = True
        self.pen = Pen(self)

        self.costume = Costumes(
           0, 35, "all around", [
            {
                'name': "circuit1",
                'path': "d4b34470d7af56cc12a962c9967235b0.png",
                'center': (449, 229),
                'scale': 2
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "pop",
                'path': "83a9787d4cb6f3b7632b4ddfebf74367.wav"
            }
        ])

        self.var_x = -107.128433125496
        self.var_y = 65.25398084054217
        self.var_a = 360
        self.var_GetDirection = 119.10047741154344
        self.var_i = 175
        self.var_la = 360



        self.sprite.layer = 16

    @on_green_flag
    async def green_flag(self, util):
        self.gotoxy(150, 125)
        self.direction = 90
        self.costume.size = 35
        self.costume.set_effect('ghost', 25)
        self.front_layer(util)

    @warp
    async def my_GetDirection(self, util, arg_dx, arg_dy):
        if eq(arg_dy, 0):
            if gt(arg_dx, 0):
                self.var_GetDirection = 90
            else:
                self.var_GetDirection = -90
        else:
            self.var_GetDirection = math.degrees(math.atan(div(arg_dx, arg_dy)))
            if lt(arg_dy, 0):
                if gt(arg_dx, 0):
                    self.var_GetDirection += 180
                else:
                    if lt(arg_dx, 0):
                        self.var_GetDirection += -180
                    else:
                        self.var_GetDirection = 180

    @on_pressed('m')
    async def key_m_pressed(self, util):
        pass

    @warp
    async def my_Reposition(self, util, ):
        self.gotoxy((((0 - self.var_x) * math.cos(math.radians(tonum(self.var_a)))) - ((0 - self.var_y) * math.sin(math.radians(tonum(self.var_a))))), (((0 - self.var_y) * math.cos(math.radians(tonum(self.var_a)))) + ((0 - self.var_x) * math.sin(math.radians(tonum(self.var_a))))))
        self.direction = (0 - tonum(self.var_a))


@sprite('fog')
class Spritefog(Target):
    """Sprite fog"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = 0
        self._ypos = 0
        self._direction = 90
        self.shown = True
        self.pen = Pen(self)

        self.costume = Costumes(
           3, 100, "don't rotate", [
            {
                'name': "Fog",
                'path': "da6c2454574d32be9f3c77cb84a3254d.png",
                'center': (480, 360),
                'scale': 2
            },
            {
                'name': "Gradient2",
                'path': "23d63f1fa4c39033921687cb03b0468e.png",
                'center': (480, 360),
                'scale': 2
            },
            {
                'name': "Gradient3",
                'path': "d57c7e883326eec0ec76d30242fefbcd.png",
                'center': (480, 360),
                'scale': 2
            },
            {
                'name': "Gradient4",
                'path': "ba6354bd04ca6caf47b95c66562f7883.png",
                'center': (480, 122),
                'scale': 2
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "pop",
                'path': "83a9787d4cb6f3b7632b4ddfebf74367.wav"
            }
        ])

        self.var_y = 0
        self.var_i = 0
        self.var_psp = 0
        self.var_yy = 0
        self.var_z = 0
        self.var_x1 = 0
        self.var_x2 = 0
        self.var_t = 0
        self.var_road_target = 0
        self.var_road_time = 0
        self.var_nextCarY = 0
        self.var_nextCar = 0
        self.var_debug = 0
        self.var_ecsp = 0
        self.var_ects = 0
        self.var_NextLapY = 0
        self.var_LapTicks = 0

        self.list_RoadLag = StaticList(
            []
        )

        self.sprite.layer = 14

    @on_green_flag
    async def green_flag(self, util):
        self.gotoxy(0, 0)
        self.shown = True
        self.front_layer(util)


@sprite('map trace')
class Spritemaptrace(Target):
    """Sprite map trace"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = 173.8
        self._ypos = 162.45
        self._direction = 90
        self.shown = True
        self.pen = Pen(self)

        self.costume = Costumes(
           1, 100, "all around", [
            {
                'name': "path",
                'path': "cfba1a6258c5c82fb1d2b97b828231f8.png",
                'center': (6, 26),
                'scale': 2
            },
            {
                'name': "red dot",
                'path': "74da904f605317f24e7877d6176e3704.png",
                'center': (8, 8),
                'scale': 2
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "pop",
                'path': "83a9787d4cb6f3b7632b4ddfebf74367.wav"
            }
        ])

        self.var_d = 1



        self.sprite.layer = 18

    @on_green_flag
    async def green_flag(self, util):
        self.costume.switch("red dot")
        self.shown = True
        await self.sleep(0.1)
        self.front_layer(util)

    @on_pressed('m')
    async def key_m_pressed(self, util):
        self.costume.switch("path")
        self.gotoxy(0, 0)
        self.shown = True
        await self.sleep(0.1)
        self.front_layer(util)

    @on_broadcast('tick')
    async def broadcast_tick(self, util):
        self.var_d = ((math.floor(div(util.sprites["Game"].var_y, 400)) % len(util.sprites.stage.list_track_x)) + 1)
        self.gotoxy((util.sprites["map"].xpos + (tonum(util.sprites.stage.list_track_y[toint(self.var_d)]) * 0.35)), (util.sprites["map"].ypos - (tonum(util.sprites.stage.list_track_x[toint(self.var_d)]) * 0.35)))


@sprite('Sprite_FX_Dust_0013')
class Sprite_FX_Dust_0013(Target):
    """Sprite Sprite_FX_Dust_0013"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = -9.977243402337551
        self._ypos = -136
        self._direction = 90
        self.shown = False
        self.pen = Pen(self)

        self.costume = Costumes(
           3, 150, "all around", [
            {
                'name': "Sprite_FX_Dust_2",
                'path': "55eda6d867b90e6b38b147a807876778.png",
                'center': (66, 35),
                'scale': 2
            },
            {
                'name': "Sprite_FX_Dust_3",
                'path': "15c553610f11c000c96c110f791ce519.png",
                'center': (62, 33),
                'scale': 2
            },
            {
                'name': "Sprite_FX_Dust_4",
                'path': "544fa2b7ad042acbc67fe0169da64532.png",
                'center': (64, 35),
                'scale': 2
            },
            {
                'name': "Sprite_FX_Dust_5",
                'path': "1f936adf5adfb4d78d8046d79b55e7a8.png",
                'center': (64, 35),
                'scale': 2
            },
            {
                'name': "Sprite_FX_Dust_6",
                'path': "055acb33597e867db438cdd8b11b4f67.png",
                'center': (66, 33),
                'scale': 2
            },
            {
                'name': "Sprite_FX_Dust_7",
                'path': "1dba00576e07223cf13808bd54d0b24c.png",
                'center': (69, 33),
                'scale': 2
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "pop",
                'path': "83a9787d4cb6f3b7632b4ddfebf74367.wav"
            }
        ])

        self.var_frame = 0
        self.var_mode = 0



        self.sprite.layer = 13

    @on_green_flag
    async def green_flag(self, util):
        self.shown = False
        self.costume.size = 150
        self.var_frame = 0
        self.var_mode = 0

    @on_broadcast('tick')
    async def broadcast_tick(self, util):
        if ((gt(util.sprites.stage.var_IsAccellerating, 0) and lt(util.sprites.stage.var_speed, 5)) or (lt(util.sprites.stage.var_IsAccellerating, 0) and gt(util.sprites.stage.var_speed, 6))):
            if not eq(self.var_mode, 1):
                self.front_layer(util)
                self.var_mode = 1
                self.var_frame = 0
            else:
                self.var_frame += 0.25
            await self.my_SetCostumeA(util, ((math.floor(self.var_frame) % 6) + 1), 150)
            self.gotoxy(util.sprites["Game"].xpos, (util.sprites["Game"].ypos - 16))
            self.shown = True
        else:
            if gt(util.sprites.stage.var_car_slide, 5):
                if not eq(self.var_mode, 2):
                    self.front_layer(util)
                    self.var_mode = 2
                    self.var_frame = 0
                else:
                    self.var_frame += 0.25
                await self.my_SetCostumeA(util, ((math.floor(self.var_frame) % 6) + 1), 200)
                self.gotoxy((util.sprites["Game"].xpos - (util.sprites.stage.var_car_sx * 2)), (util.sprites["Game"].ypos - 16))
                self.shown = True
            else:
                self.var_mode = 0
                self.shown = False

    @warp
    async def my_SetCostumeA(self, util, arg_costume, arg_size):
        if not eq(arg_costume, self.costume.number):
            self.costume.switch(arg_costume)
        if not eq(arg_size, round(self.costume.size)):
            self.costume.size = arg_size


@sprite('ENG-RPM')
class SpriteENGRPM(Target):
    """Sprite ENG-RPM"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = -53
        self._ypos = -36
        self._direction = 90
        self.shown = True
        self.pen = Pen(self)

        self.costume = Costumes(
           0, 100, "all around", [
            {
                'name': "costume1",
                'path': "d36f6603ec293d2c2198d3ea05109fe0.png",
                'center': (0, 0),
                'scale': 2
            }
        ])

        self.sounds = Sounds(
            10, [

        ])





        self.sprite.layer = 4

    @on_green_flag
    async def green_flag(self, util):
        util.sprites.stage.var_GEAR = 1
        util.sprites.stage.var_MaxRpm = 7500

    @on_broadcast('crash')
    async def broadcast_crash(self, util):
        self.stop_other()
        util.sprites.stage.var_RPM = 0

    @on_broadcast('tick')
    async def broadcast_tick(self, util):
        global eng
        if eq(util.sprites.stage.var_CHANGE, 0):
            if eq(util.sprites.stage.var_GEAR, 1):
                if (eq(util.sprites.stage.var_IsAccellerating, 1) and lt(util.sprites.stage.var_RPM, util.sprites.stage.var_MaxRpm)):
                    util.sprites.stage.var_RPM += 416
                else:
                    if gt(util.sprites.stage.var_RPM, 750):
                        util.sprites.stage.var_RPM += -97
            if eq(util.sprites.stage.var_GEAR, 2):
                util.sprites.stage.var_RPM = ((util.sprites.stage.var_KMH * 95) + 750)
            if eq(util.sprites.stage.var_GEAR, 3):
                util.sprites.stage.var_RPM = ((util.sprites.stage.var_KMH * 58) + 750)
            if eq(util.sprites.stage.var_GEAR, 4):
                util.sprites.stage.var_RPM = ((util.sprites.stage.var_KMH * 40.3) + 750)
            if eq(util.sprites.stage.var_GEAR, 5):
                util.sprites.stage.var_RPM = ((util.sprites.stage.var_KMH * 32.6) + 750)
            if eq(util.sprites.stage.var_GEAR, 6):
                util.sprites.stage.var_RPM = ((util.sprites.stage.var_KMH * 27.4) + 750)
            if eq(util.sprites.stage.var_GEAR, 7):
                util.sprites.stage.var_RPM = ((util.sprites.stage.var_KMH * 24.2) + 750)
            if eq(util.sprites.stage.var_GEAR, 8):
                util.sprites.stage.var_RPM = ((util.sprites.stage.var_KMH * 21.3) + 750)
            if lt(util.sprites.stage.var_RPM, 750):
                util.sprites.stage.var_RPM = 750
            if gt(util.sprites.stage.var_RPM, 8000):
                util.sprites.stage.var_RPM = 8000
            if eq(util.sprites.stage.var_IsAccellerating, -1):
                if gt(util.sprites.stage.var_RPM, 750):
                    util.sprites.stage.var_RPM += -100
            if lt(util.sprites.stage.var_speed, 0):
                util.sprites.stage.var_speed = 0
        eng.specific_rpm(util.sprites.stage.var_RPM)
        emulator.answer['RPM'] = '<exec>ECU_R_ADDR_E + " 04 41 0C %.4X" % int(4 * '+str(util.sprites.stage.var_RPM)+')</exec><writeln />'
        if (util.sprites.stage.var_speed*7)*1.609344>255:
            emulator.answer['SPEED'] = '<header>7E8</header><size>02</size><subd>41 0D</subd><eval>"%.2X" % 255</eval><space /><writeln />'
        else:
            emulator.answer['SPEED'] = '<header>7E8</header><size>02</size><subd>41 0D</subd><eval>"%.2X" % '+str(int(util.sprites.stage.var_speed*7*1.609344))+'</eval><space /><writeln />'
        emulator.answer['THROTTLE_POS'] = '<exec>ECU_R_ADDR_E + " 04 41 11 %.2X" % int(255 * '+str(max(0, util.sprites.stage.var_IsAccellerating))+')</exec><writeln />'
    @on_broadcast('tick')
    async def broadcast_tick1(self, util):
        pass

    @on_broadcast('tick')
    async def broadcast_tick2(self, util):
        util.sprites.stage.var_KMH = ((util.sprites.stage.var_speed * 7) * 1.609)


@sprite('GEARS')
class SpriteGEARS(Target):
    """Sprite GEARS"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = -179
        self._ypos = -122.33953857421875
        self._direction = 90
        self.shown = True
        self.pen = Pen(self)

        self.costume = Costumes(
           0, 100, "all around", [
            {
                'name': "not",
                'path': "3fa9cbd3b3080ac10f1ef05646785001.png",
                'center': (12, 17),
                'scale': 2
            },
            {
                'name': "not2",
                'path': "25ad044f448f18c29ed3a7ae38bb21fe.png",
                'center': (9, 17),
                'scale': 2
            },
            {
                'name': "not9",
                'path': "a6b9b2c9512b847425c279f802294edd.png",
                'center': (9, 17),
                'scale': 2
            },
            {
                'name': "not3",
                'path': "7cd9c55717fb6bc46dbafc4fa6ae7562.png",
                'center': (10, 17),
                'scale': 2
            },
            {
                'name': "not10",
                'path': "123373605b45077085f2ad2ac99cda17.png",
                'center': (10, 17),
                'scale': 2
            },
            {
                'name': "not4",
                'path': "313317402e8f6abda4647f922d7d1eb1.png",
                'center': (11, 17),
                'scale': 2
            },
            {
                'name': "not11",
                'path': "d4cb7c82a1657dfe52ef1ed236b8c068.png",
                'center': (11, 17),
                'scale': 2
            },
            {
                'name': "not5",
                'path': "a5f9489ae7521258a9e3fc22c0826893.png",
                'center': (11, 17),
                'scale': 2
            },
            {
                'name': "not12",
                'path': "3cf56c611a98a3144bfa1004adb22196.png",
                'center': (11, 17),
                'scale': 2
            },
            {
                'name': "not6",
                'path': "d9ddda7ad10ed691c9d15bd8e89a8403.png",
                'center': (10, 17),
                'scale': 2
            },
            {
                'name': "not13",
                'path': "5cc57fffa70593313cc15cb980e093c8.png",
                'center': (10, 17),
                'scale': 2
            },
            {
                'name': "not7",
                'path': "c67427ad6ffb9e5838e7cb01e7c0a87b.png",
                'center': (10, 17),
                'scale': 2
            },
            {
                'name': "not14",
                'path': "b5c9e020be2af084c162fed78b9b21f4.png",
                'center': (10, 17),
                'scale': 2
            },
            {
                'name': "not8",
                'path': "25c1578cfe1944e149aeafc32151ee87.png",
                'center': (11, 17),
                'scale': 2
            },
            {
                'name': "not15",
                'path': "f4e2dde059f0f2fd0496994662190727.png",
                'center': (11, 17),
                'scale': 2
            },
            {
                'name': "not16",
                'path': "85370247c539be4edaddd7b2c07c4f9d.png",
                'center': (8, 15),
                'scale': 2
            },
            {
                'name': "not17",
                'path': "56af6a4b3624b767836de82827b7aca9.png",
                'center': (8, 15),
                'scale': 2
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "pop",
                'path': "83a9787d4cb6f3b7632b4ddfebf74367.wav"
            }
        ])





        self.sprite.layer = 17

    @on_green_flag
    async def green_flag(self, util):
        util.sprites.stage.var_RPM = 0
        self.costume.size = 100
        if eq(util.sprites.stage.var_IsAccellerating, 1):
            util.sprites.stage.var_GEAR = 2
        else:
            util.sprites.stage.var_GEAR = 1
        self.costume.switch("not")
        util.sprites.stage.var_ON = 1
        self.front_layer(util)
        for _ in range(15):
            util.sprites.stage.var_RPM += 50

            await self.yield_()
        util.sprites.stage.var_DMODE = 2
        util.sprites.stage.var_Gearbox = 0

    @on_green_flag
    async def green_flag1(self, util):
        util.sprites.stage.var_CHANGE = 0

    @on_broadcast('gear_up')
    async def broadcast_GEAR_UP(self, util):
        if lt(util.sprites.stage.var_GEAR, 8):
            util.sprites.stage.var_CHANGE = 1
            util.sprites.stage.var_GEAR += 1
            if eq(util.sprites.stage.var_GEAR, 3):
                while not lt(util.sprites.stage.var_RPM, ((util.sprites.stage.var_KMH * 58) + 750)):
                    util.sprites.stage.var_RPM += -231

                    await self.yield_()
                util.sprites.stage.var_CHANGE = 0
            if eq(util.sprites.stage.var_GEAR, 4):
                while not lt(util.sprites.stage.var_RPM, ((util.sprites.stage.var_KMH * 40.3) + 750)):
                    util.sprites.stage.var_RPM += -231

                    await self.yield_()
                util.sprites.stage.var_CHANGE = 0
            if eq(util.sprites.stage.var_GEAR, 5):
                while not lt(util.sprites.stage.var_RPM, ((util.sprites.stage.var_KMH * 32.6) + 750)):
                    util.sprites.stage.var_RPM += -231

                    await self.yield_()
                util.sprites.stage.var_CHANGE = 0
            if eq(util.sprites.stage.var_GEAR, 6):
                while not lt(util.sprites.stage.var_RPM, ((util.sprites.stage.var_KMH * 27.4) + 750)):
                    util.sprites.stage.var_RPM += -231

                    await self.yield_()
                util.sprites.stage.var_CHANGE = 0
            if eq(util.sprites.stage.var_GEAR, 7):
                while not lt(util.sprites.stage.var_RPM, ((util.sprites.stage.var_KMH * 24.2) + 750)):
                    util.sprites.stage.var_RPM += -231

                    await self.yield_()
                util.sprites.stage.var_CHANGE = 0
            if eq(util.sprites.stage.var_GEAR, 8):
                while not lt(util.sprites.stage.var_RPM, ((util.sprites.stage.var_KMH * 21.3) + 750)):
                    util.sprites.stage.var_RPM += -231

                    await self.yield_()
                util.sprites.stage.var_CHANGE = 0
        util.sprites.stage.var_CHANGE = 0
        await self.sleep(0.2)

    @on_broadcast('gear_down')
    async def broadcast_GEAR_DOWN(self, util):
        if gt(util.sprites.stage.var_GEAR, 1):
            util.sprites.stage.var_CHANGE = 2
            util.sprites.stage.var_GEAR += -1
            if eq(util.sprites.stage.var_GEAR, 7):
                while not gt(util.sprites.stage.var_RPM, ((util.sprites.stage.var_KMH * 21.3) + 750)):
                    util.sprites.stage.var_RPM += 231

                    await self.yield_()
                util.sprites.stage.var_CHANGE = 0
            if eq(util.sprites.stage.var_GEAR, 6):
                while not gt(util.sprites.stage.var_RPM, ((util.sprites.stage.var_KMH * 27.4) + 750)):
                    util.sprites.stage.var_RPM += 231

                    await self.yield_()
                util.sprites.stage.var_CHANGE = 0
            if eq(util.sprites.stage.var_GEAR, 5):
                while not gt(util.sprites.stage.var_RPM, ((util.sprites.stage.var_KMH * 32.6) + 750)):
                    util.sprites.stage.var_RPM += 231

                    await self.yield_()
                util.sprites.stage.var_CHANGE = 0
            if eq(util.sprites.stage.var_GEAR, 4):
                while not gt(util.sprites.stage.var_RPM, ((util.sprites.stage.var_KMH * 40.3) + 750)):
                    util.sprites.stage.var_RPM += 231

                    await self.yield_()
                util.sprites.stage.var_CHANGE = 0
            if eq(util.sprites.stage.var_GEAR, 3):
                while not gt(util.sprites.stage.var_RPM, ((util.sprites.stage.var_KMH * 58) + 750)):
                    util.sprites.stage.var_RPM += 231

                    await self.yield_()
                util.sprites.stage.var_CHANGE = 0
            if eq(util.sprites.stage.var_GEAR, 2):
                while not gt(util.sprites.stage.var_RPM, ((util.sprites.stage.var_KMH * 95) + 750)):
                    util.sprites.stage.var_RPM += 231

                    await self.yield_()
                util.sprites.stage.var_CHANGE = 0
            if eq(util.sprites.stage.var_GEAR, 1):
                util.sprites.stage.var_CHANGE = 0
        util.sprites.stage.var_CHANGE = 0
        await self.sleep(0.2)

    @on_broadcast('tick')
    async def broadcast_tick(self, util):
        if eq(util.sprites.stage.var_CHANGE, 0):
            if eq(util.sprites.stage.var_GEAR, 1):
                self.costume.switch("not")
            else:
                if gt(util.sprites.stage.var_RPM, 7000):
                    self.costume.switch((((util.sprites.stage.var_GEAR - 1) * 2) + 1))
                else:
                    self.costume.switch(((util.sprites.stage.var_GEAR - 1) * 2))
        else:
            if eq(util.sprites.stage.var_CHANGE, 1):
                self.costume.switch("not17")
            else:
                self.costume.switch("not16")

    @on_broadcast('crash')
    async def broadcast_crash(self, util):
        self.costume.switch("not")

    @on_broadcast('gear_down')
    async def broadcast_GEAR_DOWN1(self, util):
        pass

    @on_broadcast('gear_up')
    async def broadcast_GEAR_UP1(self, util):
        pass


@sprite('TransmissionSettings')
class SpriteTransmissionSettings(Target):
    """Sprite TransmissionSettings"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = 80
        self._ypos = 0
        self._direction = 90
        self.shown = True
        self.pen = Pen(self)

        self.costume = Costumes(
           0, 60, "all around", [
            {
                'name': "costume1",
                'path': "c446646a95cd43c36d25583fdaea3dbc.png",
                'center': (0, 0),
                'scale': 2
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "pop",
                'path': "83a9787d4cb6f3b7632b4ddfebf74367.wav"
            }
        ])





        self.sprite.layer = 5

    @on_broadcast('tick')
    async def broadcast_tick(self, util):
        if (not gt(util.sprites.stage.var_IsAccellerating, 0) or (gt(util.sprites.stage.var_GEAR, 3) and eq(util.sprites.stage.var_touchinggrass, 1))) and ((((util.sprites.stage.var_RPM>3800 and util.sprites.stage.var_RPM<4000) or util.sprites.stage.var_RPM<=1200) and util.sprites.stage.var_GEAR>2) or util.sprites.stage.var_speed==0 and util.sprites.stage.var_GEAR>1):
            util.send_broadcast("GEAR_DOWN")
        if (((gt(util.sprites.stage.var_IsAccellerating, 0) and (lt(util.sprites.stage.var_GEAR, 3) or not eq(util.sprites.stage.var_touchinggrass, 1))) and (gt(util.sprites.stage.var_RPM, max(1800, 7200 * util.sprites.stage.var_IsAccellerating)) or gt(util.sprites.stage.var_RPM, (util.sprites.stage.var_MaxRpm + 200)))) and lt(util.sprites.stage.var_GEAR, 8)):
            util.send_broadcast("GEAR_UP")
        if (gt(util.sprites.stage.var_IsAccellerating, 0) and eq(util.sprites.stage.var_GEAR, 1)):
            util.send_broadcast("GEAR_UP")
        if util.sprites.stage.var_IsAccellerating==1.0 and util.sprites.stage.var_CHANGE==0:
            if util.sprites.stage.var_GEAR==3 and util.sprites.stage.var_MPH<35:
                util.send_broadcast("GEAR_DOWN")
            if util.sprites.stage.var_GEAR==4 and util.sprites.stage.var_MPH<60:
                util.send_broadcast("GEAR_DOWN")
            if util.sprites.stage.var_GEAR==5 and util.sprites.stage.var_MPH<80:
                util.send_broadcast("GEAR_DOWN")
            if util.sprites.stage.var_GEAR==6 and util.sprites.stage.var_MPH<90:
                util.send_broadcast("GEAR_DOWN")
            if util.sprites.stage.var_GEAR==7 and util.sprites.stage.var_MPH<100:
                util.send_broadcast("GEAR_DOWN")
            if util.sprites.stage.var_GEAR==8 and util.sprites.stage.var_MPH<110:
                util.send_broadcast("GEAR_DOWN")


@sprite('1')
class Spriteidentifier(Target):
    """Sprite 1"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = -160
        self._ypos = -160
        self._direction = 90
        self.shown = True
        self.pen = Pen(self)

        self.costume = Costumes(
           9, 150, "all around", [
            {
                'name': "1",
                'path': "4e12357216a36ef7b46244df375b8d46.png",
                'center': (8, 20),
                'scale': 2
            },
            {
                'name': "2",
                'path': "12ac81f6efeb59714bf017899391ef00.png",
                'center': (15, 21),
                'scale': 2
            },
            {
                'name': "3",
                'path': "70b80adc5f9dac25df064fa20bb431df.png",
                'center': (14, 21),
                'scale': 2
            },
            {
                'name': "4",
                'path': "53e6a16f4e26dbd6e3756f4fa750a0f7.png",
                'center': (14, 20),
                'scale': 2
            },
            {
                'name': "5",
                'path': "da4ca8dfc7746207f354676041980d37.png",
                'center': (14, 20),
                'scale': 2
            },
            {
                'name': "6",
                'path': "9b8f675b3d67a635a256fce9d898bca6.png",
                'center': (12, 21),
                'scale': 2
            },
            {
                'name': "7",
                'path': "023d34a022ff79f513d8e3fd1d7ac187.png",
                'center': (11, 20),
                'scale': 2
            },
            {
                'name': "8",
                'path': "c244d0acc777bada6c47df42281f057f.png",
                'center': (13, 21),
                'scale': 2
            },
            {
                'name': "9",
                'path': "4ce26c4f518361a1d052ece3d7bb570d.png",
                'center': (12, 21),
                'scale': 2
            },
            {
                'name': "10",
                'path': "7b50fbc8f47862facb6f9f6c747cf0a4.png",
                'center': (12, 21),
                'scale': 2
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "pop",
                'path': "83a9787d4cb6f3b7632b4ddfebf74367.wav"
            }
        ])





        self.sprite.layer = 6

    @on_green_flag
    async def green_flag(self, util):
        pass

    @on_broadcast('tick')
    async def broadcast_tick(self, util):
        self.costume.switch(letter_of(str((util.sprites.stage.var_MPH % 10)), 1))


@sprite('10')
class SpriteidentifierA(Target):
    """Sprite 10"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = -180
        self._ypos = -160
        self._direction = 90
        self.shown = True
        self.pen = Pen(self)

        self.costume = Costumes(
           9, 150, "all around", [
            {
                'name': "1",
                'path': "4e12357216a36ef7b46244df375b8d46.png",
                'center': (8, 20),
                'scale': 2
            },
            {
                'name': "2",
                'path': "12ac81f6efeb59714bf017899391ef00.png",
                'center': (15, 21),
                'scale': 2
            },
            {
                'name': "3",
                'path': "70b80adc5f9dac25df064fa20bb431df.png",
                'center': (14, 21),
                'scale': 2
            },
            {
                'name': "4",
                'path': "53e6a16f4e26dbd6e3756f4fa750a0f7.png",
                'center': (14, 20),
                'scale': 2
            },
            {
                'name': "5",
                'path': "da4ca8dfc7746207f354676041980d37.png",
                'center': (14, 20),
                'scale': 2
            },
            {
                'name': "6",
                'path': "9b8f675b3d67a635a256fce9d898bca6.png",
                'center': (12, 21),
                'scale': 2
            },
            {
                'name': "7",
                'path': "023d34a022ff79f513d8e3fd1d7ac187.png",
                'center': (11, 20),
                'scale': 2
            },
            {
                'name': "8",
                'path': "c244d0acc777bada6c47df42281f057f.png",
                'center': (13, 21),
                'scale': 2
            },
            {
                'name': "9",
                'path': "4ce26c4f518361a1d052ece3d7bb570d.png",
                'center': (12, 21),
                'scale': 2
            },
            {
                'name': "10",
                'path': "7b50fbc8f47862facb6f9f6c747cf0a4.png",
                'center': (12, 21),
                'scale': 2
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "pop",
                'path': "83a9787d4cb6f3b7632b4ddfebf74367.wav"
            }
        ])





        self.sprite.layer = 7

    @on_broadcast('tick')
    async def broadcast_tick(self, util):
        self.costume.switch(letter_of(str((math.floor(div(util.sprites.stage.var_MPH, 10)) % 10)), 1))
        if gt(math.floor(div(util.sprites.stage.var_MPH, 10)), 0):
            self.costume.clear_effects()
        else:
            self.costume.set_effect('brightness', -25)


@sprite('100')
class SpriteidentifierB(Target):
    """Sprite 100"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = -200
        self._ypos = -160
        self._direction = 90
        self.shown = True
        self.pen = Pen(self)

        self.costume = Costumes(
           9, 150, "all around", [
            {
                'name': "1",
                'path': "4e12357216a36ef7b46244df375b8d46.png",
                'center': (8, 20),
                'scale': 2
            },
            {
                'name': "2",
                'path': "12ac81f6efeb59714bf017899391ef00.png",
                'center': (15, 21),
                'scale': 2
            },
            {
                'name': "3",
                'path': "70b80adc5f9dac25df064fa20bb431df.png",
                'center': (14, 21),
                'scale': 2
            },
            {
                'name': "4",
                'path': "53e6a16f4e26dbd6e3756f4fa750a0f7.png",
                'center': (14, 20),
                'scale': 2
            },
            {
                'name': "5",
                'path': "da4ca8dfc7746207f354676041980d37.png",
                'center': (14, 20),
                'scale': 2
            },
            {
                'name': "6",
                'path': "9b8f675b3d67a635a256fce9d898bca6.png",
                'center': (12, 21),
                'scale': 2
            },
            {
                'name': "7",
                'path': "023d34a022ff79f513d8e3fd1d7ac187.png",
                'center': (11, 20),
                'scale': 2
            },
            {
                'name': "8",
                'path': "c244d0acc777bada6c47df42281f057f.png",
                'center': (13, 21),
                'scale': 2
            },
            {
                'name': "9",
                'path': "4ce26c4f518361a1d052ece3d7bb570d.png",
                'center': (12, 21),
                'scale': 2
            },
            {
                'name': "10",
                'path': "7b50fbc8f47862facb6f9f6c747cf0a4.png",
                'center': (12, 21),
                'scale': 2
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "pop",
                'path': "83a9787d4cb6f3b7632b4ddfebf74367.wav"
            }
        ])





        self.sprite.layer = 8

    @on_broadcast('tick')
    async def broadcast_tick(self, util):
        self.costume.switch(letter_of(str(math.floor(div(util.sprites.stage.var_MPH, 100))), 1))
        if gt(math.floor(div(util.sprites.stage.var_MPH, 100)), 0):
            self.costume.clear_effects()
        else:
            self.costume.set_effect('brightness', -25)


@sprite('blink')
class Spriteblink(Target):
    """Sprite blink"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = -179
        self._ypos = -121
        self._direction = 90
        self.shown = True
        self.pen = Pen(self)

        self.costume = Costumes(
           7, 100, "all around", [
            {
                'name': "costume5",
                'path': "474a4399ed790eca27a0df95f1d328e4.png",
                'center': (84, 125),
                'scale': 2
            },
            {
                'name': "costume2",
                'path': "ce1318d120bbe33c93b7dca0acc54083.png",
                'center': (84, 125),
                'scale': 2
            },
            {
                'name': "costume3",
                'path': "dec58d80a9c26293e4003836d488c4a3.png",
                'center': (84, 125),
                'scale': 2
            },
            {
                'name': "costume4",
                'path': "91a4b3fa7b4f071c25052b6b957977c5.png",
                'center': (84, 122),
                'scale': 2
            },
            {
                'name': "costume6",
                'path': "5d5de5e2cc728a6ba0f5e447f58e4bc9.png",
                'center': (84, 117),
                'scale': 2
            },
            {
                'name': "costume7",
                'path': "3deaef8b5a64ddcae042a929ea73f174.png",
                'center': (84, 111),
                'scale': 2
            },
            {
                'name': "costume8",
                'path': "d57cf0e8af315d52f75079149466dffe.png",
                'center': (84, 101),
                'scale': 2
            },
            {
                'name': "costume9",
                'path': "c446646a95cd43c36d25583fdaea3dbc.png",
                'center': (0, 0),
                'scale': 2
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "pop",
                'path': "83a9787d4cb6f3b7632b4ddfebf74367.wav"
            }
        ])





        self.sprite.layer = 9

    @on_broadcast('tick')
    async def broadcast_tick(self, util):
        if gt(util.sprites.stage.var_RPM, 7000):
            self.costume.switch("costume5")
        if (gt(util.sprites.stage.var_RPM, 6800) and lt(util.sprites.stage.var_RPM, 7000)):
            self.costume.switch("costume2")
        if (gt(util.sprites.stage.var_RPM, 6600) and lt(util.sprites.stage.var_RPM, 6800)):
            self.costume.switch("costume3")
        if (gt(util.sprites.stage.var_RPM, 6400) and lt(util.sprites.stage.var_RPM, 6600)):
            self.costume.switch("costume4")
        if (gt(util.sprites.stage.var_RPM, 6200) and lt(util.sprites.stage.var_RPM, 6400)):
            self.costume.switch("costume6")
        if (gt(util.sprites.stage.var_RPM, 6000) and lt(util.sprites.stage.var_RPM, 6200)):
            self.costume.switch("costume7")
        if (gt(util.sprites.stage.var_RPM, 5800) and lt(util.sprites.stage.var_RPM, 6000)):
            self.costume.switch("costume8")
        if lt(util.sprites.stage.var_RPM, 5800):
            self.costume.switch("costume9")


@sprite('pointer')
class Spritepointer(Target):
    """Sprite pointer"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = -179
        self._ypos = -121
        self._direction = 65.25
        self.shown = True
        self.pen = Pen(self)

        self.costume = Costumes(
           0, 100, "all around", [
            {
                'name': "costume2",
                'path': "6c759ced580c8527e3bb0a2c76c28dc9.png",
                'center': (113, 2),
                'scale': 2
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "pop",
                'path': "83a9787d4cb6f3b7632b4ddfebf74367.wav"
            }
        ])





        self.sprite.layer = 11

    @on_broadcast('tick')
    async def broadcast_tick(self, util):
        self.direction = ((util.sprites.stage.var_RPM * 0.027) + 45)


@sprite('gauge')
class Spritegauge(Target):
    """Sprite gauge"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = -179
        self._ypos = -121
        self._direction = 90
        self.shown = True
        self.pen = Pen(self)

        self.costume = Costumes(
           0, 100, "all around", [
            {
                'name': "costume2",
                'path': "d2bf962a168bba250554f2c7df3b8d6e.png",
                'center': (113, 113),
                'scale': 2
            },
            {
                'name': "costume3",
                'path': "7c95c21ca9b5255bceaf0d855f5e653b.png",
                'center': (113, 113),
                'scale': 2
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "Meow",
                'path': "83c36d806dc92327b9e7049a565c6bff.wav"
            }
        ])





        self.sprite.layer = 10

    @on_broadcast('tick')
    async def broadcast_tick(self, util):
        if (gt(util.sprites.stage.var_RPM, 7000) and eq(util.sprites.stage.var_CHANGE, 0)):
            self.costume.switch("costume3")
        else:
            self.costume.switch("costume2")


@sprite('Sprite1')
class Sprite1(Target):
    """Sprite Sprite1"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = -134
        self._ypos = 165
        self._direction = 90
        self.shown = False
        self.pen = Pen(self)

        self.costume = Costumes(
           12, 100, "all around", [
            {
                'name': "0",
                'path': "b2c88513024d459b754e77d83f61c85e.png",
                'center': (10, 17),
                'scale': 2
            },
            {
                'name': "1",
                'path': "25ad044f448f18c29ed3a7ae38bb21fe.png",
                'center': (9, 17),
                'scale': 2
            },
            {
                'name': "2",
                'path': "7cd9c55717fb6bc46dbafc4fa6ae7562.png",
                'center': (10, 17),
                'scale': 2
            },
            {
                'name': "3",
                'path': "313317402e8f6abda4647f922d7d1eb1.png",
                'center': (11, 17),
                'scale': 2
            },
            {
                'name': "4",
                'path': "a5f9489ae7521258a9e3fc22c0826893.png",
                'center': (11, 17),
                'scale': 2
            },
            {
                'name': "5",
                'path': "d9ddda7ad10ed691c9d15bd8e89a8403.png",
                'center': (10, 17),
                'scale': 2
            },
            {
                'name': "6",
                'path': "c67427ad6ffb9e5838e7cb01e7c0a87b.png",
                'center': (10, 17),
                'scale': 2
            },
            {
                'name': "7",
                'path': "25c1578cfe1944e149aeafc32151ee87.png",
                'center': (11, 17),
                'scale': 2
            },
            {
                'name': "8",
                'path': "a5ff3b021382f90770d138e9c1b29fc4.png",
                'center': (10, 17),
                'scale': 2
            },
            {
                'name': "9",
                'path': "e0e917a56ad09fde0ff1358972e47cce.png",
                'center': (10, 17),
                'scale': 2
            },
            {
                'name': ":",
                'path': "a42ad37d8886fef1552b930768cc128a.png",
                'center': (4, 10),
                'scale': 2
            },
            {
                'name': ".",
                'path': "523eb92d0170c50158ba2ca4d3490066.png",
                'center': (4, -6),
                'scale': 2
            },
            {
                'name': "",
                'path': "c446646a95cd43c36d25583fdaea3dbc.png",
                'center': (0, 0),
                'scale': 2
            }
        ])

        self.sounds = Sounds(
            100, [

        ])

        self.var_i = 9



        self.sprite.layer = 12

    @on_green_flag
    async def green_flag(self, util):
        self.costume.set_effect('brightness', -100)
        self.gotoxy(-230, 165)
        self.var_i = 1
        for _ in range(8):
            self.shown = True
            self.create_clone_of(util, "_myself_")
            self.xpos += 12
            self.var_i += 1

            await self.yield_()
        self.shown = False

    @on_broadcast('tick')
    async def broadcast_tick(self, util):
        if gt(self.var_i, 8):
            self.costume.switch(letter_of(util.sprites.stage.var_LastLap, toint((self.var_i - 8))))
        else:
            self.costume.switch(letter_of(util.sprites.stage.var_LapTime, toint(self.var_i)))



set_deadzone(DEADZONE_TRIGGER, 0)
if __name__ == '__main__':
    emulator=elm.Elm()
    emulator.net_port=35000
    emulator.scenario='car'
    Thread(target=emulator.run, daemon=True).start()
    engine.start_program()
