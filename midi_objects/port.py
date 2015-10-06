#!/usr/bin/env python

import mido
from mido import Message
import time

#midi objects
#https://mido.readthedocs.org/en/latest/

output = mido.open_output()

c4 = Message("note_on", note=60)
c40 = Message("note_off", note=60)
#c4 = Message("note_on", note=60, velocity=64)
f4 = Message("note_on", note=65)
f40 = Message("note_off", note=65)
#f4 = Message("note_on", note=65, velocity=64)
g4 = Message("note_on", note=67)
g40 = Message("note_off", note=67)
#g4 = Message("note_on", note=67, velocity=64)

output.send(c4)
time.sleep(1)
output.send(c40)

output.send(f4)
time.sleep(1)
output.send(f40)

output.send(g4)
time.sleep(1)
output.send(g40)

output.close()
