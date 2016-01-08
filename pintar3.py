#!/usr/bin/env python

from methods import *

def main():
	lista_centros = []
	img = np.zeros((480,640,3), np.uint8)	
	while True:
		image = show_depth()		
		image = flip_image(image)		
		image = draw_lines_9(image)
		
		rslt_fc = find_centroid(image, 10000)
		
		image = rslt_fc['img']
		
		centroides = rslt_fc['centr']
		
		show_image(image, "depth")
		show_video(image, "depth")
		
		cuadrantes = []
		
		if centroides:
			cuadrantes = get_cuadrantes_9(centroides)
			
		if (1 in cuadrantes):
			azul = draw_rect(img, blue)
			show_image(azul, "")
		elif(2 in cuadrantes):
			otro3 = draw_rect(img, smColor3)
			show_image(otro3, "")
		elif(3 in cuadrantes):
			oscazul = draw_rect(img, white)
			show_image(oscazul, "")
		elif(4 in cuadrantes):
			rojo = draw_rect(img, red)
			show_image(rojo, "")
		elif(5 in cuadrantes):
			blanco = draw_rect(img, darkBlue)
			show_image(blanco, "")
		elif(6 in cuadrantes):
			rosado = draw_rect(img, pink)
			show_image(rosado, "")
		elif(7 in cuadrantes):
			otro1 = draw_rect(img, smColor1)
			show_image(otro1, "")
		elif(8 in cuadrantes):
			otro2 = draw_rect(img, smColor2)
			show_image(otro2, "")
		elif(9 in cuadrantes):
			verde = draw_rect(img, green)
			show_image(verde, "")
		else:
			negro = draw_rect(img, black)
			show_image(negro, "")
		
		c = cv2.waitKey(10)
		if 'q' == chr(c & 255):
			break

if __name__ == "__main__":
	main()
	
