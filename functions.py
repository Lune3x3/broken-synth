from pyo import *

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

class vertical_growl(PyoObject):
    def __init__(self, input, freq=100, mul=1, add=0):
        PyoObject.__init__(self, mul, add)

        self._freq = freq #pitch
        self._input = input #volume

        self.saw2 = SuperSaw(freq=self._freq*2, detune= 0.8)
        self.fm = FM(carrier=[251, 250], ratio=[.2354, .2563], index=self.saw2)
        self.lfo1 = Sine(freq=0.1, mul=50, add=10)

        self.saw1 = SuperSaw(freq=self._freq*self.fm, detune=0.2, mul=2)

        self.dis = Disto(self.saw1, drive=0.9, slope=0.6)
        self.dis1 = Disto(self.dis, drive=0.9)
        self.deg = Degrade(self.dis1)
        self.fil = Atone(self.deg, freq=self.lfo1)

        self.o1 = self.fil*0.06

        self.gt = Gate(self.deg, thresh=-30)
        self.hp = Biquad(self.gt, q=5, type=1)
        self.dis2 = Disto(self.hp, drive=0.9, slope=0.6)
        self.dis3 = Disto(self.dis2, drive=0.9)
        self.dis4 = Disto(self.dis3, drive=0.9)

        self.n = Noise(0.05)
        self.o2 = self.n*0.5

        self.tr = self.dis3*self.saw2+self.n
        self.rev = Freeverb(self.tr, size=0.7, damp=0.8, bal=0.2)
        self.o3 = self.rev*0.06

        self.sub = Sine(freq=35)
        self.o4 = self.sub*0.5

        self.ot = Sine(freq=312)
        self.dis5 = Disto(self.ot+self.dis4, drive=0.9)
        self.o5 = self.dis5*0.06

        self.allTracks = (self.o1 + self.o2 + self.o3 + self.o4 + self.o5)*self._input

        ##### cleanup
        self.vGrowl = Sig(self.allTracks, mul=mul, add=add)
        self._base_objs = self.vGrowl.getBaseObjects()

    def setInput(self, x):
        self._input = x

    def setFreq(self, x):
        self._freq = x

    @property # getter
    def input(self):
        return self._input
    @input.setter # setter
    def input(self, x):
        self.setInput(x)

    @property
    def freq(self):
        return self._freq
    @freq.setter
    def freq(self, x):
        self.setFreq(x)

    ##### play, stop, out
    def play(self, dur=0, delay=0):
        self.allTracks.play(dur, delay)
        return PyoObject.play(self, dur, delay)

    def stop(self, wait=0):
        self.allTracks.stop(wait)
        return PyoObject.stop(self, wait)

    def out(self, chnl=0, inc=1, dur=0, delay=0):
        self.allTracks.play(dur, delay)
        return PyoObject.out(self, chnl, inc, dur, delay)



class horizontal_growl(PyoObject):
    def __init__(self, input, freq=100, mul=1, add=0):
        PyoObject.__init__(self, mul, add)

        self._freq = freq #pitch
        self._input = input #volume

        self.sqr = LFO(freq=self._freq, type=2)
        self.saw = LFO(freq=self._freq/1.5, type=0)
        self.a = Disto(self.sqr*self.saw, drive=0.9)
        self.o1 = (self.a*0.1)*self._input

        self.fil = MoogLP(self.a, freq=200, res=10)
        self.dis = Disto(self.fil, drive=0.9, slope=0.6)
        self.fil1 = MoogLP(self.dis, freq=440, res=10)
        self.o2 = (self.fil1*0.1)*self._input

        self.dis1 = Disto(self.dis, drive=0.9, slope=0.6)
        self.dis2 = Disto(self.dis1, drive=0.9, slope=0.6)
        self.dis3 = Disto(self.dis2, drive=0.9, slope=0.6)
        self.lfo = LFO(freq=4.5, type=4, mul=3)
        self.fil2 = ButBP(self.dis3, freq=self.lfo*600)
        self.rev = Freeverb(self.fil2.mix(2), size=0.80, damp=0.20, bal=0.70)
        self.o3 = (self.rev*0.7)*self._input

        self.ssaw = SuperSaw(freq=[330, 400, 550], detune=0.8)
        self.lfo3 = Blit(freq=2)
        self.env = MoogLP(self.ssaw, freq=self.lfo*self.lfo3*600, res=6)
        self.dis4 = Disto(self.env, drive=0.9)
        self.rev1 = Freeverb(self.dis4.mix(2), size=0.8, damp=0.2, bal=0.6)
        self.o4 = self.rev1*self._input

        self.allTracks = self.o1 + self.o2 + self.o3 + self.o4

        ##### cleanup
        self.hGrowl = Sig(self.allTracks, mul=mul, add=add)
        self._base_objs = self.hGrowl.getBaseObjects()

    def setInput(self, x):
        self._input = x

    def setFreq(self, x):
        self._freq = x

    @property # getter
    def input(self):
        return self._input
    @input.setter # setter
    def input(self, x):
        self.setInput(x)

    @property
    def freq(self):
        return self._freq
    @freq.setter
    def freq(self, x):
        self.setFreq(x)

    ##### play, stop, out
    def play(self, dur=0, delay=0):
        self.allTracks.play(dur, delay)
        return PyoObject.play(self, dur, delay)

    def stop(self, wait=0):
        self.allTracks.stop(wait)
        return PyoObject.stop(self, wait)

    def out(self, chnl=0, inc=1, dur=0, delay=0):
        self.allTracks.play(dur, delay)
        return PyoObject.out(self, chnl, inc, dur, delay)
