# TODO use tkinter interface to show the preview of the camera
# switch between preview and running
# https://stackoverflow.com/questions/16366857/show-webcam-sequence-tkinter
# use subprocess to communicate with vcam

import tkinter as tk
import cv2
from PIL import Image, ImageTk

width, height = 640, 480
# :( opencv has an issue opening virtual cameras
cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

root = tk.Tk()
root.bind('<Escape>', lambda e: root.quit())
lmain = tk.Label(root)
lmain.pack()

def show_frame():
    success, frame = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      lmain.after(10, show_frame)
      return
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)

show_frame()
root.mainloop()