import numpy as np
import dlib
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import statistics


def verifica_clareza_do_rosto(path):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('face_landmark/shape_predictor_68_face_landmarks.dat')
    img = dlib.load_rgb_image(path)

    if len(detector(img)) == 0:
        return ('No face detected')
    rect = detector(img)[0]
    sp = predictor(img, rect)
    landmarks = np.array([[p.x, p.y] for p in sp.parts()])

    nose_bridge_x = []
    nose_bridge_y = []

    for i in [28, 29, 30, 31, 33, 34, 35]:
        nose_bridge_x.append(landmarks[i][0])
        nose_bridge_y.append(landmarks[i][1])

    ### x_min and x_max
    x_min = min(nose_bridge_x)
    x_max = max(nose_bridge_x)

    ### ymin (from top eyebrow coordinate),  ymax
    y_min = landmarks[20][1]
    y_max = landmarks[30][1]

    img2 = Image.open(path)
    img2 = img2.crop((x_min, y_min, x_max, y_max))

    img_blur = cv2.GaussianBlur(np.array(img2), (3, 3), sigmaX=0, sigmaY=0)

    edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200)

    edges_center = edges.T[(int(len(edges.T) / 2))]

    if 255 in edges_center:
        return (1)
    else:
        return (0)

def detectar_rosto_na_imagem(imagem):
    imagem = cv2.imread(imagem)
    # Carregue o classificador Haar Cascade para detecção de faces
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Converta a imagem para escala de cinza, o que ajuda na detecção de faces
    imagem_em_escala_de_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # Detecte faces na imagem
    faces = face_cascade.detectMultiScale(imagem_em_escala_de_cinza, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Se pelo menos uma face for detectada, retorne True, caso contrário, retorne False
    if len(faces) > 0:
        return True
    else:
        return False