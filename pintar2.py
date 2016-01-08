#!/usr/bin/env python

from methods import *

def main():
	lista_centros = []
		
	while True:
		image = show_depth()
		
		#~ image = flip_image(image)
		
		rslt_fc = find_centroid_pinta(image)
		
		image = rslt_fc['img']
		
		centroides = rslt_fc['centr']
		
		lista_centros.extend(centroides)
		
		image = pinta_circulo(image, lista_centros, 5)
		
		lista_centros = limpia_lst_centros(lista_centros)						
	
		show_image(image, "")
		show_video(image, "control")			
				
		c = cv2.waitKey(100)
		if 'q' == chr(c & 255):
			break


if __name__ == "__main__":
	main()
	
