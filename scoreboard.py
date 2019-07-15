import pygame.font
from pygame.sprite import Group
from  plane import Plane

class Scoreboard():
    """显示得分信息的类"""

    def __init__(self, ai_settings, screen, stats):
        """初始化显示得分涉及的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        #显示得分信息时使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        #准备初始得分和最高得分、等级信息的图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_planes()

    def prep_score(self):
        """将得分转换为一副渲染的图像"""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render("score:" + score_str, True, self.text_color,
                                            self.ai_settings.bg_color)

        #将得分放在屏幕左上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """将最高得分渲染为图像"""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render("record:" + high_score_str, True,
                                                 self.text_color,self.ai_settings.bg_color)


        #将最高得分放在屏幕顶部中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.right = self.score_rect.left -20
        self.high_score_rect.top = self.score_rect.top


    def prep_level(self):
        """把等级信息渲染为图像"""
        self.level_image = self.font.render("level:"+str(self.stats.level), True, self.text_color,
                                            self.ai_settings.bg_color)

        #将等级信息放在屏幕左上角
        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = self.screen_rect.left +20
        self.level_rect.top = self.score_rect.top


    def prep_planes(self):
        """显示剩余多少飞机"""
        self.planes = Group()
        for plane_number in range(self.stats.planes_left):
            plane = Plane(self.ai_settings, self.screen)
            plane.rect.x = self.level_rect.right +20 + \
                           plane_number * plane.rect.width
            plane.rect.centery = self.score_rect.centery
            self.planes.add(plane)



    def show_score(self):
        """在屏幕上显示得分板"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)

        #绘制剩余飞船
        self.planes.draw(self.screen)