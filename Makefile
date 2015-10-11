set:
	qjackctl &
	amsynth &

play:	
	python kinect_drumming/kinect_drumming.py c 9
	
play2:
	python kinect_drumming/kinect_drumming.py e 4

theremin:
	python theremin/digitheremin.py 
	
pitar:
	python pintar/pintar.py
