#!/usr/bin/env python

import freenect
import cv
import cv2
import numpy as np

import mido
from mido import Message

import time
import sys

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

def draw_lines_9(imagen): #draws lines to divide the camara for user
	
	#vetical lines
	cv2.line(imagen,(213,0),(213,480),(255,250,250),2)
	
	cv2.line(imagen,(426,0),(426,480),(255,250,250),2)
	
	#horizontal lines
	cv2.line(imagen, (0, 160), (640, 160), (255,250,250),2)

	cv2.line(imagen, (0, 320), (640, 320), (255,250,250),2)
	
	return imagen

def draw_lines_4(imagen): #draws lines to divide the camara for user
	
	#vetical lines
	cv2.line(imagen,(320,0),(320,480),(255,250,250),2)
	
	#horizontal lines
	cv2.line(imagen, (0, 240), (640, 240), (255,250,250),2)

	return imagen

def get_cuadrantes_9(centroides):
	
	# 1 | 2 | 3
	#-----------
	# 4 | 5 | 6
	#-----------
	# 7 | 8 | 9
	
	cuadrantes = []
	for i in range(len(centroides)):
		x = centroides[i][0]
		y = centroides[i][1]
	
		if (x < 213):
			if (y < 160):
				cuadrantes.append(1)
			elif (y < 320):
				cuadrantes.append(4)
			else:
				cuadrantes.append(7)
		elif (x < 426):
			if (y < 160):
				cuadrantes.append(2)
			elif (y < 320):
				cuadrantes.append(5)
			else:
				cuadrantes.append(8)
		else:
			if (y < 160):
				cuadrantes.append(3)
			elif (y < 320):
				cuadrantes.append(6)
			else:
				cuadrantes.append(9)
	
	return cuadrantes

def get_cuadrantes_4(centroides):
	
	# 1 | 2 |
	#--------
	# 3 | 4 |
	
	cuadrantes = []
	for i in range(len(centroides)):
		x = centroides[i][0]
		y = centroides[i][1]
	
		if (x < 320):
			if (y < 240):
				cuadrantes.append(1)
			else:
				cuadrantes.append(3)
		else:
			if (y < 240):
				cuadrantes.append(2)
			else:
				cuadrantes.append(4)
	
	return cuadrantes

def show_image(imagen, mensaje):
	
	cv2.imshow(mensaje, imagen)

def flip_image(imagen):
	#mirror image
	#http://docs.opencv.org/modules/core/doc/operations_on_arrays.html#void flip(InputArray src, OutputArray dst, int flipCode)
	
	imagen = cv2.flip(imagen,1)
	
	return imagen

#t0 = t1 = 0
def send_midi_message_9(cuadrantes, nota_inicial=60):
	global t0, t1
	# 1 | 2 | 3
	#-----------
	# 4 | 5 | 6
	#-----------
	# 7 | 8 | 9
	
	#midi objects
	#https://mido.readthedocs.org/en/latest/
	
	#definicion de notas
	c4 = Message("note_on", note=nota_inicial)
	c40 = Message("note_off", note=nota_inicial)
	
	d4 = Message("note_on", note=(nota_inicial+2))
	d40 = Message("note_off", note=(nota_inicial+2))

	e4 = Message("note_on", note=(nota_inicial+4))
	e40 = Message("note_off", note=(nota_inicial+4))
	
	f4 = Message("note_on", note=(nota_inicial+5))
	f40 = Message("note_off", note=(nota_inicial+5))
	
	g4 = Message("note_on", note=(nota_inicial+7))
	g40 = Message("note_off", note=(nota_inicial+7))
	
	a4 = Message("note_on", note=(nota_inicial+9))
	a40 = Message("note_off", note=(nota_inicial+9))
	
	b4 = Message("note_on", note=(nota_inicial+11))
	b40 = Message("note_off", note=(nota_inicial+11))
	
	c5 = Message("note_on", note=(nota_inicial+12))
	c50 = Message("note_off", note=(nota_inicial+12))
	
	d5 = Message("note_on", note=(nota_inicial+14))
	d50 = Message("note_off", note=(nota_inicial+14))
	
	if (1 in cuadrantes):
		output.send(c4)
	else:
		output.send(c40)	
	
	if (2 in cuadrantes):
		output.send(d4)
	else:
		output.send(d40)
		
	if (3 in cuadrantes):
		output.send(e4)
	else:
		output.send(e40)
		
	if (4 in cuadrantes):
		output.send(f4)
	else:
		output.send(f40)
		
	if (5 in cuadrantes):
		output.send(g4)
	else:
		output.send(g40)
		
	if (6 in cuadrantes):
		output.send(a4)
	else:
		output.send(a40)
		
	if (7 in cuadrantes):
		output.send(b4)
	else:
		output.send(b40)
		
	if (8 in cuadrantes):
		output.send(c5)
	else:
		output.send(c50)
		
	if (9 in cuadrantes):
		output.send(d5)
	else:
		output.send(d50)
		
