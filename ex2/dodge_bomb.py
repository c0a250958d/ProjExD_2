import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650   
DELTA = {
    pg.K_UP :(0, -5), 
    pg.K_DOWN :(0, +5),
    pg.K_LEFT :(-5, 0),
    pg.K_RIGHT :(+5, 0), 
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rect: pg.Rect) -> tuple[bool, bool]:

    yoko, tate = True, True
    if rect.left < 0 or WIDTH < rect.right:  # 横方向判定
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom:  # 縦方向判定
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None:
    
    black_screen = pg.Surface((WIDTH, HEIGHT))
    black_screen.fill((0, 0, 0))

    black_screen.set_alpha(200)

    font = pg.font.Font(None, 80)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    black_screen.blit(text, text_rect)

    kk_img = pg.image.load("fig/8.png")  
    
    kk_rect_l = kk_img.get_rect(center=(WIDTH // 2 - 200, HEIGHT // 2))
    black_screen.blit(kk_img, kk_rect_l)
    
    kk_rect_r = kk_img.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2))
    black_screen.blit(kk_img, kk_rect_r)

    screen.blit(black_screen, [0, 0])

    pg.display.update()
    time.sleep(5)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20 * r, 20 * r))
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        bb_img.set_colorkey((0, 0, 0)) 
        bb_imgs.append(bb_img)
        
    bb_accs = [a for a in range(1, 11)]
    return bb_imgs, bb_accs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    # 爆弾リストと加速度リストの生成
    bb_imgs, bb_accs = init_bb_imgs()
    bb_img = bb_imgs[0]  # 初期状態の爆弾
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)  # 横座標用の乱数
    bb_rct.centery = random.randint(0, HEIGHT)  # 縦座標用の乱数
    vx, vy = +5, +5  # 爆弾の初期速度

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        # こうかとんと爆弾の衝突判定
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for k, tpl in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += tpl[0] 
                sum_mv[1] += tpl[1]

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):  
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  
        screen.blit(kk_img, kk_rct)

        idx = min(tmr // 500, 9)
        avx = vx * bb_accs[idx]
        avy = vy * bb_accs[idx]
        bb_img = bb_imgs[idx]

        center = bb_rct.center
        bb_rct = bb_img.get_rect()
        bb_rct.center = center

        bb_rct.move_ip(avx, avy)  
        yoko, tate = check_bound(bb_rct)
        if not yoko:  
            vx *= -1
        if not tate: 
            vy *= -1
        screen.blit(bb_img, bb_rct)  

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()