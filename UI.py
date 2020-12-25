import pygame
from pygame import mouse
from pygame.locals import *
import time
from main import find_empty, valid ,solve,board


pygame.font.init()
fnt=pygame.font.SysFont("comiscans",40)


class Grid:
    Board= board
    def __init__(self,rows,cols,width,height,screen):
        self.cubes=[[Cube(self.Board[i][j],i,j,width,height) for j in range(cols)] for i in range(rows)]
        self.rows=rows 
        self.cols=cols
        self.width=width
        self.height=height
        self.board=None
        self.update_board()
        self.selected =None
        self.screen=screen
    
    def update_board(self):
        self.board=[[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def Solver(self):
        self.update_board()
        find=find_empty(self.board)
        if find is None:
            return True
        else:
            row,col=find
        for i in range(1,10):
            if valid(self.board,i,(row,col)):
                self.board[row][col]=i
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_changes(self.screen,False)
                self.update_board()
                pygame.display.update()
                pygame.time.delay(100)
                if self.Solver():
                    return True
                self.board[row][col]=0
                self.cubes[row][col].set(0)
                self.update_board()
                self.cubes[row][col].draw_changes(self.screen,True)
                pygame.display.update()
                pygame.time.delay(100)

        return False

    def resart_board(self):
        for i in range(len(self.Board)):
            for j in range(len(self.Board[0])):
                self.cubes[i][j].set_temp(0)
                self.cubes[i][j].set(0)
                self.update_board()
                if self.Board[i][j]!=0:
                    self.cubes[i][j].set(self.Board[i][j])
                    self.update_board()

    def place(self,val):
        row,col=self.selected
        if self.cubes[row][col].value==0:
            self.cubes[row][col].set(val)
            self.update_board()

            if valid(self.board,val,(row,col)) and solve(self.board):
                return True
            else:
                self.cubes[row][col].set_temp(0)
                self.cubes[row][col].set(0)
                self.update_board()
    def sketch(self,val):
        # Uncomfirmed number
        row,col=self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self,screen):
        # Drawing the lines 
        gap=self.width/9
        for i in range(self.rows+1):
            if i%3==0 and i!=0:
                thick=4
            else:
                thick=1
            pygame.draw.line(screen,(0,0,0),(0,i*gap),(self.width,i*gap),thick)
            pygame.draw.line(screen,(0,0,0),(i*gap,0),(i*gap,self.height),thick)
        #Drawing the cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(screen)

    def select(self,row,col):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected=False
        self.cubes[row][col].selected=True
        self.selected=(row,col)

    def click(self,pos):
        if pos[0]< self.width and pos[1]< self.height:
            gap=self.width/9
            x=pos[0]//gap
            y=pos[1]//gap
            return (int(y),int(x))
        else:
            return None

    def clear(self):
        row,col=self.selected
        if self.cubes[row][col].value==0:
            self.cubes[row][col].set_temp(0)

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value==0:
                    return False
        return True
class Cube:
    def __init__(self,value,row,col,width,height):
        self.value=value
        self.row=row
        self.col=col
        self.width=width
        self.height=height
        self.selected=False
        self.temp=0

    def draw(self,screen):
   
        gap=self.width/9
        x=self.col*gap
        y=self.row*gap

        if self.temp!=0 and self.value==0:
            text=fnt.render(str(self.temp),1,(125,125,125))
            screen.blit(text,(x+5,y+5))
        elif self.value!=0:
            text=fnt.render(str(self.value),1,(0,0,0))
            screen.blit(text,(x+(gap/2 -text.get_width()/2),y+(gap/2 -text.get_height()/2)))
        if self.selected:
            pygame.draw.rect(screen,(255,0,0),(x,y,gap,gap),3)

    def draw_changes(self,screen,backtrack=True):
        gap=self.width/9
        x=self.col*gap
        y=self.row*gap
        pygame.draw.rect(screen,(255,255,255),(x,y,gap,gap),0)
        text=fnt.render(str(self.value),1,(0,0,0))
        screen.blit(text,(x+(gap/2 - text.get_width()/2),y+(gap/2 - text.get_height()/2)))
        if backtrack:
            pygame.draw.rect(screen,(255,0,0),(x,y,gap,gap),3)
        else:
            pygame.draw.rect(screen,(0,255,0),(x,y,gap,gap),3)

    def set_temp(self,val):
        self.temp=val
    def set(self,val):
        self.value=val   

def draw_window(screen,board,time,strikes):
    screen.fill((255,255,255))
    text=fnt.render(f"Time:"+time_format(time),1,(0,0,0))
    screen.blit(text,(380,555))
    text=fnt.render(f"X: {strikes}",1,(255,0,0))
    screen.blit(text,(20,555))
    board.draw(screen)


def time_format(secs):
    sec = secs%60
    minute = secs//60
    mat = " " + str(minute) + ":" + str(sec)
    return mat



def main():
    screen=pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku")
    board=Grid(9,9,540,540,screen)
    run=True
    key=None
    start=time.time()
    strikes=0
    while run:
        play_time = round(time.time() -start)
        for event in pygame.event.get():
            if event.type==QUIT:
                run=False
            if event.type==KEYDOWN:
                if event.key==pygame.K_1 or event.key==K_KP1:
                    key=1
                if event.key==K_2 or event.key==K_KP2:
                    key=2
                if event.key==K_3 or event.key==K_KP3:
                    key=3
                if event.key==K_4 or event.key==K_KP4:
                    key=4
                if event.key==K_5 or event.key==K_KP5:
                    key=5
                if event.key==K_6 or event.key==K_KP6:
                    key=6
                if event.key==K_7 or event.key==K_KP7:
                    key=7
                if event.key==K_8 or event.key==K_KP8:
                    key=8
                if event.key==K_9 or event.key==K_KP9:
                    key=9

                if event.key==K_SPACE:
                    board.Solver()
                if event.key==K_DELETE:
                    board.resart_board()
                    key=None
                if event.key==K_BACKSPACE:
                    board.clear()
                    key=None
                if event.key==K_RETURN:
                    i,j=board.selected
                    if board.cubes[i][j].temp!=0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes+=1
                        key=None
                        if board.is_finished():
                            print("Game over")
                            run =False
            if event.type==MOUSEBUTTONDOWN:
                pos=mouse.get_pos()
                clicked=board.click(pos)
                if clicked:
                    board.select(clicked[0],clicked[1])

                    key=None

        if board.selected and key!=None:
            board.sketch(key)

        draw_window(screen,board,play_time,strikes)
        pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()