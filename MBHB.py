import pygame 
import random # ใช้สุ่มตัวเลข
import sys # ใช้สำหรับ sys.exit()

# เริ่มต้น pygame
pygame.init()
# ตั้งค่าหน้าจอแสดงผล
WIDTH = 1270 # ความยาว
HEIGHT = 720 # ความกว้าง
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MBHB")
icon = pygame.image.load('b_up.png')  # ใช้รูปเป็นไอคอน
pygame.display.set_icon(icon)  # ตั้งค่าไอคอน

# ตั้งค่าสี
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
PASTEL_BLUE = (220,237,244)
# โหลดเสียง
pygame.mixer.music.load("background-music.mp3")  # ใช้สำหรับเพลงพื้นหลัง
# ใช้ฟังก์ชันเพื่อเล่นเพลงพื้นหลังแบบลูป (-1 หมายถึงเล่นซ้ำไม่รู้จบ)
pygame.mixer.music.play(-1)
# กำหนดระดับเสียงเริ่มต้น (0.0 คือไม่มีเสียง, 1.0 คือเสียงสูงสุด)
music_volume = 0.5
# ตั้งระดับเสียงเริ่มต้น
pygame.mixer.music.set_volume(music_volume)
# โหลดรูปภาพตัวละครที่ 1
brain1_up = pygame.image.load('b_up.png')  
brain1_up = pygame.transform.scale(brain1_up, (80, 80)) 
brain1_down = pygame.image.load('b_down.png')
brain1_down = pygame.transform.scale(brain1_down, (80, 80)) 
brain1_left = pygame.image.load('b_left.png')
brain1_left = pygame.transform.scale(brain1_left, (80, 80)) 
brain1_right = pygame.image.load('b_right.png')
brain1_right = pygame.transform.scale(brain1_right, (80, 80))
brain1_dead = pygame.image.load('brain1_dead.png')
brain1_dead = pygame.transform.scale(brain1_dead, (80, 80))
# โหลดรูปภาพตัวละครที่ 2
brain2_up = pygame.image.load('b2_up.png')  
brain2_up = pygame.transform.scale(brain2_up, (80, 80)) 
brain2_down = pygame.image.load('b2_down.png')
brain2_down = pygame.transform.scale(brain2_down, (80, 80)) 
brain2_left = pygame.image.load('b2_left.png')
brain2_left = pygame.transform.scale(brain2_left, (80, 80)) 
brain2_right = pygame.image.load('b2_right.png')
brain2_right = pygame.transform.scale(brain2_right, (80, 80))
brain2_dead = pygame.image.load('brain2_dead.png')
brain2_dead = pygame.transform.scale(brain2_dead, (80, 80))
# โหลดภาพพื้นหลัง
bg_math = pygame.image.load('math_bg.png')
bg_math = pygame.transform.scale(bg_math, (WIDTH, HEIGHT))

# โหลดรูปภาพหลุมคำตอบ
holeImg = pygame.image.load('o.png') 
holeImg = pygame.transform.scale(holeImg, (200,200))  # ปรับขนาดรูปภาพ
# โหลดรูปหัวใจ
HeartImg = pygame.image.load('Heart.png')
HeartImg = pygame.transform.scale(HeartImg, (30, 30))  # ปรับขนาดรูปภาพ
# กำหนดฟอนต์
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)
button_font = pygame.font.Font(None, 50)

# Set ตัวละครเริ่มต้น
player_size = 100  
player1_x = WIDTH // 3 - player_size // 2  # ตำแหน่งเริ่มต้นของตัวละครที่ 1
player1_y = HEIGHT - player_size - 10  
player2_x = 2 * WIDTH // 3 - player_size // 2  # ตำแหน่งเริ่มต้นของตัวละครที่ 2
player2_y = HEIGHT - player_size - 10
player_speed1 = 5  # ความเร็วในการเคลื่อนที่ตัวละครที่ 1
player_speed2 = 5  # ความเร็วในการเคลื่อนที่ตัวละครที่ 2

