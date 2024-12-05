import pygame
from PIL import Image
from Constantes import *
import csv
import json

# Funcion que carga los gif
def cargar_gif(ruta_gif):
    gif = Image.open(ruta_gif)
    fotogramas = []
    try:
        while True:
            fotograma = gif.copy()
            fotograma = fotograma.convert("RGBA")
            fotogramas.append(pygame.image.fromstring(fotograma.tobytes(), fotograma.size, "RGBA"))
            gif.seek(len(fotogramas))
    except EOFError:
        pass
    return fotogramas, gif.info.get("duration", 100)

# Función para mostrar un texto en la pantalla
def mostrar_texto(superficie, texto, posicion, fuente, color=pygame.Color('black')):
    palabras = [palabra.split(' ') for palabra in texto.splitlines()]
    espacio = fuente.size(' ')[0] 
    ancho_maximo, alto_maximo = superficie.get_size()
    x, y = posicion

    for linea in palabras:
        for palabra in linea:
            superficie_palabra = fuente.render(palabra, False, color)
            ancho_palabra, alto_palabra = superficie_palabra.get_size()

            if x + ancho_palabra >= ancho_maximo:
                x = posicion[0]
                y += alto_palabra

            superficie.blit(superficie_palabra, (x, y))
            x += ancho_palabra + espacio
        x = posicion[0]
        y += alto_palabra

# Funcion que dibuja unas franjas horizontales
def dibujar_franjas(pantalla, color, altura):
    pygame.draw.rect(pantalla, color, (0, 0, ANCHO, altura))
    pygame.draw.rect(pantalla, color, (0, ALTO - altura, ANCHO, altura))

# Funcion para el boton flotante
def dibujar_boton_flotante(pantalla, boton, color_normal, color_flot, texto, fuente, color_texto):
    # Detecta si el cursor está sobre el botón
    if boton.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(pantalla, color_flot, boton)
    else:
        pygame.draw.rect(pantalla, color_normal, boton)

    # Renderiza el texto del botón
    texto_boton = fuente.render(texto, True, color_texto)
    texto_rect = texto_boton.get_rect(center=boton.center)
    pantalla.blit(texto_boton, texto_rect)

# Función para mostrar el tiempo
def mostrar_tiempo(pantalla, tiempo, font, color=pygame.Color('white')):
    minutos = tiempo // 60000
    segundos = (tiempo % 60000) // 1000
    microsegundos = (tiempo % 1000)

    microsegundos = microsegundos // 10
    tiempo_texto = f"{minutos:02}:{segundos:02}:{microsegundos:02}"
    mostrar_texto(pantalla, tiempo_texto, (10, 25), font, color)
    return tiempo_texto

# Función para dibujar la pantalla de puntos
import pygame

import pygame

