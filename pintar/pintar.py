#!/usr/bin/env python

import freenect
import cv
import cv2
import numpy as np

threshold = 100
current_depth = 480

def video_cv(video):
    video = video[:, :, ::-1]  # RGB -> BGR
    image = cv.CreateImageHeader((video.shape[1], video.shape[0]),cv.IPL_DEPTH_8U,3)
    cv.SetData(image, video.tostring(),video.dtype.itemsize * 3 * video.shape[1])
    return image

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
	
def get_depth():
	depth, timestamp = freenect.sync_get_depth()
	depth = depth.astype(np.uint8)
	
	return depth
	
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
			cv2.drawContours(imagen,[cnt],0,(200,255,200),2)
			contorno = contours[0]
			M = cv2.moments(cnt)
			
			if (int(M['m00'])!=0):
				centro = (int(M['m10']/M['m00']),int(M['m01']/M['m00']))						
				#cv2.circle(imagen, centro, 16, 100, -1)
				list_centros.append(centro)		
	
	return {'img':imagen, 'centr':list_centros}


def pinta_circulo(imagen, list_centros):
	for i in range(len(list_centros)):
		cv2.circle(imagen, list_centros[i], 16, (210,200,255), -1)
	
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
		 
		c = cv2.waitKey(10)
		if 'q' == chr(c & 255):
			break
