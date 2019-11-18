# Kinect-Ins
Musical instrument with Kinect

En los útlimos años, la comunicación entre humano y computadora se ha vuelto muy fácil y natural. Dispositivos como cámaras de profundidad hacen posible una interacción cada vez más fluida.

Aparatos como el Kinect hacen posible la comunicación sin contacto físico ni controles de ningún tipo.

En el presente proyecto se describe el diseño, la implementación y la puesta en escena de una aplicación para utilizar un Kinect como interfaz visual y musical.

En general, es una implementación con Python, se utilizó MIDI para la interfaz musical y OpenCV para la interfaz visual.

Se desciben los algoritmos implementados el preprocesamiento y la conversión de la información, además, se muestran los resultados obtenidos.

La implementación fue exitosa, por lo que este documento puede servir como referencia para futuras aplicaciones afines.

# --------------------------------------------------------------------------------------------------------------------------

Para el kinect_drumming:
-Abra el sintetizador de su preferencia con el instrumento de su preferencias. Se recomienda AmSynth.
-Abra el programa de configuración de Jack de su preferencia. Se recomiend Qjackctl. 
Vaya a conexiones, ALSA, y conecte como puerto de salida el Midi Through y como entrada su sintetizador
 
Modifique el makefile según la escala que necesita (c, c#, d, d#, e, f, f#, g, g#, a, a#, b) y la cantidad de divsiones (4 o 9)

$python kinect_drumming/kinect_drumming.py {escala} {divisiones}

ejemplo de do mayor con 9 divisiones:
$python kinect_drumming/kinect_drumming.py c 9

Para el theremin:
$make theremin

Para el módulo pintar:
$make pintar

