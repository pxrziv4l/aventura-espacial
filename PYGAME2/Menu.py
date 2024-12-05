import pygame
from Constantes import *
from Funciones import mostrar_texto, dibujar_boton_flotante

pygame.init()

# Inicializa la música y los sonidos
pygame.mixer.init()
pygame.mixer.music.load(r"PYGAME2\Sonidos\Menu_song.mp3")
fondo = pygame.image.load(r"PYGAME2\Imagenes\Pixelart_Menu.jpg")
fondo = pygame.transform.scale(fondo, VENTANA)

# Creación y configuración de los botones
lista_botones = []

for i in range(4):
    boton = {}
    boton["superficie"] = pygame.Surface(TAMAÑO_BOTON)
    boton["superficie"].fill(COLOR_BOTON)
    boton["rectangulo"] = boton["superficie"].get_rect()
    lista_botones.append(boton)



# Variable de retorno que indica la siguiente pantalla a mostrar
def mostrar_menu(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event],sonido_boton) -> str:
    retorno = "menu"

    # Reproducir música de fondo si no está sonando
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(r"PYGAME2\Sonidos\Menu_song.mp3")
        pygame.mixer.music.play(-1)

    # Manejar los eventos del menú
    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            for i, boton in enumerate(lista_botones):
                if boton["rectangulo"].collidepoint(evento.pos):
                    sonido_boton.play()
                    if i == BOTON_SALIR:
                        retorno = "salir"
                        pygame.mixer.music.stop()
                    elif i == BOTON_JUGAR:
                        retorno = "juego"
                        pygame.mixer.music.stop()
                    elif i == BOTON_PUNTUACIONES:
                        retorno = "rankings"
                    elif i == BOTON_AJUSTES:
                        retorno = "ajustes"
        elif evento.type == pygame.QUIT:
            retorno = "salir"
            pygame.mixer.music.stop()

    # Dibujar el fondo del menú
    pantalla.blit(fondo, (0, 0))

    # Dibujar el título del juego "AVENTURA ESPACIAL" con sombra
    fuente_titulo = pygame.font.Font(r"PYGAME2\Fuentes\PixelCalculon-eP3x.ttf", 100)

    texto_parte_1 = fuente_titulo.render("AVENTURA", True, COLOR_TEXTO_TITULO)
    texto_parte_2 = fuente_titulo.render("ESPACIAL", True, COLOR_TEXTO_TITULO)

    sombra_parte_1 = fuente_titulo.render("AVENTURA", True, COLOR_SOMBRA_TITULO)
    sombra_parte_2 = fuente_titulo.render("ESPACIAL", True, COLOR_SOMBRA_TITULO)

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

    # Dibujar el título "UTN AVELLANEDA" más pequeño y centrado
    fuente_subtitulo = pygame.font.Font(r"PYGAME2\Fuentes\PixelTandysoft-0rJG.ttf", 40)

    texto_subtitulo = fuente_subtitulo.render("UTN AVELLANEDA", True, COLOR_TEXTO_TITULO)
    sombra_subtitulo = fuente_subtitulo.render("UTN AVELLANEDA", True, COLOR_SOMBRA_TITULO)

    # Ajuste de la posición del subtítulo
    subtitulo_width = texto_subtitulo.get_width()
    subtitulo_height = texto_subtitulo.get_height()
    subtitulo_x = (VENTANA[0] - subtitulo_width) // 2
    subtitulo_y = center_y + total_height // 2 + -16 

    pantalla.blit(sombra_subtitulo, (subtitulo_x + sombra_offset, subtitulo_y + sombra_offset))
    pantalla.blit(texto_subtitulo, (subtitulo_x, subtitulo_y))

    # Configurar las posiciones y los textos de los botones
    posiciones_botones = [(328, 400), (328, 450), (328, 500), (328, 550)]
    textos_botones = ["JUGAR", "AJUSTES", "PUNTOS", "SALIR"]

    # Dibujar los botones en pantalla
    for i, boton in enumerate(lista_botones):
        boton["rectangulo"] = pantalla.blit(boton["superficie"], posiciones_botones[i])
        texto = textos_botones[i]
        fuente_boton = pygame.font.Font(r"PYGAME2\Fuentes\PressStart2P-Regular.ttf", 20)
        dibujar_boton_flotante(pantalla, boton["rectangulo"], COLOR_BOTON, COLOR_BOTON_FLOT, texto, fuente_boton, COLOR_TEXTO)

    # Dibujar un mensaje especial en la esquina inferior derecha
    mensaje_especial = "Gracias a mi bb por apoyarme en esto"
    fuente_mensaje = pygame.font.Font(r"PYGAME2\Fuentes\PressStart2P-Regular.ttf", 7)
    texto_mensaje = fuente_mensaje.render(mensaje_especial, True, (225, 240, 240))
    texto_mensaje_rect = texto_mensaje.get_rect(bottomright=(VENTANA[0] - 5, VENTANA[1] - 5))
    pantalla.blit(texto_mensaje, texto_mensaje_rect)

    return retorno