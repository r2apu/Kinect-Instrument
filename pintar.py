#!/usr/bin/env python

from methods import *

def main():
	lista_centros = []
		
	while True:
		image = show_depth()
		frame = get_real()
		
		image = flip_image(image)
		
		frame = flip_image(frame)
		
		rslt_fc = find_centroid_pinta(image)
		
		image = rslt_fc['img']
		
		centroides = rslt_fc['centr']
		
		lista_centros.extend(centroides)
		
		image = pinta_circulo(image, lista_centros)
		
		lista_centros = limpia_lst_centros(lista_centros, 3)
		
		new_image = convert_BGR(image)
		 
		dst = cv2.add(new_image, frame)
		
		show_image(dst, "final")
		show_video_colors(dst, "final")
		 
		c = cv2.waitKey(10)
		if 'q' == chr(c & 255):
			break


if __name__ == "__main__":
	main()
	
