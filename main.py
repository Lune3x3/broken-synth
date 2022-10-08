from pyo import *
import random

s = Server().boot()

#gain control
s.amp = 0.1
#fundemetal frequency
freq = 100
#highest harmonic
high = 20

class ambient(EventInstrument):
    def __init__(self, **args):
        EventInstrument.__init__(self, **args)

        self.phase = Sine([self.freq, self.freq*1.003])
        self.ssaw = SuperSaw(freq=[100, 101], detune=0.6, bal=0.8, mul= 0.5)

        self.duty = Expseg([(0, 0.05), (self.dur, 0.5)], exp=4).play()
        self.osc = Compare(self.phase+self.ssaw, self.duty, mode="<", mul=1, add=-0.5)
        self.filt = Biquad(self.osc, freq=600, q=5, type=0, mul=self.env)
        self.r = Freeverb(self.filt.mix(2), size=0.80, damp=0.20, bal=0.70).out()

        self.noise = Noise(0.05)
        self.lfo1 = Sine(freq=0.1, mul=50, add=10)
        self.lfo2 = Sine(freq=0.4).range(2, 8)
        self.lfo3 = LFO(freq=4, type=2).range(4, 12)

        self.bg = ButBP(self.noise, freq=self.lfo1, mul=self.lfo2)
        self.de = SmoothDelay(self.bg, delay=random.randint(4, 7), feedback=0.1).out(1)
        self.rev = Freeverb(self.bg.mix(2), size=0.80, damp=0.10, bal=0.85).out(1)


pad_midi_1 = [56, 48, 46, 46, 60, 51, 51, 50, 65, 55, 55, 53]

pad_db = -10

c1 = Events(instr = ambient,
           midinote = EventSeq(pad_midi_1),
           beat = 10, db = pad_db, bpm=78,
           attack=2, decay=1, sustain=3, release=5)

class vertical_growl(EventInstrument):
    def __init__(self, **args):
        EventInstrument.__init__(self, **args)
        self.saw2 = SuperSaw(freq=self.freq*2, detune= 0.8)
        self.fm = FM(carrier=[251, 250], ratio=[.2354, .2563], index=self.saw2)
        self.lfo1 = Sine(freq=0.1, mul=50, add=10)

        self.saw1 = SuperSaw(freq=self.freq*self.fm, detune=0.2, mul=2)

        self.dis = Disto(self.saw1, drive=0.9, slope=0.6)
        self.dis1 = Disto(self.dis, drive=0.9)
        self.deg = Degrade(self.dis1)
        self.fil = Atone(self.deg, freq=self.lfo1).out()

        self.gt = Gate(self.deg, thresh=-30)
        self.hp = Biquad(self.gt, q=5, type=1)
        self.dis2 = Disto(self.hp, drive=0.9, slope=0.6)
        self.dis3 = Disto(self.dis2, drive=0.9)
        self.dis4 = Disto(self.dis3, drive=0.9)

        self.n = Noise(0.05).out()
        self.tr = self.dis3*self.saw2+self.n
        self.rev = Freeverb(self.tr, size=0.7, damp=0.8, bal=0.2).out()

        self.sub = Sine(freq=35).out(1)

        self.ot = Sine(freq=312)
        self.dis5 = Disto(self.ot+self.dis4, drive=0.9).out()

distortion_dB = -60

c2 = Events(instr = vertical_growl,
           midinote = EventSeq(pad_midi_1),
           beat = 5, db = distortion_dB, bpm=78,
           attack=0.5, decay=0.25, sustain=2, release=1)

#sel = Selector([osc1, osc2, osc3, osc4]).out()

s.gui(locals())
