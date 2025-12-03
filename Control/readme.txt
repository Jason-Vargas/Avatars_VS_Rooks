Control Físico — Avatars vs Rooks
Raspberry Pi Pico W — USB HID Controller

Este directorio contiene el código y la documentación del control físico diseñado para el videojuego Avatars vs Rooks.
El control utiliza una Raspberry Pi Pico W que se conecta por USB y actúa como un dispositivo HID (teclado) para enviar entradas al juego.

El juego no necesita modificar su código para funcionar con este control, ya que recibe las teclas igual que un teclado normal.

-Funcionalidad del Control
Elemento	                    Pin Pico	Equivalente en el Juego	    Descripción
Botón Colocar rook	            GP2	        X	                        Coloca el rook seleccionado si hay suficientes monedas.
Botón Agarrar monedas	        GP3	        Z	                        Recoge las monedas presentes en el tablero.
Botón Pausa / Guardar	        GP4	        ESC	                        Abre menú de pausa y guarda la partida.
Botón Cambiar rook seleccionado	GP5	        TAB	                        Cambia entre los rooks disponibles (como un selector cíclico).
Joystick X/Y	                GPIO27      Flechas	                    Mueve el cursor del tablero en las cuatro direcciones.
                                GPIO26	

-LEDs del control
LED	                    Pin Pico	Función en el juego
LED Avatar	            GP12	    Se enciende cuando aparece un avatar en el nivel.
LED Fin de nivel	    GP13	    Se enciende cuando muere el último avatar (nivel completado).


-Requisitos
Firmware

Para usar la Pico como HID, debe ejecutar una versión de CircuitPython que incluya soporte USB HID.

Descarga desde:
https://circuitpython.org/board/raspberry_pi_pico_w/

-Librerías necesarias

Dentro de la carpeta /lib en la Pico deben estar:

adafruit_hid/ (carpeta completa)


-Instalación en la Pico

Conecta la Pico manteniendo presionado BOOTSEL.

Arrastrá el archivo de firmware de CircuitPython (.uf2).

La Pico aparecerá como una unidad USB llamada CIRCUITPY.

Copiá dentro:

--control_hid_pico.py → renómbralo a code.py para que se ejecute automáticamente.
--La carpeta lib/adafruit_hid/.