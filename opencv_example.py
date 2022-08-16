#!/usr/bin/python3

import tellopy
import time, cv2
import av
import numpy

tello = tellopy.Tello()
tello.connect()
tello.wait_for_connection(60.0)

retry = 3
container = None
while container is None and 0 < retry:
    retry -= 1
    try:
        container = av.open(tello.get_video_stream())
    except av.AVError as ave:
        print(ave)
        print('retry...')

# skip first 300 frames
frame_skip = 300
while True:
    for frame in container.decode(video=0):
        if 0 < frame_skip:
            frame_skip = frame_skip - 1
            continue
        start_time = time.time()
        image = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2BGR)
        cv2.imshow('EyeInTheSkAi', image)
        cv2.waitKey(1)
        if frame.time_base < 1.0/60:
            time_base = 1.0/60
        else:
            time_base = frame.time_base
        frame_skip = int((time.time() - start_time)/time_base)
