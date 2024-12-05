import pygame
from Constantes import *
from Funciones import leer_json,escribir_json, dibujar_boton_flotante

pygame.mixer.init()
fondo_ajustes = pygame.image.load(r"PYGAME2\Imagenes\Pixelart_SubMenu.jpg")
ajustes_json= leer_json()

# Configuración de imagen de fondo
ancho_original, alto_original = fondo_ajustes.get_size()
relacion_aspecto = ancho_original / alto_original

if VENTANA[0] / VENTANA[1] > relacion_aspecto:
    nuevo_ancho = int(VENTANA[1] * relacion_aspecto)
    nuevo_alto = VENTANA[1]
else:
    nuevo_ancho = VENTANA[0]
    nuevo_alto = int(VENTANA[0] / relacion_aspecto)

fondo_ajustes = pygame.transform.scale(fondo_ajustes, (nuevo_ancho, nuevo_alto))
fondo_ajustes_x = (VENTANA[0] - nuevo_ancho) // 2
fondo_ajustes_y = (VENTANA[1] - nuevo_alto) // 2

#region Variables persistentes
boton_menos = pygame.Rect(35, 395, 30, 30)
boton_mas = pygame.Rect(120, 395, 30, 30)

barra_rect_musica = pygame.Rect(35, 185, 200, 10)
manija_rect_musica = pygame.Rect(barra_rect_musica.x + (190 * ajustes_json["musica"] / 100), barra_rect_musica.y - 5, 10, 20)

barra_rect_sonido = pygame.Rect(35, 275, 200, 10)
manija_rect_sonido = pygame.Rect(barra_rect_sonido.x + (190 * ajustes_json["sonido"] / 100), barra_rect_sonido.y - 5, 10, 20)
#endregion

arrastrando = False  # Control para saber si la manija está siendo arrastrada

