#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Benjamin Dotse
"""
import cv2
import numpy as np

draw = True
fill = 2
brush = 0
window_name = "Paint Brush Application"
bgr_track = {'B': 255, 'G': 255, 'R': 255}

img = np.zeros((450, 800, 3), np.uint8)
cv2.namedWindow(window_name)
shape = "rectangle"

font = cv2.FONT_HERSHEY_SIMPLEX


def nothing(x):
    pass


def update_brush(x):
    global brush
    brush = x


def update_fill(x):
    global fill
    if x == 1:
        fill = -1
    else:
        fill = 2


def update_R_value(x):
    global bgr_track
    bgr_track['R'] = x


def update_G_value(x):
    global bgr_track
    bgr_track['G'] = x


def update_B_value(x):
    global bgr_track
    bgr_track['B'] = x


def draw(event, x, y, flags, param):

    global draw, img, shape, fill, brush

    bSize = cv2.getTrackbarPos("Brush Size", window_name)

   # draw rectangle/circle on double tap
    if event == cv2.EVENT_LBUTTONDBLCLK:
        if shape == "rectangle":
            cv2.rectangle(img, (x, y), (x+40, y+20),
                          (cv2.getTrackbarPos("B", window_name),
                           cv2.getTrackbarPos("G", window_name),
                           cv2.getTrackbarPos("R", window_name)),
                          fill)

        elif shape == "circle":
            cv2.circle(img, (x, y), 20,
                       (cv2.getTrackbarPos("B", window_name),
                        cv2.getTrackbarPos("G", window_name),
                        cv2.getTrackbarPos("R", window_name)),
                       fill)

    elif event == cv2.EVENT_LBUTTONDOWN:
        draw = True

    elif event == cv2.EVENT_MOUSEMOVE:
        if draw:
            # Rectangle Brush
            if brush == 1:
                cv2.rectangle(img, (x, y), (x + (bSize + 4), y + (bSize + 2)),
                              (cv2.getTrackbarPos("B", window_name),
                               cv2.getTrackbarPos("G", window_name),
                               cv2.getTrackbarPos("R", window_name)),
                              fill)
            # Diamond Brush
            elif brush == 2:
                pts = np.array([[x, y], [x-(bSize + 2), y+(bSize + 2)], [x, y+(bSize + 13)],
                               [x+(bSize + 2), y+(bSize + 2)]], np.int32)
               # pts = pts.reshape((-1, 1, 2))

                if fill == -1:
                    cv2.fillPoly(img, [pts], (cv2.getTrackbarPos("B", window_name),
                                              cv2.getTrackbarPos(
                                                  "G", window_name),
                                              cv2.getTrackbarPos("R", window_name)))
                else:
                    cv2.polylines(img, [pts], True, (cv2.getTrackbarPos("B", window_name),
                                                     cv2.getTrackbarPos(
                                                         "G", window_name),
                                                     cv2.getTrackbarPos("R", window_name)))

            # Circle Brush
            else:
                cv2.circle(img, (x, y), cv2.getTrackbarPos("Brush Size", window_name),
                           (cv2.getTrackbarPos("B", window_name),
                            cv2.getTrackbarPos("G", window_name),
                            cv2.getTrackbarPos("R", window_name)),
                           fill)

    elif event == cv2.EVENT_LBUTTONUP:
        draw = False


cv2.createTrackbar("R", window_name, 0, 255, update_R_value)
cv2.createTrackbar("G", window_name, 0, 255, update_G_value)
cv2.createTrackbar("B", window_name, 0, 255, update_B_value)
cv2.createTrackbar("Brush Size", window_name, 1, 10, nothing)
cv2.createTrackbar("Fill: 0=No-Fill 1=Fill", window_name, 1, 1, update_fill)
cv2.createTrackbar("Brush Type: 0=Circle 1=Rectangle 2=Diamond",
                   window_name, 0, 2, update_brush)
cv2.setMouseCallback(window_name, draw)


while(1):
    cv2.imshow(window_name, img)
    key = cv2.waitKey(1) & 0xff
    if key == ord('q'):
        break
    elif key == ord('r'):
        img[:] = (0, 0, 0)
    elif key == ord('c'):
        if shape == "rectangle":
            shape = "circle"
        else:
            shape = "rectangle"

    b = cv2.getTrackbarPos("B", window_name)
    g = cv2.getTrackbarPos("G", window_name)
    r = cv2.getTrackbarPos("R", window_name)
    cv2.rectangle(img,  (5, 425), (40, 440), (b, g, r), -1)
    cv2.putText(img, "c: Change shape", (510, 440),
                font, 0.5, (255, 255, 255), 1)
    cv2.putText(img, "r: Reset", (660, 440),
                font, 0.5, (255, 255, 255), 1)
    cv2.putText(img, "q: Quit", (740, 440),
                font, 0.5, (255, 255, 255), 1)
cv2.destroyAllWindows()
