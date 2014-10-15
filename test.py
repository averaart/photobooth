import Tkinter as tk
import cv2
from PIL import Image, ImageTk
from datetime import datetime


# A simple version of camera capture using OpenCv and Tkinter:
# http://stackoverflow.com/a/23553802

# Motion detection using a webcam, Python, OpenCV and Differential Images
# http://www.steinm.com/blog/motion-detection-webcam-python-opencv-differential-images/


colorCode = cv2.COLOR_BGR2RGB

cap = cv2.VideoCapture(0)
target_size = (10, 10)
t_minus = cv2.resize(cv2.cvtColor(cap.read()[1], cv2.COLOR_RGB2GRAY), target_size)
t = cv2.resize(cv2.cvtColor(cap.read()[1], cv2.COLOR_RGB2GRAY), target_size)
display_image = cap.read()[1]
t_plus = cv2.resize(cv2.cvtColor(display_image, cv2.COLOR_RGB2GRAY), target_size)


def save_image(event):
    global display_image
    cv2.imwrite(datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg", display_image)


def diffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)


def show_frame():
    global t, t_plus, t_minus, display_image

    # Read next image
    t_minus = t
    t = t_plus
    display_image = cap.read()[1]
    display_image = cv2.flip(display_image, 1)
    t_plus = cv2.resize(cv2.cvtColor(display_image, cv2.COLOR_RGB2GRAY), target_size)

    diff_img = diffImg(t_minus, t, t_plus)
    movement = sum([sum(k) for k in diff_img]) / (len(diff_img) * len(diff_img[0]))
    if movement > 2:
        print "Haha, you moved!"
    converted = cv2.cvtColor(display_image, colorCode)
    img = Image.fromarray(converted)
    img_resize = img.resize((w, new_height), Image.ANTIALIAS)
    imgtk = ImageTk.PhotoImage(image=img_resize)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(40, show_frame)


root = tk.Tk()
root.configure(background='black')

w, h = root.winfo_screenwidth(), root.winfo_screenheight()
img_width = len(display_image[0])
img_height = len(display_image)
new_height = int(float(img_height) / float(img_width) * float(w))

root.wm_attributes('-fullscreen', 1)
root.wm_attributes('-modified', 1)
root.deiconify()
root.bind('<Escape>', lambda e: root.quit())
root.bind('<space>', save_image)

lmain = tk.Label(root)
lmain.pack()

show_frame()
root.mainloop()

diff_img = diffImg(t_minus, t, t_plus)
