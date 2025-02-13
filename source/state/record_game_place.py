import pygame
import copy
from .. import setup
from .. import constant as C
from .. import tool

class Record_Game_Place:
    def __init__(self):
        self.finished = False
        self.next = 'record_info'
        self.border_hor_wide = pygame.transform.scale(setup.border_hor_wide, ((6,90)))
        self.border_hor = pygame.transform.scale(setup.border_hor, ((6,33)))
        self.border_vert = pygame.transform.scale(setup.border_vert, ((36,6)))
        self.corner_bottom_left_wide = pygame.transform.scale(setup.corner_bottom_left_wide, (36,90))
        self.corner_bottom_left = pygame.transform.scale(setup.corner_bottom_left, (36,33))
        self.corner_bottom_right_wide = pygame.transform.scale(setup.corner_bottom_right_wide, (36,90))
        self.corner_bottom_right = pygame.transform.scale(setup.corner_bottom_right, (36,33))
        self.corner_up_left = pygame.transform.scale(setup.corner_up_left, (36,33))
        self.corner_up_right = pygame.transform.scale(setup.corner_up_right, (36,33))
        self.sound_explosion = setup.explosion_sounds[0]
        self.sound_button = setup.sounds['button']
        self.sound_click = setup.click_sounds[0]
        self.sound_finish = setup.sounds["finish"]
        self.replay_cursor = pygame.transform.scale(setup.replay_cursor, (38,40))
        self.replay_play = pygame.transform.scale(setup.replay_play, (36,36))
        self.replay_pause = pygame.transform.scale(setup.replay_pause, (36,36))
        self.replay_end = pygame.transform.scale(setup.replay_end, (36,36))
        self.mouse_cursor = pygame.transform.scale(setup.mouse_cursor, (36,57))
        self.button_enable=True
        self.record_place=None
        self.mines_rect=[]
        self.mines_map=[]
        self.mines_explore=[]
        self.play_rect=pygame.Rect(241.5,46.5,69,69)
        self.play_mode=0
        self.slide_rect=pygame.Rect(26,680,500,23)
        self.cursor_rect=pygame.Rect(26,670,38,40)
        self.slide_length=500
        self.slide_check=False
        self.game_length=0
        self.time=pygame.time.get_ticks()
        self.curr_frame=0
        self.flags=0
        self.frame_length=0
        

    def update(self,screen,events,pos,game_setting):
        #print(self.curr_frame,self.game_length)
        self.sound_explosion = setup.explosion_sounds[game_setting["explode_type"]-1]
        self.sound_click = setup.click_sounds[game_setting["click_type"]-1]
        pygame.mixer.Sound.set_volume(self.sound_button,game_setting["sound_scale"]/10)
        pygame.mixer.Sound.set_volume(self.sound_explosion,game_setting["explode_scale"]/10)
        pygame.mixer.Sound.set_volume(self.sound_click,game_setting["sound_scale"]/10)
        pygame.mixer.Sound.set_volume(self.sound_finish,game_setting["sound_scale"]/10)
        w=game_setting["game_place"][0]
        h=game_setting["game_place"][1]
        m=game_setting["game_place"][2]
        block_size=game_setting["block_size"]
        if len(self.mines_rect)==0:
            self.play_rect=pygame.Rect(screen.get_width()//2-34.5,46.5,69,69)
            self.cursor_rect=pygame.Rect(26,screen.get_height()-62,38,40)
            self.slide_rect=pygame.Rect(26,screen.get_height()-52,screen.get_width()-52,23)
            self.slide_length=screen.get_width()-52
            self.frame_length=(screen.get_width()-52-38)/(self.game_length-1)
            for i in range(h):
                temp=[]
                for j in range(w):
                    temp.append(pygame.Rect((36+block_size*j),(162+block_size*i),block_size,block_size))
                self.mines_rect.append(temp)
        if self.play_mode==1:
            self.time=pygame.time.get_ticks()
            self.time-=self.record_place["gaming"][self.curr_frame]["time"]
        if self.play_mode==2 and self.curr_frame!=self.game_length-1:
            self.play_mode=0
        if self.curr_frame>=self.game_length or self.slide_check:
            pass
        else:
            if self.record_place["gaming"][self.curr_frame]["time"]<=pygame.time.get_ticks()-self.time and self.play_mode==0:
                #self.time=pygame.time.get_ticks()
                if self.record_place["gaming"][self.curr_frame].get("mines_explore")!=None:
                    self.mines_explore=copy.deepcopy(self.record_place["gaming"][self.curr_frame]["mines_explore"])
                    #copy()只保證第一個記憶體位址不同，但是裡面的元素還是指向同一個記憶體位址，所以要用deepcopy
                if self.record_place["gaming"][self.curr_frame].get("sound")!=None:
                    if self.record_place["gaming"][self.curr_frame]["sound"][0]==1:
                        self.sound_button.play()
                    if self.record_place["gaming"][self.curr_frame]["sound"][1]==1:
                        self.sound_explosion.play()
                    if self.record_place["gaming"][self.curr_frame]["sound"][2]==1:
                        self.sound_click.play()
                    if self.record_place["gaming"][self.curr_frame]["sound"][3]==1:
                        self.sound_finish.play()
                if self.record_place["gaming"][self.curr_frame].get("flag")!=None:
                    flag=self.record_place["gaming"][self.curr_frame]["flag"]
                    if self.mines_explore[flag[0]][flag[1]]==0:
                        self.mines_explore[flag[0]][flag[1]]=2
                        self.flags-=1
                    elif self.mines_explore[flag[0]][flag[1]]==2:
                        self.mines_explore[flag[0]][flag[1]]=0
                        self.flags+=1
                
                if self.curr_frame==self.game_length-1:
                    self.mines_explore=[[1 for j in range(w)] for i in range(h)]
                    self.mines_map=self.record_place["gaming"][self.curr_frame]["final_map"]
                    self.flags=0
                    self.play_mode=2
                elif self.curr_frame<self.game_length:
                    self.curr_frame+=1
                self.cursor_rect.topleft=[26+int(self.frame_length*self.curr_frame),screen.get_height()-62]
        self.set_backgroud(screen,w,h,m,block_size)
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and self.button_enable:
                if not self.slide_check:
                    if self.play_rect.collidepoint(pos):
                        self.sound_button.play()
                        if event.button == 3:
                            self.finished = True
                            self.next = 'record_info'
                            self.record_place=None
                            self.mines_rect=[]
                            self.mines_map=[]
                            self.mines_explore=[]
                            self.play_mode=0
                            self.game_length=0
                            self.time=pygame.time.get_ticks()
                            self.curr_frame=0
                            self.flags=0
                            self.frame_length=0
                            self.slide_check=False
                            return "reset_size"
                        else:
                            if self.play_mode==0:
                                self.play_mode=1
                            elif self.play_mode==1:
                                self.play_mode=0
                            elif self.play_mode==2:
                                self.play_mode=0
                                self.curr_frame=0
                                self.time=pygame.time.get_ticks()
                                self.mines_explore=[[0 for j in range(w)] for i in range(h)]
                                if self.record_place["gaming"][0]["first_grid"]!=[-1,-1]:
                                    self.mines_explore[self.record_place["gaming"][0]["first_grid"][0]][self.record_place["gaming"][0]["first_grid"][1]]=1
                                self.flags=self.record_place["mines"]
                self.slide_check=False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.slide_rect.collidepoint(pos) or self.cursor_rect.collidepoint(pos):
                    self.slide_check=True
        self.button_enable=False
        if any(pygame.mouse.get_pressed()):
            self.button_enable=True
            if self.slide_check:
                if pos[0]-26>=self.slide_length-38:
                    self.cursor_rect.topleft=[self.slide_length+26-38,screen.get_height()-62]
                    self.curr_frame=self.game_length-1
                    self.time=pygame.time.get_ticks()
                    self.time-=self.record_place["gaming"][self.curr_frame]["time"]
                    self.mines_explore=[[1 for j in range(w)] for i in range(h)]
                    self.mines_map=self.record_place["gaming"][self.curr_frame]["final_map"]
                    self.flags=0
                elif pos[0]-26<0:
                    self.cursor_rect.topleft=[26,screen.get_height()-62]
                    self.curr_frame=0
                    self.time=pygame.time.get_ticks()
                    self.mines_explore=[[0 for j in range(w)] for i in range(h)]
                    if self.record_place["gaming"][0]["first_grid"]!=[-1,-1]:
                        self.mines_explore[self.record_place["gaming"][0]["first_grid"][0]][self.record_place["gaming"][0]["first_grid"][1]]=1
                    self.flags=self.record_place["mines"]
                else:
                    self.cursor_rect.topleft=[pos[0],screen.get_height()-62]
                    self.curr_frame=int((pos[0]-26)/self.frame_length)
                    if self.curr_frame>=self.game_length:
                        self.curr_frame=self.game_length-1
                    self.time=pygame.time.get_ticks()
                    self.time-=self.record_place["gaming"][self.curr_frame]["time"]
                    self.mines_explore=[[0 for j in range(w)] for i in range(h)]
                    self.flags=self.record_place["mines"]
                    temp=0
                    for i in range(self.curr_frame):
                        f=self.curr_frame-i
                        if self.record_place["gaming"][f].get("mines_explore")!=None:
                            self.mines_explore=copy.deepcopy(self.record_place["gaming"][f]["mines_explore"])
                            temp=f
                            flag_change=0
                            for j in self.mines_explore:
                                flag_change+=j.count(2)
                            #print(flag_change)
                            self.flags-=flag_change
                            break
                    for i in range(temp,self.curr_frame):
                        if self.record_place["gaming"][i].get("flag")!=None:
                            flag=self.record_place["gaming"][i]["flag"]
                            if self.mines_explore[flag[0]][flag[1]]==0:
                                self.mines_explore[flag[0]][flag[1]]=2
                                self.flags-=1
                            elif self.mines_explore[flag[0]][flag[1]]==2:
                                self.mines_explore[flag[0]][flag[1]]=0
                                self.flags+=1
            elif self.play_rect.collidepoint(pos):
                temp = pygame.Surface((60,60))
                temp.fill(C.GRAY)
                if self.play_mode==1:
                    tool.blit_image(temp,self.replay_play,(temp.get_width()/2,temp.get_height()/2),True)
                elif self.play_mode==0:
                    tool.blit_image(temp,self.replay_pause,(temp.get_width()/2,temp.get_height()/2),True)
                elif self.play_mode==2:
                    tool.blit_image(temp,self.replay_end,(temp.get_width()/2,temp.get_height()/2),True)
                temp = pygame.transform.scale(temp,(69,69))
                screen.blit(temp,self.play_rect)

                

        
    
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
        if self.play_mode==1:
            temp = setup.grids[15].copy()
            tool.blit_image(temp,self.replay_play,(temp.get_width()/2,temp.get_height()/2),True)
            temp = pygame.transform.scale(temp,(69,69))
            screen.blit(temp,self.play_rect)
        elif self.play_mode==0:
            temp = setup.grids[15].copy()
            tool.blit_image(temp,self.replay_pause,(temp.get_width()/2,temp.get_height()/2),True)
            temp = pygame.transform.scale(temp,(69,69))
            screen.blit(temp,self.play_rect)
        elif self.play_mode==2:
            temp = setup.grids[15].copy()
            tool.blit_image(temp,self.replay_end,(temp.get_width()/2,temp.get_height()/2),True)
            temp = pygame.transform.scale(temp,(69,69))
            screen.blit(temp,self.play_rect)
        temp=pygame.Surface((screen.get_width()-52,23)).convert()
        temp.fill(C.DARK_GRAY)
        tool.blit_rectangle(temp,C.WHITE,(0,0),(temp.get_width()-3,20))
        screen.blit(temp,self.slide_rect.topleft)

        temp=self.replay_cursor.copy()
        temp2=pygame.Surface((10,20)).convert()
        temp2.fill(C.GRAY)
        temp.blit(temp2,(8,10))
        screen.blit(temp,self.cursor_rect.topleft)


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


        if self.record_place["mines"]>999:
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
                t=self.record_place["gaming"][self.curr_frame]["time"]
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
                t=self.record_place["gaming"][self.curr_frame]["time"]
                t=t//1000
                if t>999:
                    t=999
                temp=setup.numbers[t//100]
                screen.blit(temp,(screen.get_width()-168,46.5))
                temp=setup.numbers[t%100//10]
                screen.blit(temp,(screen.get_width()-129,46.5))
                temp=setup.numbers[t%10]
                screen.blit(temp,(screen.get_width()-90,46.5))
        
        screen.blit(self.mouse_cursor,self.record_place["gaming"][self.curr_frame]["pos"])


        

    def get_record_game_place(self,record_info,record):
        for i in record:
            if i[0] == record_info:
                self.record_place = copy.deepcopy(i[1])
                #print(self.record_place)
                self.game_length=len(i[1]["gaming"])
                self.mines_map=i[1]["mines_map"]
                self.mines_explore=[[0 for j in range(i[1]["width"])] for k in range(i[1]["height"])]
                if i[1]["gaming"][0]["first_grid"]!=[-1,-1]:
                    self.mines_explore[i[1]["gaming"][0]["first_grid"][0]][i[1]["gaming"][0]["first_grid"][1]]=1
                self.flags=i[1]["mines"]
                break
        
    def create_button_base(self):
        temp = pygame.Surface((480,96)).convert()
        temp2=pygame.Surface((48,24)).convert()
        temp2.blit(setup.grids[15],(0,-12))
        for i in range(0,480,48):
            temp.blit(setup.grids[15],(i,0))
            temp.blit(setup.grids[15],(i,48))
            temp.blit(temp2,(i,36))
        temp2=pygame.Surface((24,48)).convert()
        temp2.blit(setup.grids[15],(-12,0))
        for i in range(36,468,48):
            temp.blit(temp2,(i,0))
            temp.blit(temp2,(i,48))
            temp3=pygame.Surface((24,24)).convert()
            temp3.blit(setup.grids[15],(-12,-12))
            temp.blit(temp3,(i,36))
        return temp
    def blit_title(self,temp,text):
        tool.blit_text(temp,setup.mine_sweeper_font_32,text,C.WHITE,(temp.get_width()/2+3,temp.get_height()/2+3),True)
        tool.blit_text(temp,setup.mine_sweeper_font_32,text,C.WHITE,(temp.get_width()/2-3,temp.get_height()/2-3),True)
        tool.blit_text(temp,setup.mine_sweeper_font_32,text,C.WHITE,(temp.get_width()/2+3,temp.get_height()/2-3),True)
        tool.blit_text(temp,setup.mine_sweeper_font_32,text,C.WHITE,(temp.get_width()/2-3,temp.get_height()/2+3),True)
        tool.blit_text(temp,setup.mine_sweeper_font_32,text,C.BLACK,(temp.get_width()/2,temp.get_height()/2),True)