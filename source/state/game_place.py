import pygame
import random
from .. import setup
from .. import constant as C
from .. import tool

class Game_Place:
    def __init__(self):
        self.finished = False
        self.next = 'main_menu'
        self.border_hor_wide = pygame.transform.scale(setup.border_hor_wide, ((6,90)))
        self.border_hor = pygame.transform.scale(setup.border_hor, ((6,33)))
        self.border_vert = pygame.transform.scale(setup.border_vert, ((36,6)))
        self.corner_bottom_left_wide = pygame.transform.scale(setup.corner_bottom_left_wide, (36,90))
        self.corner_bottom_left = pygame.transform.scale(setup.corner_bottom_left, (36,33))
        self.corner_bottom_right_wide = pygame.transform.scale(setup.corner_bottom_right_wide, (36,90))
        self.corner_bottom_right = pygame.transform.scale(setup.corner_bottom_right, (36,33))
        self.corner_up_left = pygame.transform.scale(setup.corner_up_left, (36,33))
        self.corner_up_right = pygame.transform.scale(setup.corner_up_right, (36,33))
        self.sound_explosion_1 = setup.sounds['explosion_1']
        self.sound_explosion_2 = setup.sounds['explosion_2']
        self.sound_button = setup.sounds['button']
        self.sound_click = setup.sounds["click"]
        self.sound_finish = setup.sounds["finish"]
        self.face_rect=pygame.Rect(241.5,46.5,69,69)
        self.mines_rect = []
        self.mines_map = []
        self.mines_explore = []
        self.flags=0
        self.time=pygame.time.get_ticks()
        self.face_check = False
        self.lose=False
        self.win=False
        self.record_time=0
        self.record_check=False
        self.record_explore=False
        
    def update(self,screen,events,pos,game_setting):
        sound_explosion = self.sound_explosion_1 if game_setting["explode_type"]==1 else self.sound_explosion_2
        pygame.mixer.Sound.set_volume(self.sound_button,game_setting["sound_scale"]/10)
        pygame.mixer.Sound.set_volume(sound_explosion,game_setting["sound_scale"]/10)
        pygame.mixer.Sound.set_volume(self.sound_click,game_setting["sound_scale"]/10)
        pygame.mixer.Sound.set_volume(self.sound_finish,game_setting["sound_scale"]/10)
        sound_list=[False,False,False,False]
        self.record_explore=False
        w=game_setting["game_place"][0]
        h=game_setting["game_place"][1]
        m=game_setting["game_place"][2]
        block_size=game_setting["block_size"]
        if len(self.mines_rect)==0:
            self.face_rect=pygame.Rect(screen.get_width()//2-34.5,46.5,69,69)
            self.mines_explore=[[0 for i in range(w)] for i in range(h)]
            for i in range(h):
                temp=[]
                for j in range(w):
                    temp.append(pygame.Rect((36+block_size*j),(162+block_size*i),block_size,block_size))
                self.mines_rect.append(temp)
            self.flags=m
        self.set_backgroud(screen,w,h,m,block_size)
        for event in events:
            if event.type==pygame.MOUSEBUTTONUP:
                self.face_check=False
                if self.face_rect.collidepoint(pos):
                    self.sound_button.play()
                    sound_list[0]=True
                    if event.button==3:
                        self.mines_rect = []
                        self.mines_map = []
                        self.mines_explore = []
                        self.finished = True
                        self.next = "main_menu"
                        self.lose=False
                        self.win=False
                        self.record_time=0
                        self.record_check=False
                        return "reset_size"
                    else:
                        self.mines_rect = []
                        self.mines_map = []
                        self.mines_explore = []
                        self.lose=False
                        self.win=False
                        self.record_time=0
                        self.record_check=False
                if not (self.lose or self.win):
                    for a in range(len(self.mines_rect)):
                        for b in range(len(self.mines_rect[a])):
                            if self.mines_rect[a][b].collidepoint(pos):
                                if len(self.mines_map)==0:
                                    self.time=pygame.time.get_ticks()
                                    self.mines_map=[[0 for i in range(w)] for i in range(h)]
                                    temp=random.sample(range(w*h),m)
                                    if m!=w*h:
                                        while a*w+b in temp:
                                            temp=random.sample(range(w*h),m)
                                    for i in temp:
                                        self.mines_map[i//w][i-w*(i//w)]=10
                                    for i in range(h):
                                        for j in range(w):
                                            for l in [-1,0,1]:
                                                for k in [-1,0,1]:
                                                    if self.mines_map[i][j]!=10 and (0 <= i+l and i+l < h) and (0 <= j+k and j+k <w):
                                                        if self.mines_map[i+l][j+k]==10:
                                                            self.mines_map[i][j]+=1
                                if event.button==1:
                                    if self.mines_explore[a][b]==0:
                                        self.record_explore=True
                                        if self.mines_map[a][b]==10:
                                            self.mines_map[a][b]=12
                                            for i in range(h):
                                                for j in range(w):
                                                    if self.mines_explore[i][j]==2 and self.mines_map[i][j]!=10:
                                                        self.mines_map[i][j]=11
                                                    if self.mines_explore[i][j]==2 and self.mines_map[i][j]==10:
                                                        self.mines_map[i][j]=14
                                            self.mines_explore=[[1 for i in range(w)] for i in range(h)]
                                            self.lose=True
                                            sound_explosion.play()
                                            sound_list[1]=True
                                        else:
                                            self.explore(a,b,w,h)
                                            check=0
                                            for i in range(h):
                                                for j in range(w):
                                                    if self.mines_explore[i][j]==1 and self.mines_map[i][j]!=10:
                                                        check+=1
                                            if check==w*h-m:
                                                self.win=True
                                                self.sound_finish.play()
                                                sound_list[3]=True
                                                self.flags=0
                                                for i in range(h):
                                                    for j in range(w):
                                                        if self.mines_map[i][j]==10:
                                                            self.mines_map[i][j]=14
                                                self.mines_explore=[[1 for i in range(w)] for i in range(h)]
                                            else:
                                                self.sound_click.play()
                                                sound_list[2]=True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.face_rect.collidepoint(pos):
                    self.face_check=True
                if not (self.lose or self.win):
                    for a in range(len(self.mines_rect)):
                        for b in range(len(self.mines_rect[a])):
                            if self.mines_rect[a][b].collidepoint(pos):
                                if event.button==3:
                                    if self.mines_explore[a][b]==0:
                                        self.mines_explore[a][b]=2
                                        self.flags-=1
                                    elif self.mines_explore[a][b]==2:
                                        self.mines_explore[a][b]=0
                                        self.flags+=1
        if any(pygame.mouse.get_pressed()):
            if self.face_check:
                if self.face_rect.collidepoint(pos):
                    temp=setup.faces[4]
                    temp=pygame.transform.scale(temp,(69,69))
                    screen.blit(temp,self.face_rect.topleft)
            elif not (self.lose or self.win):
                if pygame.mouse.get_pressed()[0]:
                    temp=setup.faces[1]
                    temp=pygame.transform.scale(temp,(69,69))
                    screen.blit(temp,self.face_rect.topleft)
                    for i in range(len(self.mines_rect)):
                        for j in range(len(self.mines_rect[i])):
                            if self.mines_rect[i][j].collidepoint(pos):
                                if self.mines_explore[i][j]==0:
                                    temp=setup.grids[0]
                                    temp=pygame.transform.scale(temp,(block_size,block_size))
                                    screen.blit(temp,(self.mines_rect[i][j].topleft))
                                elif self.mines_explore[i][j]==3:
                                    temp=setup.grids[9]
                                    temp=pygame.transform.scale(temp,(block_size,block_size))
                                    screen.blit(temp,(self.mines_rect[i][j].topleft))
        if len(self.mines_map)!=0 and self.record_check==False:
            self.record_check=True
            return "record/"+str(self.record_time)+"/"+str(pos)+"/"+str(self.flags)+"/"+str(w)+"/"+str(h)+"/"+str(m)+"/"+str(self.mines_map)
        elif self.record_check==True:
            s="record/"+str(self.record_time)+"/"+str(pos)+"/"+str(self.flags)
            if self.record_explore:
                s=s+"/"+str(self.mines_explore)
            if any(sound_list):
                s=s+"/"+str(sound_list)
            return s
    def set_backgroud(self,screen,width,height,mines,block_size):
        w=int(width*block_size+36)
        h=int(162+height*block_size)
        screen.blit(self.corner_up_left,(0,0))
        for i in range(36,w,6):
            screen.blit(self.border_hor,(i,0))
            screen.blit(self.border_hor,(i,129))
            screen.blit(self.border_hor_wide,(i,h))
        screen.blit(self.corner_up_right,(w,0))
        screen.blit(self.corner_bottom_left_wide,(0,h))
        screen.blit(self.corner_bottom_right_wide,(w,h))
        for i in range(33,129,6):
            screen.blit(self.border_vert,(0,i))
            screen.blit(self.border_vert,(w,i))
        screen.blit(self.corner_bottom_left,(0,129))
        screen.blit(self.corner_bottom_right,(w,129))
        temp = pygame.Surface((36,16)).convert()
        temp.blit(self.corner_up_left,(0,-17))
        screen.blit(temp,(0,146))
        temp = pygame.Surface((36,16)).convert()
        temp.blit(self.corner_up_right,(0,-17))
        screen.blit(temp,(w,146))
        for i in range(162,h,6):
            screen.blit(self.border_vert,(0,i))
            screen.blit(self.border_vert,(w,i))
        
        for i in range(len(self.mines_rect)):
            for j in range(len(self.mines_rect[i])):
                if len(self.mines_map)==0:
                    temp=setup.grids[15]
                else:
                    if self.mines_explore[i][j]==1:
                        temp=setup.grids[self.mines_map[i][j]]
                    elif self.mines_explore[i][j]==2:
                        temp=setup.grids[14]
                    else:
                        temp=setup.grids[15]
                temp=pygame.transform.scale(temp,(block_size,block_size))
                screen.blit(temp,self.mines_rect[i][j].topleft)
        temp=pygame.Surface((75,75))
        temp.fill(C.DARK_GRAY)
        screen.blit(temp,(self.face_rect.topleft[0]-3,self.face_rect.topleft[1]-3))
        if self.lose:
            temp=setup.faces[2]
        elif self.win:
            temp=setup.faces[3]
        else:
            temp=setup.faces[0]
        temp=pygame.transform.scale(temp,(69,69))
        screen.blit(temp,self.face_rect.topleft)
        
        pygame.draw.polygon(screen,C.DARK_GRAY,[(49,44.5),(49,117.5),(170,44.5)])
        pygame.draw.polygon(screen,C.DARK_GRAY,[(screen.get_width()-170,44.5),(screen.get_width()-170,117.5),(screen.get_width()-49,44.5)])
        pygame.draw.polygon(screen,C.WHITE,[(170,117.5),(49,117.5),(170,44.5)])
        pygame.draw.polygon(screen,C.WHITE,[(screen.get_width()-170,117.5),(screen.get_width()-49,117.5),(screen.get_width()-49,44.5)])
        if len(self.mines_map)==0:
            temp=setup.numbers[0]
            screen.blit(temp,(screen.get_width()-168,46.5))
            screen.blit(temp,(screen.get_width()-129,46.5))
            screen.blit(temp,(screen.get_width()-90,46.5))
        else:
            if not (self.lose or self.win):
                t=pygame.time.get_ticks()-self.time
                self.record_time=t
                t=t//1000
                if t>999:
                    t=999
            temp=setup.numbers[t//100]
            screen.blit(temp,(screen.get_width()-168,46.5))
            temp=setup.numbers[t%100//10]
            screen.blit(temp,(screen.get_width()-129,46.5))
            temp=setup.numbers[t%10]
            screen.blit(temp,(screen.get_width()-90,46.5))
        if self.flags<0:
            temp=setup.numbers[11]
            screen.blit(temp,(51,46.5))
            f=self.flags*-1
            if f>99:
                f=99
            temp=setup.numbers[f//10]
            screen.blit(temp,(90,46.5))
            temp=setup.numbers[f%10]
            screen.blit(temp,(129,46.5))
        else:
            temp=setup.numbers[self.flags//100]
            screen.blit(temp,(51,46.5))
            temp=setup.numbers[self.flags%100//10]
            screen.blit(temp,(90,46.5))
            temp=setup.numbers[self.flags%10]
            screen.blit(temp,(129,46.5))
    def explore(self,a,b,w,h):
        if self.mines_explore[a][b]==1 or self.mines_explore[a][b]==2:
            return
        if self.mines_map[a][b] in range(9):
            self.mines_explore[a][b]=1
        if self.mines_map[a][b]==0:
            for i in [-1,0,1]:
                for j in [-1,0,1]:
                    if (not (i==0 and j==0)) and (0<=a+i and a+i<h) and(0<=b+j and b+j<w):
                        self.explore(a+i,b+j,w,h)