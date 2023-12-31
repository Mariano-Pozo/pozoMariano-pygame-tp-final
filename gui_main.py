import pygame
from pygame.locals import *
import sys
from constantes import *
from gui_form import Form
from gui_form_menu_A import FormMenuA
from settings import FormMenuSettings
from gui_form_menu_B import FormMenuB
from gui_form_menu_C import FormMenuC
from gui_menu_levels import FormMenuLevels
from gui_form_menu_game_l1 import FormGameLevel1
from gui_form_menu_game_l2 import FormGameLevel2
from gui_form_menu_game_l3 import FormGameLevel3

flags = DOUBLEBUF 
screen = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA), flags, 16)
pygame.init()
clock = pygame.time.Clock()

form_menu_levels = FormMenuLevels(name="form_menu_levels",master_surface = screen,x=400,y=300,w=400,h=350,
                                  color_background=None,color_border=None,active=True)
form_menu_A = FormMenuA(name="form_menu_A",master_surface = screen,x=300,y=200,w=500,h=400,
                        color_background=(255,255,0),color_border=(255,0,255),active=True)
form_menu_B = FormMenuSettings(name="form_menu_B",master_surface = screen,x=400,y=300,w=400,h=350,
                               color_background=(0,255,255),color_border=(255,0,255),active=False)
form_menu_C = FormMenuC(name="form_menu_C",master_surface = screen,x=0,y=0,w=ANCHO_VENTANA,h=ALTO_VENTANA,
                        color_background=(0,255,255),color_border=(255,0,255),active=False)

form_game_L1 = FormGameLevel1(name="form_game_L1",master_surface = screen,x=0,y=0,w=ANCHO_VENTANA,h=ALTO_VENTANA,
                              color_background=(0,255,255),color_border=(255,0,255),active=False)
form_game_L2 = FormGameLevel2(name="form_game_L2",master_surface = screen,x=0,y=0,w=ANCHO_VENTANA,h=ALTO_VENTANA,
                              color_background=(0,255,255),color_border=(255,0,255),active=False)
form_game_L3 = FormGameLevel3(name="form_game_L3",master_surface = screen,x=0,y=0,w=ANCHO_VENTANA,h=ALTO_VENTANA,
                              color_background=(0,255,255),color_border=(255,0,255),active=False)

while True:     
    lista_eventos = pygame.event.get()
    for event in lista_eventos:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    delta_ms = clock.tick(FPS)

    aux_form_active = Form.get_active()
    if(aux_form_active != None):
        aux_form_active.update(lista_eventos,keys,delta_ms)
        aux_form_active.draw()
    
    


    pygame.display.flip()


'''
plataformas = leer_json("path")["nivel_2"]["config_plataformas"]
enemigos = leer_json("path","clave_a_leer")["nivel_2"]["config_enemigos"]

for subl in lista:
    plat = plataforma(subl[0],subl[1])
    plat.do_some_thing()

for enemigo in enemigos:
    enemigo_juego = enemigo(enemigo[0],enemigo[1])
    enemigo_juego.do_some_thing()
'''



    


  



