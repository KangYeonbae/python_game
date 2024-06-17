import pygame
import random

#####################################################################################
# 기본 초기화부분 반드시 해야하는것들
pygame.init()
pygame.mixer.init()

# 화면 크기 설정
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("dusqo Game") #게임이름

# FPS
clock = pygame.time.Clock()

#####################################################################################
# 1. 사용자 게임 초기화 (배경화면, 캐릭터, 좌표, 폰트등)

# 배경화면 설정
background = pygame.image.load("D:/KYB/Project/2_WepProject/3_React/React_clone_test/kyb_study/server/python/game/back.jpg")

#음악넣기
pygame.mixer.music.load("D:/KYB/Project/2_WepProject/3_React/React_clone_test/kyb_study/server/python/game/stranger-things-124008.mp3")
pygame.mixer.music.set_volume(0.5) #음악 볼륨
pygame.mixer.music.play(-1, start=3.0)  #음악 무한반복

# 캐릭터 넣기
character = pygame.image.load("D:/KYB/Project/2_WepProject/3_React/React_clone_test/kyb_study/server/python/game/ㅂㄹ.jpg")
# character = pygame.image.load("D:/KYB/Project/2_WepProject/3_React/React_clone_test/kyb_study/server/python/game/그림3.png")
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height

# 이동할 좌표
to_x = 0
to_y = 0

# 캐릭터 스피드
character_speed = 0.6

# 적캐릭터
enemy_image = pygame.image.load("D:/KYB/Project/2_WepProject/3_React/React_clone_test/kyb_study/server/python/game/그림5.png")
# enemy_image = pygame.image.load("D:/KYB/Project/2_WepProject/3_React/React_clone_test/kyb_study/server/python/game/그림5.png")
enemy_size = enemy_image.get_rect().size
enemy_width = enemy_size[0]
enemy_height = enemy_size[1]

# 적(엄) 여러 개 생성
number_of_enemies = 1
number_of_enemies += 1
enemies = []

for i in range(number_of_enemies):
    enemy_x_pos = random.randint(0, screen_width - enemy_width)
    enemy_y_pos = 0 - (i * 300)  # 적들이 시간차를 두고 나타나도록 초기 위치 조정
    enemy_speed = random.randint(1, 1)  # 속도를 더 낮은 값으로 조정
    enemies.append([enemy_x_pos, enemy_y_pos, enemy_speed])

# 글자 넣기
# 폰트 정의
game_font = pygame.font.Font(None, 40) # 폰트 객체 생성 (폰트, 크기)

# 총 시간
total_time = 10

# 시간 계산
start_ticks = pygame.time.get_ticks()

level = 1
# 레벨 표시 함수
def display_level(level):
    level_text = game_font.render(f"Level: {level}", True, (255, 255, 255))  # 레벨 텍스트 렌더링
    screen.blit(level_text, (10, 50))  # 화면에 레벨 텍스트 표시 위치


# 이벤트 루프
running = True
while running:
    dt = clock.tick(60)  # 게임화면의 초당 프레임 수

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 창이 닫히는 이벤트가 발생하였는가?
            running = False

        if event.type == pygame.KEYDOWN:  # 키가 눌러졌는지 확인
            if event.key == pygame.K_LEFT:
                to_x -= character_speed
            if event.key == pygame.K_RIGHT:
                to_x += character_speed
            if event.key == pygame.K_UP:
                to_y -= character_speed
            if event.key == pygame.K_DOWN:
                to_y += character_speed

        if event.type == pygame.KEYUP:  # 방향키를 떼면 멈춤
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                to_y = 0

    # 3. 캐릭터 위치 정의
    character_x_pos += to_x * dt
    character_y_pos += to_y * dt

    # 화면 경계값 처리
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    if character_y_pos < 0:
        character_y_pos = 0
    elif character_y_pos > screen_height - character_height:
        character_y_pos = screen_height - character_height

    # 적(엄) 떨어지기
    for enemy in enemies:
        enemy[1] += enemy[2] * dt  # 적의 Y 좌표를 속도만큼 이동
        if enemy[1] > screen_height:
            enemy[1] = 0 - enemy_height
            enemy[0] = random.randint(0, screen_width - enemy_width)
            enemy[2] = random.randint(1, 1)  # 적 속도 재설정


    # 충돌 처리
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    # 각 적(엄)에 대해 충돌 검사
    for idx, enemy in enumerate(enemies):
        enemy_rect = enemy_image.get_rect()
        enemy_rect.left = enemy[0]
        enemy_rect.top = enemy[1]

        if character_rect.colliderect(enemy_rect):
            print('재우님이 죽었어요')
            running = False


    # 4. 화면에 그리기
    screen.blit(background, (0, 0))

    for enemy in enemies:
        screen.blit(enemy_image, (enemy[0], enemy[1]))

    screen.blit(character, (character_x_pos, character_y_pos))

    display_level(level)

    # 타이머 넣기
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render(str(int(total_time - elapsed_time)), True, (255, 255, 255))
    screen.blit(timer, (10, 10))

    # 시간이 0 이하이면 게임 종료
    if total_time - elapsed_time <= 0:
        print('레벨업!')
        start_ticks = pygame.time.get_ticks()
        level += 1

    pygame.display.update()  # 게임화면 다시 그리기

# 잠시 대기
pygame.time.delay(1000)
# pygame 종료
pygame.quit()
