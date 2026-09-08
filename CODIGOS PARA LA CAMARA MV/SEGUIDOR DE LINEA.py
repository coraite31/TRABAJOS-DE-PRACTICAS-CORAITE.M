import sensor  # Importa la librería para controlar el hardware de la cámara OpenMV
import time    # Importa la librería para gestionar retardo y tiempos de espera

# ==============================
# CONFIGURACIÓN DE LA CÁMARA
# ==============================

sensor.reset()                          # Reinicia la cámara a sus valores predeterminados para asegurar una configuración limpia
sensor.set_pixformat(sensor.GRAYSCALE)  # Configura la captura en escala de grises (modo blanco y negro, ideal para detectar líneas)
sensor.set_framesize(sensor.QQVGA)      # Ajusta la resolución de la imagen a QQVGA (160 píxeles de ancho por 120 de alto)
sensor.skip_frames(time=2000)           # Pausa la ejecución por 2000 ms (2 segundos) para permitir la estabilización del brillo del sensor

# ==============================
# CONFIGURACIÓN DE PARÁMETROS
# ==============================

# Definición del umbral para el color negro en escala de grises (valores de brillo de 0 = negro absoluto a 60 = gris oscuro)
NEGRO = (0, 60)

# Variables que almacenan las dimensiones totales de la imagen capturada (resolución QQVGA)
ANCHO = 160  # Ancho total de la toma en píxeles
ALTO = 120   # Alto total de la toma en píxeles

# ==============================
# BUCLE PRINCIPAL DE Detección
# ==============================

while True:  # Bucle infinito para procesar imágenes fotograma por fotograma de forma continua

    # Captura un fotograma en escala de grises de la cámara y lo almacena en la variable 'img'
    img = sensor.snapshot()

    # =================================
    # EVALUACIÓN DE LA ZONA IZQUIERDA
    # =================================

    # Busca manchas/bloques (blobs) que cumplan el rango del color NEGRO dentro del ROI (Región de Interés)
    # roi=(X_inicial, Y_inicial, Ancho_cuadro, Alto_cuadro)
    izquierda = img.find_blobs(
        [NEGRO],               # Lista con el umbral de color a buscar (NEGRO)
        roi=(0, 70, 50, 50),   # Región de Interés: evalúa la esquina izquierda (X=0 a 50, Y=70 a 120)
        pixels_threshold=20,   # Descarta detecciones con menos de 20 píxeles negros mínimos
        area_threshold=20      # Descarta detecciones cuyo cuadro delimitador abarque un área menor a 20 píxeles
    )

    # =================================
    # EVALUACIÓN DE LA ZONA CENTRO
    # =================================

    # Busca bloques negros en el cuadro central de la imagen
    centro = img.find_blobs(
        [NEGRO],                # Lista con el umbral de color a buscar (NEGRO)
        roi=(55, 70, 50, 50),   # Región de Interés: evalúa la parte central (X=55 a 105, Y=70 a 120)
        pixels_threshold=20,    # Requiere un mínimo de 20 píxeles para ser considerado una línea válida
        area_threshold=20       # Requiere un área mínima de 20 píxeles para evitar falsos positivos
    )

    # =================================
    # EVALUACIÓN DE LA ZONA DERECHA
    # =================================

    # Busca bloques negros en la franja derecha de la imagen
    derecha = img.find_blobs(
        [NEGRO],                 # Lista con el umbral de color a buscar (NEGRO)
        roi=(110, 70, 50, 50),   # Región de Interés: evalúa la esquina derecha (X=110 a 160, Y=70 a 120)
        pixels_threshold=20,     # Mínimo de 20 píxeles negros necesarios
        area_threshold=20        # Área mínima de 20 píxeles necesarios
    )

    # =================================
    # TOMA DE DECISIÓN DE DIRECCIÓN
    # =================================

    if len(centro) > 0:  # Evalúa si la lista 'centro' detectó al menos un bloque negro

        print("AVANZAR")  # Muestra la instrucción de continuar derecho en la consola serie

    elif len(izquierda) > 0:  # Si el centro está libre pero la lista 'izquierda' halló la línea

        print("GIRAR IZQUIERDA")  # Muestra la instrucción de corrección a la izquierda en consola

    elif len(derecha) > 0:  # Si el centro e izquierda están libres pero 'derecha' halló la línea

        print("GIRAR DERECHA")  # Muestra la instrucción de corrección a la derecha en consola

    else:  # Ejecuta esta opción si ninguna de las 3 zonas (ROI) detectó presencia de color negro

        print("LINEA NO ENCONTRADA")  # Advierte en consola que el vehículo perdió el trazo de la línea
