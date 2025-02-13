import pygame
from .. import setup
from .. import constant as C
from .. import tool

class Options:
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
        self.t_left = pygame.transform.scale(setup.t_left, (36,33))
        self.t_right = pygame.transform.scale(setup.t_right, (36,33))
        self.replay_play = pygame.transform.scale(setup.replay_play, (32,32))
        self.sound_explosion = setup.explosion_sounds[0]
        self.sound_button = setup.sounds['button']
        self.sound_click = setup.click_sounds[0]
        self.sound_finish = setup.sounds["finish"]

        self.music_block_rect = pygame.Rect(61+4,187+4,70-8,70-8)
        self.sound_block_rect = pygame.Rect(61+4,307+4,70-8,70-8)
        self.mine_block_rect = pygame.Rect(61+4,427+4,70-8,70-8)
        self.music_arrow_left = pygame.Rect(156+4,187+4,40-4,70-8)
        self.music_arrow_right = pygame.Rect(451,187+4,40-4,70-8)
        self.sound_arrow_left = pygame.Rect(156+4,307+4,40-4,70-8)
        self.sound_arrow_right = pygame.Rect(451,307+4,40-4,70-8)
        self.mine_arrow_left = pygame.Rect(156+4,427+4,40-4,70-8)
        self.mine_arrow_right = pygame.Rect(451,427+4,40-4,70-8)
        self.fox_rect = pygame.Rect(62,543,68,82)
        self.toggle_rect = pygame.Rect(156+4,556+4,140-8,56-8)

        self.title = pygame.Rect(36,33,480,96)

        self.button_enable=True
        
    def update(self,screen,events,pos,game_setting):
        self.set_backgroud(screen,game_setting)
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
                elif self.music_arrow_left.collidepoint(pos):
                    self.sound_button.play()
                    return "music_down"
                elif self.music_arrow_right.collidepoint(pos):
                    self.sound_button.play()
                    return "music_up"
                elif self.music_block_rect.collidepoint(pos):
                    self.sound_button.play()
                    return "music_change"
                elif self.sound_arrow_left.collidepoint(pos):
                    self.sound_button.play()
                    return "sound_down"
                elif self.sound_arrow_right.collidepoint(pos):
                    self.sound_button.play()
                    return "sound_up"
                elif self.sound_block_rect.collidepoint(pos):
                    temp = game_setting["click_type"]-1
                    temp = (temp+1)%len(setup.click_sounds)
                    click = setup.click_sounds[temp]
                    click.play()
                    return "sound_change"
                elif self.mine_arrow_left.collidepoint(pos):
                    self.sound_button.play()
                    return "explode_down"
                elif self.mine_arrow_right.collidepoint(pos):
                    self.sound_button.play()
                    return "explode_up"
                elif self.mine_block_rect.collidepoint(pos):
                    temp = game_setting["explode_type"]-1
                    temp = (temp+1)%len(setup.explosion_sounds)
                    explosion = setup.explosion_sounds[temp]
                    explosion.play()
                    return "explode_change"
                elif self.fox_rect.collidepoint(pos):
                    temp = setup.sounds["yamete_kudasai"]
                    temp.play()
                elif self.toggle_rect.collidepoint(pos):
                    self.sound_button.play()
                    return "opening_change"

        self.button_enable=False
        if any(pygame.mouse.get_pressed()):
            self.button_enable=True
            if self.title.collidepoint(pos):
                temp = pygame.Surface((500,100))
                temp.fill(C.GRAY)
                self.blit_title(temp,'Options')
                temp = pygame.transform.scale(temp,(480,96))
                screen.blit(temp,self.title.topleft)
            elif self.music_arrow_left.collidepoint(pos):
                temp = pygame.Surface((36,62))
                temp.fill(C.GRAY)
                arrow=pygame.transform.scale(self.replay_play,(23,48))
                arrow=pygame.transform.flip(arrow,True,False)
                tool.blit_image(temp,arrow,(18,31),True)
                screen.blit(temp,self.music_arrow_left.topleft)
            elif self.music_arrow_right.collidepoint(pos):
                temp = pygame.Surface((36,62))
                temp.fill(C.GRAY)
                arrow=pygame.transform.scale(self.replay_play,(23,48))
                tool.blit_image(temp,arrow,(18,31),True)
                screen.blit(temp,self.music_arrow_right.topleft)
            elif self.music_block_rect.collidepoint(pos):
                block = self.create_block()
                temp = pygame.Surface((62,62)).convert()
                temp.fill(C.GRAY)
                block.blit(temp,(4,4))
                temp = pygame.transform.scale(setup.music_icon,(46,37))
                tool.blit_image(block,temp,(35,35),True)
                screen.blit(block,(61,187))
            elif self.sound_arrow_left.collidepoint(pos):
                temp = pygame.Surface((36,62))
                temp.fill(C.GRAY)
                arrow=pygame.transform.scale(self.replay_play,(23,48))
                arrow=pygame.transform.flip(arrow,True,False)
                tool.blit_image(temp,arrow,(18,31),True)
                screen.blit(temp,self.sound_arrow_left.topleft)
            elif self.sound_arrow_right.collidepoint(pos):
                temp = pygame.Surface((36,62))
                temp.fill(C.GRAY)
                arrow=pygame.transform.scale(self.replay_play,(23,48))
                tool.blit_image(temp,arrow,(18,31),True)
                screen.blit(temp,self.sound_arrow_right.topleft)
            elif self.sound_block_rect.collidepoint(pos):
                block = self.create_block()
                temp = pygame.Surface((62,62)).convert()
                temp.fill(C.GRAY)
                block.blit(temp,(4,4))
                temp = pygame.transform.scale(setup.sound_icon,(34,38))
                tool.blit_image(block,temp,(35,35),True)
                screen.blit(block,(61,307))
            elif self.mine_arrow_left.collidepoint(pos):
                temp = pygame.Surface((36,62))
                temp.fill(C.GRAY)
                arrow=pygame.transform.scale(self.replay_play,(23,48))
                arrow=pygame.transform.flip(arrow,True,False)
                tool.blit_image(temp,arrow,(18,31),True)
                screen.blit(temp,self.mine_arrow_left.topleft)
            elif self.mine_arrow_right.collidepoint(pos):
                temp = pygame.Surface((36,62))
                temp.fill(C.GRAY)
                arrow=pygame.transform.scale(self.replay_play,(23,48))
                tool.blit_image(temp,arrow,(18,31),True)
                screen.blit(temp,self.mine_arrow_right.topleft)
            elif self.mine_block_rect.collidepoint(pos):
                block = self.create_block()
                temp = pygame.Surface((62,62)).convert()
                temp.fill(C.GRAY)
                block.blit(temp,(4,4))
                temp = pygame.transform.scale(setup.mine_icon,(48,48))
                tool.blit_image(block,temp,(35,35),True)
                screen.blit(block,(61,427))
            elif self.fox_rect.collidepoint(pos):
                temp = pygame.Surface((68,82)).convert()
                temp.fill(C.GRAY)
                fox = pygame.transform.scale(setup.pixel_fox,(61,74))
                temp.blit(fox,(3,4))
                screen.blit(temp,self.fox_rect.topleft)
            elif self.toggle_rect.collidepoint(pos):
                temp = pygame.Surface((132,48))
                temp.fill(C.BLACK)
                screen.blit(temp,self.toggle_rect.topleft)
                temp = pygame.transform.scale(setup.grids[13],(48,48))
                screen.blit(temp,(202,560))
            
                

        
    
    def set_backgroud(self,screen,game_setting):
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

        
        block = self.create_block()
        temp = pygame.transform.scale(setup.music_icon,(48,39))
        tool.blit_image(block,temp,(35,35),True)
        screen.blit(block,(61,187))
        tool.blit_text(screen,setup.mine_sweeper_font_16,'Music',C.WHITE,(96+2,272+2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_16,'Music',C.WHITE,(96+2,272-2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_16,'Music',C.WHITE,(96-2,272+2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_16,'Music',C.WHITE,(96-2,272-2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_16,'Music',C.BLACK,(96,272),True)


        block = self.create_block()
        temp = pygame.transform.scale(setup.sound_icon,(36,40))
        tool.blit_image(block,temp,(35,35),True)
        screen.blit(block,(61,307))
        tool.blit_text(screen,setup.mine_sweeper_font_16,'Sound',C.WHITE,(96+2,392+2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_16,'Sound',C.WHITE,(96+2,392-2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_16,'Sound',C.WHITE,(96-2,392+2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_16,'Sound',C.WHITE,(96-2,392-2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_16,'Sound',C.BLACK,(96,392),True)

        block = self.create_block()
        temp=pygame.transform.scale(setup.mine_icon,(50,50))
        tool.blit_image(block,temp,(35,35),True)
        screen.blit(block,(61,427))
        tool.blit_text(screen,setup.mine_sweeper_font_16,'Mine',C.WHITE,(96+2,512+2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_16,'Mine',C.WHITE,(96+2,512-2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_16,'Mine',C.WHITE,(96-2,512+2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_16,'Mine',C.WHITE,(96-2,512-2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_16,'Mine',C.BLACK,(96,512),True)


        number_base = self.create_number_base()
        screen.blit(number_base,(156,187))
        tool.blit_text(screen,setup.mine_sweeper_font_24,str(int(game_setting["music_scale"]*10))+"%",C.WHITE,(323,222),True)
        tool.blit_text(screen,setup.mine_sweeper_font_16,'Volume',C.WHITE,(323+2,272+2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_16,'Volume',C.WHITE,(323+2,272-2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_16,'Volume',C.WHITE,(323-2,272+2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_16,'Volume',C.WHITE,(323-2,272-2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_16,'Volume',C.BLACK,(323,272),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,"-",C.WHITE,(178+2,270+2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,"-",C.WHITE,(178+2,270-2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,"-",C.WHITE,(178-2,270+2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,"-",C.WHITE,(178-2,270-2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,"-",C.BLACK,(178,270),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,"+",C.WHITE,(469+2,270+2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,"+",C.WHITE,(469+2,270-2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,"+",C.WHITE,(469-2,270+2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,"+",C.WHITE,(469-2,270-2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,"+",C.BLACK,(469,270),True)

        screen.blit(number_base,(156,307))
        tool.blit_text(screen,setup.mine_sweeper_font_24,str(int(game_setting["sound_scale"]*10))+"%",C.WHITE,(323,342),True)
        tool.blit_text(screen,setup.mine_sweeper_font_16,'Volume',C.WHITE,(323+2,392+2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_16,'Volume',C.WHITE,(323+2,392-2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_16,'Volume',C.WHITE,(323-2,392+2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_16,'Volume',C.WHITE,(323-2,392-2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_16,'Volume',C.BLACK,(323,392),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,"-",C.WHITE,(178+2,390+2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,"-",C.WHITE,(178+2,390-2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,"-",C.WHITE,(178-2,390+2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,"-",C.WHITE,(178-2,390-2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,"-",C.BLACK,(178,390),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,"+",C.WHITE,(469+2,390+2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,"+",C.WHITE,(469+2,390-2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,"+",C.WHITE,(469-2,390+2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,"+",C.WHITE,(469-2,390-2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,"+",C.BLACK,(469,390),True)

        screen.blit(number_base,(156,427))
        tool.blit_text(screen,setup.mine_sweeper_font_24,str(int(game_setting["explode_scale"])*10)+"%",C.WHITE,(323,462),True)
        tool.blit_text(screen,setup.mine_sweeper_font_16,'Explosion',C.WHITE,(323+2,512+2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_16,'Explosion',C.WHITE,(323+2,512-2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_16,'Explosion',C.WHITE,(323-2,512+2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_16,'Explosion',C.WHITE,(323-2,512-2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_16,'Explosion',C.BLACK,(323,512),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,"-",C.WHITE,(178+2,510+2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,"-",C.WHITE,(178+2,510-2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,"-",C.WHITE,(178-2,510+2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,"-",C.WHITE,(178-2,510-2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,"-",C.BLACK,(178,510),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,"+",C.WHITE,(469+2,510+2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,"+",C.WHITE,(469+2,510-2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,"+",C.WHITE,(469-2,510+2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,"+",C.WHITE,(469-2,510-2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,"+",C.BLACK,(469,510),True)

        temp = pygame.transform.scale(setup.pixel_fox,(68,82))
        screen.blit(temp,(62,543))
        toggle = self.create_toggle_base()
        screen.blit(toggle,(156,556))
        if game_setting["opening"]:
            temp = pygame.transform.scale(setup.grids[14],(48,48))
            screen.blit(temp,(244,556+4))
            tool.blit_text(screen,setup.mine_sweeper_font_16,"On",C.WHITE,(202+2,584+2),True)
            tool.blit_text(screen,setup.mine_sweeper_font_16,"On",C.WHITE,(202+2,584-2),True)
            tool.blit_text(screen,setup.mine_sweeper_font_16,"On",C.WHITE,(202-2,584+2),True)
            tool.blit_text(screen,setup.mine_sweeper_font_16,"On",C.WHITE,(202-2,584-2),True)
            tool.blit_text(screen,setup.mine_sweeper_font_16,"On",C.BLACK,(202,584),True)
        else:
            temp = pygame.transform.scale(setup.grids[15],(48,48))
            screen.blit(temp,(156+4,556+4))
            tool.blit_text(screen,setup.mine_sweeper_font_16,"Off",C.WHITE,(250+2,584+2),True)
            tool.blit_text(screen,setup.mine_sweeper_font_16,"Off",C.WHITE,(250+2,584-2),True)
            tool.blit_text(screen,setup.mine_sweeper_font_16,"Off",C.WHITE,(250-2,584+2),True)
            tool.blit_text(screen,setup.mine_sweeper_font_16,"Off",C.WHITE,(250-2,584-2),True)
            tool.blit_text(screen,setup.mine_sweeper_font_16,"Off",C.BLACK,(250,584),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,"Opening",C.WHITE,(402+2,584+2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,"Opening",C.WHITE,(402+2,584-2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,"Opening",C.WHITE,(402-2,584+2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,"Opening",C.WHITE,(402-2,584-2),True)
        tool.blit_text(screen,setup.mine_sweeper_font_24,"Opening",C.BLACK,(402,584),True)


        temp = self.create_button_base()
        self.blit_title(temp,'Options')
        screen.blit(temp,self.title.topleft)
        
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
    def create_block(self):
        block=pygame.Surface((70,70)).convert()
        block.fill(C.GRAY)
        temp=pygame.Surface((4,70)).convert()
        temp.fill(C.DARK_GRAY)
        block.blit(temp,(0,0))
        temp.fill(C.WHITE)
        block.blit(temp,(66,0))
        temp=pygame.Surface((70,4)).convert()
        temp.fill(C.DARK_GRAY)
        block.blit(temp,(0,0))
        temp.fill(C.WHITE)
        block.blit(temp,(0,66))
        temp=pygame.Surface((4,62)).convert()
        temp.fill(C.WHITE)
        block.blit(temp,(4,4))
        temp.fill(C.DARK_GRAY)
        block.blit(temp,(62,4))
        temp=pygame.Surface((62,4)).convert()
        temp.fill(C.WHITE)
        block.blit(temp,(4,4))
        temp.fill(C.DARK_GRAY)
        block.blit(temp,(4,62))
        temp=pygame.Surface((2,2)).convert()
        temp.fill(C.GRAY)
        block.blit(temp,(68,0))
        block.blit(temp,(66,2))
        block.blit(temp,(64,4))
        block.blit(temp,(62,6))
        block.blit(temp,(0,68))
        block.blit(temp,(2,66))
        block.blit(temp,(4,64))
        block.blit(temp,(6,62))
        temp.fill(C.WHITE)
        block.blit(temp,(68,2))
        block.blit(temp,(4,62))
        temp.fill(C.DARK_GRAY)
        block.blit(temp,(0,66))
        block.blit(temp,(64,6))
        return block
    def create_number_base(self):
        number_base=pygame.Surface((335,70)).convert()
        number_base.fill(C.BLACK)
        arrow=pygame.Surface((36,62)).convert()
        arrow.fill(C.GRAY)
        temp=pygame.Surface((4,62)).convert()
        temp.fill(C.WHITE)
        arrow.blit(temp,(0,0))
        temp.fill(C.DARK_GRAY)
        arrow.blit(temp,(32,0))
        temp=pygame.Surface((36,4)).convert()
        temp.fill(C.WHITE)
        arrow.blit(temp,(0,0))
        temp.fill(C.DARK_GRAY)
        arrow.blit(temp,(0,58))
        temp=pygame.Surface((2,2)).convert()
        temp.fill(C.GRAY)
        arrow.blit(temp,(34,0))
        arrow.blit(temp,(32,2))
        arrow.blit(temp,(0,60))
        arrow.blit(temp,(2,58))
        temp.fill(C.DARK_GRAY)
        arrow.blit(temp,(34,2))
        temp.fill(C.WHITE)
        arrow.blit(temp,(0,58))
        left_arrow=arrow.copy()
        right_arrow=arrow.copy()
        temp=self.replay_play.copy()
        temp=pygame.transform.scale(temp,(25,50))
        tool.blit_image(right_arrow,temp,(18,31),True)
        temp=pygame.transform.flip(temp,True,False)
        tool.blit_image(left_arrow,temp,(18,31),True)
        number_base.blit(left_arrow,(4,4))
        number_base.blit(right_arrow,(295,4))
        temp=pygame.Surface((335,4)).convert()
        temp.fill(C.DARK_GRAY)
        number_base.blit(temp,(0,0))
        temp.fill(C.WHITE)
        number_base.blit(temp,(0,66))
        temp=pygame.Surface((4,62)).convert()
        temp.fill(C.DARK_GRAY)
        number_base.blit(temp,(0,4))
        temp.fill(C.WHITE)
        number_base.blit(temp,(331,4))
        temp=pygame.Surface((2,2)).convert()
        temp.fill(C.GRAY)
        number_base.blit(temp,(333,0))
        number_base.blit(temp,(331,2))
        number_base.blit(temp,(0,68))
        number_base.blit(temp,(2,66))
        temp.fill(C.WHITE)
        number_base.blit(temp,(333,2))
        temp.fill(C.DARK_GRAY)
        number_base.blit(temp,(0,66))
        temp=pygame.Surface((255,4)).convert()
        temp.fill(C.WHITE)
        number_base.blit(temp,(40,4))
        temp.fill(C.DARK_GRAY)
        number_base.blit(temp,(40,62))
        temp=pygame.Surface((4,62)).convert()
        temp.fill(C.WHITE)
        number_base.blit(temp,(40,4))
        temp.fill(C.DARK_GRAY)
        number_base.blit(temp,(291,4))
        temp=pygame.Surface((2,2)).convert()
        temp.fill(C.GRAY)
        number_base.blit(temp,(291,6))
        number_base.blit(temp,(293,4))
        number_base.blit(temp,(40,64))
        number_base.blit(temp,(42,62))
        temp.fill(C.DARK_GRAY)
        number_base.blit(temp,(42,64))
        temp.fill(C.WHITE)
        number_base.blit(temp,(291,4))
        return number_base
    def create_toggle_base(self):
        toggle=pygame.Surface((140,56)).convert()
        toggle.fill(C.BLACK)
        temp=pygame.Surface((4,56)).convert()
        temp.fill(C.DARK_GRAY)
        toggle.blit(temp,(0,0))
        temp.fill(C.WHITE)
        toggle.blit(temp,(136,0))
        temp=pygame.Surface((140,4)).convert()
        temp.fill(C.DARK_GRAY)
        toggle.blit(temp,(0,0))
        temp.fill(C.WHITE)
        toggle.blit(temp,(0,52))
        temp=pygame.Surface((2,2)).convert()
        temp.fill(C.GRAY)
        toggle.blit(temp,(138,0))
        toggle.blit(temp,(136,2))
        toggle.blit(temp,(0,54))
        toggle.blit(temp,(2,52))
        temp.fill(C.WHITE)
        toggle.blit(temp,(138,2))
        temp.fill(C.DARK_GRAY)
        toggle.blit(temp,(0,52))
        return toggle
    def blit_title(self,temp,text):
        tool.blit_text(temp,setup.mine_sweeper_font_32,text,C.WHITE,(temp.get_width()/2+3,temp.get_height()/2+3),True)
        tool.blit_text(temp,setup.mine_sweeper_font_32,text,C.WHITE,(temp.get_width()/2-3,temp.get_height()/2-3),True)
        tool.blit_text(temp,setup.mine_sweeper_font_32,text,C.WHITE,(temp.get_width()/2+3,temp.get_height()/2-3),True)
        tool.blit_text(temp,setup.mine_sweeper_font_32,text,C.WHITE,(temp.get_width()/2-3,temp.get_height()/2+3),True)
        tool.blit_text(temp,setup.mine_sweeper_font_32,text,C.BLACK,(temp.get_width()/2,temp.get_height()/2),True)