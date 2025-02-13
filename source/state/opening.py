import pygame, time
from .. import setup
from .. import constant as C
from .. import tool

class Opening:
    def __init__(self):
        self.finished = False
        self.next = 'main_menu'
        self.time = time.time()
        self.alpha = 255
        self.fox = pygame.transform.scale(setup.fox, (269, 327))

    def update(self,screen,events,pos,game_setting):
        self.set_backgroud(screen)
        if time.time()-self.time>5:
            self.finished = True
        elif time.time()-self.time<=2:
            self.alpha = 255-(time.time()-self.time)*127.5
        elif time.time()-self.time>=3:
            self.alpha = (time.time()-self.time-3)*127.5
    def set_backgroud(self,screen):
        screen.fill(C.BLACK)
        tool.blit_image(screen, self.fox, (C.SCREEN_SIZE[0]//2, C.SCREEN_SIZE[1]//2-100), True)
        tool.blit_text(screen, setup.mine_sweeper_font_32, 'Presented by', C.WHITE, (C.SCREEN_SIZE[0]//2, C.SCREEN_SIZE[1]//2+100), True)
        tool.blit_text(screen, setup.mine_sweeper_font_32, '7tail_PurpleFox', C.WHITE, (C.SCREEN_SIZE[0]//2, C.SCREEN_SIZE[1]//2+200), True)
        temp = pygame.Surface((C.SCREEN_SIZE[0], C.SCREEN_SIZE[1]))
        temp.fill(C.BLACK)
        temp.set_alpha(self.alpha)
        screen.blit(temp,(0,0))

        
        
    