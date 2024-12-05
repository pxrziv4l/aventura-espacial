import pygame
from Constantes import *
from Funciones import cargar_gif,dibujar_boton_flotante, dibujar_pantalla_puntos, escribir_csv
from datetime import datetime
from PIL import Image


# Creación y configuración de los botones
lista_botones = []

for i in range(3):
    boton = {}
    boton["superficie"] = pygame.Surface(TAMAÑO_BOTON)
    boton["superficie"].fill(COLOR_BOTON)
    boton["rectangulo"] = boton["superficie"].get_rect()
    lista_botones.append(boton)

# Cargar el GIF de fondo utilizando cargar_gif
ruta_gif = r"PYGAME2\Imagenes\GameOver.gif"
fotogramas_originales, duracion = cargar_gif(ruta_gif)

# Escalar los fotogramas al tamaño de la ventana
fotogramas = [pygame.transform.scale(f, VENTANA) for f in fotogramas_originales]
indice_fotograma = 0
tiempo_anterior = pygame.time.get_ticks()

# Variable de retorno que indica la siguiente pantalla a mostrar
def mostrar_game_over(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event],puntaje,tiempo_final,sonido_boton) -> str:
    global indice_fotograma, tiempo_anterior
    retorno = "game over"
    
    # Manejar los eventos del menú
    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            for i, boton in enumerate(lista_botones):
                if boton["rectangulo"].collidepoint(evento.pos):
                    sonido_boton.play()
                    if i == 0:
                        retorno = "juego"
                    elif i == 1:
                        fuente_texto = pygame.font.Font(r"PYGAME2\Fuentes\PressStart2P-Regular.ttf", 40)
                        fuente_boton = pygame.font.Font(r"PYGAME2\Fuentes\PressStart2P-Regular.ttf", 20)
                        nombre = dibujar_pantalla_puntos(pantalla, fuente_texto, fuente_boton, COLOR_TEXTO, COLOR_FONDO, COLOR_BOTON, COLOR_BOTON_FLOT, COLOR_TEXTO)
                        if len(nombre) == 0 :
                            nombre = 'XXX'
                        escribir_csv([nombre, tiempo_final, puntaje, datetime.now().strftime("%d/%m/%Y")])
                        retorno = "rankings"
                    elif i == 2:
                        retorno = "menu"
        elif evento.type == pygame.QUIT:
            retorno = "salir"

    # Dibujar el fondo animado del game over
    tiempo_actual = pygame.time.get_ticks()
    if tiempo_actual - tiempo_anterior >= duracion:
        tiempo_anterior = tiempo_actual
        indice_fotograma = (indice_fotograma + 1) % len(fotogramas)

    fotograma_actual = fotogramas[indice_fotograma]
    pantalla.blit(fotograma_actual, (0, 0))

    #region Dibujar el título "GAME OVER" con sombra
    fuente_titulo = pygame.font.Font(r"PYGAME2\Fuentes\PixelCalculon-eP3x.ttf", 100)

    texto_parte_1 = fuente_titulo.render("GAME", True, COLOR_TEXTO_TITULO)
    texto_parte_2 = fuente_titulo.render("OVER", True, COLOR_TEXTO_TITULO)

    sombra_parte_1 = fuente_titulo.render("GAME", True, COLOR_SOMBRA_TITULO)
    sombra_parte_2 = fuente_titulo.render("OVER", True, COLOR_SOMBRA_TITULO)

    # Calcula el centro de la pantalla y la altura total del texto
    total_height = texto_parte_1.get_height() + texto_parte_2.get_height() + 10
    center_x = (VENTANA[0] - max(texto_parte_1.get_width(), texto_parte_2.get_width())) // 2
    center_y = (VENTANA[1] - total_height) // 2 - 140

    # Desplaza la sombra un poco hacia abajo y hacia la derecha
    sombra_offset = 5
    pantalla.blit(sombra_parte_1, (center_x + sombra_offset, center_y + sombra_offset))
    pantalla.blit(sombra_parte_2, (center_x + sombra_offset, center_y + sombra_offset + texto_parte_1.get_height() + 10))

    # Dibujar el texto real encima de la sombra
    pantalla.blit(texto_parte_1, (center_x, center_y))
    pantalla.blit(texto_parte_2, (center_x, center_y + texto_parte_1.get_height() + 10))
    #endregion

    # Configurar las posiciones y los textos de los botones
    posiciones_botones = [(328, 400), (328, 450), (328, 500)]
    textos_botones = ["REINTENTAR", "PUNTUACION", "MENU"]

    # Dibujar los botones en pantalla
    for i, boton in enumerate(lista_botones):
        boton["rectangulo"] = pantalla.blit(boton["superficie"], posiciones_botones[i])
        texto = textos_botones[i]
        fuente_boton = pygame.font.Font(r"PYGAME2\Fuentes\PressStart2P-Regular.ttf", 15)
        dibujar_boton_flotante(pantalla, boton["rectangulo"], COLOR_BOTON, COLOR_BOTON_FLOT, texto, fuente_boton, COLOR_TEXTO)

    return retorno