import sensor, time, image
from pyb import UART, LED

# UART3 en OpenMV (Pin P4 = TX) a 9600 baudios hacia la Teensy 4.1
uart = UART(3, 9600)

# LEDs integrados en la cámara para confirmar visualmente
led_verde = LED(2)
led_rojo = LED(1)

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA) # 160x120
sensor.skip_frames(time=2000)

# 1. Cargar las plantillas de tu rostro
archivos = ["cara_frente.pgm", "cara_sonrisa.pgm", "cara_izq.pgm", "cara_der.pgm"]
plantillas = []

for archivo in archivos:
    try:
        plantillas.append(image.Image(archivo))
        print("Cargada: " + archivo)
    except OSError:
        print("No se encontro: " + archivo)

# 2. Calibrar fondo vacio
print("Calibrando fondo vacio... no te pongas al frente")
time.sleep_ms(1500)
fondo = sensor.snapshot().copy()
print("Fondo calibrado.")

# Umbral de coincidencia para tu cara
UMBRAL_TU_CARA = 0.68

clock = time.clock()

while True:
    clock.tick()
    img = sensor.snapshot()

    # 3. Detectar presencia en el entorno por diferencia de fondo
    img_diff = img.copy()
    img_diff.difference(fondo)
    stats = img_diff.get_statistics()

    hay_alguien = stats.mean > 12
    es_mi_cara = False

    if hay_alguien:
        # Buscar tus plantillas en la imagen real
        for template in plantillas:
            r = img.find_template(template, UMBRAL_TU_CARA, step=4, search=image.SEARCH_EX)
            if r:
                img.draw_rectangle(r, color=255)
                es_mi_cara = True
                break

    # 4. Enviar decision por UART a la Teensy y actualizar LEDs
    if not hay_alguien:
        uart.write(b'N')
        led_verde.off()
        led_rojo.off()
        print(">> Nadie en camara -> MOTOR APAGADO")

    elif es_mi_cara:
        uart.write(b'1')
        led_verde.on()
        led_rojo.off()
        print(">> Tu cara detectada -> MOTOR ENCENDIDO")

    else:
        uart.write(b'0')
        led_verde.off()
        led_rojo.on()
        print(">> Otra persona detectada -> MOTOR DETENIDO")

    time.sleep_ms(100)
