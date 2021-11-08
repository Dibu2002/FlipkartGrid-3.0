import cv2
import cv2.aruco as aruco
import numpy as np
import imutils
import json
from qr import detectMarker


def angle(a, b, c):
    ang = degrees(atan2(c[1] - b[1], c[0] - b[0]) - atan2(a[1] - b[1], a[0] - b[0]))
    return ang


def displacement(x, y, a, b):
    disp = abs(((x - a) ** 2 + (y - b) ** 2) ** (1 / 2))
    return disp

# def detectMarker(img, markerSize=4, totalMarker=50, draw=True):
#     imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarker}')
#     arucoDict = aruco.Dictionary_get(key)

#     arucoParam = aruco.DetectorParameters_create()
#     bbox, ids, rejected = aruco.detectMarkers(imgGray, arucoDict, parameters=arucoParam)
    
#     return [bbox, ids, center]


cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap.set(3, 1420)
cap.set(4, 800)

width=1420
height=800

cx, cy = 0, 0
py = 250
while True:
    _, frame = cap.read()

    pts1 = np.float32([[74, 68], [1193, 47], [7, 644], [1272, 664]])
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    frame = cv2.warpPerspective(frame, matrix, (width, height))


    arucoDetected = detectMarker(frame)

    center = arucoDetected[2]
    if center is not None:
        for i in center:
            frame = cv2.circle(frame, i, 7, (0, 255, 0), -1)
            cx, cy = i

    
    print(f'cx = {cx} and cy = {cy}')
    h = min(60, (cx - py // 6))

    
    h1 = str(min(30, (cx - py // 6)))
    h2 = str(min(60, (cx - py // 6)))
    h = str(max(0, h))
    
    h = '0'*(3-len(h)) + h
    h1 = '0'*(3-len(h1)) + h1
    h2 = '0'*(3-len(h2)) + h2
    if cy > py:
        tranx = 3
        dictionary = {'func': f'0101{h2}{h1}'}
        print ("For ward")
    # elif shortestAngle >= 1:
    #     tranx = 2
        
    #     print ("Turn Right")
    #     dictionary = {'func': f'1010{h1}{h2}'}
    # elif shortestAngle < 1:
    #     tranx = 4
    #     dictionary = {'func': f'1010{h2}{h1}'}
    #     print ("Turn Left")
    else:
        dictionary = {'func': '0000000000'}
        



    json_object = json.dumps(dictionary, indent=4)
    print(json_object)
    with open("data.json", "w") as file:
        file.write(json_object)


    cv2.imshow("result", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
cv2.destroyAllWindows()
