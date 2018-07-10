import cv2

import numpy as np
import StringIO
import datetime
import pytz
from math import cos, sin
from pprint import pprint
#from skvideo.io import VideoWriter

import angus

def main():
    #angus.con
    conn = angus.connect("https://gate.angus.ai", )
    service = conn.services.get_service("scene_analysis", version=1)
    service.enable_session()
    try:
        camera = cv2.VideoCapture("/Users/rafiahmed/Downloads/GOPR1379.MP4")
        print("Video stream is of resolution {} x {}".format(camera.get(3), camera.get(4)))
        #camera.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 640)
        #camera.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480)
        #camera.set(cv2.cv.CV_CAP_PROP_FPS, 10)
    except:
        print "CV2 Bombed"
        return
    #video = skvideo.io.VideoCapture("/Users/rafiahmed/Downloads/GOPR1379.mp4")
    ret, frame = camera.read()
    i = 0
    while(ret):
        ret, frame = camera.read()
        cv2.imshow("Frame", frame)

        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, buff = cv2.imencode(".jpg", gray, [cv2.IMWRITE_JPEG_QUALITY, 80])
        buff = StringIO.StringIO(np.array(buff).tostring())
        t = datetime.datetime.now(pytz.utc)
        #print("Calling service")
        #job = service.process({"image": buff,
        #                       "timestamp": t.isoformat()
        #                       })

        job = service.process({"image": buff,
                               "timestamp": t.isoformat(),
                               "camera_position": "ceiling",
                               "sensitivity": {
                                   "appearance": 0.7,
                                   "disappearance": 0.7,
                                   "age_estimated": 0.4,
                                   "gender_estimated": 0.5,
                                   "focus_locked": 0.9,
                                   "emotion_detected": 0.4,
                                   "direction_estimated": 0.8
                               }
                               })

        #print("Called service")
        res = job.result
        pprint(res)
        if "error" in res:
            print("Bomb")
            print(res["error"])
        else:
            # This parses the entities data
            print("No Bomb")
            for key, val in res["entities"].iteritems():
                print("Iterating")
                # display only gaze vectors
                # retrieving eyes points
                eyel, eyer = val["face_eye"]
                eyel = tuple(eyel)
                eyer = tuple(eyer)

                # retrieving gaze vectors
                psi = 0
                g_yaw, g_pitch = val["gaze"]
                theta = - g_yaw
                phi = g_pitch

                # Computing projection on screen
                # and drawing vectors on current frame
                length = 150
                xvec = int(length * (sin(phi) * sin(psi) - cos(phi) * sin(theta) * cos(psi)))
                yvec = int(- length * (sin(phi) * cos(psi) - cos(phi) * sin(theta) * sin(psi)))
                cv2.line(frame, eyel, (eyel[0] + xvec, eyel[1] + yvec), (0, 140, 0), 3)

                xvec = int(length * (sin(phi) * sin(psi) - cos(phi) * sin(theta) * cos(psi)))
                yvec = int(- length * (sin(phi) * cos(psi) - cos(phi) * sin(theta) * sin(psi)))
                cv2.line(frame, eyer, (eyer[0] + xvec, eyer[1] + yvec), (0, 140, 0), 3)
                i = i+1
                print (str("Frame: ") + str(i))
        cv2.imshow('original', frame)
        service.disable_session()
if __name__ == '__main__':
    main()











