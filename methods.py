import freenect
import cv2
import numpy as np

import mido
from mido import Message

import time
import sys

#-------------------------PARAMETERS------------------------------------

threshold = 100
current_depth = 480

color_R = 255
color_G = 0
color_B = 0

# -- algunos colores
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)

# -- matriz de puntos
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
 
CANT_PUNTOS_X = 20
CANT_PUNTOS_Y = 20

# matriz de puntos
i = 0
pos_PUNTOS_X = []

while i<CANT_PUNTOS_X:
	pos_PUNTOS_X.append(i*SCREEN_WIDTH/CANT_PUNTOS_X)
	i += 1

j = 0
pos_PUNTOS_Y = []	

while j<CANT_PUNTOS_Y:
	pos_PUNTOS_Y.append(i*SCREEN_HEIGHT/CANT_PUNTOS_Y+1)
	j += 1

#-----------------------------------------------------------------------

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

	depth = freenect.sync_get_depth()[0]
	depth = 255 * np.logical_and(depth >= current_depth - threshold, depth <= current_depth + threshold)
	depth = depth.astype(np.uint8)
	
	return depth

def def_plane(threshold,current_depth):
	
	depth = freenect.sync_get_depth()[0]	
	depth = 255 * np.logical_and(depth >= current_depth, depth <= current_depth + threshold)
	depth = depth.astype(np.uint8)
	
	return depth
	
def show_video(image, image_name):	
	cv2.namedWindow(image_name)
	cv2.createTrackbar(image_name + ' threshold', image_name, threshold, 1000, change_threshold)
	cv2.createTrackbar(image_name + ' depth', image_name, current_depth, 1000, change_depth)

def show_video_colors(image, image_name):
	global color_R
	global color_G
	global color_B
		
	cv2.namedWindow(image_name)
	cv2.createTrackbar(image_name + ' R', image_name, color_R, 255, change_color_R)
	cv2.createTrackbar(image_name + ' G', image_name, color_G, 255, change_color_G)
	cv2.createTrackbar(image_name + ' B', image_name, color_B, 255, change_color_B)
	
def show_image(imagen, mensaje):
	cv2.imshow(mensaje, imagen)

def flip_image(imagen):
	#mirror image
	#http://docs.opencv.org/modules/core/doc/operations_on_arrays.html#void flip(InputArray src, OutputArray dst, int flipCode)
	imagen = cv2.flip(imagen,1)
	
	return imagen
	
def show_ent_depth():
	depth = freenect.sync_get_depth()[0]
	depth = depth.astype(np.uint8)
	
	#~ print "depth "+str(np.shape(depth))
	
	return depth

def get_real():
    array = freenect.sync_get_video()[0]
    
    #~ print "real "+str(np.shape(array))
    
    array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
    #array = cv2.cvtColor(array,cv2.COLOR_RGB2GRAY)
    return array
	
def convert_gray(array):
	array = cv2.cvtColor(array,cv2.COLOR_RGB2GRAY)
	return array

def convert_RGB(array):
	array = cv2.cvtColor(array,cv2.COLOR_BGR2RGB)
	return array
	
def convert_BGR(array):
	
	array = cv2.cvtColor(array, cv2.COLOR_GRAY2BGR)
	
	return array

def find_centroid_pinta(imagen, max_contours=100000):
	global color_R
	global color_G
	global color_B
	
	ret, thres = cv2.threshold(imagen, 127,255,0)
		
	contours = cv2.findContours(thres, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]	
	
	list_centros = []
	
	for cnt in contours:
		if 1000 < cv2.contourArea(cnt) < max_contours:
			cv2.drawContours(imagen,[cnt],0,(0,0,55),2)
			M = cv2.moments(cnt)
			
			if (int(M['m00'])!=0):
				centro = (int(M['m10']/M['m00']),int(M['m01']/M['m00']))						
				#cv2.circle(imagen, centro, 16, 100, -1)
				list_centros.append([centro, (color_R, color_G, color_B),time.clock()])		
				#~ list_centros.append([centro, red])		
	
	return {'img':imagen, 'centr':list_centros}
		
def find_centroid(imagen, max_contours=100000):
	#http://stackoverflow.com/questions/10262600/how-to-detect-region-of-large-of-white-pixels-using-opencv

	ret, thres = cv2.threshold(imagen, 127,255,0)
		
	contours = cv2.findContours(thres, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]
	
	list_centros = []
	
	for cnt in contours:
		if 1000 < cv2.contourArea(cnt) < max_contours:
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

def pinta_circulo(imagen, list_centros, radio=16):
	for i in range(len(list_centros)):
		cv2.circle(imagen, list_centros[i][0], radio, list_centros[i][1], -1)
	
	return imagen

def limpia_lst_centros(list_centros, duracion=1):
	if list_centros == []:
		return []
	else:	
		nuev_list_centros=[]
		for i in range(len(list_centros)):
			if ( time.clock()-list_centros[i][2] < duracion ):
				nuev_list_centros.append(list_centros[i])
		return nuev_list_centros

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

#-----------------------MIDI MEthods------------------------------------

def send_midi_message_9(output, cuadrantes, nota_inicial=60):
	
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
		
def send_midi_message_4(output, cuadrantes, nota_inicial=60):
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

def send_midi_message(output, on, nota_entera, bend, nota_anterior):
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

def define_note (str_nota):
	if(str_nota == "c"):
		return 60
	elif(str_nota == "c#"):
		return 61
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
		print "ERROR: La nota incial no es correcta"
		return 0

def define_lineas(str_divisiones, image):
	if(str_divisiones == "4"):
		imagen_lineas = draw_lines_4(image)
		return 1
	elif(str_divisiones == "9"):
		imagen_lineas = draw_lines_9(image)
		return 1
	else:
		print "ERROR: Solamente se puede dividir la pantalla en 4 o en 9"
		return 0

def position_2_note(pos_x):
	#Se mapea la posici'on x a notas
		# la posici'on 0 representa la nota A0 (nota 21)
		# la posici'on 640 representa la nota B7 (nota 107)
	#La ecuaci'on de la recta es la siguiente:
		# nota = 0.134375*posicion_x+21
	
	#~ nota = 0.134375*pos_x+21
	nota = 0.134375*pos_x+41
	
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

#--------------------IMAGE GENERATION-----------------------------------
def gen_image_puntos(centroides):
	ancho_de_punto = 4
	
	local_threshold_x = 40
	local_threshold_y = 40
	
	img_puntos = np.zeros((480,640,3), np.uint8)
		
	for circ_x in pos_PUNTOS_X:
		for circ_y in pos_PUNTOS_X:
			if centroides == []:
				cv2.circle(img_puntos, (circ_x,circ_y), 4, red, -1)
			else:
				for i in range(len(centroides)):
					x = centroides[i][0]
					y = centroides[i][1]
				
					if (np.logical_and(x <= circ_x +local_threshold_x, x >= circ_x -local_threshold_x) and np.logical_and(y <= circ_y +local_threshold_y, y >= circ_y -local_threshold_y)):
						if x <= circ_x +local_threshold_x:
							cv2.circle(img_puntos, (circ_x,circ_y+(-(1/4)*(circ_x-x)+20)), ancho_de_punto, red, -1)
						else:
							cv2.circle(img_puntos, (circ_x,circ_y-(-(1/4)*(circ_x-x)+20)), ancho_de_punto, red, -1)
					else:
						cv2.circle(img_puntos, (circ_x,circ_y), ancho_de_punto, red, -1)
				
	return img_puntos
