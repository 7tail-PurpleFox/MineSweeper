import pygame
import os
from . import constant as C

class Game:
    def __init__(self,state_dict,start_state):
        self.screen = pygame.display.get_surface()
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.sub_background = self.background.copy()
        self.background.fill(C.GRAY)
        self.clock = pygame.time.Clock()
        self.running = True
        self.keys = pygame.key.get_pressed()
        self.state_dict = state_dict
        self.state = self.state_dict[start_state]
        
    def update(self):
        self.background.fill(C.GRAY)
        if self.state.finished:
            next_state = self.state.next
            self.state.finished = False
            self.state = self.state_dict[next_state]
        self.state.update(self.background,self.keys)
        
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.keys = pygame.key.get_pressed()
                elif event.type == pygame.KEYUP:
                    self.keys = pygame.key.get_pressed()
            self.update()
            self.blit_background()
            pygame.display.update()
            self.clock.tick(120)
        pygame.quit()
    def blit_background(self):
        if self.screen.get_width()==C.MAX_WIDTH:
            screen_width, screen_height = self.screen.get_size()
            background_width, background_height = self.sub_background.get_size()
            background_width = int(screen_height * background_width / background_height)
            background_height = screen_height
            self.sub_background =self.background.copy()
            self.sub_background = pygame.transform.scale(self.sub_background, (background_width, background_height)) 
        elif self.screen.get_size() != self.sub_background.get_size():
            screen_width, screen_height = self.screen.get_size()
            background_width, background_height = self.sub_background.get_size()
            if screen_width != background_width:
                background_height = int(screen_width * background_height / background_width)
                screen_height = background_height
                background_width = screen_width
            elif screen_height != background_height:
                background_width = int(screen_height * background_width / background_height)
                screen_width = background_width
                background_height = screen_height
            self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            self.sub_background =self.background.copy()
            self.sub_background = pygame.transform.scale(self.sub_background, (background_width, background_height)) 
        else:
            self.sub_background = pygame.transform.scale(self.background.copy(),self.sub_background.get_size())
        rect=self.sub_background.get_rect()
        rect.center=self.screen.get_rect().center
        self.screen.blit(self.sub_background,rect.topleft)

def load_image(path, accept={"png", "jpg", "bmp", "gif"}):
    #載入圖片
    #accept:可接受的檔案類型
    #return:圖片物件dict
    images={}
    for pic in os.listdir(path):
        name, ext = os.path.splitext(pic)
        if ext[1:].lower() in accept:
            img = pygame.image.load(os.path.join(path, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img=img.convert()
            images[name]=img
    return images

def get_image(sheet,x,y,w,h,colorkey=None,scale=1):
    #切割圖片
    #sheet:圖片物件
    #x,y,w,h:切割區域
    #return:圖片物件
    img=pygame.Surface((w,h))
    img.blit(sheet,(0,0),(x,y,w,h))#將sheet的(x,y,w,h)區域貼到img上
    img.set_colorkey(colorkey)#設定透明色(和colorkey相同的顏色會變透明)
    img=pygame.transform.scale(img,(int(w*scale),int(h*scale)))#縮放
    return img

def load_font(path, size, accept={"ttf","otf"}):
    #accept:可接受的檔案類型
    #return:圖片物件dict
    fonts={}
    for f in os.listdir(path):
        name, ext = os.path.splitext(f)
        if ext[1:].lower() in accept:
            font=pygame.font.Font(os.path.join(path, f),size)
            fonts[name]=font
    return fonts

def blit_text(screen,font,text,color,pos,center=False):
    #顯示文字
    #screen:畫布
    #text:文字
    #font:字型
    #color:顏色
    #pos:位置
    img=font.render(text,True,color)
    if center:
        rect=img.get_rect()
        rect.center=pos
        screen.blit(img,rect.topleft)
    else:
        screen.blit(img,pos)
