import pygame
from pygame.locals import *
from constantes import *
from auxiliar import Auxiliar
from disparos import Fire
from bullet import Bullet

class Player:
    def __init__(self,x,y,speed_walk,speed_run,gravity,jump_power,frame_rate_ms,move_rate_ms,jump_height,p_scale=1,interval_time_jump=100) -> None:
        '''
        self.walk_r = Auxiliar.getSurfaceFromSpriteSheet("images/caracters/stink/walk.png",15,1,scale=p_scale)[:12]
        '''

        self.stay_r = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/players/zero/stay ({0}).png",1,6,flip=False,scale=p_scale)
        self.stay_l = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/players/zero/stay ({0}).png",1,6,flip=True,scale=p_scale)
        self.jump_r = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/players/zero/jump ({0}).png",1,12,flip=False,scale=p_scale)
        self.jump_l = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/players/zero/jump ({0}).png",1,12,flip=True,scale=p_scale)
        self.walk_r = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/players/zero/walk ({0}).png",1,11,flip=False,scale=p_scale)
        self.walk_l = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/players/zero/walk ({0}).png",1,11,flip=True,scale=p_scale)
        self.shoot_r = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/players/zero/shot_stay ({0}).png",1,3,flip=False,scale=p_scale,repeat_frame=2)
        self.shoot_l = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/players/zero/shot_stay ({0}).png",1,3,flip=True,scale=p_scale,repeat_frame=2)
        self.knife_r = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/players/zero/saber_attack ({0}).png",1,7,flip=False,scale=p_scale,repeat_frame=1)
        self.knife_l = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/players/zero/saber_attack ({0}).png",1,7,flip=True,scale=p_scale,repeat_frame=1)
        self.damaged = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/players/zero/hit ({0}).png",1,4,flip=True,scale=p_scale,repeat_frame=1)

        self.frame = 0
        self.lives = 5
        self.score = 0
        self.move_x = 0
        self.move_y = 0
        self.speed_walk =  speed_walk
        self.speed_run =  speed_run
        self.gravity = gravity
        self.jump_power = jump_power
        self.animation = self.stay_r
        self.direction = DIRECTION_R
        self.image = self.animation[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collition_rect = pygame.Rect(x+self.rect.width/3,y,self.rect.width/3,self.rect.height)
        self.ground_collition_rect = pygame.Rect(self.collition_rect)
        self.ground_collition_rect.height = GROUND_COLLIDE_H
        self.ground_collition_rect.y = y + self.rect.height - GROUND_COLLIDE_H

        #estados
        self.is_attack = False
        self.is_damage = False
        self.is_dead = False
        self.is_jump = False
        self.is_fall = False
        self.is_shoot = False
        self.is_knife = False
        self.vivo = True

        self.direccion = 1
        self.ultimo_disparo=0

        self.tiempo_transcurrido_animation = 0
        self.frame_rate_ms = frame_rate_ms 
        self.tiempo_transcurrido_move = 0
        self.move_rate_ms = move_rate_ms
        self.y_start_jump = 0
        self.jump_height = jump_height

        self.tiempo_transcurrido = 0
        self.tiempo_last_jump = 0 # en base al tiempo transcurrido general
        self.interval_time_jump = interval_time_jump
    

        self.rect_disparos = pygame.Rect(self.collition_rect.x, self.rect.width,self.collition_rect.y, self.rect.height)
        self.rect_disparos.width = 1000
        self.rect_disparos.center = self.rect.center
        self.bullet_list = []
        
    def points(self,coin_list):
        for coins in coin_list:
            
            if coins.rect.colliderect(self.rect):
                # If the coin collides with ALGO, remove the rectangle from the coins list
                coin_list.remove(coins)
                self.score += 1  # Increment the score by 1
                print(self.score)

    def walk(self,direction):
        if(self.is_jump == False and self.is_fall == False):
            if(self.direction != direction or (self.animation != self.walk_r and self.animation != self.walk_l)):
                self.frame = 0
                self.direction = direction
                if(direction == DIRECTION_R):
                    self.move_x = self.speed_walk
                    self.animation = self.walk_r
                else:
                    self.move_x = -self.speed_walk
                    self.animation = self.walk_l

    def shoot(self,on_off = True):
        self.is_shoot = on_off
        if(on_off == True and self.is_jump == False and self.is_fall == False):

            if(self.animation != self.shoot_r and self.animation != self.shoot_l):
                self.frame = 0
                self.is_shoot = True
                if(self.direction == DIRECTION_R):
                    self.animation = self.shoot_r
                else:
                    self.animation = self.shoot_l       

    def receive_shoot(self):
        self.lives -= 1

    def saber(self,on_off = True):
        self.is_knife = on_off
        if(on_off == True and self.is_jump == False and self.is_fall == False):
            if(self.animation != self.knife_r and self.animation != self.knife_l):
                self.frame = 0
                if(self.direction == DIRECTION_R):
                    self.animation = self.knife_r
                else:
                    self.animation = self.knife_l      

    def jump(self,on_off = True):
        if(on_off and self.is_jump == False and self.is_fall == False):
            self.y_start_jump = self.rect.y
            self.move_x = int(self.move_x / 2)
            self.move_y = -self.jump_power
            #self.move_x = int(self.move_x / 2)
            self.move_y = -self.jump_power
            self.frame = 0
            self.is_jump = True
            if(self.direction == DIRECTION_R):
                self.animation = self.jump_r
            else:
                self.animation = self.jump_l
        if(on_off == False):
            self.is_jump = False
            self.stay()

    def stay(self):
        if(self.is_knife or self.is_shoot):
            return

        if(self.animation != self.stay_r and self.animation != self.stay_l):
            if(self.direction == DIRECTION_R):
                self.animation = self.stay_r
            else:
                self.animation = self.stay_l
            self.move_x = 0
            self.move_y = 0
            self.frame = 0

    def change_x(self,delta_x):
        self.rect.x += delta_x
        self.collition_rect.x += delta_x
        self.ground_collition_rect.x += delta_x

    def change_y(self,delta_y):
        self.rect.y += delta_y
        self.collition_rect.y += delta_y
        self.ground_collition_rect.y += delta_y

    def do_movement(self,delta_ms,plataform_list):
        self.tiempo_transcurrido_move += delta_ms
        if(self.tiempo_transcurrido_move >= self.move_rate_ms):
            self.tiempo_transcurrido_move = 0

            if(abs(self.y_start_jump - self.rect.y) > self.jump_height and self.is_jump):
                self.move_y = 0
          
            self.change_x(self.move_x)
            self.change_y(self.move_y)

            if(not self.is_on_plataform(plataform_list)):
                if(self.move_y == 0):
                    self.is_fall = True
                    self.change_y(self.gravity)
            else:
                if (self.is_jump): 
                    self.jump(False)
                self.is_fall = False            

    def is_on_plataform(self,plataform_list):
        retorno = False
        
        if(self.ground_collition_rect.bottom >= GROUND_LEVEL):
            retorno = True     
        else:
            for plataforma in  plataform_list:
                if(self.ground_collition_rect.colliderect(plataforma.ground_collition_rect)):
                    retorno = True
                    break       
        return retorno                 

    def do_animation(self,delta_ms):
        self.tiempo_transcurrido_animation += delta_ms
        if(self.tiempo_transcurrido_animation >= self.frame_rate_ms):
            self.tiempo_transcurrido_animation = 0
            if(self.frame < len(self.animation) - 1):
                self.frame += 1 
                #print(self.frame)
            else: 
                self.frame = 0

    def can_shoot(self):
        contador_disparo = pygame.time.get_ticks() 
        if contador_disparo - self.ultimo_disparo > 750:
            self.ultimo_disparo = contador_disparo
            return True
        else:
            return False
      

    def disparo_player(self,bullet_list,lista_enemigos):
            self.contador_cd = pygame.time.get_ticks()
            
            if self.can_shoot():
                
                if self.direction == DIRECTION_R:
                    bullet_list.append(Bullet(self, x_init=self.rect.right+14, y_init=self.rect.centery -13,x_end= 1800,y_end= self.rect.centery,speed=10, path="images/caracters/enemies/ork_sword/IDLE/bullet (1).png", frame_rate_ms=100, move_rate_ms=20, width=8, height=10))
                    
                    
                elif self.direction == DIRECTION_L:
                    bullet_list.append(Bullet(self, x_init=self.rect.left+14, y_init=self.rect.centery-13,x_end= 0, y_end=self.rect.centery,speed=10, path="images/caracters/enemies/ork_sword/IDLE/bullet (1).png", frame_rate_ms=100, move_rate_ms=20, width=8, height=10))
                    

    def check_alive(self):
        if self.lives <= 0:
            self.lives = 0
            self.speed_walk = 0
            self.vivo = False
            print("MORIDO")
            

 
    def update(self,delta_ms,plataform_list,list_coin):
        if self.vivo:
            self.do_movement(delta_ms,plataform_list)
            self.do_animation(delta_ms)
            self.points(list_coin)
            self.check_alive()
            self.rect_disparos.center = self.rect.center
        
        
    
    def draw(self,screen):
        
        if(DEBUG):
            pygame.draw.rect(screen,color=(255,0 ,0),rect=self.collition_rect)
            pygame.draw.rect(screen,color=(255,255,0),rect=self.ground_collition_rect)
            pygame.draw.rect(screen,color=(250,251,100),rect=self.rect_disparos)
        
        self.image = self.animation[self.frame]
        screen.blit(self.image,self.rect)
        
        for bala in self.bullet_list:
            bala.draw(screen)
    
        
        

    def events(self,delta_ms,keys,bullet_list,enemigo):
        self.tiempo_transcurrido += delta_ms

        if(not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not keys[pygame.K_SPACE]and not keys[pygame.K_a] and not keys[pygame.K_s]):
            #nada presionado
            self.stay()
        if(keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not keys[pygame.K_a] and not keys[pygame.K_s] ):
            self.walk(DIRECTION_L)
            self.direction = DIRECTION_L

        if(not keys[pygame.K_LEFT] and keys[pygame.K_RIGHT] and not keys[pygame.K_a] and not keys[pygame.K_s] ):
            self.walk(DIRECTION_R)
            self.direction = DIRECTION_R

        
        if(keys[pygame.K_LEFT] and keys[pygame.K_RIGHT] and not keys[pygame.K_SPACE]):
            self.stay()  

        if(keys[pygame.K_SPACE]and not self.is_fall):
            if keys[pygame.K_RIGHT]:
                self.direction = DIRECTION_R
                self.move_x = self.speed_walk
                self.animation = self.jump_r
            elif keys[pygame.K_LEFT]:
                self.direction = DIRECTION_L
                self.move_x = -self.speed_walk
                self.animation = self.jump_l
            else:
                self.move_x = 0
            if((self.tiempo_transcurrido - self.tiempo_last_jump)> self.interval_time_jump):
                self.jump(True)
                self.tiempo_last_jump = self.tiempo_transcurrido

        if(not keys[pygame.K_s]):
            self.shoot(False)

        if(not keys[pygame.K_a]):
            self.saber(False)  

        if(keys[pygame.K_s] and not keys[pygame.K_a]and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not keys[pygame.K_SPACE]):
            self.move_x= 0
            self.shoot()
            print("pressed S")
            self.disparo_player(bullet_list,enemigo)

        if(keys[pygame.K_a] and not keys[pygame.K_s]and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not keys[pygame.K_SPACE]):
            self.move_x= 0
            self.saber()   
           
