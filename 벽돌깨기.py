# coding=utf-8
import pygame
import random
import math


#  막대 및 벽돌 클래스
class Block(pygame.sprite.Sprite):
    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img.convert_alpha()
        self.image2 = None
        self.image3 = None
        self.rect = img.get_rect()
        self.life = 3

    def add_image(self, img2, img3):
        self.image2 = img2
        self.image3 = img3


# 농구공 클래스
class Ball(pygame.sprite.Sprite):
    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img.convert_alpha()
        self.rect = img.get_rect()
        self.mask = pygame.mask.from_surface(img)
        self.velx = 0.0
        self.vely = 0.0
        # self.radius = 20
        # self.speed = random.randint(10, 16)


pygame.init()
screen = pygame.display.set_mode((1200, 768))

# 벽돌
brick = [pygame.image.load("brick/brick1.png").convert_alpha(),
         pygame.image.load("brick/brick2.png").convert_alpha(),
         pygame.image.load("brick/brick3.png").convert_alpha(),
         pygame.image.load("brick/brick4.png").convert_alpha(),
         pygame.image.load("brick/brick5.png").convert_alpha(),
         pygame.image.load("brick/brick6.png").convert_alpha(),
         pygame.image.load("brick/brick7.png").convert_alpha(),
         pygame.image.load("brick/brick8.png").convert_alpha()
         ]

# 금간 벽돌
broken_brick1 = [pygame.image.load("broken_brick/brick1.png").convert_alpha(),
                 pygame.image.load("broken_brick/brick2.png").convert_alpha(),
                 pygame.image.load("broken_brick/brick3.png").convert_alpha(),
                 pygame.image.load("broken_brick/brick4.png").convert_alpha(),
                 pygame.image.load("broken_brick/brick5.png").convert_alpha(),
                 pygame.image.load("broken_brick/brick6.png").convert_alpha(),
                 pygame.image.load("broken_brick/brick7.png").convert_alpha(),
                 pygame.image.load("broken_brick/brick8.png").convert_alpha()
                 ]

#  금간 벽돌 2
broken_brick2 = [pygame.image.load("broken_brick2/brick1.png").convert_alpha(),
                 pygame.image.load("broken_brick2/brick2.png").convert_alpha(),
                 pygame.image.load("broken_brick2/brick3.png").convert_alpha(),
                 pygame.image.load("broken_brick2/brick4.png").convert_alpha(),
                 pygame.image.load("broken_brick2/brick5.png").convert_alpha(),
                 pygame.image.load("broken_brick2/brick6.png").convert_alpha(),
                 pygame.image.load("broken_brick2/brick7.png").convert_alpha(),
                 pygame.image.load("broken_brick2/brick8.png").convert_alpha()
                 ]

block_list = pygame.sprite.Group()

for j in range(0, 7):
    for i in range(0, 6):
        rand = random.randrange(8)
        block = Block(brick[rand])
        block.add_image(broken_brick1[rand], broken_brick2[rand])
        block.rect.x = i * 100 + 300
        block.rect.y = j * 40
        block.mask = pygame.mask.from_surface(block.image)
        block_list.add(block)

# 공
ball_list = pygame.sprite.Group()
ball_pic = pygame.image.load("picture/ball.png").convert_alpha()
last_ball = None
ball_angle = 0

# 화살표
trgimg = pygame.image.load("picture/삼각형.png")
trg = trgimg.get_rect()
trg.center = (screen.get_rect().centerx, 550)

# 막대
stick_image = pygame.image.load('picture/stick.png')
stick = Block(stick_image)
stick.mask = pygame.mask.from_surface(stick_image)

# 배경
BG_LEFT_IMAGE = pygame.image.load("picture/배경왼쪽.png")
BG_RIGHT_IMAGE = pygame.image.load("picture/배경오른쪽.png")

start = -1  # 화살표 애니메이션 / 공 애니메이션      체크
angle = 0.0  # 공의 각도
life = 5  # 던질 수 있는 공의 개수
check = 0  # 충돌 처리가 이상하게 된 횟수
game = -1  #  게임 승패 여부


done = True