def dibujar_pantalla_puntos(pantalla, fuente_texto, fuente_boton, color_texto, color_borde, color_boton, color_boton_flot, color_texto_boton):
    # Variables locales para manejar el estado del nombre y retorno
    nombre = ""
    retorno = None

    # Configuración de la pantalla
    tamaño = pygame.Rect(200, 150, 400, 300)
    boton_rect = pygame.Rect(300, 350, 200, 50) 

    # Cargar la imagen de fondo
    fondo = pygame.image.load(r"PYGAME2\Imagenes\GameOver.gif") 

    # Redimensionar la imagen para que cubra toda la pantalla
    fondo = pygame.transform.scale(fondo, (pantalla.get_width(), pantalla.get_height()))

    # Reducir el tamaño del texto "INGRESE SU NOMBRE"
    fuente_texto_pequena = pygame.font.Font(r"PYGAME2\Fuentes\PressStart2P-Regular.ttf", 20) 

    # Bucle para manejar la interacción
    while retorno is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if len(nombre) < 3 and event.unicode.isalpha(): 
                    nombre += event.unicode.upper() 
                elif event.key == pygame.K_BACKSPACE:  
                    nombre = nombre[:-1]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_rect.collidepoint(event.pos):  
                    retorno = "rankings"

        # Dibuja el fondo redimensionado para que cubra toda la pantalla
        pantalla.blit(fondo, (0, 0)) 

        # Dibujar una superficie con color semi-transparente para el modal
        modal_surface = pygame.Surface((tamaño.width, tamaño.height), pygame.SRCALPHA)
        modal_surface.fill((0, 0, 0, 150)) 

        # Colocar el fondo semi-transparente en la pantalla
        pantalla.blit(modal_surface, (tamaño.x, tamaño.y)) 

        # Dibuja el borde del modal (sin redondeo)
        pygame.draw.rect(pantalla, color_borde, tamaño, width=3)

        # Crear un texto con guiones bajos para el nombre (3 guiones bajos por defecto)
        indicador_nombre = "_" * 3 
        for i in range(len(nombre)):
            indicador_nombre = indicador_nombre[:i] + nombre[i] + indicador_nombre[i + 1:] 

        # Renderiza el texto del modal
        texto_modal = fuente_texto_pequena.render("INGRESE SU NOMBRE", True, color_texto)
        texto_rect = texto_modal.get_rect(center=(tamaño.centerx, tamaño.y + 40))
        pantalla.blit(texto_modal, texto_rect)

        # Renderiza el indicador visual del nombre
        nombre_texto = fuente_texto.render(indicador_nombre, True, color_texto)
        nombre_rect = nombre_texto.get_rect(center=(tamaño.centerx, tamaño.centery))
        pantalla.blit(nombre_texto, nombre_rect)

        # Dibuja el botón de "Aceptar" con bordes redondeados
        if boton_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(pantalla, color_boton_flot, boton_rect, border_radius=10) 
        else:
            pygame.draw.rect(pantalla, color_boton, boton_rect, border_radius=10) 

        pygame.draw.rect(pantalla, color_borde, boton_rect, width=2, border_radius=10)

        # Renderiza el texto del botón
        texto_boton = fuente_boton.render("ACEPTAR", True, color_texto_boton)
        texto_boton_rect = texto_boton.get_rect(center=boton_rect.center)
        pantalla.blit(texto_boton, texto_boton_rect)

        pygame.display.flip()

    return nombre

def escribir_csv(datos):

    # Datos que quieres escribir en el archivo CSV
    resultados = []

    # Nombre del archivo CSV
    nombre_archivo = "resultados_juego.csv"
    indice = None

    with open(nombre_archivo,  newline='', encoding='utf-8') as archivo_csv:
        lector_csv = csv.DictReader(archivo_csv)
    # Leer las filas del archivo
        for  fila in lector_csv:
            resultados.append([fila["nombre"],fila["tiempo"],fila["puntaje"],fila["fecha"]])
        
        resultados.append(datos)
        resultados.sort(key=lambda x: int(x[2]), reverse=True)
    
    # Crear el archivo CSV y escribir los datos
    if len(resultados) > 10:
        resultados = resultados[0:10]
    with open(nombre_archivo, mode='w', newline='') as archivo_csv:
        writer = csv.writer(archivo_csv)
        
        # Escribir la cabecera (nombres de las columnas)
        writer.writerow(["nombre", "tiempo", "puntaje", "fecha"])
        
        # Escribir los datos
        writer.writerows(resultados)

def leer_csv():
    # Nombre del archivo CSV
    resultados = []
    
    with open(NOMBRE_ARCHIVO,  newline='', encoding='utf-8') as archivo_csv:
        lector_csv = csv.DictReader(archivo_csv)
    # Leer las filas del archivo
        for fila in lector_csv:
            
            resultados.append([fila["nombre"],fila["tiempo"],fila["puntaje"],fila["fecha"]])
        
    return resultados

def escribir_json(lista_de_datos):    
    with open(JSON_ARCHIVO, "w") as archivo:
        json.dump(lista_de_datos, archivo, indent=2)

def leer_json():
    with open(JSON_ARCHIVO, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)
    
    return datos