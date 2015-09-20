#!/usr/bin/python
# -*- coding: utf-8 -*-

from sys import argv
import sys
import cv2
import os
import numpy as np
import math

def carregar_imagem(caminho):
    return cv2.imread(caminho);

def media_rgb(img):
    media = [0, 0, 0];
    for pixel in img:
        for cor in pixel:
            media[0] += cor[0] #R
            media[1] += cor[1] #G
            media[2] += cor[2] #B
    height, width, _ = img.shape
    pixels = height * width
    media[0] /= pixels;
    media[1] /= pixels;
    media[2] /= pixels;
    return media;

def montar_media_imagens(caminho):
    imagens = []
    for _, _, arquivos in os.walk(caminho):
        for arquivo in arquivos:
            caminho_arquivo = caminho + arquivo;
            img = carregar_imagem(caminho_arquivo);
            imagens.append([img, media_rgb(img)]);
    return imagens;

def mostrar_imagem(nome, img):
    cv2.imshow(nome, img);

def bloquear_execucao():
    cv2.waitKey(0);
    cv2.destroyAllWindows();

def criar_imagem(largura, comprimento, escala):
    return np.zeros((largura, comprimento, escala), dtype=np.uint8);

def redimencionar_imagem(img, largura, comprimento, proporcao):
    largura = largura / proporcao if largura / proporcao > 0 else 1
    comprimento = comprimento / proporcao if comprimento / proporcao > 0 else 1
    return cv2.resize(img, (largura, comprimento));

def calcular_distancia(media_parte, media_imagem):
    r = math.pow(media_parte[0] - media_imagem[0], 2);
    g = math.pow(media_parte[1] - media_imagem[1], 2);
    b = math.pow(media_parte[2] - media_imagem[2], 2);
    return math.sqrt(r + g + b);

def adicionar_imagem(mosaico, pos, imagens, imagem_original, visitados, proporcao):
    calculados = {}
    imagem_escolhida = None
    distancia_escolhida = None
    for imagem in imagens:
        img = redimencionar_imagem(imagem[0], imagem[0].shape[0], imagem[0].shape[1], proporcao);
        x, y = pos;
        parte_img = imagem_original[y: y + img.shape[0], x: x + img.shape[1]];
        media = 0;
        if ((img.shape[1], img.shape[0]) not in calculados):
            media = media_rgb(parte_img);
            calculados[(img.shape[1], img.shape[0])] = media;
        else: media = calculados[(img.shape[1], img.shape[0])];
        distancia = calcular_distancia(media, imagem[1]);
        if (distancia_escolhida == None or distancia < distancia_escolhida):
            distancia_escolhida = distancia;
            imagem_escolhida = img;
    adicionar_no_mosaico(mosaico, imagem_escolhida, pos, visitados);


def adicionar_no_mosaico(mosaico, imagem_escolhida, pos, visitados):
    for x in range(0, imagem_escolhida.shape[1]):
        for y in range(0, imagem_escolhida.shape[0]):
            if ((pos[0] + x < mosaico.shape[1]) and (pos[1] + y < mosaico.shape[0])):
                    visitados.add((pos[0] + x, pos[1] + y));
                    mosaico[pos[1] + y][pos[0] + x] = imagem_escolhida[y][x];

def criar_mosaico(imagens, imagem_original, proporcao):
    visitados = set();
    mosaico = criar_imagem(imagem_original.shape[0], imagem_original.shape[1], imagem_original.shape[2]);
    for x in range(0, imagem_original.shape[1]):
        for y in range(0, imagem_original.shape[0]):
            if ((x, y) not in visitados):
                adicionar_imagem(mosaico, (x, y), imagens, imagem_original, visitados, proporcao);
    return mosaico;

def salvar_imagem(nome, img):
    cv2.imwrite(nome, img);

if __name__ == '__main__':
    if (len(argv) < 4): 
        print 'Insira caminho com imagens, proporção e imagem para criação do mosaico.'
        exit(1);

    caminho_imagens = argv[1];
    proporcao = int(argv[2]);
    imagem_original = carregar_imagem(argv[3]);
    print 'Calculando média das imagens...', 
    sys.stdout.flush()
    imagens = montar_media_imagens(caminho_imagens);
    print 'Pronto!';
    print 'Criando mosaico...',
    sys.stdout.flush()
    mosaico = criar_mosaico(imagens, imagem_original, proporcao);
    print 'Pronto!';
    print 'Salvando imagem...',
    sys.stdout.flush()
    salvar_imagem(argv[3] + '_' + str(proporcao) + '.jpg', mosaico);
    print 'Pronto!';
