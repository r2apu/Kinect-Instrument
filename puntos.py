#!/usr/bin/env python

from methods import *

def main():
	while True:
		image = show_depth()
		image = flip_image(image)
		rslt_fc = find_centroid(image)
		image = rslt_fc['img']
		centroides = rslt_fc['centr']
		
		img_punt = gen_image_puntos(centroides)
		
		show_image(image, "depth")
		show_image(img_punt, "puntos")
		
		c = cv2.waitKey(10)
		if 'q' == chr(c & 255):
			break
	

if __name__ == "__main__":
	main()
