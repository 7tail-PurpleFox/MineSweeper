#!/usr/bin/env python3
import pygame, os
from source import tool, setup
from source.state import main_menu, game_place, game_menu, record, record_info

def main():
    state_dict = { 'main_menu' : main_menu.MainMenu(),
                   'game_place' : game_place.Game_Place(), 
                   'game_menu' : game_menu.Game_Menu(),
                   'record' : record.Record(),
                   'record_info' : record_info.Record_Info()}
    game = tool.Game(state_dict, 'main_menu')
    game.run()

if __name__ == '__main__':
    if not os.path.exists('./source/record'):
        os.makedirs('./source/record')
    main()