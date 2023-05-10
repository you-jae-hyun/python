import os
import pygame
pygame.init()

screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("팡팡건")

clock = pygame.time.Clock()

current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "images")

background = pygame.image.load(os.path.join(image_path, "background.png"))

stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]

character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height - stage_height

character_to_x = 0
character_speed = 5

weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]


ball_images = [
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),
    pygame.image.load(os.path.join(image_path, "balloon4.png"))]


ball_speed_y = [-18, -15, -12, -9] #index 0, 1, 2, 3,에 해당하는 값


#공들
balls = []

balls.append({
    "pos_x" : 50,   # 공의 x 좌표
    "pos_y" : 50,   # 공의 y 좌표
    "img_idx" : 0,  # 공의 이미지 인덱스/ 공의 크기별 몇번쨰 크기의 공인지
    "to_x" : 3,  # x축 이동방향, -3이면 왼쪽으로, 3이면 오른쪽으로
    "to_y" : -6,     # y축 이동방향
    "init_spd_y" : ball_speed_y[0]}) # 공마다의 y축 최초 속도/ 위에서 최초 속도 정의함.첫번째 큰공이니 [0]번째 것으로 입력

# 사라질 무기, 공 정보 저장 변수
weapon_to_remove = -1
ball_to_remove = -1


# Font 정의'
game_font = pygame.font.Font(None, 40)

##############################################################

#게임플레이 시작
total_time = 100
start_ticks = pygame.time.get_ticks()  #시간 정의

game_result = "Game Over"

#무기는 한번에 여러발 발사 가능/ 리스트를 만든다
weapons = []

#무기 이동 속도
weapon_speed = 10

running = True
while running:
    dt = clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width/2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])
        
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    character_x_pos += character_to_x

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width
    
    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons]
    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons if w[1]>0]

    # 공 위치 정의
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]    #balls의 pos_x 값을 ball_pos_x 변수에 넣는다
        ball_pos_y = ball_val["pos_y"]    #balls의 pos_y 값을 ball_pos_y 변수에 넣는다
        ball_img_idx = ball_val["img_idx"]         #balls의 img_idx 값을 ball_img_idx 변수에 넣는다


        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        #가로벽에 닿았을때 공 이동 위치 변경 (팅겨나오는 효과)
        if ball_pos_x <= 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1

         #세로위치
        if ball_pos_y >= screen_height - stage_height - ball_height: #공이 스테이지에 닿은경우
            ball_val["to_y"] = ball_val["init_spd_y"]
        else: #그외 모든 경우에는 속도를 증가
            ball_val["to_y"] += 0.5


        # to_x, to_y의 값을 실제 좌표 값에 적용합니다.
        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

################################################################

# 4. 충돌처리

    #캐릭터 rect정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]
        #공 rect 정보 업데이트
        ball_rect = ball_images[ball_img_idx]. get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y
        #공과 캐릭터 충돌 처리
        if character_rect.colliderect(ball_rect):
            running = False
            break

        #공과 무기들 충돌 처리
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0] #무기의 x좌표
            weapon_pos_y = weapon_val[1] #무기의 y좌표


            #무기 크기 정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x #weapon_rect.left에 무기의 x좌표 업데이트
            weapon_rect.top = weapon_pos_y #weapon_rect.top에 무기의 y좌표 업데이트

        
            #충돌체크
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx #해당무기 없애기 위한 값 설정
                ball_to_remove = ball_idx #해당 공 없애기 위한 값 설정
                

                #가장 작은 공이 아니라면 다음단계의 공으로 나누기
                if ball_img_idx < 3:
                    #현재 공크기 정보를 가지고 옴
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    #나눠진 공 정보
                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    #왼쪽으로 튕겨나가는 작은공
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2),  #공의 x 좌표
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2),  #공의 y 좌표
                        "img_idx" : ball_img_idx + 1 ,  #공의 이미지 인덱스
                        "to_x" : -3, # x축 이동방향, 오른쪽으로 이동하므로 3 
                        "to_y" : -6,      # y축 이동방향
                        "init_spd_y" : ball_speed_y[ball_img_idx + 1]})  # y 최초 속도

                    #오른쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2),  #공의 x 좌표
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2),  #공의 y 좌표
                        "img_idx" : ball_img_idx + 1 ,  #공의 이미지 인덱스
                        "to_x" : 3, # x축 이동방향, 오른쪽으로 이동하므로 3 
                        "to_y" : -6,      # y축 이동방향
                        "init_spd_y" : ball_speed_y[ball_img_idx + 1]})  # y 최초 속도
    

                break
        else: #계속 게임을 진행
            continue #안쪽 for문 조건이 맞지 않으면 continue, 바깥 for문 수행
        break
    #충돌된 공 또는 무기 없애기
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1
    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1    
  
 #########################################################
  
    #모든 공을 없앤 경우 게임종료
    if len(balls) == 0:    #len():갯수 반환
        game_result = "Mission Complete"
        running = False

    screen.blit(background, (0, 0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))


    #경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 #ms => s
    timer = game_font.render("time : {}".format(int(total_time - elapsed_time)), True, (255, 255, 255))
    screen.blit(timer, (10, 10))

    #시간 초과 했다면
    if total_time - elapsed_time <= 0:
        game_result = "Time Over"
        running = False
    


    pygame.display.update()     #한번 더 화면 업데이트를 하도록 추가 합니다.


#게임 오버 메시지
msg = game_font.render(game_result, True, (255, 255, 0))  #노란색
msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height /2)))   #화면중앙 좌표
screen.blit(msg, msg_rect)

    
pygame.display.update()
#2초 대기
pygame.time.delay(2000)
#pygame 종료
pygame.quit()