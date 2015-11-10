#!/usr/bin/env python

from methods import *

def main():
	lista_centros = []
		
	while True:
		image = show_depth()
		frame = get_real()
		
		image = flip_image(image)
		frame = flip_image(frame)
		
		image = draw_lines_9(image)
		
		rslt_fc = find_centroid(image, 10000)
		
		image = rslt_fc['img']
		
		centroides = rslt_fc['centr']
		
		show_image(image, "depth")
		
		cuadrantes = []
		
		if centroides:
			cuadrantes = get_cuadrantes_9(centroides)
			
		if (2 in cuadrantes):
			frame_db = show_ent_depth()
			frame_db = flip_image(frame_db)
			show_image(frame_db, "real")
			show_video(frame_db, "real")
		elif(6 in cuadrantes):
			frame_gray = convert_gray(frame)
			show_image(frame_gray, "real")
			show_video(frame_gray, "real")
		elif(9 in cuadrantes):
			frame_pit = convert_RGB(frame)
			show_image(frame_pit, "real")
			show_video(frame_pit, "real")
		else:
			show_image(frame, "real")
			show_video(frame, "real")
		
		c = cv2.waitKey(10)
		if 'q' == chr(c & 255):
			break

if __name__ == "__main__":
	main()
