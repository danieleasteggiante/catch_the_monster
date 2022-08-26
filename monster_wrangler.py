import pygame, random

pygame.init()

WINDOWS_WIDTH = 1200
WINDOWS_HEIGHT = 700

display_surface = pygame.display.set_mode((WINDOWS_WIDTH,WINDOWS_HEIGHT))

pygame.display.set_caption("Monster catch")

FPS = 60 
clock = pygame.time.Clock()

#Classes
class Game():
    #Gameplay
    def __init__(self, player, monster_group):
        self.score = 0
        self.round_number = 0
        
        self.round_time = 0
        self.frame_count = 0
        
        self.player = player
        self.monster_group = monster_group

        #sound
        self.next_level_sound = pygame.mixer.Sound('assets/next_level.wav')

        #font
        self.font = pygame.font.Font('assets/Abrushow.ttf', 24)

        #set image
        blue_image = pygame.image.load("assets/blue_monster.png")
        green_image = pygame.image.load("assets/green_monster.png")
        purple_image = pygame.image.load("assets/purple_monster.png")
        yellow_image = pygame.image.load("assets/yellow_monster.png")

        #list monster
        self.target_monster_images = [blue_image,green_image,purple_image,yellow_image]

        self.target_monster_type = random.randint(0,3)
        self.target_monster_image = self.target_monster_images[self.target_monster_type]

        self.target_monster_rect = self.target_monster_image.get_rect()
        self.target_monster_rect.centerx = WINDOWS_WIDTH/2
        self.target_monster_rect.top = 30

    def update(self):
        if self.check_if_in_the_arena():
            self.frame_count += 1
        if self.frame_count == FPS:
            self.round_time +=1
            self.frame_count = 0
        self.check_collisions()
    
    def check_if_in_the_arena(self):
        if self.player.rect.y > 100 and self.player.rect.y < WINDOWS_HEIGHT - 100:
            return True
        else:
            return False


    def draw(self):
        WHITE = (255,255,255)
        BLUE = (20,176,235)
        GREEN = (87,207,47)
        PURPLE = (226,73,243)
        YELLOW = (243,157,20)

        #add the color to a list
        colors = [BLUE, GREEN, PURPLE, YELLOW]

        #Set text
        catch_text = self.font.render("Catch this monster", True, WHITE)
        catch_rect = catch_text.get_rect()
        catch_rect.centerx = WINDOWS_WIDTH/2
        catch_rect.top = 5

        score_text = self.font.render("Score: " + str(self.score), True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.topleft = (5,5)

        lives_text = self.font.render("Lives: " + str(self.player.lives), True, WHITE)
        lives_rect = lives_text.get_rect()
        lives_rect.topleft = (5,35)

        round_text = self.font.render("Current Round: " + str(self.round_number), True,  WHITE)
        round_rect =round_text.get_rect()
        round_rect.topleft = (5,65)

        time_text = self.font.render("Round time: " + str(self.round_time), True, WHITE)
        time_rect = time_text.get_rect()
        time_rect.topright= (WINDOWS_WIDTH - 10, 5)

        warp_text = self.font.render("Warps: " + str(self.player.warps), True, WHITE)
        warp_rect = warp_text.get_rect()
        warp_rect.topright= (WINDOWS_WIDTH - 10,35)

        #Blit the HUD
        display_surface.blit(catch_text, catch_rect)
        display_surface.blit(score_text,score_rect)
        display_surface.blit(round_text,round_rect)
        display_surface.blit(lives_text, lives_rect)
        display_surface.blit(time_text, time_rect)
        display_surface.blit(warp_text, warp_rect)
        display_surface.blit(self.target_monster_image, self.target_monster_rect)

        pygame.draw.rect(display_surface, colors[self.target_monster_type],(WINDOWS_WIDTH/2 - 32, 30, 64,64), 2)
        pygame.draw.rect(display_surface, colors[self.target_monster_type], (0,100, WINDOWS_WIDTH, WINDOWS_HEIGHT-200),4)


    def check_collisions(self):
        #check for collision with individual monster
        #perform a test to isolate the monster
        collided_monster = pygame.sprite.spritecollideany(self.player, self.monster_group)
        
        if collided_monster:
            #controle the sttate
            if collided_monster.type == self.target_monster_type:
                self.score += 100*self.round_number
                #Remove cought monster
                collided_monster.remove(self.monster_group)
                # if self.monster is > 0
                if self.monster_group:
                    self.player.catch_sound.play()
                    self.choose_new_target()
                else:
                    #round is complete
                    self.player.reset()
                    self.start_new_round()
            #Cought the wrong monster
            else:
                self.player.die_sound.play()
                self.player.lives -=1
                if self.player.lives <= 0:
                    self.pause_game("Final Score: " + str(self.score), "Press enter to play again")
                    self.reset_game()
                self.player.reset()

    def start_new_round(self):
        #Provide a score bonus basod on how quicli the round was finished
        self.score += int(1000*self.round_number/(1+self.round_time))

        #Reset round values
        self.round_time = 0
        self.frame_count = 0
        self.round_number += 1
        self.player.warps += 1
        
        #Remove remaining monster
        for el in self.monster_group:
            self.monster_group.remove(el)

        #Add monster
        for i in range(self.round_number):
            self.monster_group.add(Monster(random.randint(0,WINDOWS_WIDTH-64), random.randint(100,WINDOWS_HEIGHT-164), self.target_monster_images[0],0))
            self.monster_group.add(Monster(random.randint(0,WINDOWS_WIDTH-64), random.randint(100,WINDOWS_HEIGHT-164), self.target_monster_images[1],1))
            self.monster_group.add(Monster(random.randint(0,WINDOWS_WIDTH-64), random.randint(100,WINDOWS_HEIGHT-164), self.target_monster_images[2],2))
            self.monster_group.add(Monster(random.randint(0,WINDOWS_WIDTH-64), random.randint(100,WINDOWS_HEIGHT-164), self.target_monster_images[3],3))

        #Choose new target monster
        self.choose_new_target()
        self.next_level_sound.play()

    def choose_new_target(self):
        target_monster = random.choice(self.monster_group.sprites())
        self.target_monster_type = target_monster.type
        self.target_monster_image = target_monster.image

    def pause_game(self, main_text, sub_text):
        global running
        WHITE = (255,255,255)
        BLACK = (0,0,0)
        main_text_t = self.font.render(main_text, True, WHITE)
        main_text_rect = main_text_t.get_rect()
        main_text_rect.center = (WINDOWS_WIDTH/2, WINDOWS_HEIGHT/2)

        sub_text_t = self.font.render(sub_text, True, WHITE)
        sub_text_rect = sub_text_t.get_rect()
        sub_text_rect.center = (WINDOWS_WIDTH/2, WINDOWS_HEIGHT/2 + 50)

        #Display pause surface
        display_surface.fill(BLACK)
        display_surface.blit(main_text_t, main_text_rect)
        display_surface.blit(sub_text_t, sub_text_rect)
        pygame.display.update()

        #pause game
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key ==  pygame.K_RETURN:
                        is_paused = False
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False
        

    def reset_game(self):
        self.score = 0
        self.round_number = 0
        
        self.player.lives = 5
        self.player.warps = 2
        self.player.reset()

        self.start_new_round()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/knight.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOWS_WIDTH/2
        self.rect.bottom = WINDOWS_HEIGHT

        self.lives= 5
        self.warps = 2
        self.velocity = 8

        self.catch_sound =  pygame.mixer.Sound("assets/catch.wav")
        self.die_sound =  pygame.mixer.Sound("assets/die.wav")
        self.warp_sound =  pygame.mixer.Sound("assets/warp.wav")


        
    def update(self):
        keys =  pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.rect.right < WINDOWS_WIDTH:
            self.rect.x += self.velocity
        if keys[pygame.K_UP] and self.rect.top > 100:
            self.rect.y -= self.velocity
        if keys[pygame.K_DOWN] and self.rect.bottom < WINDOWS_HEIGHT-100:
            self.rect.y += self.velocity
            
    def warp(self):
        if self.warps >0:
            self.warps -=1
            self.warp_sound.play()
            self.rect.bottom = WINDOWS_HEIGHT
              
    def reset(self):
        self.rect.centerx = WINDOWS_WIDTH/2
        self.rect.bottom = WINDOWS_HEIGHT

class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y, image, moster_type):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()

        self.rect.topleft=(x,y)
        #monster type 0 -> blue - 1 -> green - 2 -> purple - 3 -> yellow
        self.type = moster_type

        #set random motion
        self.dx = random.choice([-1,1])
        self.dy = random.choice([-1,1])
        self.velocity = random.randint(1,5)
            
    def update(self):
        self.rect.x += self.dx*self.velocity
        self.rect.y += self.dy*self.velocity

        #Bounce the monster
        if self.rect.left <=0 or self.rect.right >= WINDOWS_WIDTH:
            self.dx = -1 * self.dx
        if self.rect.top <=100 or self.rect.bottom >= WINDOWS_HEIGHT-164:
            self.dy = -1* self.dy

#Create a player
my_player_group = pygame.sprite.Group()
my_player = Player()
my_player_group.add(my_player)

#Create a monster group
my_monster_group = pygame.sprite.Group()
#test monster
monster_t = Monster(500,500, pygame.image.load('assets/green_monster.png'),1)

#Create Game obj
my_game = Game(my_player, my_monster_group)
my_game.pause_game("Monster Catch", "Press Enter to begin")
my_game.start_new_round()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.type == pygame.K_SPACE:
                my_player.warp()

    #fill diplay
    display_surface.fill((0,0,0))   

    #update and draw Sprites
    my_player_group.update()
    my_player_group.draw(display_surface)

    my_monster_group.update()
    my_monster_group.draw(display_surface)
    #update and draw Game
    my_game.update()
    my_game.draw()
        
    #clock run and update display
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()