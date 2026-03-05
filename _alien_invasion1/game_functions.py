import sys
import pygame
from ship import Ship

from alien_invasion1.settings import Settings


def check_events():
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                # 向右移动飞船
                Ship.rect.centerx += 1



def update_screen(ai_settings, screen, ship):
    """更新屏幕上的图像，并切换至新屏幕"""
    # 每次循环都重绘屏幕
    screen.fill(ai_settings.bg_color)
    ship.blitme()

    # 让最近绘制的屏幕可见
    pygame.display.flip()
