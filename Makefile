test:
	freenect-glview

set:
	qjackctl &
	amsynth &

play:	
	python kinect_drumming.py c 9
	
play2:
	python kinect_drumming.py e 4

theremin:
	python digitheremin.py 
	
pitar:
	python pintar.py

pitar2:
	python pintar2.py

efecto:
	python efecto.py
