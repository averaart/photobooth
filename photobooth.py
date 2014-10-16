from Tkinter import *
from datetime import datetime, timedelta
from PIL import Image, ImageTk
import piggyphoto as pp
import cv2


class WebCam:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def get_preview(self):
        return self.cap.read()[1]

    def get_picture(self):
        filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
        cv2.imwrite(filename, self.get_preview())
        return filename

class DSLR:
    def __init__(self):
        self.cam = pp.Camera()
        self.cam.leave_locked()

    def get_preview(self):
        preview = self.cam.capture_preview("preview.jpg")
        return cv2.imread("preview.jpg")

    def get_picture(self):
        filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
        self.cam.set_config()
        self.cam.capture_image(filename)
        return filename


class PhotoBooth:
    def __init__(self, parent):
        self.COUNTDOWN = 6
        self.DISPLAY_LATEST = 6
        self.capture_device = self.get_camera()

        # Calculate ideal size for images
        w = root.winfo_screenwidth()
        h = root.winfo_screenheight()
        test_image = self.capture_device.get_preview()
        img_width = len(test_image[0])
        img_height = len(test_image)
        new_height = int(float(img_height) / float(img_width) * float(w))
        self.target_size = (w, new_height)

        # Setup the TK instance and its bindings
        self.parent = parent
        self.parent.bind('<Escape>', lambda e: root.quit())
        self.parent.bind('<space>', self.set_next_picture)

        # Setup the content container
        self.text_display = StringVar()
        self.container = Label(self.parent)
        self.container.configure(
            width=w,
            height=h,
            background="black",
            foreground="white",
            font=("Helvetica", 256),
            textvariable=self.text_display,
            compound=CENTER)
        self.container.pack()

        self.next_picture_time = None
        self.next_picture_seconds = 0
        self.display_latest_until = None
        self.latest_filename = None

        # kick off heartbeat
        self.heartbeat()

    def heartbeat(self):

        # See if it's time to take a picture
        if self.next_picture_time is not None:
            next_picture_seconds = (self.next_picture_time - datetime.now()).seconds
            if next_picture_seconds is not self.next_picture_seconds:
                self.next_picture_seconds = next_picture_seconds
                self.text_display.set(self.next_picture_seconds)
            if next_picture_seconds == 0:
                self.next_picture_time = None
                self.text_display.set("")
                self.latest_filename = self.capture_device.get_picture()
                self.display_latest_until = datetime.now() + timedelta(seconds=self.DISPLAY_LATEST)
                image = Image \
                    .open(self.latest_filename) \
                    .transpose(Image.FLIP_LEFT_RIGHT) \
                    .resize(self.target_size, Image.ANTIALIAS)
                display_image = ImageTk.PhotoImage(image)
                self.container.imgtk = display_image
                self.container.configure(image=display_image)

        if self.display_latest_until is None:
            # Capture preview
            preview = self.capture_device.get_preview()
            # Fix color
            preview = cv2.cvtColor(preview, cv2.COLOR_BGR2RGB)
            # Flip, so it makes sense to the user
            preview = cv2.flip(preview, 1)
            display_image = ImageTk.PhotoImage(image=Image.fromarray(preview).resize(self.target_size, Image.ANTIALIAS))
            self.container.imgtk = display_image
            self.container.configure(image=display_image)

        elif self.display_latest_until < datetime.now():
            self.display_latest_until = None

        self.parent.after(40, self.heartbeat)

    def set_next_picture(self, event):
        # Make sure the latest image stops displaying
        self.display_latest_until = None

        self.next_picture_time = datetime.now() + timedelta(seconds=self.COUNTDOWN)

    def get_camera(self):
        try:
            return DSLR()
        except Exception:
            return WebCam()



root = Tk()
root.configure(background='black')
root.wm_attributes('-fullscreen', 1)
root.wm_attributes('-modified', 1)
root.deiconify()

photo_booth = PhotoBooth(root)
root.mainloop()