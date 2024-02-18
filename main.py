import pygame 
import random
import sys
from agent import QLearningAgent
import matplotlib.pyplot as plt

agent = QLearningAgent(21, 4)
scores = []

try:
    agent.load_model("model.pkl")
    print("Checkpoint loaded")
except:
    print("New")
    pass

for game in range(100000):

    pygame.init()


    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Basic Game Loop")

    clock = pygame.time.Clock()


    direction = "right"
    rect_color = (0, 128, 255) 
    rect_pos = [200, 150]   
    snake_pos = []
    rect_size = (10, 10)

    fruit_pos = [random.randint(0,width-1),random.randint(0,height-1)]
    fruit_color = (255, 0, 0) 

    def snake():
        for pos in snake_pos:
            pygame.draw.rect(screen, rect_color, (pos[0], pos[1], rect_size[0], rect_size[1]))

    def fruit():
        pygame.draw.rect(screen, fruit_color, (fruit_pos[0], fruit_pos[1], rect_size[0], rect_size[1]))

    def collision():
        if rect_pos == fruit_pos:
            fruit_pos = [random.randint(0,width-1),random.randint(0,height-1)]

    def performs_action(action):
        if action == 0:
            direction = "left"
        elif action == 1:
            direction = "right"
        elif action == 2:
            direction = "up"
        elif action == 3:
            direction = "down"
        return direction

    def get_state(snake_pos, fruit_pos, direction, width, height):
        head_x, head_y = snake_pos[-1]
        fruit_horizontal = ""
        fruit_vertical = ""

        if fruit_pos[0] < head_x:
            fruit_horizontal = "left"
        elif fruit_pos[0] > head_x:
            fruit_horizontal = "right"

        if fruit_pos[1] < head_y:
            fruit_vertical = "up"
        elif fruit_pos[1] > head_y:
            fruit_vertical = "down"



        danger_up = head_y <= 0 or (head_x, head_y - 20) in snake_pos 
        danger_down = head_y >= height - 20 or (head_x, head_y + 20) in snake_pos 
        danger_left = head_x <= 0 or (head_x - 20, head_y) in snake_pos 
        danger_right = head_x >= width - 20 or (head_x + 20, head_y) in snake_pos 

        distance = 20  


        self_up = False
        self_down = False
        self_left = False
        self_right = False

        if direction == 'up':
            self_up = any(segment[0] == head_x and segment[1] < head_y for segment in snake_pos if head_y - segment[1] <= distance)
        elif direction == 'down':
            self_down = any(segment[0] == head_x and segment[1] > head_y for segment in snake_pos if segment[1] - head_y <= distance)
        elif direction == 'left':
            self_left = any(segment[1] == head_y and segment[0] < head_x for segment in snake_pos if head_x - segment[0] <= distance)
        elif direction == 'right':
            self_right = any(segment[1] == head_y and segment[0] > head_x for segment in snake_pos if segment[0] - head_x <= distance)



        if fruit_horizontal == "left":
            if fruit_vertical == "up":
                state = "Food above and left"
                index = 0
            elif fruit_vertical == "down":
                state = "Food below and left"
                index = 1
            else:
                state = "Food left"
                index = 2
            
        elif fruit_horizontal == "right":
            if fruit_vertical == "up":
                state = "Food above and right"
                index = 3
            elif fruit_vertical == "down":
                state = "Food below and right"
                index = 4
            else:
                state = "Food right"
                index = 5
        else:
            if fruit_vertical == "up":
                state = "Food above and Smae H"
                index = 6
            elif fruit_vertical == "down":
                state = "Food below and Same H"
                index = 7
            else:
                state = "Same V and Same H"
                index = 8

        if danger_up and danger_left:
            state = "Danger up and left"
            index = 9
        elif danger_up and danger_right:
            state = "Danger up and right"
            index = 10
        elif danger_down and danger_left:
            state = "Danger down and left"
            index = 11
        elif danger_down and danger_right:
            state = "Danger down and right"
            index = 12
        elif danger_up:
            state = "Danger up"
            index = 13
        elif danger_down:
            state = "Danger down"
            index = 14
        elif danger_left:
            state = "Danger left"
            index = 15
        elif danger_right:
            state = "Danger right"
            index = 16

        elif self_down:
            state = "Danger self down"
            index = 17
        elif self_up:
            state = "Danger self up"
            index = 18
        elif self_left:
            state = "Danger self left"
            index = 19
        elif self_right:
            state = "Danger self right"
            index = 20
        else:
            pass
       
        return state,index
  


    font = pygame.font.Font(None, 36) 


    count = 0
    score = 0
    running = True
    reward = 0
    while running:
  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = "left"
                elif event.key == pygame.K_RIGHT:
                    direction = "right"
                elif event.key == pygame.K_UP:
                    direction = "up"
                elif event.key == pygame.K_DOWN:
                    direction = "down"

  
        screen.fill((255, 255, 255))  
        snake_pos.append(rect_pos.copy())
        
        done = False
        for pos in snake_pos:
            pygame.draw.rect(screen, rect_color, (pos[0], pos[1], rect_size[0], rect_size[1]))


        fruit()
        if (
            rect_pos[0] < fruit_pos[0] + rect_size[0] and
            rect_pos[0] + rect_size[0] > fruit_pos[0] and
            rect_pos[1] < fruit_pos[1] + rect_size[1] and
            rect_pos[1] + rect_size[1] > fruit_pos[1]
            ): 
            score+=1
            reward = 1
            fruit_pos = [random.randint(0,width-1),random.randint(0,height-1)]
        else:
            if count >=3:
                snake_pos.pop(0)

        score_text = font.render("Score: {}".format(score), True, (0, 0, 0)) 
        screen.blit(score_text, (10, 10))



        game_text = font.render("Epoch: {}".format(game), True, (0, 0, 0))


        text_width, text_height = game_text.get_size()
        text_x = (width - text_width) // 2  
        text_y = 10  
        screen.blit(game_text, (text_x, text_y))


        pygame.display.flip()

        clock.tick(60) 
        state = get_state(snake_pos, fruit_pos, direction, width, height)
        action = agent.choose_action(state[1])
        previous = direction
        direction = performs_action(action)


        if direction == "right":
            if previous == "left":
                rect_pos[0]-=10
            else:
                rect_pos[0]+=10
        elif direction == "left":
            if previous == "right":
                rect_pos[0]+=10
            else:
                rect_pos[0]-=10
        elif direction == "up":
            if previous == "down":
                rect_pos[1]+=10
            else:
                rect_pos[1]-=10
        elif direction == "down":
            if previous == "up":
                rect_pos[1]-=10
            else:
                rect_pos[1]+=10
        
        if count >=1:

            if not (0 <= rect_pos[0] < width and 0 <= rect_pos[1] < height):
                reward = -1
                done = True
                scores.append(score)
                new_state = get_state(snake_pos, fruit_pos, direction, width, height)
                agent.learn(state[1],action,reward,new_state[1],done)
                break
        
            if any(segment == rect_pos for segment in snake_pos[1:]):
                reward = -1
                done = True
                scores.append(score)
                new_state = get_state(snake_pos, fruit_pos, direction, width, height)
                agent.learn(state[1],action,reward,new_state[1],done)
                break
            

        new_state = get_state(snake_pos, fruit_pos, direction, width, height)
        agent.learn(state[1],action,reward,new_state[1],done)
        count+=1
agent.save_model("model.pkl")

pygame.quit()
sys.exit()
