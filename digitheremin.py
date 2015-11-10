#!/usr/bin/env python

from methods import * 

def main():
	print "Presione 'q' para salir"
			
	output = mido.open_output()
	
	nota_anterior = 69
	
	while True:
		#~ msg_inst = Message("program_change", program=36)	
		#~ output.send(msg_inst)
		
		image = show_depth()
		
		image = flip_image(image)
		
		rslt_fc = find_centroid(image)
		
		image = rslt_fc['img']
		
		centroides = rslt_fc['centr']
		
		if (centroides==[]):
			send_midi_message(output, 0, 1, 1, nota_anterior)
			
		if centroides:
			x = centroides[0][0]
			y = centroides[0][1]
		
			nota = position_2_note(x)
		
			nota_entera = np.int(np.floor(nota))
		
			bend = np.int(round(note_2_frec_n_bend(nota)))
			
			send_midi_message(output, 1, nota_entera, bend, nota_anterior)
				
			nota_anterior = nota_entera	
				
		show_image(image, "matching")
		show_video(image, "matching")
		
		c = cv2.waitKey(10)
		
		if 'q' == chr(c & 255):
			break
			output.close()
	
if __name__ == "__main__":
	main()
	