while done:
    # 배경세팅
    screen.fill((0, 0, 0))
    screen.blit(BG_LEFT_IMAGE, (0, 0))  # 왼쪽 배경
    screen.blit(BG_RIGHT_IMAGE, (950, 0))  # 오른족 배경

    block_list.draw(screen)

    #  시작화면
    if start == -1:
        font = pygame.font.Font("Amiri/Amiri-Regular.ttf", 50)
        start_text = font.render("press R to start", True, (255, 255, 255))
        screen.blit(start_text, (500, 600))

    # 화살표 조준 및 공 각도 정하기
    elif start == 0:
        # 화살표
        position = pygame.mouse.get_pos()
        angle = math.atan2(position[1] - 550, position[0] - screen.get_rect().centerx)
        trgrrot = pygame.transform.rotate(trgimg, 360 - angle * 57.29)
        yplus = 150 * math.sin(angle)
        xplus = 150 * math.cos(angle)
        trg.center = (screen.get_rect().centerx + xplus, 550 + yplus)
        screen.blit(trgrrot, trg)

    #  공 이동
    elif start == 1:
        position = pygame.mouse.get_pos()
        stick.rect.center = (position[0], 738)
        for ball in ball_list:
            ball.rect.centerx += ball.velx
            ball.rect.centery += ball.vely
            screen.blit(ball.image, ball.rect)
        screen.blit(stick_image, stick.rect)

    ball_angle += 5
    ballrot = pygame.transform.rotate(ball_pic, ball_angle)
    plusx = (ballrot.get_rect().width - 40) / 2
    plusy = (ballrot.get_rect().height - 40) / 2

    # 공위치 조정
    for ball in ball_list:
        screen.blit(ballrot, (ball.rect.left - plusx, ball.rect.top - plusy))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN and start == 0:  # 공이 조준중이며 클릭했을때

            # 공의 이동방향 정하기
            last_ball.velx = math.cos(angle) * 15
            last_ball.vely = math.sin(angle) * 15

            start = 1  # 공 움직이는 애니메이션으로 변경
        elif event.type == pygame.KEYDOWN and start != 0 and life != 0:  # 공이 조준중이 아니며 공을 쏠 수 있는 횟수가 남아있고
            if event.key == pygame.K_r:  # r키를 눌렀을때
                life -= 1

                #  공 객체 생성
                ball = Ball(ball_pic)
                ball.rect.center = (screen.get_rect().centerx, 550)

                ball.radius = 20  # 공의 반지름
                ball_list.add(ball)

                last_ball = ball  # 마지막 공의 주소 저장
                start = 0  # 공을 조준하는 애니메이션으로 변경

    # 공의 쏠 수 있는 횟수 출력
    font = pygame.font.Font("Amiri/Amiri-Regular.ttf", 100)
    if life == 0:  # 공을 쏠 수 있는 횟수가 남지 않았을때 x를 출력
        life_text = font.render("X", True, (255, 255, 255))
    else:
        life_text = font.render(str(life), True, (255, 255, 255))
    screen.blit(life_text, (75, 510))

    # 플레이 한 시간 출력
    font = pygame.font.Font("Amiri/Amiri-Regular.ttf", 80)
    timetext = font.render(str((pygame.time.get_ticks()) / 60000) + ":"
                           + str((pygame.time.get_ticks()) / 1000 % 60).zfill(2), True, (255, 255, 255))
    screen.blit(timetext, (1020, 520))

    pygame.display.flip()

    # 벽돌 충돌 체크 및 공의 이동방향 처리
    for block in block_list:
        for ball in ball_list:
            if pygame.sprite.collide_mask(ball, block):
                block.life -= 1  # 공과 충돌시 벽돌 수명 -1

                if block.rect.top + abs(ball.vely) >= ball.rect.bottom >= block.rect.top:
                    ball.vely *= -1
                elif block.rect.left + abs(ball.velx) >= ball.rect.right >= block.rect.left:
                    ball.velx *= -1
                elif block.rect.bottom - abs(ball.vely) <= ball.rect.top <= block.rect.bottom:
                    ball.vely *= -1
                elif block.rect.right - abs(ball.velx) <= ball.rect.left <= block.rect.right:
                    ball.velx *= -1
                else:
                    ball.velx *= -1
                    ball.vely *= -1
                    check += 1

                if block.life == 2:
                    block.image = block.image2
                elif block.life == 1:
                    block.image = block.image3
                elif block.life == 0:
                    block_list.remove(block)

    #  공이 화면 끝과 충돌 했을 때 및 공의 이동방향 처리
    for ball in ball_list:
        if ball.rect.bottom >= 768:  # 스틱으로 공을 받지 못해 공이 밑으로 나갔을 경우
            ball_list.remove(ball)  # 공삭제
            if life == 0 and len(ball_list) == 0:  # 공을 던질 수 있는 횟수가 0 이며 화면에 있는 공들이 죽었을 때
                done = False
        elif ball.rect.top <= 0:
            ball.rect.centery += 3  # 공이 벽 안으로 들어가는 오류 방지
            ball.vely *= -1
        elif ball.rect.left <= 250:
            ball.rect.centerx += 3  # 공이 벽 안으로 들어가는 오류 방지
            ball.velx *= -1
        elif ball.rect.right >= 950:
            ball.rect.centerx -= 3  # 공이 벽 안으로 들어가는 오류 방지
            ball.velx *= -1

    #  공이 막대와 충돌 했을 때 및 공의 이동방향 처리
    for ball in ball_list:
        if pygame.sprite.collide_mask(ball, stick):
            barx = ball.rect.centerx
            bx = barx - stick.rect.centerx

            if stick.rect.centerx < barx:
                angle = math.radians(-100 + bx * 0.7)
            elif stick.rect.centerx > barx:
                angle = math.radians(-80 + bx * 0.7)

            ball.velx = math.cos(angle) * 15
            ball.vely = math.sin(angle) * 15

    if len(block_list) == 0:
        done = False
        game = 1


while 1:
    screen.fill((0, 0, 0))
    font = pygame.font.Font("Amiri/Amiri-Regular.ttf", 100)
    if game == 1:
        gametext = font.render("YOU WIN", True, (255, 255, 255))
    else:
        gametext = font.render("GAME OVER", True, (255, 255, 255))

    screen.blit(gametext, (500, 500))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()

