import cv2
import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
from streamlit_drawable_canvas import st_canvas
from BaselineRemoval import BaselineRemoval


def mudar_cord(max1, max2, x):
    resultado = x * max1 // max2
    return resultado


def processar_imagem(imagem, limiar):
    # Aplicar um limiar para converter a imagem em binário
    _, imagem_binaria = cv2.threshold(imagem, limiar, 255, cv2.THRESH_BINARY_INV)

    # Aplicar a máscara ao original
    imagem_processada = imagem * (imagem_binaria == 0)

    return imagem_processada


width, height = 600, 400
# Carregar a imagem
imagem_colorida = cv2.imread("1Gui271023005.jpg")
imagem_colorida = cv2.cvtColor(imagem_colorida, cv2.COLOR_BGR2RGB)

# Converter para escala de cinza
imagem_em_escala_de_cinza = cv2.cvtColor(imagem_colorida, cv2.COLOR_BGR2GRAY)

imagem_em_escala_de_cinza = cv2.bitwise_not(imagem_em_escala_de_cinza)

st.image(imagem_colorida, width=width)
st.image(imagem_em_escala_de_cinza, width=width)


imagem_em_escala_de_cinza_pil = Image.fromarray(imagem_em_escala_de_cinza)

altura, largura, _ = imagem_colorida.shape
st.write("Selecione a area sem borda")
canvas_result = st_canvas(
    fill_color="rgba(0, 0, 0, 0)",
    background_image=imagem_em_escala_de_cinza_pil,
    stroke_color="rgba(255, 0, 0, 1)",
    drawing_mode="rect",
    stroke_width=2,
    height=height,
    width=width,
)

if len(canvas_result.json_data["objects"]) > 0:
    # st.write(canvas_result.json_data["objects"][-1])

    left, top, width_cord, height_cord = [
        canvas_result.json_data["objects"][-1][cord]
        for cord in ["left", "top", "width", "height"]
    ]

    x1 = int(left)
    x2 = int(left + width_cord)
    y1 = int(top)
    y2 = int(top + height_cord)

    x1 = mudar_cord(largura, width, x1)
    x2 = mudar_cord(largura, width, x2)
    y1 = mudar_cord(altura, height, y1)
    y2 = mudar_cord(altura, height, y2)
    imagem_cortada = imagem_em_escala_de_cinza[y1:y2, x1:x2]
else:
    st.stop()

colunas = st.columns(2)
with colunas[0]:
    # Certifique-se de que imagem_cortada seja uma imagem em escala de cinza com valores no intervalo [0, 255]
    limear = st.slider("escolha o threshold", 0, 255, 40)

with colunas[1]:
    imagem_cortada = cv2.normalize(imagem_cortada, None, 0, 255, cv2.NORM_MINMAX)

    imagem_teste = processar_imagem(imagem_cortada, limear)

    imagem_teste = cv2.normalize(imagem_teste, None, 0, 255, cv2.NORM_MINMAX)

    st.image(imagem_teste)
