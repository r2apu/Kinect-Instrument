# Kinect-Ins
Musical instrument with Kinect

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

