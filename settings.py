class Settings():
    """存储《外星人入侵》的所有设置选项的类"""

    def __init__(self):
        """初始化游戏的设置选项"""
        self.screen_width = 1040
        self.screen_height = 680
        self.bg_color = (255, 255, 102)

        #子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullet_allowed = 5

        #飞机设置
        self.plane_limit = 1

        #外星人设置
        self.fleet_drop_speed = 10
        #加快游戏速度
        self.speedup_scale = 3
        #外星人点数增加速度
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏而变化的设置"""
        self.myplane_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        #fleet_direction为1时表示向右
        self.fleet_direction = 1

        #记分
        self.alien_points = 50

    def increase_speed(self):
        """提高速度设置和外星人的点数"""
        self.myplane_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)