def mostrar_ajustes(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event],sonido_boton : pygame.mixer.Sound,lista_sonidos:list) -> str:
    global ajustes_json, arrastrando, manija_rect_musica, manija_rect_sonido

    
    retorno = "ajustes"

    lista_botones_ajustes = []
    boton_volver = pygame.Rect(20, VENTANA[1] - TAMAÑO_BOTON_VOLVER[1] - 20, *TAMAÑO_BOTON_VOLVER)
    lista_botones_ajustes.append(boton_volver)

    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_volver.collidepoint(evento.pos):
                sonido_boton.play()
                escribir_json(ajustes_json)
                retorno = "menu"
            elif manija_rect_musica.collidepoint(evento.pos):
                arrastrando = True
            elif manija_rect_sonido.collidepoint(evento.pos): 
                arrastrando = True
            elif barra_rect_musica.collidepoint(evento.pos):  
                manija_rect_musica.x = max(barra_rect_musica.x, min(evento.pos[0] - manija_rect_musica.width // 2, barra_rect_musica.x + barra_rect_musica.width - manija_rect_musica.width))
                ajustes_json["musica"] = int((manija_rect_musica.x - barra_rect_musica.x) / (barra_rect_musica.width - manija_rect_musica.width) * 100)
                pygame.mixer.music.set_volume(ajustes_json["musica"] / 100.0)
            elif barra_rect_sonido.collidepoint(evento.pos): 
                manija_rect_sonido.x = max(barra_rect_sonido.x, min(evento.pos[0] - manija_rect_sonido.width // 2, barra_rect_sonido.x + barra_rect_sonido.width - manija_rect_sonido.width))
                ajustes_json["sonido"] = int((manija_rect_sonido.x - barra_rect_sonido.x) / (barra_rect_sonido.width - manija_rect_sonido.width) * 100)
                for sonido in lista_sonidos:
                    pygame.mixer.Sound.set_volume(sonido, ajustes_json["sonido"] / 100.0)  
            elif boton_menos.collidepoint(evento.pos):  
                if ajustes_json["vidas"] > 1:
                    ajustes_json["vidas"] -= 1
                    sonido_boton.play()
            elif boton_mas.collidepoint(evento.pos):  
                if ajustes_json["vidas"] < 5:
                    ajustes_json["vidas"] += 1
                    sonido_boton.play()    
        elif evento.type == pygame.MOUSEBUTTONUP:
            arrastrando = False
        elif evento.type == pygame.MOUSEMOTION and arrastrando:
            if manija_rect_musica.collidepoint(evento.pos):  
                manija_rect_musica.x = max(barra_rect_musica.x, min(evento.pos[0] - manija_rect_musica.width // 2, barra_rect_musica.x + barra_rect_musica.width - manija_rect_musica.width))
                ajustes_json["musica"] = int((manija_rect_musica.x - barra_rect_musica.x) / (barra_rect_musica.width - manija_rect_musica.width) * 100)
                pygame.mixer.music.set_volume(ajustes_json["musica"] / 100.0)
            elif manija_rect_sonido.collidepoint(evento.pos):  
                manija_rect_sonido.x = max(barra_rect_sonido.x, min(evento.pos[0] - manija_rect_sonido.width // 2, barra_rect_sonido.x + barra_rect_sonido.width - manija_rect_sonido.width))
                ajustes_json["sonido"] = int((manija_rect_sonido.x - barra_rect_sonido.x) / (barra_rect_sonido.width - manija_rect_sonido.width) * 100)
                for sonido in lista_sonidos:
                    pygame.mixer.Sound.set_volume(sonido, ajustes_json["sonido"] / 100.0)

    #region Dibujar el fondo
    pantalla.fill(COLOR_FONDO)
    pantalla.blit(fondo_ajustes, (fondo_ajustes_x, fondo_ajustes_y))

    # Dibujar el rectángulo de ajustes
    rect_ajustes = pygame.Rect(25, 100, 750, 400)
    superficie_rect_ajustes = pygame.Surface((rect_ajustes.width, rect_ajustes.height), pygame.SRCALPHA)
    superficie_rect_ajustes.fill((0, 0, 0, 180))
    pantalla.blit(superficie_rect_ajustes, rect_ajustes.topleft)

    # Franja con el título "VOLUMEN"
    franja_volumen = pygame.Rect(rect_ajustes.x, rect_ajustes.y, rect_ajustes.width, 30)
    pygame.draw.rect(pantalla, COLOR_BOTON, franja_volumen)
    fuente_titulo_volumen = pygame.font.Font(r"PYGAME2\Fuentes\PressStart2P-Regular.ttf", 20)
    texto_titulo_volumen = fuente_titulo_volumen.render("VOLUMEN", True, COLOR_TEXTO)
    pantalla.blit(texto_titulo_volumen, (franja_volumen.x + 10, franja_volumen.y + 7))
    #endregion

    #region Dibujar el título y subtitulos
    fuente_titulo = pygame.font.Font(r"PYGAME2\Fuentes\PressStart2P-Regular.ttf", 25)
    texto_titulo = fuente_titulo.render("AJUSTES", True, COLOR_TEXTO)
    ancho_titulo, alto_titulo = fuente_titulo.size("AJUSTES")
    cuadro_titulo = pygame.Rect((VENTANA[0] - ancho_titulo) // 2, 20, ancho_titulo + 20, alto_titulo + 10)
    pygame.draw.rect(pantalla, COLOR_BOTON, cuadro_titulo)
    texto_rect_titulo = texto_titulo.get_rect(center=cuadro_titulo.center)
    pantalla.blit(texto_titulo, texto_rect_titulo)

    # Subtítulo y barra deslizante para música
    fuente_subtitulo_musica = pygame.font.Font(r"PYGAME2\Fuentes\PressStart2P-Regular.ttf", 15)
    texto_subtitulo_musica = fuente_subtitulo_musica.render("Música", True, COLOR_TEXTO)
    pantalla.blit(texto_subtitulo_musica, (rect_ajustes.x + 10, rect_ajustes.y + 50))
    pygame.draw.rect(pantalla, COLOR_SOMBRA_TITULO, barra_rect_musica)  # Barra música
    pygame.draw.rect(pantalla, COLOR_TEXTO_TITULO, manija_rect_musica)  # Manija música
    fuente_volumen = pygame.font.Font(r"PYGAME2\Fuentes\PressStart2P-Regular.ttf", 15)
    texto_volumen = fuente_volumen.render(f"{ajustes_json["musica"]}%", True, COLOR_TEXTO)
    pantalla.blit(texto_volumen, (barra_rect_musica.x + barra_rect_musica.width + 10, barra_rect_musica.y - 0))

    # Subtítulo y barra deslizante para sonido
    fuente_subtitulo_sonido = pygame.font.Font(r"PYGAME2\Fuentes\PressStart2P-Regular.ttf", 15)
    texto_subtitulo_sonido = fuente_subtitulo_sonido.render("Sonido", True, COLOR_TEXTO)
    pantalla.blit(texto_subtitulo_sonido, (rect_ajustes.x + 10, rect_ajustes.y + 140))
    pygame.draw.rect(pantalla, COLOR_SOMBRA_TITULO, barra_rect_sonido)  # Barra sonido
    pygame.draw.rect(pantalla, COLOR_TEXTO_TITULO, manija_rect_sonido)  # Manija sonido
    texto_volumen_sonido = fuente_volumen.render(f"{ajustes_json["sonido"]}%", True, COLOR_TEXTO)
    pantalla.blit(texto_volumen_sonido, (barra_rect_sonido.x + barra_rect_sonido.width + 10, barra_rect_sonido.y - 0))
    #endregion

    #region Franja con el título "JUEGO"
    franja_juego = pygame.Rect(rect_ajustes.x, rect_ajustes.y + 215, rect_ajustes.width, 30)
    pygame.draw.rect(pantalla, COLOR_BOTON, franja_juego)
    fuente_titulo_juego = pygame.font.Font(r"PYGAME2\Fuentes\PressStart2P-Regular.ttf", 20)
    texto_titulo_juego = fuente_titulo_juego.render("JUEGO", True, COLOR_TEXTO)
    pantalla.blit(texto_titulo_juego, (franja_juego.x + 10, franja_juego.y + 7))

    # Subtítulo y controles para vidas
    fuente_subtitulo_vidas = pygame.font.Font(r"PYGAME2\Fuentes\PressStart2P-Regular.ttf", 15)
    texto_subtitulo_vidas = fuente_subtitulo_vidas.render("Vida", True, COLOR_TEXTO)
    pantalla.blit(texto_subtitulo_vidas, (rect_ajustes.x + 10, rect_ajustes.y + 265))

    pygame.draw.rect(pantalla, COLOR_BOTON, boton_menos)
    pygame.draw.rect(pantalla, COLOR_BOTON, boton_mas)  
    texto_menos = fuente_subtitulo_vidas.render("-", True, COLOR_TEXTO)
    texto_mas = fuente_subtitulo_vidas.render("+", True, COLOR_TEXTO)

    # Para el botón menos
    pos_texto_menos = (boton_menos.x + (boton_menos.width - texto_menos.get_width()) // 2,boton_menos.y + (boton_menos.height - texto_menos.get_height()) // 2)

    # Para el botón más
    pos_texto_mas = (boton_mas.x + (boton_mas.width - texto_mas.get_width()) // 2,boton_mas.y + (boton_mas.height - texto_mas.get_height()) // 2)

    pantalla.blit(texto_menos, pos_texto_menos)
    pantalla.blit(texto_mas, pos_texto_mas)


    texto_vidas = fuente_subtitulo_vidas.render(f"{ajustes_json["vidas"]}", True, COLOR_TEXTO)
    pantalla.blit(texto_vidas, (boton_menos.x + 50, boton_menos.y + 5))
    #endregion


    # Dibujar el botón de volver
    pygame.draw.rect(pantalla, COLOR_BOTON, boton_volver)
    fuente_boton = pygame.font.Font(r"PYGAME2\Fuentes\PressStart2P-Regular.ttf", 20)
    dibujar_boton_flotante(pantalla, boton_volver, COLOR_BOTON, COLOR_BOTON_FLOT, "volver", fuente_boton, COLOR_TEXTO)

    return retorno