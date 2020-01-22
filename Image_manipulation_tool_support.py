#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 4.26
#  in conjunction with Tcl version 8.6
#    Jan 16, 2020 01:20:14 AM IST  platform: Windows NT
#    Jan 16, 2020 01:24:16 AM IST  platform: Windows NT
#    Jan 16, 2020 11:48:16 AM IST  platform: Windows NT


try:

    import tkinter as tk
    from tkinter import filedialog, messagebox
    import os
except ImportError:
    import Tkinter as tk
    from Tkinter import filedialog, messagebox

import Image_manipulation_tool as imt

import sys
from cv2 import cv2
from PIL import ImageTk, Image
import numpy as np


try:
    import tkinter.ttk as ttk
    py3 = True
except ImportError:
    import ttk
    py3 = False


def set_Tk_var():
    global che50, che49, che51, radio, job, output
    che50 = tk.IntVar()
    che49 = tk.IntVar()
    che51 = tk.IntVar()
    radio = tk.IntVar()
    job = None
    output = None


class ImageFrame(tk.Canvas):
    #
    #
    # make sure it retain the aspect ratio of the image
    #
    #
    #

    def __init__(self, master, path=None, img=None, **kwargs):
        tk.Canvas.__init__(self, master, **kwargs)
        if path is not None:
            if path is not '':
                self.img_copy = Image.open(path)
                # this is overriden every time the image is redrawn so there is no need to make it yet
                self.image = None
                self.bind("<Configure>", self._resize_image)
        elif img is not None:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            self.img_copy = img
            # this is overriden every time the image is redrawn so there is no need to make it yet
            self.image = None
            self.bind("<Configure>", self._resize_image)

        else:
            pass

    def _resize_image(self, event):
        origin = (0, 0)
        size = (event.width, event.height)
        if self.bbox("bg") != origin + size:
            self.delete("bg")
            self.image = self.img_copy.resize(size)
            self.background_image = ImageTk.PhotoImage(self.image)
            self.create_image(*origin, anchor="nw",
                              image=self.background_image, tags="bg")
            self.tag_lower("bg", "all")


def source_file():
    w.source_path.delete(0, 'end')
    root.filepath = filedialog.askopenfilename(
        initialdir="/", title="Select file", filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
    w.source_path.insert(0, root.filepath)
    im = ImageFrame(root, path=root.filepath, height=w.Canvas1.winfo_height(),
                    width=w.Canvas1.winfo_width())
    im.place(relx=0.014, rely=0.462)
    # print('imts.source_file')
    sys.stdout.flush()


def dest_file():
    w.Destination_path.delete(0, 'end')
    root.D_path = filedialog.askdirectory()
    w.Destination_path.insert(0, root.D_path)
    print('imts.dest_file')

    sys.stdout.flush()


def reset_btn():
    global output
    if hasattr(root, 'filepath'):
        output = cv2.imread(root.filepath)
        im = ImageFrame(root, img=output, height=w.Canvas1.winfo_height(
        ), width=w.Canvas1.winfo_width())
        im.place(relx=0.014, rely=0.462)
        im.update()
        w.Intensity.set(0)
    else:
        messagebox.showerror(
            "Error", "Please choose Image!")
    sys.stdout.flush()


def blurr_face():
    global output
    try:
        output = cv2.imread(root.filepath)
        roi = output.copy()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        face_cascade = cv2.CascadeClassifier(
            dir_path+'\\haarcascade_frontalface_alt.xml')
        gray = cv2.cvtColor(output, cv2.COLOR_RGB2GRAY)
        face_rects = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3)
        for (x, y, wi, h) in face_rects:
            roi = roi[y:y+h, x:x+wi]
            blurred_roi = cv2.medianBlur(roi, 99)
            output[y:y+h, x:x+wi] = blurred_roi

        im = ImageFrame(root, img=output,
                        height=w.Canvas1.winfo_height(), width=w.Canvas1.winfo_width())
        im.place(relx=0.014, rely=0.462)
        im.update()
    except:
        messagebox.showerror("Something Went Wrong !",
                             "Make sure Image path is added right")
    sys.stdout.flush()