# กำหนดตำแหน่งของหลุม
hole_positions = [(350, 350), (650, 350), (950, 350)]  # ตำแหน่งหลุม

# ตัวแปรของเกม
correct_answer_index = 0  # เก็บตำแหน่งของคำตอบที่ถูกต้อง
question = ""  # เก็บคำถามปัจจุบัน
answer_choices = []  # เก็บตัวเลือกคำตอบ
score1 = 0  # คะแนนตัวละครที่ 1
score2 = 0  # คะแนนตัวละครที่ 2
Latest_score1 = 0 # คะแนนล่าสุดตัวละครที่ 1 ไว้ใช้คำนวณความเร็ว
Latest_score2 = 0 # คะแนนล่าสุดตัวละครที่ 2 ไว้ใช้คำนวณความเร็ว
Heart1 = 3  # จำนวนหัวใจตัวละครที่ 1
Heart2 = 3  # จำนวนหัวใจตัวละครที่ 2
waiting = False  # ตัวแปรสำหรับเริ่มเกม
keys = pygame.key.get_pressed() # ตรวจสอบการกดปุ่มของคีย์บอร์ด
# ฟังก์ชันสร้างคำถาม
def generate_question():
    global question, answer_choices, correct_answer_index
    num1 = random.randint(1, 100)  # สุ่มเลขที่ 1
    num2 = random.randint(1, 100)  # สุ่มเลขที่ 2
    operation = random.choice(["+", "-","*","/","%"])  # สุ่มเครื่องหมายบวกลบคูณหารหรือมอดุโล
    
    # คำนวณคำตอบที่ถูกต้อง
    if operation == "+":
        correct_answer = num1 + num2
    elif  operation == "-" :
        correct_answer = num1 - num2
    elif  operation == "*" :
        correct_answer = num1 * num2
    elif  operation == "/" :
        correct_answer = num1 // num2 # หารไม่แบบปัดเศษ
    elif  operation == "%" :
        correct_answer = num1 % num2

    # สร้างความคำถาม
    question = f"{num1} {operation} {num2} = ?"
    
    # สร้างคำตอบที่ไม่ถูกต้อง
    incorrect_answers = []
    while len(incorrect_answers) < 2:
        wrong_answer = correct_answer + random.randint(-10, 10)  # สุ่มคำตอบที่ผิดโดยการเอาคำตอบที่ถูกมาบวกกับเลขที่สุ่มตั้งแต่ -10 ถึง 10
        if wrong_answer != correct_answer and wrong_answer not in incorrect_answers:
            incorrect_answers.append(wrong_answer)  # เพิ่มคำตอบที่ผิดลงในลิส

    # กำหนดตำแหน่งของคำตอบที่ถูกแบบสุ่ม
    answer_choices = incorrect_answers[:]
    correct_answer_index = random.randint(0, 2)
    answer_choices.insert(correct_answer_index, correct_answer)  # เพิ่มคำตอบที่ถูกต้องลงในตำแหน่งที่สุ่ม

