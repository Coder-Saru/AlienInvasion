import sys

import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from plane import Plane
import game_functions as gf
from bullet import Bullet
from alien import Alien
from button import Button

def run_game():
    
    #初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("外星人入侵")

    #创建play按钮
    play_button = Button(screen, "play")

    #创建一个用于存储游戏统计信息的实例，并创建得分板
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    #创建一架飞机
    myplane = Plane(ai_settings, screen)
    #创建一个子弹编组
    bullets = Group()
    #创建一个外星人编组
    aliens = Group()
    gf.create_fleet(ai_settings, screen, aliens ,myplane)


    #开始游戏的主循环
    while True:
        
        #监听键盘和鼠标事件
        gf.check_events(ai_settings, screen, myplane ,bullets, aliens, stats, sb, play_button)

        if stats.game_active:

            myplane.update()
            gf.update_bullet(ai_settings, stats, sb, screen, bullets, aliens, myplane)
            gf.update_aliens(aliens, bullets, ai_settings, screen, myplane, stats, sb)
                
        #让最近绘制的屏幕可见
        gf.update_screen(ai_settings, screen, myplane, bullets ,aliens, stats, sb, play_button)

run_game()
