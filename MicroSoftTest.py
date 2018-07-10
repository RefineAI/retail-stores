import cognitive_face as CF

import json
import operator
import numpy as np
import operator
import cv2

Key = "15d101488ccd49f0aa7735ca0a022a8a"
CF.Key.set(Key)

emotions = ["Anger", "Contempt", "Disgust", "Fear", "Happiness", "Neutral", "Sadness", "Surprise"]

def getResponse(img_url):
    data = {}
    resp = None
    try:
        print "In MS: " + "Looking for " + img_url
        result = CF.face.detect(img_url, False, True, 'age,gender,emotion,headPose' )
        resp = json.loads(json.dumps(result))
        print resp
    except Exception:
        print "Error invoking Microsoft Service" + str(Exception)
    if resp:
        data["strongestEmotion"] =  max(data.iteritems(), key=operator.itemgetter(1))[0]
        arr_list = getEmotionArray(data)
        data["class"] = max(arr_list)
        data["gender"] = resp[0]["faceAttributes"]["gender"]
        data["age"] = resp[0]["faceAttributes"]["age"]
        #da
        return data


def getEmotionArray(data):
    listing = []
    listing.append(data["Anger"])
    listing.append(data["Contempt"])
    listing.append(data["Disgust"])
    listing.append(data["Fear"])
    listing.append(data["Happiness"])
    listing.append(data["Neutral"])
    listing.append(data["Sadness"] )
    listing.append(data["Surprise"] )

    return listing
