#!/usr/bin/env python3 # -*- coding: UTF-8 -*-
import pygame, os, json
from source import tool, setup, constant as C
from source.state import main_menu, game_place, game_menu, options, record, record_info, record_game_place, opening, turtorial

def main():
    state_dict = { 'main_menu' : main_menu.MainMenu(),
                   'game_place' : game_place.Game_Place(), 
                   'game_menu' : game_menu.Game_Menu(),
                   'record' : record.Record(),
                   'record_info' : record_info.Record_Info(),
                   'record_game_place' : record_game_place.Record_Game_Place(),
                   'opening' : opening.Opening(),
                   'options' : options.Options(),
                   'tutorial' : turtorial.Tutorial()}
    if os.path.exists("source/game_setting.json"):
        with open("source/game_setting.json","r") as f:
            setting = json.load(f)
            if setting["opening"]:
                game = tool.Game(state_dict, 'opening')
            else:
                game = tool.Game(state_dict, 'main_menu')
            pygame.mixer.music.load(setup.musics[setting["music_category"]-1])
            pygame.mixer.music.set_volume(setting["music_scale"]/10)
    else:
        game = tool.Game(state_dict, 'main_menu')
    pygame.mixer.music.play(-1)
    game.run()

if __name__ == '__main__':
    if not os.path.exists(C.RECORD_PATH):
        os.makedirs(C.RECORD_PATH)
    main()