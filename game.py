import pygame
import multiprocessing
import multiprocessing.managers

pygame.init()

height = 500
width = 500

screen = pygame.display.set_mode((width, height))

xy = [] # 0 = x vel 1, = y vel
def get_arr():
    return xy

class MyListManager(multiprocessing.managers.BaseManager):
    pass

def init():
    MyListManager.register("xy", get_arr, exposed=['__getitem__', '__setitem__', '__str__', 'append', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort'])

    psswrd = bytes('password', encoding='utf-8')

    manager = MyListManager(address=('127.0.0.1', 5000), authkey=psswrd)
    manager.start()

    global xy_tmp
    xy_tmp = manager.xy()
    print('xy (master): ', xy, 'xy_tmp:', xy_tmp)

    xy_tmp.append(0)
    xy_tmp.append(0)

if __name__ == '__main__':
    init()
    running = True
    prevxy = (0, 0) # 0 = x vel 1, = y vel
    curxy = (0, 0)

    clock = pygame.time.Clock()

    while running:
        curxy = pygame.mouse.get_pos()

        xvel = abs(curxy[0] - prevxy[0])
        yvel = abs(curxy[1] - prevxy[1])

        xy_tmp.__setitem__(0, xvel)
        xy_tmp.__setitem__(1, yvel)
        print(xvel)

        prevxy = curxy

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        clock.tick(10)
    pygame.quit()
