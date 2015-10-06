#!/usr/bin/env python

import freenect
import cv
import cv2
import numpy as np

import mido
from mido import Message

import time

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
	
	#grises = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
	
	ret, thres = cv2.threshold(imagen, 127,255,0)
		
	contours, hier = cv2.findContours(thres, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)	
	
	#print str(contours)+"\n"
	
	list_centros = []
	
	for cnt in contours:
		if 1000 < cv2.contourArea(cnt) < 100000:
			cv2.drawContours(imagen,[cnt],0,(200,255,200),2)
			
			#centroide	
			#http://docs.opencv.org/master/dd/d49/tutorial_py_contour_features.html#gsc.tab=0
			contorno = contours[0]
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

def show_image(imagen, mensaje):
	
	cv2.imshow(mensaje, imagen)

def flip_image(imagen):
	#mirror image
	#http://docs.opencv.org/modules/core/doc/operations_on_arrays.html#void flip(InputArray src, OutputArray dst, int flipCode)
	
	imagen = cv2.flip(imagen,1)
	
	return imagen

def send_midi_message(cuadrantes):
	global t0, t1
	# 1 | 2 | 3
	#-----------
	# 4 | 5 | 6
	#-----------
	# 7 | 8 | 9
	
	#midi objects
	#https://mido.readthedocs.org/en/latest/
	
	#definicion de notas
	c4 = Message("note_on", note=60)
	c40 = Message("note_off", note=60)
	
	d4 = Message("note_on", note=62)
	d40 = Message("note_off", note=62)

	e4 = Message("note_on", note=64)
	e40 = Message("note_off", note=64)
	
	f4 = Message("note_on", note=65)
	f40 = Message("note_off", note=65)
	
	g4 = Message("note_on", note=67)
	g40 = Message("note_off", note=67)
	
	a4 = Message("note_on", note=69)
	a40 = Message("note_off", note=69)
	
	b4 = Message("note_on", note=71)
	b40 = Message("note_off", note=71)
	
	c5 = Message("note_on", note=72)
	c50 = Message("note_off", note=72)
	
	d5 = Message("note_on", note=74)
	d50 = Message("note_off", note=74)
	
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

if __name__ == "__main__":
	print "Presione 'q' para salir"
			
	output = mido.open_output()	
	while 1:
		image = show_depth()
		
		image = flip_image(image)
		
		rslt_fc = find_centroid(image)
		
		image = rslt_fc['img']
		
		centroides = rslt_fc['centr']
		
		imagen_lineas = draw_lines_9(image)
		
		if (centroides==[]):
			send_midi_message([])
		
		if centroides:
			cuadrantes = get_cuadrantes_9(centroides)
			send_midi_message(cuadrantes)
				
		show_image(image, "matching")
		show_video(image, "matching")
		
		c = cv2.waitKey(10)
		
		if 'q' == chr(c & 255):
			break
	output.close()