def edge_detect():
    global output
    try:
        output = cv2.imread(root.filepath)
        output = output.copy()
        output = cv2.GaussianBlur(output, (17, 17), 0)
        output = cv2.Canny(image=output,
                          threshold1=10, threshold2=100)
        output = cv2.cvtColor(output, cv2.COLOR_GRAY2BGR)
        im = ImageFrame(root, img=output,
                        height=w.Canvas1.winfo_height(), width=w.Canvas1.winfo_width())
        im.place(relx=0.014, rely=0.462)
        im.update()

    except:
        messagebox.showerror("Something Went Wrong !",
                                "Make sure Image path is added right")
    sys.stdout.flush()
    


def face_detect():
    global output
    try:
        output = cv2.imread(root.filepath)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        face_cascade = cv2.CascadeClassifier(
            dir_path+'\\haarcascade_frontalface_alt.xml')
        gray = cv2.cvtColor(output, cv2.COLOR_RGB2GRAY)
        face_rects = face_cascade.detectMultiScale(gray)
        for (x, y, wi, h) in face_rects:
            cv2.rectangle(output, (x, y), (x+wi, y+h), (0, 255, 0), 10)

        im = ImageFrame(root, img=output,
                        height=w.Canvas1.winfo_height(), width=w.Canvas1.winfo_width())
        im.place(relx=0.014, rely=0.462)
        im.update()

    except:
        messagebox.showerror("Something Went Wrong !",
                             "Make sure Image path is added right")

    sys.stdout.flush()
# def vertical_blurr_check():
#     # print('vertical_blurr_check', che49.get())
#     sys.stdout.flush()

# def horizontal_blurr_check():
#     # print('horizontal_blurr_check', che50.get())
#     sys.stdout.flush()


# def sharpness_check():
#     # print('sharpness_check', che51.get())


def intensity_range(*args):
    global job
    if job:
        root.after_cancel(root.job)
    job = root.after(500, do_something())
    # print('imts.intensity_range')
    sys.stdout.flush()


def do_something():
    global job
    job = None
    counter = w.Intensity.get()
    img = cv2.imread(root.filepath)
    edit_img = editor(img, counter)
    im = ImageFrame(root, img=edit_img, height=w.Canvas1.winfo_height(
    ), width=w.Canvas1.winfo_width())
    im.place(relx=0.014, rely=0.462)
    im.update()


def unsharp_mask(image, kernel_size=(5, 5), sigma=1.0, amount=1.0, threshold=0):
    """Return a sharpened version of the image, using an unsharp mask."""
    blurred = cv2.GaussianBlur(image, kernel_size, sigma)
    sharpened = float(amount + 1) * image - float(amount) * blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)
    if threshold > 0:
        low_contrast_mask = np.absolute(image - blurred) < threshold
        np.copyto(sharpened, image, where=low_contrast_mask)
    return sharpened


def editor(img, num):
    vvar = che49.get()
    hvar = che50.get()
    svar = che51.get()
    global output
    if num != 0:
        if vvar == 1 and hvar == 1:
            kernel_3 = np.ones((num, num), dtype=np.float32) / (num * num)
            output = cv2.filter2D(img, -1, kernel_3)
            # print('output', output)

        elif hvar == 1:
            h_blur = np.zeros((num, num))
            h_blur[num // 2, :] = np.ones(num)
            h_blur = h_blur / num
            output = cv2.filter2D(img, -1, h_blur)
            # print('output', output)

        elif vvar == 1:
            v_blur = np.zeros((num, num))
            v_blur[:, num // 2] = np.ones(num)
            v_blur = v_blur / num
            output = cv2.filter2D(img, -1, v_blur)

        elif svar == 1:
            output = unsharp_mask(img, (5, 5), 2, num, 0)
            # print('output', output)

    else:
        output = img
    return output


def save_btn():
    global output
    print(output is not None)
    print(hasattr(root, "D_path"))
    if (output is not None) and (hasattr(root, "D_path")):
        cv2.imwrite(root.D_path + "/test_new.jpg", output)
        messagebox.showinfo("Output", "Image Saved !")

    elif hasattr(root, "D_path"):
        output2 = cv2.imread(root.filepath)
        cv2.imwrite(root.D_path + "/Original_copy.jpg", output2)
        messagebox.showinfo(
            "Output", "No change happend to the Image. original Image Copy Saved !")

    else:
        messagebox.showerror(
            "Error", "Something Went Wrong ! Make sure you added the path")
    sys.stdout.flush()


def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top


def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None


if __name__ == '__main__':
    import Image_manipulation_tool as imt
    imt.vp_start_gui()