def send_midi_message_4(cuadrantes, nota_inicial=60):
	# 1 | 2 |
	#--------
	# 3 | 4 |
	
	#definicion de notas
	c4 = Message("note_on", note=nota_inicial)
	c40 = Message("note_off", note=nota_inicial)
	
	d4 = Message("note_on", note=(nota_inicial+4))
	d40 = Message("note_off", note=(nota_inicial+4))

	e4 = Message("note_on", note=(nota_inicial+7))
	e40 = Message("note_off", note=(nota_inicial+7))
	
	f4 = Message("note_on", note=(nota_inicial+11))
	f40 = Message("note_off", note=(nota_inicial+11))
	
	if (1 in cuadrantes):
		output.send(c4)
	else:
		output.send(c40)	
	
	if (2 in cuadrantes):
		output.send(d4)
	else:
		output.send(d40)
		
	if (3 in cuadrantes):
		output.send(e4)
	else:
		output.send(e40)
		
	if (4 in cuadrantes):
		output.send(f4)
	else:
		output.send(f40)

def define_note (str_nota):
	if(str_nota == "c"):
		return 60
	elif(str_nota == "d"):
		return 62
	elif(str_nota == "d#"):
		return 63
	elif(str_nota == "e"):
		return 64
	elif(str_nota == "f"):
		return 65
	elif(str_nota == "f#"):
		return 66
	elif(str_nota == "g"):
		return 67
	elif(str_nota == "g#"):
		return 68
	elif(str_nota == "a"):
		return 69
	elif(str_nota == "a#"):
		return 70
	elif(str_nota == "b"):
		return 71
	else:
		print "ERROR: La nota no es correcta"
		return 0

def define_lineas(str_divisiones):
	if(str_divisiones == "4"):
		imagen_lineas = draw_lines_4(image)
		return 1
	elif(str_divisiones == "9"):
		imagen_lineas = draw_lines_9(image)
		return 1
	else:
		print "ERROR: Solamente se puede dividir la pantalla en 4 o en 9"
		return 0
	

if __name__ == "__main__":
	print "Presione 'q' para salir"
			
	output = mido.open_output()	
	while 1:
		image = show_depth()
		
		image = flip_image(image)
		
		rslt_fc = find_centroid(image)
		
		image = rslt_fc['img']
		
		centroides = rslt_fc['centr']
		
		str_nota = sys.argv[1]
		str_divisiones = sys.argv[2]
		
		#### definir divisiones
		bool_lineas = define_lineas(str_divisiones)
		
		### definir notas
		nota_inicial = define_note(str_nota)
		
		if not (nota_inicial and bool_lineas):
			print "Saliendo"
			break
		
		if (centroides==[]):
			send_midi_message_9([])
		
		if centroides:
			if(str_divisiones == "4"):
				cuadrantes = get_cuadrantes_4(centroides)
				send_midi_message_4(cuadrantes, nota_inicial)
			else:
				cuadrantes = get_cuadrantes_9(centroides)
				send_midi_message_9(cuadrantes, nota_inicial)
				
		show_image(image, "matching")
		show_video(image, "matching")
		
		c = cv2.waitKey(10)
		
		if 'q' == chr(c & 255):
			break
			output.close()
