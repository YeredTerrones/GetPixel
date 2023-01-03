from PyQt5 import QtWidgets, uic
from iconos import *
from PyQt5.QtWidgets import QFileDialog
from messagebox import msg_error
import cv2
import numpy as np

# iniciar la aplicación
app = QtWidgets.QApplication([])

# Obtener el ancho y alto de tu pantalla
screen = app.desktop().screenGeometry()
width = screen.width()
height = screen.height()

# Cargar archivos .ui
window = uic.loadUi("pixel.ui")

filename = None
img_color = np.zeros((200, 200, 3), np.uint8)


def cargarImagen():
    global filename, img_original
    try:
        filename = QFileDialog.getOpenFileName(filter="Image (*.*)")[0]
        img = cv2.imread(filename)
        if img.shape[1] < img.shape[0] and height < img.shape[0]:
            img = cv2.resize(img, (int(img.shape[1] / 6), int(img.shape[0] / 6)), interpolation=cv2.INTER_AREA)
        elif img.shape[1] > img.shape[0] and img.shape[1] > width:
            img = cv2.resize(img, (int(img.shape[1] / 6), int(img.shape[0] / 6)), interpolation=cv2.INTER_AREA)
        elif img.shape[0] > height and img.shape[0] < 1000:
            img = cv2.resize(img, (int(img.shape[1] / 2), int(img.shape[0] / 2)), interpolation=cv2.INTER_AREA)
        else:
            img = cv2.resize(img, (int(img.shape[1] / 2), int(img.shape[0] / 2)), interpolation=cv2.INTER_AREA)

        img_original = img.copy()


        cv2.imshow('Cuadro', img)

        cv2.setMouseCallback('Cuadro', color)
    except:
        msg_error("Error", "No seleccionaste ninguna imagen")


def color(event, x, y, flags, param):
    global img, img_original
    if event == cv2.EVENT_LBUTTONDBLCLK:
        color = img[y, x].tolist()
        cv2.circle(img_original, (x, y), 10, (0, 0, 0), 1)
        img_color[:] = [color[0], color[1], color[2]]
        hex1 = color[2]
        hex2 = color[1]
        hex3 = color[0]
        rgb2hex(hex1, hex2, hex3)

    elif event == cv2.EVENT_LBUTTONUP:
        img = img_original.copy()
        cv2.imshow('Cuadro', img)


def rgb2hex(r, g, b):
    a = "#{:02x}{:02x}{:02x}".format(r, g, b)
    window.label_pixel.setText("")
    window.label_rgb.setText(f"{r},{g},{b}")
    window.label_hex.setText(f"{a}")
    return window.label_pixel.setStyleSheet("background-color: {}".format(a))


def salir():
    app.exit()


window.actionOpen.triggered.connect(cargarImagen)
window.actionExit.triggered.connect(salir)

# Ejecutable
window.show()
app.exec()