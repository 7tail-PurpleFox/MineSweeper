import pygame
import os
from . import constant as C
import json

class Game:
    def __init__(self,state_dict,start_state):
        self.screen = pygame.display.get_surface()
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.sub_background = self.background.copy()
        self.background.fill(C.GRAY)
        self.clock = pygame.time.Clock()
        self.running = True
        self.events = pygame.event.get()
        self.state_dict = state_dict
        self.state = self.state_dict[start_state]
        self.pos = pygame.mouse.get_pos()
        self.record_info = ""
        if os.path.exists("source/game_setting.json"):
            with open("source/game_setting.json","r") as f:
                self.game_setting = json.load(f)
                self.sound_scale = self.game_setting["sound_scale"]
                self.music_scale = self.game_setting["music_scale"]
                self.explode_type = self.game_setting["explode_type"]
                self.custom_field = self.game_setting["custom_field"]
                self.game_place = [9,9,10]
                self.block_size = 480/9
        else:
            self.sound_scale = 5
            self.music_scale = 5
            self.explode_type = 1
            self.custom_field = [9,9,10]
            self.game_place = [9,9,10]
            self.block_size = 480/9
            self.game_setting = {"sound_scale":self.sound_scale,
                                "music_scale":self.music_scale,
                                "explode_type":self.explode_type,
                                "custom_field":self.custom_field,
                                "game_place":self.game_place,
                                "block_size":self.block_size}
        self.record=[]
        for i in os.listdir("source/record"):
            if i[-5:]==".json":
                with open("source/record/"+i,"r") as f:
                    self.record.append([i[:-5],json.load(f)])
        self.record_temp={}
            
    def update(self):
        self.background.fill(C.GRAY)
        self.game_setting["sound_scale"] = self.sound_scale
        self.game_setting["music_scale"] = self.music_scale
        self.game_setting["explode_type"] = self.explode_type
        self.game_setting["custom_field"] = self.custom_field
        self.game_setting["game_place"] = self.game_place
        self.game_setting["block_size"] = self.block_size
        feedback = self.state.update(self.background,self.events,self.pos,self.game_setting)
        if feedback != None:
            self.handle_feedback(feedback)
        if self.state.finished:
            next_state = self.state.next
            self.state.finished = False
            self.state = self.state_dict[next_state]
            if next_state=="record":
                self.state.get_record(self.record)
            elif next_state=="record_info":
                self.state.get_record_info(self.record_info,self.record)
            elif next_state=="record_game_place":
                self.state.get_record_game_place(self.record_info,self.record)
        
            
    def run(self):
        while self.running:
            self.screen.fill(C.BLACK)
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.running = False
            self.pos = pygame.mouse.get_pos()
            self.blit_background()
            self.update()
            pygame.display.update()
            self.clock.tick(120)
        with open("source/game_setting.json","w") as f:
            json.dump(self.game_setting,f)
        temp=os.listdir("source/record")
        for i in temp:
            os.remove("source/record/"+i)
        for i in self.record:
            with open("source/record/"+i[0]+".json","w") as f:
                json.dump(i[1],f)
        pygame.quit()
    def blit_background(self):
        if self.screen.get_width()==C.MAX_WIDTH:
            screen_width, screen_height = self.screen.get_size()
            background_width, background_height = self.sub_background.get_size()
            background_width = int(screen_height * background_width / background_height)
            background_height = screen_height
            if background_width > screen_width:
                background_height = int(screen_width * background_height / background_width)
                background_width = screen_width
                self.pos = (self.pos[0]*(72+self.block_size*self.game_place[0])//screen_width,(self.pos[1]-((screen_height-background_height)//2))*(252+self.block_size*self.game_place[1])//background_height)
            else:
                self.pos = ((self.pos[0]-((C.MAX_WIDTH-background_width)//2))*(72+self.block_size*self.game_place[0])//background_width,self.pos[1]*(252+self.block_size*self.game_place[1])//screen_height)
            self.sub_background =self.background.copy()
            self.sub_background = pygame.transform.scale(self.sub_background, (background_width, background_height))
        elif self.screen.get_size() != self.sub_background.get_size():
            screen_width, screen_height = self.screen.get_size()
            background_width, background_height = self.sub_background.get_size()
            self.pos = (self.pos[0]*(72+self.block_size*self.game_place[0])//screen_width,self.pos[1]*(252+self.block_size*self.game_place[1])//screen_height)
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
            screen_width, screen_height = self.screen.get_size()
            self.pos = (self.pos[0]*(72+self.block_size*self.game_place[0])//screen_width,self.pos[1]*(252+self.block_size*self.game_place[1])//screen_height)
            self.sub_background = pygame.transform.scale(self.background.copy(),self.sub_background.get_size())
        rect=self.sub_background.get_rect()
        rect.center=self.screen.get_rect().center
        self.screen.blit(self.sub_background,rect.topleft)
        
    def handle_feedback(self,feedback):
        f=feedback.split('.')
        if len(f)>2:
            for i in f[2:]:
                f[1]+="."
                f[1]+=i
        if f[0] == "quit":
            self.running = False
        elif f[0] == "reset_size":
            self.game_place = [9,9,10]
            self.block_size = 480/9
            if self.screen.get_width()!=C.MAX_WIDTH:
                h=self.screen.get_height()
                ratio=h/(252+self.block_size*self.game_place[1])
                w=(72+self.block_size*self.game_place[0])*ratio
                self.screen=pygame.display.set_mode((w, h), pygame.RESIZABLE)
            self.background=pygame.Surface((72+self.block_size*self.game_place[0],252+self.block_size*self.game_place[1])).convert()
            self.sub_background=self.background.copy()
        elif f[0] == "custom_field":
            temp=f[1].split()
            self.custom_field=[int(temp[0]),int(temp[1]),int(temp[2])]
            self.game_setting["custom_field"]=self.custom_field
        elif f[0] == "game_places":
            temp=f[1].split()
            self.game_place=[int(temp[0]),int(temp[1]),int(temp[2])]
            self.game_setting["game_place"]=self.game_place
            if 480/min(self.game_place[0],self.game_place[1])<30:
                self.block_size=30
            else:
                self.block_size=480/min(self.game_place[0],self.game_place[1])
            if self.screen.get_width()!=C.MAX_WIDTH:
                h=self.screen.get_height()
                ratio=h/(252+self.block_size*self.game_place[1])
                w=(72+self.block_size*self.game_place[0])*ratio
                self.screen=pygame.display.set_mode((w, h), pygame.RESIZABLE)
            self.background=pygame.Surface((72+self.block_size*self.game_place[0],252+self.block_size*self.game_place[1])).convert()
            self.sub_background=self.background.copy()
        elif f[0] == "record":
            temp=f[1].split('/')
            if "Init" in temp[0]:
                self.record_temp={}
                self.record_temp["flags"]=int(temp[3])
                self.record_temp["width"]=int(temp[4])
                self.record_temp["height"]=int(temp[5])
                self.record_temp["mines"]=int(temp[6])
                self.record_temp["date"]=temp[8]
                flag=temp[9].split(' ')
                m=temp[7].split(',')
                mines_map=[]
                for i in m:
                    mines_map.append(list(map(int,i.split(' '))))
                self.record_temp["mines_map"]=mines_map
                self.record_temp["gaming"]=[]
                g={}
                g["time"]=int(temp[1])
                g["pos"]=list(map(float,temp[2].split(" ")))
                if int(flag[0])!=-1 and int(flag[1])!=-1:
                    g["flag"]=[int(flag[0]),int(flag[1])]
                g["sound"]=list(map(int,temp[10].split(' ')))
                g["first_grid"]=list(map(int,temp[11].split(' ')))
                self.record_temp["gaming"].append(g)
            else:
                g={}
                g["time"]=int(temp[1])
                g["pos"]=list(map(float,temp[2].split(" ")))
                if "Map" in temp[0]:
                    m=temp[3].split(',')
                    explore_map=[]
                    for i in m:
                        explore_map.append(list(map(int,i.split(' '))))
                    g["mines_explore"]=explore_map
                if "Sound" in temp[0]:
                    s=temp[4].split(' ')
                    s=list(map(int,s))
                    g["sound"]=s
                if "Lose" in temp[0] or "Win" in temp[0]:
                    m=temp[5].split(',')
                    final_map=[]
                    for i in m:
                        final_map.append(list(map(int,i.split(' '))))
                    g["final_map"]=final_map
                if "Flag" in temp[0]:
                    s=temp[6].split(' ')
                    s=list(map(int,s))
                    g["flag"]=s
                self.record_temp["gaming"].append(g)
                
                if "Lose" in temp[0] or "Win" in temp[0]:
                    if "Lose" in temp[0]:
                        self.record_temp["result"]="Lose"
                    else:
                        self.record_temp["result"]="Win"
                    check=False
                    for i in self.record:
                        if i[0]=="Last Game":
                            i[1]=self.record_temp
                            check=True
                    if not check:
                        self.record.append(["Last Game",self.record_temp])
        elif f[0] == "record_info":
            self.record_info=f[1]
                
        
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
def blit_dialog(screen,font,text_list,color,pos,size=[],center=False,frame_width=5,frame_color=(255,255,255),background_color=(0,0,0),width_blank=10,height_blank=5):
    #顯示對話框
    #screen:畫布
    #text_list:文字列表
    #font:字型
    #color:顏色
    #pos:位置
    #size:對話框大小
    #center:是否置中
    #frame_width:邊框寬度
    #frame_color:邊框顏色
    #background_color:背景顏色
    w = len(max(text_list,key=len))*font.size("  ")[0]+2*frame_width+2*width_blank
    h = len(text_list)*font.get_height()+2*frame_width+2*height_blank
    if size==[]:
        size=(w,h)
    img=pygame.Surface(size)
    img.fill(frame_color)
    img2=pygame.Surface((size[0]-2*frame_width,size[1]-2*frame_width))
    img2.fill(background_color)
    img3=pygame.Surface((w-2*frame_width,h-2*frame_width))
    img3.fill(background_color)
    for i,text in enumerate(text_list):
        blit_text(img3,font,text,color,(img3.get_width()//2,height_blank+(i+0.5)*font.get_height()),center=True)
    if(img3.get_width()>img2.get_width()):
        img3=pygame.transform.scale(img3,(img2.get_width(),img3.get_height()*img2.get_width()//img3.get_width()))
    blit_image(img2,img3,(img2.get_width()//2,img2.get_height()//2),center=True)
    img.blit(img2,(frame_width,frame_width))
    if center:
        rect=img.get_rect()
        rect.center=pos
        screen.blit(img,rect.topleft)
    else:
        screen.blit(img,pos)
def blit_image(screen,img,pos,center=False):
    #顯示圖片
    #screen:畫布
    #img:圖片
    #pos:位置
    #center:是否置中
    if center:
        rect=img.get_rect()
        rect.center=pos
        screen.blit(img,rect.topleft)
    else:
        screen.blit(img,pos)
def blit_rectangle(screen,color,pos,size,center=False):
    #顯示矩形
    #screen:畫布
    #color:顏色
    #pos:位置
    #size:大小
    #center:是否置中
    img=pygame.Surface(size)
    img.fill(color)
    if center:
        rect=img.get_rect()
        rect.center=pos
        screen.blit(img,rect.topleft)
    else:
        screen.blit(img,pos)
def load_sound(path, accept={"wav","mp3"}):
    #載入音效
    #accept:可接受的檔案類型
    #return:音效物件dict
    sounds={}
    for s in os.listdir(path):
        name, ext = os.path.splitext(s)
        if ext[1:].lower() in accept:
            sound=pygame.mixer.Sound(os.path.join(path, s))
            sounds[name]=sound
    return sounds