# ฟังก์ชันวาดหลุมและแสดงคำตอบ
def draw_holes():
    for i, pos in enumerate(hole_positions):
        screen.blit(holeImg, (pos[0] - holeImg.get_width() // 2, pos[1] - holeImg.get_height() // 2))  # วาดหลุม
        text = font.render(str(answer_choices[i]), True, BLUE)  # สร้างข้อความคำตอบ
        screen.blit(text, (pos[0] - text.get_width() // 2, pos[1] - holeImg.get_height() // 2 - text.get_height() - 10))

# ฟังก์ชันวาดตัวละคร
def draw_players(keys):
    if keys[pygame.K_w] and  Heart1>0 :  # ตัวละครที่ 1 เดินขึ้น
        screen.blit(brain1_up, (player1_x, player1_y))
    elif keys[pygame.K_s] and  Heart1>0:  # ตัวละครที่ 1 เดินลง
        screen.blit(brain1_down, (player1_x, player1_y))
    elif keys[pygame.K_a] and  Heart1>0:  # ตัวละครที่ 1 เดินไปซ้าย
        screen.blit(brain1_left, (player1_x, player1_y))
    elif keys[pygame.K_d] and  Heart1>0:  # ตัวละครที่ 1 เดินไปขวา
        screen.blit(brain1_right, (player1_x, player1_y))
    elif Heart1>0: # เมื่อตัวละครมีหัวใจแต่ไม่เดิน
        screen.blit(brain1_up, (player1_x, player1_y))
    else : # เมื่อตัวละครไม่มีหัวใจ
        screen.blit(brain1_dead, (player1_x, player1_y))


    if keys[pygame.K_UP] and  Heart2>0:  # ตัวละครที่ 2 เดินขึ้น
        screen.blit(brain2_up, (player2_x, player2_y))
    elif keys[pygame.K_DOWN] and  Heart2>0:  # ตัวละครที่ 2 เดินลง
        screen.blit(brain2_down, (player2_x, player2_y))
    elif keys[pygame.K_LEFT] and  Heart2>0:  # ตัวละครที่ 2 เดินไปซ้าย
        screen.blit(brain2_left, (player2_x, player2_y))
    elif keys[pygame.K_RIGHT] and  Heart2>0:  # ตัวละครที่ 2 เดินไปขวา
        screen.blit(brain2_right, (player2_x, player2_y))
    elif Heart2>0: # เมื่อตัวละครมีหัวใจแต่ไม่เดิน
        screen.blit(brain2_up, (player2_x, player2_y))
    else:# เมื่อตัวละครไม่มีหัวใจ
        screen.blit(brain2_dead, (player2_x, player2_y))
        
# ฟังก์ชันวาดหัวใจ
def draw_hearts():
    for i in range(Heart1):
        x = 10 + i * 40 # กำหนดตำแหน่งหัวใจ
        y = 50
        screen.blit(HeartImg, (x, y))
    for i in range(Heart2):
        x = 1125 + i * 40 # กำหนดตำแหน่งหัวใจ
        y = 50
        screen.blit(HeartImg, (x, y))

# ฟังก์ชันตรวจสอบการชนของตัวละครกับหลุม
def check_collision(player_rect):
    for i, pos in enumerate(hole_positions):
        hole_rect = pygame.Rect(pos[0] - 0.4, pos[1] - 15, 1, 1)
        if player_rect.colliderect(hole_rect):
            return i
    return None
# ฟังก์ชันรีเซ็ตเกม
def reset_game():
    global score1, score2, Heart1, Heart2, player1_x, player1_y, player2_x, player2_y, waiting
    score1 = 0
    score2 = 0
    Heart1 = 3
    Heart2 = 3
    player1_x = WIDTH // 3 - player_size // 2
    player1_y = HEIGHT - player_size - 10
    player2_x = 2 * WIDTH // 3 - player_size // 2
    player2_y = HEIGHT - player_size - 10
    generate_question()
    waiting = False
    player_speed1 = 5  
    player_speed2 = 5  

# ฟังก์ชันเมนูเกม
def game_menu():
    while True:
        screen.blit(bg_math, (0, 0))  # เพิ่มพื้นหลังหน้าเมนูเกม
        
        # วาดปุ่ม New Game
        new_game_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 60)
        pygame.draw.rect(screen,ORANGE, new_game_button)
        draw_text('NEW GAME', button_font, WHITE, screen, WIDTH // 2, HEIGHT // 2 - 20)
        
        # วาดปุ่ม Exit
        exit_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 50, 300, 60)
        pygame.draw.rect(screen, ORANGE, exit_button)
        draw_text('EXIT', button_font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 80)

        # เช็คเหตุการณ์ต่างๆ
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if new_game_button.collidepoint(event.pos):
                    return  # เริ่มเกม
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        # อัพเดทหน้าจอ
        pygame.display.update()
# ฟังก์ชันแสดงข้อความบนหน้าจอ
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# เริ่มเกม
game_menu()# เรียกเมนูเกม
# ลูปหลักของเกม
reset_game()

while True:
    screen.fill(PASTEL_BLUE)  # สีพื้นหลัง
    if waiting:
        end_text = None
        if Heart1 == 0 and Heart2 == 0:
            # วางตำแหน่งตัวละครหลังจบเกม (ตัวละครที่ 1 ด้านซ้าย, ตัวละครที่ 2 ด้านขวา)
            player1_x = WIDTH // 6 - player_size // 2  # วาง ตัวละครที่ 1 ที่ด้านซ้าย
            player1_y = HEIGHT // 2 - player_size // 2  # ตำแหน่งแนวตั้งกลางหน้าจอ
            player2_x = 3 * WIDTH // 3.5 - player_size // 2  # วาง ตัวละครที่ 2 ที่ด้านขวา
            player2_y = HEIGHT // 2 - player_size // 2  # ตำแหน่งแนวตั้งกลางหน้าจอ

            # วาดผู้เล่นทั้งสองที่ตำแหน่งใหม่
    
            screen.blit(brain1_up, (player1_x, player1_y))  # ตัวละครที่ 1
            screen.blit(brain2_up, (player2_x, player2_y))  # ตัวละครที่ 2

            # แสดงคะแนนของผู้เล่นทั้ง 2 บนหัวตัวละครตอนจบเกม
            score_text1 = font.render(f"Player 1: {score1}", True, RED)
            screen.blit(score_text1, (player1_x + player_size // 4 - score_text1.get_width() // 2, player1_y - score_text1.get_height()))
            
            score_text2 = font.render(f"Player 2: {score2}", True, BLUE)
            screen.blit(score_text2, (player2_x + player_size // 4 - score_text2.get_width() // 2, player2_y - score_text2.get_height()))

            # แสดงผลว่าใครชนะ
            if score1 > score2:
                end_text = font.render('Player 1 Wins!', True, RED)
            elif score2 > score1:
                end_text = font.render('Player 2 Wins!', True, BLUE)
            else:
                end_text = font.render('It\'s a Draw!', True, GREEN)

            # แสดงข้อความสรุปผลเกม
            screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 3 - end_text.get_height() // 2))
        else:
            waiting = False
        # สร้างปุ่ม RESTART GAME
        screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 3 - end_text.get_height() // 2))
        restart_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 20, 300, 50)
        pygame.draw.rect(screen, ORANGE, restart_button)
        draw_text('RESTART GAME', button_font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 5)
        # สร้างปุ่ม Quit Game
        quit_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 60, 300, 50)
        pygame.draw.rect(screen, ORANGE, quit_button)
        draw_text('QUIT GAME', button_font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 85)
        # เช็คเหตุการณ์ต่างๆ
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    reset_game()
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
    else:
        question_text = font.render(question, True, BLACK)
        screen.blit(question_text, (WIDTH // 2 - question_text.get_width() // 2, 50))
        draw_holes()
        draw_players(keys)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        # เช็คว่าตัวละครที่ 1 มีหัวใจมั้ย
        if Heart1 > 0:
            if keys[pygame.K_a] and player1_x > 0:
                player1_x -= player_speed1
                urrent_brain1_image = brain1_left
            if keys[pygame.K_d] and player1_x < WIDTH - player_size:
                player1_x += player_speed1
                current_brain1_image = brain1_right
            if keys[pygame.K_w] and player1_y > 0:
                player1_y -= player_speed1
                current_brain1_image = brain1_up
            if keys[pygame.K_s] and player1_y < HEIGHT - player_size:
                player1_y += player_speed1
                current_brain1_image = brain1_down
            else :
                current_brain1_image = brain1_dead
        # # เช็คว่าตัวละครที่ 2 มีหัวใจมั้ย
        if Heart2 > 0:
            if keys[pygame.K_LEFT] and player2_x > 0:  
                player2_x -= player_speed2
                current_brain2_image = brain2_left
            if keys[pygame.K_RIGHT] and player2_x < WIDTH - player_size:  
                player2_x += player_speed2
                current_brain2_image = brain2_right
            if keys[pygame.K_UP] and player2_y > 0:  
                player2_y -= player_speed2
                current_brain2_image = brain2_up
            if keys[pygame.K_DOWN] and player2_y < HEIGHT - player_size:  
                player2_y += player_speed2
                current_brain2_image = brain2_down
            else:
                current_brain2_image = brain2_dead
        # การกำหนดตำแหน่งและขนาดตัวละคร
        player1_rect = pygame.Rect(player1_x, player1_y, player_size, player_size)
        player2_rect = pygame.Rect(player2_x, player2_y, player_size, player_size)
        
        #เช็คการชนของผู้เล่นคนที่1
        collision_index1 = check_collision(player1_rect)
        if collision_index1 is not None:
            if collision_index1 == correct_answer_index:
                score1 += 1
                Latest_score1 += 1 # คะแนนล่าสุดของตัวละครที่ 1 เพื่อนำมาคำนวณความมเร็ว
                if Latest_score1 <= 10:
                    player_speed1 = player_speed1 + Latest_score1*(0.5) # เพิ่มความเร็ว
                elif Latest_score1 > 10:
                    player_speed1 = 32 # ปรับให้ความเร็วคงที่
                    
            else:
                Heart1 -= 1
                Latest_score1 = 0 #ให้คะแนนล่าสุดเป็น0เพื่อให้ความเร็วเท่าเดิม
                player_speed1 = 5 + Latest_score1*(0) # ลดความเร็ว
            generate_question()
            player1_x = WIDTH // 3 - player_size // 2 # ตำแหน่งเริ่มต้นของผู้เล่น 1 หลังจบข้อนั้น
            player1_y = HEIGHT - player_size - 10
            player2_x = 2 * WIDTH // 3 - player_size // 2 # ตำแหน่งเริ่มต้นของผู้เล่น 1 หลังจบข้อนั้น
            player2_y = HEIGHT - player_size - 10

        #เช็คการชนของผู้เล่นคนที่2
        collision_index2 = check_collision(player2_rect)
        if collision_index2 is not None:
            if collision_index2 == correct_answer_index:
                score2 += 1
                Latest_score2 += 1 # คะแนนล่าสุดของตัวละครที่ 2 เพื่อนำมาคำนวณความมเร็ว
                if Latest_score2 <= 10:
                    player_speed2 = player_speed2 + Latest_score2*(0.5) # เพิ่มความเร็ว
                elif Latest_score2 >10 :
                    player_speed2 = 32 # ปรับให้ความเร็วคงที่
            else:
                Heart2 -= 1
                Latest_score2 = 0 #ให้คะแนนล่าสุดเป็น0เพื่อให้ความเร็วเท่าเดิม
                player_speed2 = 5 + Latest_score2*(0) #ลดความเร็ว
            generate_question()
            player2_x = 2 * WIDTH // 3 - player_size // 2 # ตำแหน่งเริ่มต้นของผู้เล่น 2 หลังจบข้อนั้น
            player2_y = HEIGHT - player_size - 10
            player1_x = WIDTH // 3 - player_size // 2 # ตำแหน่งเริ่มต้นของผู้เล่น 1 หลังจบข้อนั้น
            player1_y = HEIGHT - player_size - 10


        if Heart1 == 0 and Heart2 == 0:
            waiting = True  # จบเกมเมื่อหัวใจผู้เล่นทั้งสองหมด

        score_text1 = small_font.render(f"Player 1 Score: {score1}", True, BLACK)
        screen.blit(score_text1, (10, 10))
        score_text2 = small_font.render(f"Player 2 Score: {score2}", True, BLACK)
        screen.blit(score_text2, (1040, 10))

        draw_hearts()

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
