import pygame
from .. import setup
from .. import constant as C
from .. import tool

class Tutorial:
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
        self.sound_explosion = setup.explosion_sounds[0]
        self.sound_button = setup.sounds['button']
        self.sound_click = setup.click_sounds[0]
        self.sound_finish = setup.sounds["finish"]

        self.title = pygame.Rect(36,33,480,96)
        self.page_up_rect = pygame.Rect(27+4,660+4,46,46)
        self.page_down_rect = pygame.Rect(471+4,660+4,46,46)
        self.page2_grid_rect = pygame.Rect(276-48,330-48,96,96)
        self.page2_mine_rect = pygame.Rect(276-48,560-48,96,96)
        self.page3_mine_rects = [pygame.Rect(276-64-32,500-32,64,64),pygame.Rect(276+32,500-32,64,64),pygame.Rect(276-32,500-64-32,64,64),pygame.Rect(276-32,500+32,64,64),pygame.Rect(276-64-32,500+32,64,64),pygame.Rect(276+32,500+32,64,64),pygame.Rect(276+32,500-64-32,64,64),pygame.Rect(276-64-32,500-64-32,64,64)]
        self.page3_number_rect = pygame.Rect(276-32,500-32,64,64)
        self.page4_mark_rect = pygame.Rect(276-48,350-48,96,96)
        self.button_enable=True
        self.page2_grid_enable=False
        self.page2_mine_enable=False
        self.page3_mine_enables=[False,False,False,False,False,False,False,False]
        self.page3_number_enable=False
        self.page4_mark_enable=False

        self.page = 1
        
    def update(self,screen,events,pos,game_setting):
        self.set_backgroud(screen)
        self.sound_explosion = setup.explosion_sounds[game_setting["explode_type"]-1]
        self.sound_click = setup.click_sounds[game_setting["click_type"]-1]
        pygame.mixer.Sound.set_volume(self.sound_button,game_setting["sound_scale"]/10)
        pygame.mixer.Sound.set_volume(self.sound_explosion,game_setting["explode_scale"]/10)
        pygame.mixer.Sound.set_volume(self.sound_click,game_setting["sound_scale"]/10)
        pygame.mixer.Sound.set_volume(self.sound_finish,game_setting["sound_scale"]/10)
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and self.button_enable:
                if self.title.collidepoint(pos):
                    self.sound_button.play()
                    self.finished = True
                    self.next = "main_menu"
                    self.page = 1
                    self.page2_grid_enable = False
                    self.page2_mine_enable = False
                    self.page3_number_enable = False
                    self.page3_mine_enables = [False,False,False,False,False,False,False,False]
                    self.page4_mark_enable = False
                elif self.page_up_rect.collidepoint(pos):
                    self.sound_button.play()
                    if self.page > 1:
                        self.page -= 1
                    if self.page == 2:
                        self.page2_grid_enable = False
                        self.page2_mine_enable = False
                    elif self.page == 3:
                        self.page3_number_enable = False
                        self.page3_mine_enables = [False,False,False,False,False,False,False,False]
                    elif self.page == 4:
                        self.page4_mark_enable = False
                elif self.page_down_rect.collidepoint(pos):
                    self.sound_button.play()
                    if self.page < 7:
                        self.page += 1
                    if self.page == 2:
                        self.page2_grid_enable = False
                        self.page2_mine_enable = False
                    elif self.page == 3:
                        self.page3_number_enable = False
                        self.page3_mine_enables = [False,False,False,False,False,False,False,False]
                    elif self.page == 4:
                        self.page4_mark_enable = False
                else:
                    if event.button == 1:
                        if self.page == 2:
                            if self.page2_grid_rect.collidepoint(pos):
                                if not self.page2_grid_enable:
                                    self.page2_grid_enable = True
                                    self.sound_click.play()
                            elif self.page2_mine_rect.collidepoint(pos):
                                if not self.page2_mine_enable:
                                    self.page2_mine_enable = True
                                    self.sound_explosion.play()
                        elif self.page == 3:
                            if self.page3_number_rect.collidepoint(pos):
                                if not self.page3_number_enable:
                                    self.page3_number_enable = True
                                    self.sound_click.play()
                            else:
                                for i in range(8):
                                    if self.page3_mine_rects[i].collidepoint(pos):
                                        if not self.page3_mine_enables[i]:
                                            self.page3_mine_enables[i] = True
                                            self.sound_explosion.play()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    if self.page == 4:
                        if self.page4_mark_rect.collidepoint(pos):
                            self.page4_mark_enable = not self.page4_mark_enable
        self.button_enable=False
        if any(pygame.mouse.get_pressed()):
            self.button_enable=True
            if self.title.collidepoint(pos):
                temp = pygame.Surface((500,100))
                temp.fill(C.GRAY)
                self.blit_title(temp,'Tutorial')
                temp = pygame.transform.scale(temp,(480,96))
                screen.blit(temp,self.title.topleft)
            elif self.page_up_rect.collidepoint(pos):
                block = self.create_block()
                temp = pygame.Surface((46,46)).convert()
                temp.fill(C.GRAY)
                block.blit(temp,(4,4))
                temp = pygame.transform.scale(setup.replay_previous,(30,30))
                tool.blit_image(block,temp,(27,27),True)
                screen.blit(block,(27,660))
            elif self.page_down_rect.collidepoint(pos):
                block = self.create_block()
                temp = pygame.Surface((46,46)).convert()
                temp.fill(C.GRAY)
                block.blit(temp,(4,4))
                temp = pygame.transform.scale(setup.replay_next,(30,30))
                tool.blit_image(block,temp,(27,27),True)
                screen.blit(block,(471,660))
            
            
            else:
                if pygame.mouse.get_pressed()[0]:
                    if self.page == 2:
                        if self.page2_grid_rect.collidepoint(pos) and not self.page2_grid_enable:
                            temp = pygame.Surface((96,96)).convert()
                            temp.fill(C.GRAY)
                            screen.blit(temp,(276-48,330-48))
                        elif self.page2_mine_rect.collidepoint(pos) and not self.page2_mine_enable:
                            temp = pygame.Surface((96,96)).convert()
                            temp.fill(C.GRAY)
                            screen.blit(temp,(276-48,560-48))
                    elif self.page == 3:
                        if self.page3_number_rect.collidepoint(pos) and not self.page3_number_enable:
                            temp = pygame.Surface((64,64)).convert()
                            temp.fill(C.GRAY)
                            screen.blit(temp,(276-32,500-32))
                        else:
                            for i in range(8):
                                if self.page3_mine_rects[i].collidepoint(pos):
                                    if self.page == 3 and not self.page3_mine_enables[i]:
                                        temp = pygame.Surface((64,64)).convert()
                                        temp.fill(C.GRAY)
                                        screen.blit(temp,self.page3_mine_rects[i].topleft)
                   
                

        
    
    def set_backgroud(self,screen):
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
        
        temp = self.create_button_base()
        self.blit_title(temp,'Tutorial')
        screen.blit(temp,self.title.topleft)

        temp = pygame.Surface((6,480)).convert()
        temp.fill(C.WHITE)
        screen.blit(temp,(36,162))
        temp.fill(C.DARK_GRAY)
        screen.blit(temp,(510,162))
        temp = pygame.Surface((480,6)).convert()
        temp.fill(C.WHITE)
        screen.blit(temp,(36,162))
        temp.fill(C.DARK_GRAY)
        screen.blit(temp,(36,636))
        temp = pygame.Surface((3,3)).convert()
        temp.fill(C.GRAY)
        screen.blit(temp,(513,162))
        screen.blit(temp,(510,165))
        screen.blit(temp,(36,639))
        screen.blit(temp,(39,636))
        temp.fill(C.DARK_GRAY)
        screen.blit(temp,(513,165))
        temp.fill(C.WHITE)
        screen.blit(temp,(36,636))

        tool.blit_text(screen,setup.mine_sweeper_font_24,'Page: '+str(self.page),C.WHITE,(276+2,690+2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,'Page: '+str(self.page),C.WHITE,(276-2,690-2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,'Page: '+str(self.page),C.WHITE,(276+2,690-2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,'Page: '+str(self.page),C.WHITE,(276-2,690+2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,'Page: '+str(self.page),C.BLACK,(276,690),True)

        block=self.create_block()
        temp = pygame.transform.scale(setup.replay_previous,(32,32))
        tool.blit_image(block,temp,(27,27),True)
        screen.blit(block,(27,660))
        block=self.create_block()
        temp = pygame.transform.scale(setup.replay_next,(32,32))
        tool.blit_image(block,temp,(27,27),True)
        screen.blit(block,(471,660))

        if self.page == 1:
            self.blit_bold_text(screen,'Welcome to Mine*Sweeper!',(276,200))
            temp = pygame.transform.scale(setup.expert,(336,214))
            tool.blit_image(screen,temp,(276,350),True)
            self.blit_bold_text(screen,'The object of Mine*sweeper',(276,480))
            self.blit_bold_text(screen,'is to locate all the mines',(276,510))
            self.blit_bold_text(screen,'as quickly as possible',(276,540))
            self.blit_bold_text(screen,'without',(276,570))
            self.blit_bold_text(screen,'uncovering any of them.',(276,600))
        elif self.page == 2:
            self.blit_bold_text(screen,'You can uncover a square',(276,200))
            self.blit_bold_text(screen,'by left clicking it.',(276,230))
            if self.page2_grid_enable:
                temp = pygame.surface.Surface((96,96)).convert()
                temp.fill(C.GRAY)
                hole = self.create_hole()
                hole.blit(temp,(4,4))
                tool.blit_image(screen,hole,(276,330),True)
            else:
                temp = pygame.transform.scale(setup.grids[15],(96,96))
                hole = self.create_hole()
                hole.blit(temp,(4,4))
                tool.blit_image(screen,hole,(276,330),True)
            self.blit_bold_text(screen,'If you uncover a mine,',(276,430))
            self.blit_bold_text(screen,'you lose.',(276,460))
            if self.page2_mine_enable:
                temp = pygame.transform.scale(setup.mine_icon,(96,96))
                temp2 = pygame.Surface((96,96)).convert()
                temp2.fill(C.RED)
                temp2.blit(temp,(0,0))
                hole = self.create_hole()
                hole.blit(temp2,(4,4))
                tool.blit_image(screen,hole,(276,560),True)
            else:
                temp = pygame.transform.scale(setup.grids[15],(96,96))
                hole = self.create_hole()
                hole.blit(temp,(4,4))
                tool.blit_image(screen,hole,(276,560),True)
        elif self.page == 3:
            self.blit_bold_text(screen,'If a number',(276,200))
            self.blit_bold_text(screen,'appears on a square,',(276,230))
            self.blit_bold_text(screen,'it indicates how many mines',(276,260))
            self.blit_bold_text(screen,'are in the surrounding',(276,290))
            self.blit_bold_text(screen,'eight squares.',(276,320))

            hole = self.create_hole()
            hole = pygame.transform.scale(hole,(208,208))
            tool.blit_image(screen,hole,(276,500),True)
            temp = pygame.transform.scale(setup.grids[8],(64,64))
            tool.blit_image(screen,temp,(276,500),True)
            temp = pygame.transform.scale(setup.grids[12],(64,64))
            tool.blit_image(screen,temp,(276+64,500),True)
            tool.blit_image(screen,temp,(276-64,500),True)
            tool.blit_image(screen,temp,(276+64,500+64),True)
            tool.blit_image(screen,temp,(276-64,500+64),True)
            tool.blit_image(screen,temp,(276+64,500-64),True)
            tool.blit_image(screen,temp,(276-64,500-64),True)
            tool.blit_image(screen,temp,(276,500+64),True)
            tool.blit_image(screen,temp,(276,500-64),True)

            temp = pygame.transform.scale(setup.grids[15],(64,64))
            if not self.page3_number_enable:
                tool.blit_image(screen,temp,(276,500),True)
            for i in range(8):
                if not self.page3_mine_enables[i]:
                    tool.blit_image(screen,temp,self.page3_mine_rects[i].topleft,False)
        elif self.page == 4:
            self.blit_bold_text(screen,'To mark a square',(276,200))
            self.blit_bold_text(screen,'you suspect contains a mine,',(276,230))
            self.blit_bold_text(screen,'right click it.',(276,260))
            hole = self.create_hole()
            if self.page4_mark_enable:
                temp = pygame.transform.scale(setup.grids[14],(96,96))
                hole.blit(temp,(4,4))
                tool.blit_image(screen,hole,(276,350),True)
            else:
                temp = pygame.transform.scale(setup.grids[15],(96,96))
                hole.blit(temp,(4,4))
                tool.blit_image(screen,hole,(276,350),True)

            self.blit_bold_text(screen,'In game, You can left click',(276,450))
            self.blit_bold_text(screen,'the face to restart the game',(276,480))
            self.blit_bold_text(screen,'or right click the face',(276,510))
            self.blit_bold_text(screen,'to return to the menu.',(276,540))
            temp = pygame.transform.scale(setup.faces[0],(64,64))
            tool.blit_image(screen,temp,(276,590),True)
        elif self.page == 5:
            self.blit_bold_text(screen,'In Record, you can',(276,200))
            self.blit_bold_text(screen,'view and save the replay of',(276,230))
            self.blit_bold_text(screen,'your games.',(276,260))
            self.blit_bold_text(screen,'right click the play button',(276,310))
            self.blit_bold_text(screen,'to return to the menu.',(276,340))
            temp = pygame.transform.scale(setup.replay_play,(64,64))
            tool.blit_image(screen,temp,(276,390),True)
            self.blit_bold_text(screen,'In Options, you can',(276,450))
            self.blit_bold_text(screen,'change',(276,480))
            self.blit_bold_text(screen,'the volume and type',(276,510))
            self.blit_bold_text(screen,'of sound and music.',(276,540))
            temp = pygame.transform.scale(setup.music_icon,(64,64))
            tool.blit_image(screen,temp,(276,595),True)
        elif self.page == 6:
            self.blit_bold_text(screen,'Coder: 7tail_PurpleFox',(276,200))
            self.blit_bold_text(screen,'material from:',(276,250))
            self.blit_bold_text(screen,'Microsoft MineSweeper',(276,280))
            self.blit_bold_text(screen,'sound effect from:',(276,330))
            self.blit_bold_text(screen,'free source on the internet',(276,360))
            self.blit_bold_text(screen,'music from:',(276,410))
            self.blit_bold_text(screen,'see in the README.md',(276,440))
        elif self.page == 7:
            fox = pygame.transform.scale(setup.fox,(269,327))
            tool.blit_image(screen,fox,(276,350),True)
            self.blit_bold_text(screen,'Presented by',(276,550))
            self.blit_bold_text(screen,'7tail_PurpleFox',(276,580))






        
        
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

    def blit_bold_text(self,temp,text,pos):
        tool.blit_text(temp,setup.mine_sweeper_font_16,text,C.WHITE,(pos[0]+2,pos[1]+2),True)
        tool.blit_text(temp,setup.mine_sweeper_font_16,text,C.WHITE,(pos[0]-2,pos[1]-2),True)
        tool.blit_text(temp,setup.mine_sweeper_font_16,text,C.WHITE,(pos[0]+2,pos[1]-2),True)
        tool.blit_text(temp,setup.mine_sweeper_font_16,text,C.WHITE,(pos[0]-2,pos[1]+2),True)
        tool.blit_text(temp,setup.mine_sweeper_font_16,text,C.BLACK,pos,True)
    def create_block(self):
        block=pygame.Surface((54,54)).convert()
        block.fill(C.GRAY)
        temp=pygame.Surface((4,54)).convert()
        temp.fill(C.DARK_GRAY)
        block.blit(temp,(0,0))
        temp.fill(C.WHITE)
        block.blit(temp,(50,0))
        temp=pygame.Surface((54,4)).convert()
        temp.fill(C.DARK_GRAY)
        block.blit(temp,(0,0))
        temp.fill(C.WHITE)
        block.blit(temp,(0,50))
        temp=pygame.Surface((4,46)).convert()
        temp.fill(C.WHITE)
        block.blit(temp,(4,4))
        temp.fill(C.DARK_GRAY)
        block.blit(temp,(46,4))
        temp=pygame.Surface((46,4)).convert()
        temp.fill(C.WHITE)
        block.blit(temp,(4,4))
        temp.fill(C.DARK_GRAY)
        block.blit(temp,(4,46))
        temp=pygame.Surface((2,2)).convert()
        temp.fill(C.GRAY)
        block.blit(temp,(52,0))
        block.blit(temp,(50,2))
        block.blit(temp,(48,4))
        block.blit(temp,(46,6))
        block.blit(temp,(0,52))
        block.blit(temp,(2,50))
        block.blit(temp,(4,48))
        block.blit(temp,(6,46))
        temp.fill(C.WHITE)
        block.blit(temp,(52,2))
        block.blit(temp,(4,46))
        temp.fill(C.DARK_GRAY)
        block.blit(temp,(0,50))
        block.blit(temp,(48,6))
        return block
    def create_hole(self):
        hole=pygame.Surface((104,104)).convert()
        hole.fill(C.GRAY)
        temp=pygame.Surface((4,104)).convert()
        temp.fill(C.DARK_GRAY)
        hole.blit(temp,(0,0))
        temp.fill(C.WHITE)
        hole.blit(temp,(100,0))
        temp=pygame.Surface((104,4)).convert()
        temp.fill(C.DARK_GRAY)
        hole.blit(temp,(0,0))
        temp.fill(C.WHITE)
        hole.blit(temp,(0,100))
        temp=pygame.Surface((2,2)).convert()
        temp.fill(C.GRAY)
        hole.blit(temp,(102,0))
        hole.blit(temp,(100,2))
        hole.blit(temp,(0,102))
        hole.blit(temp,(2,100))
        temp.fill(C.WHITE)
        hole.blit(temp,(102,2))
        temp.fill(C.DARK_GRAY)
        hole.blit(temp,(0,100))
        return hole