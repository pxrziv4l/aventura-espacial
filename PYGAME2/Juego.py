import pygame
import random
import time
from Constantes import *
from Funciones import *

# Función para manejar la jugabilidad
def ejecutar_juego(pantalla, flujo, sonido_puntos, sonido_explosion_1, sonido_explosion_2,sonido_perdiste):
    # Cargar música de fondo para el juego
    pygame.mixer.music.load(r"PYGAME2\Sonidos\Musica_Juego.wav")
    pygame.mixer.music.play(loops=-1, start=0.0)
    sonido_reproduciendose = False 

    jugando = True
    # Inicialización del jugador
    jugador_x = ANCHO // 2 - JUGADOR_ANCHO // 2
    jugador_y = ALTO // 2 - JUGADOR_ALTO // 2 + 150
    velocidad_x = 0
    velocidad_y = 0
    vidas = leer_json()["vidas"]
    invulnerable = False
    tiempo_invulnerable = 0
    puntaje = 0
    velocidad_puntaje = 0.1
    tiempo_inicio = pygame.time.get_ticks()
    tiempo_acumulado = 0
    tiempo_acumulado += pygame.time.get_ticks() - tiempo_inicio
    tiempo_final = None

    # Cargar la imagen JPG de la nave
    nave_imagen = pygame.image.load(r"PYGAME2\Imagenes\Nave_png.png").convert_alpha()
    
    # Crear una superficie para la nave
    tamaño_nave = (JUGADOR_ANCHO, JUGADOR_ALTO)
    capa_base_nave = pygame.Surface(tamaño_nave, pygame.SRCALPHA)
    color_base_nave = (255, 255, 255, 255)  # blanco para que tome todos los colores
    # square_surface.fill(square_color)
    radio_redondeo = 80
    pygame.draw.rect(capa_base_nave, color_base_nave, (0, 0, *tamaño_nave), border_radius=radio_redondeo)
    # Ajustar el tamaño de la máscara para que coincida con el cuadrado
    mascara_nave = pygame.transform.scale(nave_imagen, tamaño_nave)
    # Combinar el cuadrado y la máscara
    capa_base_nave.blit(mascara_nave, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    asteroide_imagen = pygame.image.load(r"PYGAME2\Imagenes\asteroide_enemigo.png").convert_alpha()

    # Crear una superficie para los enemigos
    tamaño_enemigo = (ENEMIGO_ANCHO, ENEMIGO_ALTO)
    capa_base_enemigo = pygame.Surface(tamaño_enemigo, pygame.SRCALPHA)
    color_base_enemigo = (255, 255, 255, 255)  # blanco para que tome todos los colores
    # square_surface.fill(square_color)
    radio_redondeo = 100
    pygame.draw.rect(capa_base_enemigo, color_base_enemigo, (0, 0, *tamaño_enemigo), border_radius=radio_redondeo)
    # Ajustar el tamaño de la máscara para que coincida con el cuadrado
    mascara_enemigo = pygame.transform.scale(asteroide_imagen, tamaño_enemigo)

    capa_base_enemigo.blit(mascara_enemigo, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    

    # Generar estrellas
    num_stars = 100
    stars = [{"pos": (random.randint(0, 800), random.randint(0, 600)), "intensity": random.randint(50, 255)} for _ in range(num_stars)]

    # Límite inferior y superior de la pantalla 
    limite_superior = 60 
    limite_inferior = ALTO - 60 - JUGADOR_ALTO 

    # Inicialización de enemigos
    enemigos = []
    velocidades_enemigos = []

    # Generar enemigos sin que se superpongan ni amontonen
    posiciones_x = [i * (ANCHO // ENEMIGO_CANTIDAD) for i in range(ENEMIGO_CANTIDAD)]
    random.shuffle(posiciones_x)
    

    while len(enemigos) < ENEMIGO_CANTIDAD:
        enemigo_x = posiciones_x[len(enemigos)]
        enemigo_y = random.randint(-ENEMIGO_ALTO, limite_superior)

        # Comprobamos que el nuevo enemigo no se superponga con los ya existentes
        superpuesto = False
        for ex, ey in enemigos:
            if enemigo_x < ex + ENEMIGO_ANCHO and enemigo_x + ENEMIGO_ANCHO > ex and enemigo_y < ey + ENEMIGO_ALTO and enemigo_y + ENEMIGO_ALTO > ey:
                superpuesto = True
                break
        
        if not superpuesto:
            enemigos.append([enemigo_x, enemigo_y]) 
            velocidades_enemigos.append(random.uniform(ENEMIGO_VELOCIDAD - ENEMIGO_VELOCIDAD_VARIACION, ENEMIGO_VELOCIDAD + ENEMIGO_VELOCIDAD_VARIACION))



    while jugando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return ["salir"]
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    velocidad_x = -JUGADOR_VELOCIDAD
                elif evento.key == pygame.K_RIGHT:
                    velocidad_x = JUGADOR_VELOCIDAD
                elif evento.key == pygame.K_UP:
                    velocidad_y = -JUGADOR_VELOCIDAD
                elif evento.key == pygame.K_DOWN:
                    velocidad_y = JUGADOR_VELOCIDAD
            elif evento.type == pygame.KEYUP:
                if evento.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    velocidad_x = 0
                elif evento.key in (pygame.K_UP, pygame.K_DOWN):
                    velocidad_y = 0

        jugador_x += velocidad_x
        jugador_y += velocidad_y

        # Restringir al jugador dentro de los bordes de la ventana y las franjas
        jugador_x = max(0, min(ANCHO - JUGADOR_ANCHO, jugador_x))
        jugador_y = max(limite_superior, min(limite_inferior, jugador_y))

        # Movimiento de los enemigos
        for i, enemigo in enumerate(enemigos):
            enemigo[1] += velocidades_enemigos[i]

            # Si el enemigo llega al borde inferior
            if enemigo[1] > ALTO:
                enemigo[0] = random.randint(0, ANCHO - ENEMIGO_ANCHO)
                enemigo[1] = random.randint(-ENEMIGO_ALTO, limite_superior)

        # Verificar colisiones con el jugador
        for enemigo in enemigos:
            if (jugador_x < enemigo[0] + ENEMIGO_ANCHO and jugador_x + JUGADOR_ANCHO > enemigo[0] and 
                jugador_y < enemigo[1] + ENEMIGO_ALTO and jugador_y + JUGADOR_ALTO > enemigo[1]):
                
                if not invulnerable:  
                    vidas -= 1 
                    invulnerable = True
                    tiempo_invulnerable = pygame.time.get_ticks()
                    
                    # Reproducir sonido aleatorio si vidas > 1
                    if vidas > 0:
                        random.choice([sonido_explosion_1, sonido_explosion_2]).play()
                    
                    # Si es la última vida, terminar el juego
                    if vidas == 0:
                        sonido_perdiste.play()
                        pygame.mixer.music.stop()
                        return ["game over",tiempo_final, puntaje]

        # Si el jugador está invulnerable, hacer parpadear
        if invulnerable:
            if pygame.time.get_ticks() - tiempo_invulnerable < JUGADOR_INVULNERABILIDAD_TEMPO * 1000:
                # Alternar la visibilidad de la nave (parpadeo)
                if pygame.time.get_ticks() % 2:
                    nave_visible = False
                else:
                    nave_visible = True
            else:
                invulnerable = False
                nave_visible = True
        else:
            nave_visible = True
        
                
        tiempo_transcurrido = (pygame.time.get_ticks() - tiempo_inicio) / 1000
        if tiempo_transcurrido > 30:
            velocidad_puntaje = 0.2  # Más lento que antes
        elif tiempo_transcurrido > 60:
            velocidad_puntaje = 0.3  # Aumentar más lentamente

        # Incrementa el puntaje solo si el jugador no está invulnerable
        if not invulnerable:
            puntaje += velocidad_puntaje

        # Reproducir sonido cada 100 puntos (verificar si el puntaje es un múltiplo de 100)
        if int(puntaje) % 100 == 0 and puntaje > 0 and not sonido_reproduciendose:
            sonido_puntos.play()
            sonido_reproduciendose = True

        # Luego de que termine de reproducirse el sonido, restablecer la variable
        if not pygame.mixer.get_busy():  # Verifica si no hay ningún sonido reproduciéndose
            sonido_reproduciendose = False


        # Dibuja todo
        pantalla.fill((0, 0, 0))
        for star in stars:
            intensity = random.randint(50, 255)  # Cambia la intensidad aleatoriamente
            pygame.draw.circle(pantalla, (intensity, intensity, intensity), star["pos"], 2)


        if nave_visible:
            # Dibuja la nave con la imagen JPG y la hitbox ajustada
            pantalla.blit(capa_base_nave, (jugador_x, jugador_y))
        # Dibuja los enemigos
        for enemigo in enemigos:
            pantalla.blit(capa_base_enemigo, (enemigo[0], enemigo[1]))

        #region Dibuja las franjas
        dibujar_franjas(pantalla, COLOR_BOTON, 60)

         # Dibujar las estrellas
        
        # Mostrar las vidas en la franja inferior izquierda
        fuente = pygame.font.Font(r"PYGAME2\Fuentes\PressStart2P-Regular.ttf", 15)
        texto_vidas = fuente.render(f'Vidas: {vidas}', True, (255, 255, 255))
        pantalla.blit(texto_vidas, (10, ALTO - 38))

        # Mostrar el tiempo en la franja superior izquierda
        fuente_tiempo = pygame.font.Font(r"PYGAME2\Fuentes\PressStart2P-Regular.ttf", 15)
        tiempo_final = mostrar_tiempo(pantalla, pygame.time.get_ticks() - tiempo_inicio + tiempo_acumulado,fuente_tiempo , (255, 255, 255))

        # Mostrar el puntaje en la parte superior derecha
        fuente_puntaje = pygame.font.Font(r"PYGAME2\Fuentes\PressStart2P-Regular.ttf", 15)
        texto_score = fuente_puntaje.render("Score", True, (255, 255, 255))
        texto_puntaje = fuente_puntaje.render(f"{int(puntaje):04d}", True, (255, 255, 255))
        pantalla.blit(texto_score, (ANCHO - 120, 15))
        pantalla.blit(texto_puntaje, (ANCHO - 112, 35))
        #endregion

        pygame.display.update()
        flujo.tick(FPS)
