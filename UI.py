import pygame
from pygame.locals import *
import time
from main import valid ,solve
class Grid:
    def __init__(self) -> None:
        super().__init__()
        pass

class Cube:
    def __init__(self) -> None:
        super().__init__()
        pass

def time_format(secs):
    secs=secs%60
    mins=secs//60
    Time=f"{mins}:{secs}"
    return Time


def main():
    win=pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku")
    win.fill((255,255,255))
    pygame.display.update()
    run=True
    start=time.time()
    strikes=0
    while run:
        play_time=round(time.time() - start)
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()




if __name__ == "__main__":
    pygame.init()
    main()
    # pygame.quit()