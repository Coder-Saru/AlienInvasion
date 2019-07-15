import sys
from time import sleep

import pygame
from bullet import Bullet
from alien import Alien


def myplane_hit(aliens, bullets, ai_settings, screen, myplane, stats, sb):
    """响应外星人撞到飞机或外星人到达了底端"""
    if stats.planes_left > 0:
        #将planes_left减1
        stats.planes_left -= 1
        #更新剩余飞机数量
        sb.prep_planes()

        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        #重新创建一群外星人，并将飞机放回底部中央
        create_fleet(ai_settings, screen, aliens ,myplane)
        myplane.center_plane()

        #暂停时间
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_down_events(event, bullets ,ai_settings, screen, myplane):
    """响应按下键盘"""
    if event.key == pygame.K_RIGHT:
        #向右边移动飞机
        myplane.moving_right = True
    elif event.key == pygame.K_LEFT:
        #向右边移动飞机
        myplane.moving_left = True

    elif event.key == pygame.K_SPACE:
        fire_bullet(bullets ,ai_settings, screen, myplane)

    elif event.key == pygame.K_q:
        pygame.quit()
        sys.exit()
    

def fire_bullet(bullets ,ai_settings, screen, myplane):
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, myplane)
        bullets.add(new_bullet)       
        
def check_up_events(event, myplane):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        myplane.moving_right = False
    elif event.key == pygame.K_LEFT:
        myplane.moving_left = False


def check_events(ai_settings, screen, myplane ,bullets, aliens, stats, sb, play_button):
    """响应键盘或鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_down_events(event, bullets ,ai_settings, screen, myplane)
        elif event.type == pygame.KEYUP:
            check_up_events(event, myplane)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, stats, sb, play_button, mouse_x, mouse_y, aliens, bullets)


def check_play_button(ai_settings, stats, sb, play_button, mouse_x, mouse_y, aliens, bullets):
    """单击按钮后开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #重置飞机、外星人、子弹速度
        ai_settings.initialize_dynamic_settings()
        #鼠标可见
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True

        #重置计分板
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_planes()

        #清空外星人和子弹列表
        aliens.empty()
        bullets.empty()


def get_number_aliens_x(ai_settings, alien_width):
    """计算每行外星人数"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, alien_height, myplane_height):
    """计算屏幕可以容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height -
                         myplane_height - 3 * alien_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    alien.x = alien_width + 2 * alien_number * alien_width
    alien.y = alien_height + 2 * row_number * alien_height
    alien.rect.x = alien.x
    alien.rect.y = alien.y
    aliens.add(alien)

def create_fleet(ai_settings, screen, aliens ,myplane):
    """创建一群外星人"""
    #创建一个外星人，并计算一行可以容纳多少外星人
    #外星人的间距为外星人的宽度
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, alien.rect.height,
                                  myplane.rect.height)
    
    #创建多行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)
        

def update_bullet(ai_settings, stats, sb, screen, bullets, aliens, myplane):
    """更新子弹的位置，并删除已经消失的子弹"""
    #更新子弹的位置
    bullets.update()
    #删除已经消失的子弹
    for bullet in bullets.copy():
            if bullet.rect.top <= 0:
                bullets.remove(bullet)
    check_bullet_alien_collisions(bullets, aliens, ai_settings, stats, sb, screen, myplane)

def check_aliens_bottom(aliens, bullets, ai_settings, screen, myplane, stats, sb):
    """检查外星人是否到了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #像外星人撞到飞机那样处理
            myplane_hit(aliens, bullets, ai_settings, screen, myplane, stats, sb)
            break

def check_bullet_alien_collisions(bullets, aliens, ai_settings, stats, sb, screen, myplane):
    #检查是否有子弹射中了外星人，如果是，删除子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        #删除现有的子弹并重新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()
        #外星人被消灭干净，提升等级
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, aliens , myplane)
          
def update_screen(ai_settings, screen, myplane, bullets , aliens, stats, sb, play_button):
    """更新屏幕的图像并切换到新图像"""
    
    #每次循环都重新绘制屏幕
    screen.fill(ai_settings.bg_color)
    myplane.blitme()
    aliens.draw(screen)
    #重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    #显示得分
    sb.show_score()

    #如果游戏处于非活动状态，就绘制play按钮
    if not stats.game_active:
        play_button.draw_button()

    #让最近绘制的屏幕可见
    pygame.display.flip()
    

def check_fleet_edges(aliens, ai_settings):
    """外星人碰到边界采取措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break
        
def change_fleet_direction(ai_settings, aliens):
    """将所有外星人整体下移并改变方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def update_aliens(aliens, bullets, ai_settings, screen, myplane, stats, sb):
    """检查是否有外星人在屏幕边缘，并更新外星人的位置"""
    check_fleet_edges(aliens, ai_settings)
    aliens.update()

    #检测外星人和飞机之间的碰撞
    if pygame.sprite.spritecollideany(myplane, aliens):
        print("飞机被撞！！！")
        myplane_hit(aliens, bullets, ai_settings, screen, myplane, stats, sb)

        #检查外星人是否到了屏幕底端
    check_aliens_bottom(aliens, bullets, ai_settings, screen, myplane, stats, sb)

def check_high_score(stats, sb):
    """检查是否获得了最高分数"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
    #不管有没有破纪录，为了保持得分板和记录板的距离，记录板都要重绘
    sb.prep_high_score()