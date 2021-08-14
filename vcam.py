import cv2
import os
import numpy as np
import pyvirtualcam as pv

import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_selfie_segmentation = mp.solutions.selfie_segmentation

indexImg = 0
threshold = 0.58
exposure = 0
BG_COLOR = (255, 0, 255)
VIDEO_SIZE = (1280, 720)
SEGMENTATION_MODEL = 0 # or 1

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, VIDEO_SIZE[0])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, VIDEO_SIZE[1])

# load background images
listImg = os.listdir("bgImages")
imgList = []
for imgPath in listImg:
    img = cv2.resize(cv2.imread(f'bgImages/{imgPath}'), VIDEO_SIZE)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img.flags.writeable = False
    imgList.append(img)

fallback_image = np.zeros(imgList[0].shape, dtype=np.uint8)
fallback_image[:] = BG_COLOR

with mp_selfie_segmentation.SelfieSegmentation(model_selection=SEGMENTATION_MODEL) as selfie_segmentation, \
    pv.Camera(width=VIDEO_SIZE[0], height=VIDEO_SIZE[1], fps=24) as cam:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue

    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = selfie_segmentation.process(image)

    mask = results.segmentation_mask
    # mask = cv2.bilateralFilter(mask, 10, 100, 100)
    mask = cv2.blur(mask, (8, 8))
    mask_rgb = np.stack((mask,) * 3, axis=-1)
    mask_rgb_inverse = 1.0 - mask_rgb
    condition = mask_rgb > threshold

    # image.flags.writeable = True
    # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    output_image = np.where(condition, image, imgList[0])
    # output_image = cv2.convertScaleAbs(cv2.multiply(mask_rgb, np.float32(image)/256) + np.multiply(mask_rgb_inverse, np.float32(imgList[0])/256), alpha=256)
    
    # cv2.imshow('MediaPipe Selfie Segmentation', output_image)
    # key = cv2.waitKey(5)
    # if key == ord('q'): 
    #    break
    cam.send(output_image)
    cam.sleep_until_next_frame()
cap.release()
