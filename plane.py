import pygame
from pygame.sprite import Sprite

class Plane(Sprite):
    """初始化飞机及其位置参数"""
    def __init__(self, ai_settings, screen):
        self.screen = screen
        self.ai_settings = ai_settings
        super(Plane, self).__init__()

        
        #加载飞机图像并获取其外形矩形
        self.image = pygame.image.load('images/plane00.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #将飞机放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #在飞机属性中存储浮点值
        self.center = float(self.rect.centerx)
                
        #移动标志
        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.myplane_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.myplane_speed_factor

        #根据self.centerx更新rect对象
        self.rect.centerx = self.center

    def blitme(self):
        """在指定位置绘制飞机"""
        self.screen.blit(self.image, self.rect)

    def center_plane(self):
        self.center = self.screen_rect.centerx