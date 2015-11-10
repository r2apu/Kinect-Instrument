#!/usr/bin/env python

from methods import *

def main():
	global threshold
	global current_depth
	print "Presione 'q' para salir"
			
	output = mido.open_output()
	stop = Message("control_change",control=123)
		
	while True:
		
		image = show_depth()
		
		image = flip_image(image)
		
		rslt_fc = find_centroid(image)
		
		image = rslt_fc['img']
		
		centroides = rslt_fc['centr']
		
		if (len(sys.argv) == 3):
			str_nota = sys.argv[1]
			str_divisiones = sys.argv[2]
		else:
			print "ERROR: No se indica escala y/o divisiones"
			break
		
		#### definir divisiones
		bool_lineas = define_lineas(str_divisiones, image)
		
		### definir notas
		nota_inicial = define_note(str_nota)
		
		if not (nota_inicial and bool_lineas):
			print "Saliendo"
			break
		
		if (centroides==[]):
			output.send(stop)
			#send_midi_message_9(output,[])
		
		if centroides:
			if(str_divisiones == "4"):
				cuadrantes = get_cuadrantes_4(centroides)
				send_midi_message_4(output,  cuadrantes, nota_inicial)
			else:
				cuadrantes = get_cuadrantes_9(centroides)
				send_midi_message_9(output, cuadrantes, nota_inicial)
				
		show_image(image, "matching")
		show_video(image, "matching")
		
		c = cv2.waitKey(10)
		
		if 'q' == chr(c & 255):			
			output.send(stop)
			output.close()
			break
	

if __name__ == "__main__":
	main()
	
	
