from pyo import *
import multiprocessing
import multiprocessing.managers
import functions

if __name__ == '__main__':
    s = Server().boot()

    #gain control
    s.amp = 0.1
    #fundemetal frequency
    freq = 56
    #highest harmonic
    high = 20

    ##### -------------------------------------------------------- start doing instrument stuff
    pad_midi_1 = [56, 48, 46, 46, 60, 51, 51, 50, 65, 55, 55, 53]
    pad_db = -10

    c1 = Events(instr = functions.ambient,
               midinote = EventSeq(pad_midi_1),
               beat = 10, db = pad_db, bpm=78,
               attack=2, decay=1, sustain=3, release=5).play()

    vol2 = Sig(0)

    c2 = functions.vertical_growl(vol2, freq=freq).out()

    vol3 = Sig(0)
    vol3.ctrl()

    c3 = functions.horizontal_growl(vol3, freq=freq).out()

    ##### ------------------------------------------------------ getting values from pygame
    class MyListManager(multiprocessing.managers.BaseManager):
        pass
    MyListManager.register("xy")

    psswrd = bytes('password', encoding='utf-8')

    manager = MyListManager(address=('127.0.0.1', 5000), authkey=psswrd)
    manager.connect()

    xy = manager.xy()

    vertical = 0
    horizontal = 0

    def get_arr():
        xAdd = xy.__getitem__(0)
        yAdd = xy.__getitem__(1)

        global vertical
        global horizontal
        horizontal += xAdd/10
        vertical += yAdd/10

    def pat():
        get_arr()
        global vertical
        global horizontal

        global vol2
        global vol3

        if vertical > 10:
            if vertical < 100:
                vol3.setValue(vertical/100)
            elif vertical > 100:
                vol3.setValue(1)
        else:
            vol3.setValue(0)

        if vertical > 0:
            vertical = vertical/2 - 1
        elif vertical < 0:
            vertical = 0

        if horizontal > 10:
            if horizontal < 100:
                vol2.setValue(horizontal/100)
            elif horizontal > 100:
                vol2.setValue(1)
        else:
            vol2.setValue(0)

        if horizontal > 0:
            horizontal = horizontal/2 - 1
        elif horizontal < 0:
            horizontal = 0

        print(horizontal)

    p = Pattern(pat, 0.1)
    p.play()

    s.gui(locals())
