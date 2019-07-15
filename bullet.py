import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """一个对飞机发射的子弹进行管理的类"""
    def __init__(self, ai_settings, screen, myplane):
        """在飞船位置建立一个子弹对象"""
        super().__init__()
        self.screen = screen

        #在（0,0）处建立一颗矩形子弹，再设置正确的位置
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
                                ai_settings.bullet_height)
        self.rect.centerx = myplane.rect.centerx
        self.rect.top = myplane.rect.top
        #存储浮点数用于表示子弹位置
        self.y =float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor



    def update(self):
        #更新子弹位置
        self.y -= self.speed_factor
        self.rect.y = self.y
    

    def draw_bullet(self):
        #在屏幕上绘制子弹
        pygame.draw.rect(self.screen, self.color, self.rect)
