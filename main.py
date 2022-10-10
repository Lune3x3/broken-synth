from pyo import *
import random
import functions

s = Server().boot()

#gain control
s.amp = 0.1
#fundemetal frequency
freq = 100
#highest harmonic
high = 20

pad_midi_1 = [56, 48, 46, 46, 60, 51, 51, 50, 65, 55, 55, 53]
pad_db = -10

c1 = Events(instr = functions.ambient,
           midinote = EventSeq(pad_midi_1),
           beat = 10, db = pad_db, bpm=78,
           attack=2, decay=1, sustain=3, release=5).play()


vol2 = Sig(1)
vol2.ctrl()

c2 = functions.vertical_growl(vol2, freq=56).out()

vol3 = Sig(1)
vol3.ctrl()
freq = 56

c3 = functions.horizontal_growl(vol3, freq=freq).out()

sc = Scope(c3)

s.gui(locals())
