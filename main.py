import pygame
from source import tool, setup
from source.state import main_menu, game_place, game_menu

def main():
    state_dict = { 'main_menu': main_menu.MainMenu(),
                   'game_place': game_place.Game_Place(), 
                   'game_menu': game_menu.Game_Menu() }
    game = tool.Game(state_dict, 'main_menu')
    game.run()

if __name__ == '__main__':
    main()