import pygame
from Constantes import *
from Menu import *
from Juego import ejecutar_juego
from Ajustes import mostrar_ajustes
from Funciones import leer_json
from Rankings import mostrar_puntos
from Game_Over import mostrar_game_over

# Configuraciones Básicas y carga de datos

pygame.init()
pygame.mixer.init()
sonido_boton = pygame.mixer.Sound(r"PYGAME2\Sonidos\Menu_buttons.wav")
sonido_perdiste = pygame.mixer.Sound(r"PYGAME2\Sonidos\Perdiste.wav")
sonido_puntos = pygame.mixer.Sound(r"PYGAME2\Sonidos\Points.wav")
sonido_explosion_1 = pygame.mixer.Sound(r"PYGAME2\Sonidos\Explosion_asteroid_1.wav")
sonido_explosion_2 = pygame.mixer.Sound(r"PYGAME2\Sonidos\Explosion_asteroid_2.wav")
flujo = pygame.time.Clock()
icono = pygame.image.load(r"PYGAME2\Imagenes\Icono.jpg")
pygame.display.set_icon(icono)

ajustes_json= leer_json()

pygame.mixer.music.set_volume(ajustes_json["musica"] / 100.0)
for sonido in [sonido_boton,sonido_explosion_1,sonido_explosion_2,sonido_perdiste,sonido_puntos]:
    pygame.mixer.Sound.set_volume(sonido, ajustes_json["sonido"] / 100.0)
pygame.display.set_caption("AVENTURA ESPACIAL")
pantalla = pygame.display.set_mode(VENTANA)

tiempo_final = None
puntaje = None

ventana_actual = "menu"
abrir = True

# Ciclo de vida
while abrir:
    flujo.tick(FPS)
    cola_eventos = pygame.event.get()
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            abrir = False
    # Lógica del juego según la ventana actual
    if ventana_actual == "menu":
        ventana_actual = mostrar_menu(pantalla, cola_eventos, sonido_boton)
    elif ventana_actual == "juego":
        resultado = ejecutar_juego(pantalla, flujo,sonido_puntos,sonido_explosion_1,sonido_explosion_2,sonido_perdiste)
        ventana_actual = resultado[0]
        tiempo_final = resultado[1]
        puntaje = int(resultado[2])
    elif ventana_actual == "ajustes":
        ventana_actual = mostrar_ajustes(pantalla, cola_eventos,sonido_boton,[sonido_boton,sonido_explosion_1,sonido_explosion_2,sonido_perdiste,sonido_puntos])
    elif ventana_actual == "rankings":
        ventana_actual = mostrar_puntos(pantalla, cola_eventos)
    elif ventana_actual == "salir":
        abrir = False
    elif  ventana_actual == "game over":
        ventana_actual = mostrar_game_over(pantalla, cola_eventos,puntaje,tiempo_final,sonido_boton) # También vuelve al menú si el juego termina

    # Actualizar la pantalla
    pygame.display.flip()

# Cierra Pygame correctamente al salir
pygame.quit()