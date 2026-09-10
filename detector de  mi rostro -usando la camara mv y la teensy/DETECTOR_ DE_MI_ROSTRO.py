import sensor, time, image
from pyb import UART

# UART3 (P4 = TX) a 9600 baudios hacia la Teensy
uart = UART(3, 9600)

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA) # 160x120
sensor.skip_frames(time=2000)

# Cargar las plantillas
archivos = ["cara_frente.pgm", "cara_sonrisa.pgm", "cara_izq.pgm", "cara_der.pgm"]
plantillas = []

for archivo in archivos:
    try:
        plantillas.append(image.Image(archivo))
        print("Cargada: " + archivo)
    except OSError:
        print("No se encontro: " + archivo)

# Calibrar fondo vacio
print("Calibrando fondo vacio... no te pongas al frente")
time.sleep_ms(1500)
fondo = sensor.snapshot().copy()
print("Fondo calibrado.")

# Umbral de tu cara
UMBRAL_TU_CARA = 0.68

clock = time.clock()

while True:
    clock.tick()
    img = sensor.snapshot()

    # 1. Hacemos una copia para la resta (asi img no se vuelve negra en el visor)
    img_diff = img.copy()
    img_diff.difference(fondo)
    stats = img_diff.get_statistics()

    # Comprobar presencia por cambio en el entorno
    hay_alguien = stats.mean > 12

    es_mi_cara = False

    if hay_alguien:
        # 2. Buscar tu cara sobre la imagen real original (img)
        for template in plantillas:
            r = img.find_template(template, UMBRAL_TU_CARA, step=4, search=image.SEARCH_EX)
            if r:
                img.draw_rectangle(r, color=255)
                es_mi_cara = True
                break

    # 3. Enviar decision a la Teensy 4.1
    if not hay_alguien:
        uart.write(b'N')
        print(">> Nadie en camara -> LEDs Apagados")
    elif es_mi_cara:
        uart.write(b'1')
        print(">> Tu cara reconocida -> LED Verde")
    else:
        uart.write(b'0')
        print(">> Otra persona detectada -> LED Rojo")

    time.sleep_ms(150)
