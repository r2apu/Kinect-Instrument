#!/usr/bin/env python

import freenect
import cv
import cv2
import numpy as np

threshold = 100
current_depth = 480

color_R = 255
color_G = 0
color_B = 0


def change_threshold(value):
    global threshold
    threshold = value

def change_depth(value):
    global current_depth
    current_depth = value

def change_color_R(value):
    global color_R
    color_R = value

def change_color_G(value):
    global color_G
    color_G = value

def change_color_B(value):
    global color_B
    color_B = value
    
def show_depth():
	global threshold
	global current_depth

	depth, timestamp = freenect.sync_get_depth()
	
	depth = 255 * np.logical_and(depth >= current_depth - threshold, depth <= current_depth + threshold)
	
	depth = depth.astype(np.uint8)
	
	return depth

def show_video(image, image_name):	
	cv2.namedWindow(image_name)
	cv2.createTrackbar(image_name + ' R', image_name, color_R, 255, change_color_R)
	cv2.createTrackbar(image_name + ' G', image_name, color_G, 255, change_color_G)
	cv2.createTrackbar(image_name + ' B', image_name, color_B, 255, change_color_B)
	
def flip_image(imagen):
	imagen = cv2.flip(imagen,1)
	return imagen

def show_image(imagen, mensaje):
	cv2.imshow(mensaje, imagen)

def find_centroid(imagen):
	ret, thres = cv2.threshold(imagen, 127,255,0)
		
	contours, hier = cv2.findContours(thres, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)	
	
	list_centros = []
	
	for cnt in contours:
		if 1000 < cv2.contourArea(cnt) < 10000:
			cv2.drawContours(imagen,[cnt],0,(0,0,55),2)
			M = cv2.moments(cnt)
			
			if (int(M['m00'])!=0):
				centro = (int(M['m10']/M['m00']),int(M['m01']/M['m00']))						
				#cv2.circle(imagen, centro, 16, 100, -1)
				list_centros.append([centro, (color_R, color_G, color_B)])		
	
	return {'img':imagen, 'centr':list_centros}


def pinta_circulo(imagen, list_centros):
	for i in range(len(list_centros)):
		cv2.circle(imagen, list_centros[i][0], 16, list_centros[i][1], -1)
	
	return imagen

if __name__ == "__main__":
	lista_centros = []
		
	while 1:
		image = show_depth()
		
		show_image(image, "depth")
		
		image = flip_image(image)
		
		rslt_fc = find_centroid(image)
		
		image = rslt_fc['img']
		
		centroides = rslt_fc['centr']
		
		lista_centros.extend(centroides)
		
		image = pinta_circulo(image, lista_centros)
				
		show_image(image, "pintar")
		show_video(image, "pintar")
		 
		c = cv2.waitKey(10)
		if 'q' == chr(c & 255):
			break
