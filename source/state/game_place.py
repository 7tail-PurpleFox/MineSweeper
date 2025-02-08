import pygame
import random
import datetime
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
        self.record_check2=False
        self.explore_list=[]
        self.sound_list=[False,False,False,False]
        self.explore_check=False
        self.win_check=0
        self.record_flag=[-1,-1]
        self.button_enable=True
        self.first_grid=[-1,-1]
        
        
    def update(self,screen,events,pos,game_setting):
        sound_explosion = self.sound_explosion_1 if game_setting["explode_type"]==1 else self.sound_explosion_2
        pygame.mixer.Sound.set_volume(self.sound_button,game_setting["sound_scale"]/10)
        pygame.mixer.Sound.set_volume(sound_explosion,game_setting["sound_scale"]/10)
        pygame.mixer.Sound.set_volume(self.sound_click,game_setting["sound_scale"]/10)
        pygame.mixer.Sound.set_volume(self.sound_finish,game_setting["sound_scale"]/10)
        self.sound_list=[False,False,False,False]
        self.explore_check=False
        if self.record_check==True:
            self.record_flag=[-1,-1]
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
            if event.type==pygame.MOUSEBUTTONUP and self.button_enable:
                if self.face_rect.collidepoint(pos):
                    self.sound_button.play()
                    self.sound_list[0]=True
                    if event.button==3:
                        self.mines_rect = []
                        self.mines_map = []
                        self.mines_explore = []
                        self.explore_list=[]
                        self.finished = True
                        self.next = "main_menu"
                        self.lose=False
                        self.win=False
                        self.record_time=0
                        self.record_check=False
                        self.record_check2=False
                        self.sound_list=[False,False,False,False]
                        self.explore_check=False
                        self.win_check=0
                        self.face_check=False
                        self.flags=0
                        self.first_grid=[-1,-1]
                        return "reset_size"
                    else:
                        self.mines_rect = []
                        self.mines_map = []
                        self.mines_explore = []
                        self.explore_list=[]
                        self.lose=False
                        self.win=False
                        self.record_time=0
                        self.record_check=False
                        self.record_check2=False
                        self.sound_list=[False,False,False,False]
                        self.explore_check=False
                        self.win_check=0
                        self.face_check=False 
                        self.flags=0
                        self.first_grid=[-1,-1]
                if not (self.lose or self.win) and self.face_check==False:
                    for a in range(len(self.mines_rect)):
                        for b in range(len(self.mines_rect[a])):
                            if self.mines_rect[a][b].collidepoint(pos):
                                if len(self.mines_map)==0:
                                    self.first_grid=[a,b]
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
                                            self.sound_list[1]=True
                                        else:
                                            self.explore_list.append([a,b])
                                            self.sound_click.play()
                                            self.sound_list[2]=True
                self.face_check=False
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
                                    self.record_flag=[a,b]
                                    if m==w*h:
                                        if self.flags==0:
                                            self.win=True
                                            self.sound_finish.play()
                                            self.sound_list[3]=True
                                            self.mines_map=[[14 for a in range(w)] for a in range(h)]
        self.button_enable=False
        if any(pygame.mouse.get_pressed()):
            self.button_enable=True
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
        
        if not (self.win or self.lose) and len(self.mines_explore)!=0 and len(self.mines_map)!=0:
            self.explore_map(w,h,m)
        if len(self.mines_map)!=0 and self.record_check==False:
            self.record_check=True
            temp="record."
            temp+="Init record/"+str(self.record_time)+"/"+str(pos[0])+" "+str(pos[1])+"/"+str(self.flags)+"/"+str(w)+"/"+str(h)+"/"+str(m)
            temp=temp+"/"
            for i in self.mines_map:
                for j in i:
                    temp+=str(j)
                    temp+=' '
                temp=temp[:-1]
                temp+=','
            temp=temp[:-1]
            temp=temp+"/"
            now=datetime.datetime.now()
            temp+=now.strftime("%Y %m %d %H %M %S")
            temp=temp+"/"
            temp+=str(self.record_flag[0])+" "+str(self.record_flag[1])
            temp=temp+"/"
            temp+=str(int(self.sound_list[0]))+" "+str(int(self.sound_list[1]))+" "+str(int(self.sound_list[2]))+" "+str(int(self.sound_list[3]))
            temp=temp+"/"
            temp+=str(self.first_grid[0])+" "+str(self.first_grid[1])
            return temp
        elif self.record_check==True and self.record_check2==False:
            s="record/"+str(self.record_time)+"/"+str(pos[0])+" "+str(pos[1])
            s+="/"
            if self.explore_check or self.record_time==0:
                s="Map "+s
                for i in self.mines_explore:
                    for j in i:
                        s+=str(j)
                        s+=' '
                    s=s[:-1]
                    s+=','
                s=s[:-1]
            s+="/"
            if any(self.sound_list):
                s="Sound "+s
                for i in self.sound_list:
                    s+=str(int(i))
                    s+=' '
                s=s[:-1]
            s+="/"
            if (self.lose or self.win):
                self.record_check2=True
                if self.lose:
                    s="Lose "+s
                else:
                    s="Win "+s
                for i in self.mines_map:
                    for j in i:
                        s+=str(j)
                        s+=' '
                    s=s[:-1]
                    s+=','
                s=s[:-1]
            s+="/"
            if self.record_flag[0]!=-1 and self.record_flag[1]!=-1:
                s="Flag "+s
                for i in self.record_flag:
                    s+=str(int(i))
                    s+=' '
                s=s[:-1]
            s="record."+s
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
        
        

        if mines>999:
            pygame.draw.polygon(screen,C.DARK_GRAY,[(49,44.5),(49,117.5),(209,44.5)])
            pygame.draw.polygon(screen,C.WHITE,[(209,117.5),(49,117.5),(209,44.5)])
            pygame.draw.polygon(screen,C.DARK_GRAY,[(screen.get_width()-209,44.5),(screen.get_width()-209,117.5),(screen.get_width()-49,44.5)])
            pygame.draw.polygon(screen,C.WHITE,[(screen.get_width()-209,117.5),(screen.get_width()-49,117.5),(screen.get_width()-49,44.5)])
            if self.flags<0:
                temp=setup.numbers[11]
                screen.blit(temp,(51,46.5))
                f=self.flags*-1
                if f>999:
                    f=999
                temp=setup.numbers[f//100]
                screen.blit(temp,(90,46.5))
                temp=setup.numbers[(f%100)//10]
                screen.blit(temp,(129,46.5))
                temp=setup.numbers[f%10]
                screen.blit(temp,(168,46.5))
            else:
                temp=setup.numbers[self.flags//1000]
                screen.blit(temp,(51,46.5))
                temp=setup.numbers[self.flags%1000//100]
                screen.blit(temp,(90,46.5))
                temp=setup.numbers[self.flags%100//10]
                screen.blit(temp,(129,46.5))
                temp=setup.numbers[self.flags%10]
                screen.blit(temp,(168,46.5))
            if len(self.mines_map)==0:
                temp=setup.numbers[0]
                screen.blit(temp,(screen.get_width()-207,46.5))
                screen.blit(temp,(screen.get_width()-168,46.5))
                screen.blit(temp,(screen.get_width()-129,46.5))
                screen.blit(temp,(screen.get_width()-90,46.5))
            else:
                if not (self.lose or self.win):
                    t=pygame.time.get_ticks()-self.time
                else:
                    t=self.record_time
                self.record_time=t
                t=t//1000
                if t>9999:
                    t=9999
                temp=setup.numbers[t//1000]
                screen.blit(temp,(screen.get_width()-207,46.5))
                temp=setup.numbers[t%1000//100]
                screen.blit(temp,(screen.get_width()-168,46.5))
                temp=setup.numbers[t%100//10]
                screen.blit(temp,(screen.get_width()-129,46.5))
                temp=setup.numbers[t%10]
                screen.blit(temp,(screen.get_width()-90,46.5))
        else:
            pygame.draw.polygon(screen,C.DARK_GRAY,[(49,44.5),(49,117.5),(170,44.5)])
            pygame.draw.polygon(screen,C.WHITE,[(170,117.5),(49,117.5),(170,44.5)])
            pygame.draw.polygon(screen,C.DARK_GRAY,[(screen.get_width()-170,44.5),(screen.get_width()-170,117.5),(screen.get_width()-49,44.5)])
            pygame.draw.polygon(screen,C.WHITE,[(screen.get_width()-170,117.5),(screen.get_width()-49,117.5),(screen.get_width()-49,44.5)])
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
            if len(self.mines_map)==0:
                temp=setup.numbers[0]
                screen.blit(temp,(screen.get_width()-168,46.5))
                screen.blit(temp,(screen.get_width()-129,46.5))
                screen.blit(temp,(screen.get_width()-90,46.5))
            else:
                if not (self.lose or self.win):
                    t=pygame.time.get_ticks()-self.time
                else:
                    t=self.record_time
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
    def explore_map(self,w,h,m):
        temp=[]
        for i in self.explore_list:
            if self.mines_explore[i[0]][i[1]]==1 or self.mines_explore[i[0]][i[1]]==2:
                continue
            if self.mines_map[i[0]][i[1]] in range(9):
                self.mines_explore[i[0]][i[1]]=1
                self.win_check+=1

            if self.mines_map[i[0]][i[1]]==0:
                for k in [-1,0,1]:
                    for j in [-1,0,1]:
                        if (not (k==0 and j==0)) and (0<=i[0]+k and i[0]+k<h) and(0<=i[1]+j and i[1]+j<w):
                            temp.append([i[0]+k,i[1]+j])
        #if len(self.explore_list)>0 and len(temp)==0:
        if len(self.explore_list)>0:
            self.explore_check=True
            self.check_map(w,h,m)
        self.explore_list=temp
    def check_map(self,w,h,m):
        if self.win_check==w*h-m:
            self.win=True
            self.sound_finish.play()
            self.sound_list[3]=True
            self.flags=0
            for p in range(h):
                for j in range(w):
                    if self.mines_map[p][j]==10:
                        self.mines_map[p][j]=14
            self.mines_explore=[[1 for a in range(w)] for a in range(h)]