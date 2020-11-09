# coding=utf-8
import pygame
import os

#mendatory
pygame.init()

#screen size
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

#title
pygame.display.set_caption("Doraemon Black Magic")

#FPS for timer
clock = pygame.time.Clock()

current_path= os.path.dirname(__file__) #returns current file's address
image_path = os.path.join(current_path, "images")

#background
background = pygame.image.load(os.path.join(image_path, "back.jpg"))

# #stage
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]

#character
character = pygame.image.load(os.path.join(image_path, "sponge.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height - stage_height

#character_properties
character_to_x = 0
character_speed = 10

#weapon
weapon = pygame.image.load(os.path.join(image_path, "weapon.jpg"))
weapon_size = weapon.get_rect().size
#char mid of character's mid position
weapon_width = weapon_size[0]

weapons = []
weapon_speed = 10

#ball -> 4 sizes
ball_images = [
    pygame.image.load(os.path.join(image_path, "ball1.jpg")),
    pygame.image.load(os.path.join(image_path, "ball2.jpg")),
    pygame.image.load(os.path.join(image_path, "ball3.jpg")),
    pygame.image.load(os.path.join(image_path, "ball4.jpg"))
]

#initial speed of ball
ball_speed_y = [-18, -15, -11, -8] #index 0,1,2,3

#ball  information
balls = []

#default biggest ball
balls.append({
    "pos_x": 30,# ball's x position
    "pos_y": 50, #ball's y position
    "img_index": 0, #ball_images's coreesponding index
    "to_x": 3, #x-axis of ball, left -3 if left, right then + 3
    "to_y": -6, #y -axis of ball
    "init_speed_y":ball_speed_y[0]
})

#weapon and ball to remove
weapon_to_remove = -1
ball_to_remove = -1

#Font
game_font = pygame.font.Font(None, 40)
total_time = 100
#starting time mark
start_ticks = pygame.time.get_ticks()

#game over default message
game_result = "Game Over"
#event loop
running = True
character_to_x_LEFT=0
character_to_x_RIGHT=0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x_LEFT -= character_speed # 바뀐 부분
            elif event.key == pygame.K_RIGHT:
                character_to_x_RIGHT += character_speed # 바뀐 부분
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = character_x_pos + (character_width /2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

        # 수정3 : 키에서 손을 뗄 때 LEFT, RIGHT 를 각각 처리
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT: # 이 부분은 모두 다 바뀜
                character_to_x_LEFT = 0
            elif event.key == pygame.K_RIGHT:
                character_to_x_RIGHT = 0

    #change of position
    character_x_pos += character_to_x_LEFT + character_to_x_RIGHT

    #collision
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    #relocate weapon
    #y-axis need to chage its position
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons] #put it up

    #weapon that reached the floor
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]

    #ball position
    for ball_index, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_index = ball_val["img_index"]
        ball_size = ball_images[ball_img_index].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        #width out of screen(bounce)
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            #make it bounce, -3 -> 3
            ball_val["to_x"] =  ball_val["to_x"] * -1

        #vertival out of bound
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] =  ball_val["init_speed_y"]
        else:
            ball_val["to_y"] += 0.5

        #general cases
        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

    #collision
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    #ball position
    for ball_index, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_index = ball_val["img_index"]
        ball_rect = ball_images[ball_img_index].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y
        #character dies if the ball hits the character
        if character_rect.colliderect(ball_rect):
            running = False
            break

        #handle weapons and collision
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_x_pos = weapon_val[0]
            weapon_y_pos = weapon_val[1]

            #move rect i[date
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_x_pos
            weapon_rect.top = weapon_y_pos

            #now check collision
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx #remove weapon
                ball_to_remove = ball_index #remove the ball

                #if not hte smallest ball, make iot into smaller
                if ball_img_index < 3:
                    #cur ball size
                    ball_width = ball_rect[0]
                    ball_height = ball_rect[1]

                    #willbe this size of divided ball
                    small_ball_rect = ball_images[ball_img_index + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]
                    #to the left
                    balls.append({
                        "pos_x": ball_pos_x + (ball_width / 2) - (small_ball_width / 2),# ball's x position
                        "pos_y": ball_pos_y  + (ball_height / 2) - (small_ball_height / 2), #ball's y position
                        "img_index": ball_img_index + 1, #ball_images's coreesponding index
                        "to_x": -3, #x-axis of ball, left -3 if left, right then + 3
                        "to_y": -6, #y -axis of ball
                        "init_speed_y":ball_speed_y[0]
                    })

                    #to the right
                    balls.append({
                        "pos_x": ball_pos_x + (ball_width / 2) - (small_ball_width / 2),# ball's x position
                        "pos_y": ball_pos_y  + (ball_height / 2) - (small_ball_height / 2), #ball's y position
                        "img_index": ball_img_index + 1, #ball_images's coreesponding index
                        "to_x": 3, #x-axis of ball, left -3 if left, right then + 3
                        "to_y": -6, #y -axis of ball
                        "init_speed_y":ball_speed_y[0]
                    })

            break
        else:#comtinue the game, keep the looping
            continue
        break

    #remove collided balls
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    #if all the balls are gone then time over
    if len(balls) == 0:
        game_result = "Mission Complete"
        running = False

    #draw background. order matters
    screen.blit(background, (0,0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for index, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_index = val["img_index"]
        screen.blit(ball_images[ball_img_index], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))

    elpase_time = (pygame.time.get_ticks() - start_ticks) / 1000 # ms -> s
    remaining_time = total_time - elpase_time
    timer = game_font.render("Time: {}".format(int(remaining_time)), True, (255,99,71))
    screen.blit(timer, (10, 10))

    #over time
    if remaining_time <= 0:
        game_result = "Time Over"
        running = False

    pygame.display.update()#redraw the background required

msg = game_font.render(game_result, True, (255,69,0))
msg_rect = msg.get_rect(center=(screen_width /2, screen_height / 2))
screen.blit(msg, msg_rect)
pygame.display.update()

#delay the exit
pygame.time.delay(2000)
#exit our of the game
pygame.quit()