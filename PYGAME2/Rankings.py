import pygame
from Constantes import *
from Funciones import mostrar_texto, dibujar_boton_flotante,leer_csv

pygame.mixer.init()
sonido_click = pygame.mixer.Sound(r"PYGAME2\Sonidos\Click_1.wav") 
fondo_rankings = pygame.image.load(r"PYGAME2\Imagenes\Pixelart_SubMenu.jpg")

#region ajustes de imagen
ancho_original, alto_original = fondo_rankings.get_size()
relacion_aspecto = ancho_original / alto_original

if VENTANA[0] / VENTANA[1] > relacion_aspecto:
    nuevo_ancho = int(VENTANA[1] * relacion_aspecto)
    nuevo_alto = VENTANA[1]
else:
    nuevo_ancho = VENTANA[0]
    nuevo_alto = int(VENTANA[0] / relacion_aspecto)


fondo_rankings = pygame.transform.scale(fondo_rankings, (nuevo_ancho, nuevo_alto))
fondo_rankings_x = (VENTANA[0] - nuevo_ancho) // 2
fondo_rankings_y = (VENTANA[1] - nuevo_alto) // 2
#endregion

# Dibuja la pantalla de Rankings
def mostrar_puntos(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event], desde_game_over=False) -> str:
    retorno = "rankings"
    
    lista_botones_rankings = []
    boton_volver = pygame.Rect(20, VENTANA[1] - TAMAÑO_BOTON_VOLVER[1] - 20, *TAMAÑO_BOTON_VOLVER)
    lista_botones_rankings.append(boton_volver)

    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_volver.collidepoint(evento.pos):
                sonido_click.play()
                retorno = "menu"
        elif evento.type == pygame.QUIT:
            retorno = "salir"

    # Dibuja el fondo de la pantalla de ajustes
    pantalla.fill(COLOR_FONDO)
    pantalla.blit(fondo_rankings, (fondo_rankings_x, fondo_rankings_y))

    rect_ajustes = pygame.Rect(25, 100, 750, 400)
    superficie_rect_ajustes = pygame.Surface((rect_ajustes.width, rect_ajustes.height), pygame.SRCALPHA)
    superficie_rect_ajustes.fill((0, 0, 0, 180))
    pantalla.blit(superficie_rect_ajustes, rect_ajustes.topleft)

    # Titulo Ranking
    fuente_titulo = pygame.font.Font(r"PYGAME2\Fuentes\PressStart2P-Regular.ttf", 25)
    texto_ranking = fuente_titulo.render("RANKINGS", True, COLOR_TEXTO)
    ancho_titulo, alto_titulo = fuente_titulo.size("RANKINGS")

    # Centrar titulo en la parte superior
    cuadro_titulo = pygame.Rect((VENTANA[0] - ancho_titulo) // 2, 20, ancho_titulo + 20, alto_titulo + 10)
    pygame.draw.rect(pantalla, COLOR_BOTON, cuadro_titulo)

    texto_rect_titulo = texto_ranking.get_rect(center=cuadro_titulo.center)
    pantalla.blit(texto_ranking, texto_rect_titulo)

    # Agregar el texto "TOP 10"
    fuente_top = pygame.font.Font(r"PYGAME2\Fuentes\PressStart2P-Regular.ttf", 20)
    texto_top = fuente_top.render("TOP 10", True, COLOR_TEXTO)
    texto_top_rect = texto_top.get_rect(center=(rect_ajustes.centerx, rect_ajustes.y + 25))
    pantalla.blit(texto_top, texto_top_rect)

    pygame.draw.rect(pantalla, (255, 255, 255), pygame.Rect(rect_ajustes.x, rect_ajustes.y + alto_titulo + 20, rect_ajustes.width, 2))

    # Aquí van los puntajes TOP 10
    fuente_puntajes = pygame.font.Font(r"PYGAME2\Fuentes\PressStart2P-Regular.ttf", 10)
    puntajes_texto = leer_csv()
    
    for i, texto in enumerate(puntajes_texto):
        texto_puntaje = fuente_puntajes.render(f"{i+1:02d}. {texto[0]} - {texto[1]} - {int(texto[2]):04d} - {texto[3]}", True, COLOR_TEXTO)
        if(i<len(puntajes_texto)):
            pantalla.blit(texto_puntaje, (rect_ajustes.x + 20, rect_ajustes.y + 60 + i * 30))
            pygame.draw.rect(pantalla, (255, 255, 255), pygame.Rect(rect_ajustes.x, rect_ajustes.y + 355, rect_ajustes.width, 2))
        else:
            # Último puntaje guardado
    
            ultimo_texto_puntaje = fuente_puntajes.render(texto_puntaje, True, COLOR_TEXTO)
            pantalla.blit(ultimo_texto_puntaje, (rect_ajustes.x + 20, rect_ajustes.y + 370))

    # Dibuja el botón de volver
    fuente_boton = pygame.font.Font(r"PYGAME2\Fuentes\PressStart2P-Regular.ttf", 20)
    dibujar_boton_flotante(pantalla, boton_volver, COLOR_BOTON, COLOR_BOTON_FLOT, "volver", fuente_boton, COLOR_TEXTO)

    return retorno