import pygame
import copy
from .. import setup
from .. import constant as C
from .. import tool

class Record_Info:
    def __init__(self):
        self.finished = False
        self.next = 'record'
        self.border_hor_wide = pygame.transform.scale(setup.border_hor_wide, ((6,90)))
        self.border_hor = pygame.transform.scale(setup.border_hor, ((6,33)))
        self.border_vert = pygame.transform.scale(setup.border_vert, ((36,6)))
        self.corner_bottom_left_wide = pygame.transform.scale(setup.corner_bottom_left_wide, (36,90))
        self.corner_bottom_left = pygame.transform.scale(setup.corner_bottom_left, (36,33))
        self.corner_bottom_right_wide = pygame.transform.scale(setup.corner_bottom_right_wide, (36,90))
        self.corner_bottom_right = pygame.transform.scale(setup.corner_bottom_right, (36,33))
        self.corner_up_left = pygame.transform.scale(setup.corner_up_left, (36,33))
        self.corner_up_right = pygame.transform.scale(setup.corner_up_right, (36,33))
        self.t_left = pygame.transform.scale(setup.t_left, (36,33))
        self.t_right = pygame.transform.scale(setup.t_right, (36,33))
        self.replay_cursor = pygame.transform.scale(setup.replay_cursor, (38,40))
        self.sound_explosion = setup.explosion_sounds[0]
        self.sound_button = setup.sounds['button']
        self.sound_click = setup.click_sounds[0]
        self.sound_finish = setup.sounds["finish"]
        self.title_rect = pygame.Rect(36,33,480,96)
        self.play_rect = pygame.Rect(246,540,60,60)
        self.delete_rect = pygame.Rect(316,540,180,60)
        self.save_rect = pygame.Rect(56,540,180,60)
        self.record = {}
        self.record_info = ""
        self.record_list = []
        self.button_enable=True
        self.bv = 0
        self.replay_play = pygame.transform.scale(setup.replay_play, (36,36))
        self.rename = False
        self.rename_cancel_rect = pygame.Rect(56,490,180,60)
        self.rename_save_rect = pygame.Rect(316,490,180,60)
        self.rename_text = ""
        self.delete = False
        self.duplicated_name = pygame.time.get_ticks()
        self.blank_name = pygame.time.get_ticks()
        self.forbidden_name = pygame.time.get_ticks()
    def update(self,screen,events,pos,game_setting):
        # print(self.record_info)
        # for i in self.record_list:
        #     print(i[0],end=" ")
        # print()
        self.set_backgroud(screen,pos)
        self.sound_explosion = setup.explosion_sounds[game_setting["explode_type"]-1]
        self.sound_click = setup.click_sounds[game_setting["click_type"]-1]
        pygame.mixer.Sound.set_volume(self.sound_button,game_setting["sound_scale"]/10)
        pygame.mixer.Sound.set_volume(self.sound_explosion,game_setting["explode_scale"]/10)
        pygame.mixer.Sound.set_volume(self.sound_click,game_setting["sound_scale"]/10)
        pygame.mixer.Sound.set_volume(self.sound_finish,game_setting["sound_scale"]/10)
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and self.button_enable and self.rename == False and self.delete == False:
                if self.title_rect.collidepoint(pos):
                    self.sound_button.play()
                    self.finished = True
                    self.next = 'record'
                    self.rename = False
                    self.delete = False
                if self.save_rect.collidepoint(pos):
                    self.sound_button.play()
                    self.rename = True
                    if self.record_info == "Last Game":
                        self.rename_text = ""
                    else:
                        self.rename_text = self.record_info
                if self.delete_rect.collidepoint(pos):
                    self.sound_button.play()
                    self.delete = True
                if self.play_rect.collidepoint(pos):
                    self.sound_button.play()
                    self.finished = True
                    self.next = 'record_game_place'
                    self.rename = False
                    self.delete = False
                    return "game_places."+str(self.record["width"])+" "+str(self.record["height"])+" "+str(self.record["mines"])
            elif event.type == pygame.MOUSEBUTTONUP and self.button_enable and self.rename == True and self.delete == False:
                if self.rename_cancel_rect.collidepoint(pos):
                    self.sound_button.play()
                    self.rename = False
                if self.rename_save_rect.collidepoint(pos):
                    self.sound_button.play()
                    if self.rename_text=="":
                        self.blank_name=pygame.time.get_ticks()
                        continue
                    if self.rename_text.lower()=="last game":
                        self.forbidden_name=pygame.time.get_ticks()
                        continue
                    if self.record_info == "Last Game":
                        check=False
                        for i in self.record_list:
                            if i[0].lower()==self.rename_text.lower():
                                check=True
                                self.duplicated_name=pygame.time.get_ticks()
                                break
                        if not check:
                            self.record_info=self.rename_text
                            self.record_list.append((self.record_info,self.record))
                            self.rename=False
                            return "record_info."+self.record_info
                    else:
                        check=False
                        for i in self.record_list:
                            if i[0].lower()==self.rename_text.lower():
                                check=True
                                self.duplicated_name=pygame.time.get_ticks()
                                break
                        if not check:
                            for i in range(len(self.record_list)):
                                if self.record_list[i][0]==self.record_info:
                                    self.record_list[i] = (self.rename_text, self.record_list[i][1])
                                    self.record_info=self.rename_text
                                    self.rename=False
                                    return "record_info."+self.record_info
            elif event.type == pygame.MOUSEBUTTONUP and self.button_enable and self.rename == False and self.delete == True:
                if self.rename_cancel_rect.collidepoint(pos):
                    self.sound_button.play()
                    self.delete = False
                if self.rename_save_rect.collidepoint(pos):
                    self.sound_button.play()
                    for i in range(len(self.record_list)):
                        if self.record_list[i][0]==self.record_info:
                            self.record_list.pop(i)
                            self.finished = True
                            self.next = 'record'
                            self.rename = False
                            self.delete = False
                            if len(self.record_list) != 0:
                                self.record_info = self.record_list[0][0]
                                return "record_info."+self.record_list[0][0]
                            break
            elif event.type == pygame.KEYDOWN:
                if self.rename == True:
                    if event.key == pygame.K_BACKSPACE:
                        self.rename_text = self.rename_text[:-1]
                    else:
                        if event.unicode not in ["\\", "/", ":", "*", "?", "\"", "<", ">", "|"]:
                            self.rename_text += event.unicode
        self.button_enable=False
        if any(pygame.mouse.get_pressed()):
            self.button_enable=True
            if self.rename == False and self.delete == False:
                if self.title_rect.collidepoint(pos):
                    temp = pygame.Surface((500,100))
                    temp.fill(C.GRAY)
                    self.blit_title(temp,self.record_info,setup.mine_sweeper_font_32,3)
                    temp = pygame.transform.scale(temp,(480,96))
                    screen.blit(temp,self.title_rect.topleft)
                if self.play_rect.collidepoint(pos):
                    temp = pygame.Surface((60,60))
                    temp.fill(C.GRAY)
                    tool.blit_image(temp,self.replay_play,(temp.get_width()/2,temp.get_height()/2),True)
                    screen.blit(temp,self.play_rect.topleft)
                if self.delete_rect.collidepoint(pos):
                    temp = pygame.Surface((198,66))
                    temp.fill(C.GRAY)
                    self.blit_title2(temp,setup.mine_sweeper_font_16,"Delete",C.BLACK,(99,33),2,C.WHITE,True)
                    temp = pygame.transform.scale(temp,(180,60))
                    screen.blit(temp,self.delete_rect.topleft)
                if self.save_rect.collidepoint(pos):
                    temp = pygame.Surface((198,66))
                    temp.fill(C.GRAY)
                    if self.record_info == "Last Game":
                        self.blit_title2(temp,setup.mine_sweeper_font_16,"Save",C.BLACK,(99,33),2,C.WHITE,True)
                    else:
                        self.blit_title2(temp,setup.mine_sweeper_font_16,"Rename",C.BLACK,(99,33),2,C.WHITE,True)
                    temp = pygame.transform.scale(temp,(180,60))
                    screen.blit(temp,self.save_rect.topleft)
            elif self.rename == True and self.delete == False:
                if self.rename_cancel_rect.collidepoint(pos):
                    temp = pygame.Surface((198,66))
                    temp.fill(C.GRAY)
                    self.blit_title2(temp,setup.mine_sweeper_font_16,"Cancel",C.BLACK,(99,33),2,C.WHITE,True)
                    temp = pygame.transform.scale(temp,(180,60))
                    screen.blit(temp,self.rename_cancel_rect.topleft)
                if self.rename_save_rect.collidepoint(pos):
                    temp = pygame.Surface((198,66))
                    temp.fill(C.GRAY)
                    self.blit_title2(temp,setup.mine_sweeper_font_16,"Save",C.BLACK,(99,33),2,C.WHITE,True)
                    temp = pygame.transform.scale(temp,(180,60))
                    screen.blit(temp,self.rename_save_rect.topleft)
            elif self.rename == False and self.delete == True:
                if self.rename_cancel_rect.collidepoint(pos):
                    temp = pygame.Surface((198,66))
                    temp.fill(C.GRAY)
                    self.blit_title2(temp,setup.mine_sweeper_font_16,"Cancel",C.BLACK,(99,33),2,C.WHITE,True)
                    temp = pygame.transform.scale(temp,(180,60))
                    screen.blit(temp,self.rename_cancel_rect.topleft)
                if self.rename_save_rect.collidepoint(pos):
                    temp = pygame.Surface((198,66))
                    temp.fill(C.GRAY)
                    self.blit_title2(temp,setup.mine_sweeper_font_16,"Delete",C.BLACK,(99,33),2,C.WHITE,True)
                    temp = pygame.transform.scale(temp,(180,60))
                    screen.blit(temp,self.rename_save_rect.topleft)
    def set_backgroud(self,screen,pos):
        screen.blit(self.corner_up_left,(0,0))
        for i in range(36,516,6):
            screen.blit(self.border_hor,(i,0))
            screen.blit(self.border_hor,(i,129))
            screen.blit(self.border_hor_wide,(i,642))
        screen.blit(self.corner_up_right,(516,0))
        screen.blit(self.corner_bottom_left_wide,(0,642))
        screen.blit(self.corner_bottom_right_wide,(516,642))
        for i in range(33,129,6):
            screen.blit(self.border_vert,(0,i))
            screen.blit(self.border_vert,(516,i))
        screen.blit(self.corner_bottom_left,(0,129))
        screen.blit(self.corner_bottom_right,(516,129))
        temp = pygame.Surface((36,16)).convert()
        temp.blit(self.corner_up_left,(0,-17))
        screen.blit(temp,(0,146))
        temp = pygame.Surface((36,16)).convert()
        temp.blit(self.corner_up_right,(0,-17))
        screen.blit(temp,(516,146))
        for i in range(162,642,6):
            screen.blit(self.border_vert,(0,i))
            screen.blit(self.border_vert,(516,i))

        temp = pygame.Surface((48,24)).convert()
        temp.blit(setup.grids[15],(0,-12))
        for i in range(0,480,48):
            for j in range(162,642,48):
                screen.blit(setup.grids[15],(i+36,j))
            for j in range(210,642,48):
                screen.blit(temp,(i+36,j-12))
        
        temp=pygame.Surface((24,48)).convert()
        temp.blit(setup.grids[15],(-12,0))
        for i in range(36,468,48):
            for j in range(162,642,48):
                screen.blit(temp,(i+36,j))
            temp3=pygame.Surface((24,24)).convert()
            temp3.blit(setup.grids[15],(-12,-12))
            for j in range(210,642,48):
                screen.blit(temp3,(i+36,j-12))

        temp = self.create_button_base()
        self.blit_title(temp,self.record_info,setup.mine_sweeper_font_32,3)
        screen.blit(temp,self.title_rect.topleft)

        self.blit_title2(screen,setup.mine_sweeper_font_16,"Record Name : "+self.record_info,C.BLACK,(276,200),2,C.WHITE,True)
        temp = self.record["date"].split(" ")
        temp = temp[0]+"/"+temp[1]+"/"+temp[2]+" "+temp[3]+":"+temp[4]+":"+temp[5]
        self.blit_title2(screen,setup.mine_sweeper_font_16,"Date : "+temp,C.BLACK,(276,250),2,C.WHITE,True)
        self.blit_title2(screen,setup.mine_sweeper_font_16,"Result : "+self.record["result"],C.BLACK,(276,300),2,C.WHITE,True)
        self.blit_title2(screen,setup.mine_sweeper_font_16,"Width : "+str(self.record["width"])+"  Height : "+str(self.record["height"]),C.BLACK,(276,350),2,C.WHITE,True)
        self.blit_title2(screen,setup.mine_sweeper_font_16,"Mines : "+str(self.record["mines"])+"  3BV : "+str(self.bv),C.BLACK,(276,400),2,C.WHITE,True)
        self.blit_title2(screen,setup.mine_sweeper_font_16,"Time : "+str(self.record["gaming"][-1]["time"]/1000)+" Second",C.BLACK,(276,450),2,C.WHITE,True)
        if self.record["gaming"][-1]["time"]/1000 == 0:
            self.blit_title2(screen,setup.mine_sweeper_font_16,"3BV/Second : 0",C.BLACK,(276,500),2,C.WHITE,True)
        else:
            self.blit_title2(screen,setup.mine_sweeper_font_16,"3BV/Second : "+str(round(self.bv/(self.record["gaming"][-1]["time"]/1000),5)),C.BLACK,(276,500),2,C.WHITE,True)
        temp = setup.grids[15].copy()
        tool.blit_image(temp,self.replay_play,(temp.get_width()/2,temp.get_height()/2),True)
        temp = pygame.transform.scale(temp,(60,60))
        tool.blit_image(screen,temp,(276,570),True)
        temp = self.create_button_base3()
        self.blit_title2(temp,setup.mine_sweeper_font_16,"Delete",C.BLACK,(90,30),2,C.WHITE,True)
        tool.blit_image(screen,temp,(406,570),True)
        temp = self.create_button_base3()
        if self.record_info == "Last Game":
            self.blit_title2(temp,setup.mine_sweeper_font_16,"Save",C.BLACK,(90,30),2,C.WHITE,True)
        else:
            self.blit_title2(temp,setup.mine_sweeper_font_16,"Rename",C.BLACK,(90,30),2,C.WHITE,True)
        tool.blit_image(screen,temp,(146,570),True)

        if self.rename == True:
            temp = pygame.Surface((552,732))
            temp.fill(C.BLACK)
            temp.set_alpha(200)
            screen.blit(temp,(0,0))
            temp = self.create_gray_base(500,400)
            tool.blit_image(screen,temp,(276,366),True)
            temp = self.create_button_base3()
            self.blit_title2(temp,setup.mine_sweeper_font_16,"Cancel",C.BLACK,(90,30),2,C.WHITE,True)
            tool.blit_image(screen,temp,(146,520),True)
            temp = self.create_button_base3()
            self.blit_title2(temp,setup.mine_sweeper_font_16,"Save",C.BLACK,(90,30),2,C.WHITE,True)
            tool.blit_image(screen,temp,(406,520),True)
            if self.record_info == "Last Game":
                self.blit_title2(screen,setup.mine_sweeper_font_24,"New Name",C.BLACK,(276,200),2,C.WHITE,True)
            else:
                self.blit_title2(screen,setup.mine_sweeper_font_24,"Rename",C.BLACK,(276,200),2,C.WHITE,True)
            temp = pygame.Surface((406,66))
            temp.fill(C.DARK_GRAY)
            screen.blit(temp,(73,263))
            temp = pygame.Surface((400,60))
            temp.fill(C.WHITE)
            tool.blit_text(temp,setup.mine_sweeper_font_24,self.rename_text,C.BLACK,(200,30),True)
            screen.blit(temp,(76,266))
            if pygame.time.get_ticks()-self.duplicated_name<1000:
                self.blit_title2(screen,setup.mine_sweeper_font_16,"Duplicated Name",C.BLACK,(276,400),2,C.WHITE,True)
            elif pygame.time.get_ticks()-self.blank_name<1000:
                self.blit_title2(screen,setup.mine_sweeper_font_16,"Blank Name",C.BLACK,(276,400),2,C.WHITE,True)
            elif pygame.time.get_ticks()-self.forbidden_name<1000:
                self.blit_title2(screen,setup.mine_sweeper_font_16,"Forbidden Name",C.BLACK,(276,400),2,C.WHITE,True)
        if self.delete == True:
            temp = pygame.Surface((552,732))
            temp.fill(C.BLACK)
            temp.set_alpha(200)
            screen.blit(temp,(0,0))
            temp = self.create_gray_base(500,400)
            tool.blit_image(screen,temp,(276,366),True)
            temp = self.create_button_base3()
            self.blit_title2(temp,setup.mine_sweeper_font_16,"Cancel",C.BLACK,(90,30),2,C.WHITE,True)
            tool.blit_image(screen,temp,(146,520),True)
            temp = self.create_button_base3()
            self.blit_title2(temp,setup.mine_sweeper_font_16,"Delete",C.BLACK,(90,30),2,C.WHITE,True)
            tool.blit_image(screen,temp,(406,520),True)
            self.blit_title2(screen,setup.mine_sweeper_font_24,"Do you want to",C.BLACK,(276,286),2,C.WHITE,True)
            self.blit_title2(screen,setup.mine_sweeper_font_24,"delete this record?",C.BLACK,(276,356),2,C.WHITE,True)
    def get_record_info(self,record_info,record):
        self.record_info = record_info
        for i in record:
            if i[0] == record_info:
                self.record = i[1]
                break
        self.record_list = record
        self.bv = self.count_3bv(self.record["mines_map"])
        
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
    
    def blit_title(self,temp,text,font,frame):
        tool.blit_text(temp,font,text,C.WHITE,(temp.get_width()/2+frame,temp.get_height()/2+frame),True)
        tool.blit_text(temp,font,text,C.WHITE,(temp.get_width()/2-frame,temp.get_height()/2-frame),True)
        tool.blit_text(temp,font,text,C.WHITE,(temp.get_width()/2+frame,temp.get_height()/2-frame),True)
        tool.blit_text(temp,font,text,C.WHITE,(temp.get_width()/2-frame,temp.get_height()/2+frame),True)
        tool.blit_text(temp,font,text,C.BLACK,(temp.get_width()/2,temp.get_height()/2),True)

    def blit_title2(self,screen,font,text,color,cordinate,frame,frame_color,center=False):
        tool.blit_text(screen,font,text,frame_color,(cordinate[0]+frame,cordinate[1]+frame),center)
        tool.blit_text(screen,font,text,frame_color,(cordinate[0]-frame,cordinate[1]-frame),center)
        tool.blit_text(screen,font,text,frame_color,(cordinate[0]+frame,cordinate[1]-frame),center)
        tool.blit_text(screen,font,text,frame_color,(cordinate[0]-frame,cordinate[1]+frame),center)
        tool.blit_text(screen,font,text,color,cordinate,center)

    def create_button_base3(self):
        temp = pygame.Surface((180,60))
        temp2=pygame.Surface((30,60))
        grid = setup.grids[15].copy()
        grid = pygame.transform.scale(grid,(60,60))
        temp2.blit(grid,(0,0))
        temp.blit(temp2,(0,0))
        temp2.blit(grid,(-30,0))
        temp.blit(temp2,(150,0))
        temp2 = pygame.Surface((30,30))
        temp2.blit(grid,(-15,0))
        for i in range(30,150,30):
            temp.blit(temp2,(i,0))
        temp2.blit(grid,(-15,-30))
        for i in range(30,150,30):
            temp.blit(temp2,(i,30))
        return temp
    def create_gray_base(self,width,height):
        temp = pygame.Surface((width,height))
        temp.fill(C.GRAY)
        temp2 = setup.grids[15].copy()
        temp3 = pygame.Surface((24,24))
        temp3.blit(setup.grids[15],(-12,0))
        for i in range(0,width,24):
            temp.blit(temp3,(i,0))
        temp3 = pygame.Surface((24,24))
        temp3.blit(setup.grids[15],(-12,-24))
        for i in range(0,width,24):
            temp.blit(temp3,(i,height-24))
        temp3 = pygame.Surface((24,24))
        temp3.blit(setup.grids[15],(0,-12))
        for i in range(0,height,24):
            temp.blit(temp3,(0,i))
        temp3 = pygame.Surface((24,24))
        temp3.blit(setup.grids[15],(-24,-12))
        for i in range(0,height,24):
            temp.blit(temp3,(width-24,i))
        temp3 = pygame.Surface((24,24))
        temp3.blit(setup.grids[15],(0,0))
        temp.blit(temp3,(0,0))
        temp3 = pygame.Surface((24,24))
        temp3.blit(setup.grids[15],(-24,0))
        temp.blit(temp3,(width-24,0))
        temp3 = pygame.Surface((24,24))
        temp3.blit(setup.grids[15],(0,-24))
        temp.blit(temp3,(0,height-24))
        temp3 = pygame.Surface((24,24))
        temp3.blit(setup.grids[15],(-24,-24))
        temp.blit(temp3,(width-24,height-24))
        return temp
    def count_3bv(self,map):
        count = 0
        global visited
        global container
        container = []
        visited = [[False for _ in range(len(map[0]))] for _ in range(len(map))]
        for i in range(len(map)):
            for j in range(len(map[i])):
                if visited[i][j] == False and map[i][j] == 0:
                    count += 1
                    container.append((i,j))
                    while len(container) != 0:
                        self.flood_fill_mark(map,container[0][0],container[0][1])
                        container.pop(0)
        
        for i in range(len(map)):
            for j in range(len(map[i])):
                if visited[i][j] == False and map[i][j] != 10:
                    count += 1
                    visited[i][j] = True
            #         print("#",end="")
            #     elif visited[i][j]==False:
            #         print(".",end="")
            #     elif visited[i][j]==True:
            #         print("*",end="")
            # print()
        return count

    def flood_fill_mark(self,map, i, j):
        if i < 0 or i >= len(map) or j < 0 or j >= len(map[i]):
            return
        if visited[i][j] ==  True:
            return
        visited[i][j] = True
        if map[i][j] == 0:
            container.append((i-1,j))
            container.append((i+1,j))
            container.append((i,j-1))
            container.append((i,j+1))
            container.append((i-1,j-1))
            container.append((i-1,j+1))
            container.append((i+1,j-1))
            container.append((i+1,j+1))