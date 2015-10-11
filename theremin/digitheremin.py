#!/usr/bin/env python

import freenect
import cv
import cv2
import numpy as np

import mido
from mido import Message

threshold = 100
current_depth = 480

def change_threshold(value):
    global threshold
    threshold = value

def change_depth(value):
    global current_depth
    current_depth = value

def show_depth():
	global threshold
	global current_depth

	depth, timestamp = freenect.sync_get_depth()	
	depth = 255 * np.logical_and(depth >= current_depth - threshold, depth <= current_depth + threshold)
	depth = depth.astype(np.uint8)
	
	return depth
	
def show_video(image, image_name):	
	cv2.namedWindow(image_name)
	cv2.createTrackbar(image_name + ' threshold', image_name, threshold, 500, change_threshold)
	cv2.createTrackbar(image_name + ' depth', image_name, current_depth, 500, change_depth)
	
	
def find_centroid(imagen):
	#http://stackoverflow.com/questions/10262600/how-to-detect-region-of-large-of-white-pixels-using-opencv

	ret, thres = cv2.threshold(imagen, 127,255,0)
		
	contours, hier = cv2.findContours(thres, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)	
	
	list_centros = []
	
	for cnt in contours:
		if 1000 < cv2.contourArea(cnt) < 100000:
			cv2.drawContours(imagen,[cnt],0,(200,255,200),2)
			
			#centroide	
			#http://docs.opencv.org/master/dd/d49/tutorial_py_contour_features.html#gsc.tab=0
			M = cv2.moments(cnt)
			
			if (int(M['m00'])!=0):
				centro = (int(M['m10']/M['m00']),int(M['m01']/M['m00']))						
				cv2.circle(imagen, centro, 16, 100, -1)
				list_centros.append(centro)	
	
	return {'img':imagen, 'centr':list_centros}

def show_image(imagen, mensaje):	
	cv2.imshow(mensaje, imagen)

def flip_image(imagen):
	#mirror image
	#http://docs.opencv.org/modules/core/doc/operations_on_arrays.html#void flip(InputArray src, OutputArray dst, int flipCode)
	
	imagen = cv2.flip(imagen,1)
	
	return imagen

def position_2_note(pos_x):
	#Se mapea la posici'on x a notas
		# la posici'on 0 representa la nota A0 (nota 21)
		# la posici'on 640 representa la nota B7 (nota 107)
	#La ecuaci'on de la recta es la siguiente:
		# nota = 0.134375*posicion_x+21
	
	nota = 0.134375*pos_x+21
	
	return nota

def note_2_frec_n_bend(nota):
	#Se mapea la nota a una frecuencia, se le resta la frecuencia de la
	#nota anterior y se mapea el resto a un "bend"
	
	#Se sabe que F_m = 440*2^((m-69)/12)
	#frec = 440*pow(2,(nota-69)/12)
	
	res = nota - np.floor(nota)
	
	#Se mapea el resto a un bend.
		#El resto 0 se mapea a un bend de 0
		#El resto 1 se mapea a un bend de 4096 (seg'un el manejo de pitchwheel de mido)
	#La ecuaci'on de la recta es, por tanto:
		# bend = 4096*resto
	
	bend = 4096*res
	
	return bend

def send_midi_message(on, nota_entera, bend, nota_anterior):
	msg_note_on = Message("note_on", note=nota_entera)
	msg_note_off = Message("note_off", note=nota_anterior)

	msg_bend = Message("pitchwheel", pitch=bend)
	msg_not_bend = Message("pitchwheel", pitch=0)
		
	if (on):
		output.send(msg_note_off)				
		output.send(msg_note_on)
		output.send(msg_bend)
	else:
		output.send(msg_note_off)
	
if __name__ == "__main__":
	print "Presione 'q' para salir"
			
	output = mido.open_output()	
	
	nota_anterior = 69
	
	while 1:
		image = show_depth()
		
		image = flip_image(image)
		
		rslt_fc = find_centroid(image)
		
		image = rslt_fc['img']
		
		centroides = rslt_fc['centr']
		
		if (centroides==[]):
			send_midi_message(0, 1, 1, nota_anterior)
			
		if centroides:
			x = centroides[0][0]
			y = centroides[0][1]
		
			nota = position_2_note(x)
		
			nota_entera = np.int(np.floor(nota))
		
			bend = np.int(round(note_2_frec_n_bend(nota)))
			
			send_midi_message(1, nota_entera, bend, nota_anterior)
				
			nota_anterior = nota_entera	
				
		show_image(image, "matching")
		show_video(image, "matching")
		
		c = cv2.waitKey(10)
		
		if 'q' == chr(c & 255):
			break
			output.close()
