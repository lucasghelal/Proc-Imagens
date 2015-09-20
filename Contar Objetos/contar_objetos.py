#!/usr/bin/python

import cv2
import numpy as np
from matplotlib import pyplot as plt
from sys import argv

# cor usada para pintar
#pintado = 5

# carregar imagem na escala cinza
def carregar_imagem(caminho):
    return cv2.imread(caminho, 0);

# pausa execucao para mostrar as imagens
def bloquear_execucao():
    cv2.waitKey();
    cv2.destroyAllWindows();

# mostra imagem na tela
def mostrar_imagem(nome, img):
    cv2.imshow(nome, img);

# pega os 4 vizinhos de uma coordenada
def vizinhos(img, y, x):
    vizinhos = [];
    if (y + 1 < len(img)):
        vizinhos.append((y + 1, x));
    if (y - 1 >= 0):
        vizinhos.append((y - 1, x));
    if (x + 1 < len(img[y])):
        vizinhos.append((y, x + 1));
    if (x - 1 >= 0):
        vizinhos.append((y, x - 1));
    return vizinhos;

# busca em largura na imagem
def bfs(img, ponto, pintado):
    y, x = ponto
    img[y][x] = pintado
    fila = [ponto];
    while fila:
        y, x = fila.pop()
        for vizinho in vizinhos(img, y, x):
            y_v, x_v = vizinho;
            cor = img[y_v][x_v];
            if (cor > 0 and cor != pintado):
                img[y_v][x_v] = pintado;
                fila.append(vizinho);

# conta quantidade de objetos em uma imagem binaria
def contar_objetos(img):
    pintado = 5
    total_objetos = 0;
    for y in range(0, len(img)):
        for x in range(0, len(img[y])):
            cor = img[y][x];
            if cor == 255 and cor != pintado:
                total_objetos += 1;
                bfs(img, (y, x), pintado);
        	pintado += 5  
    print 'Quantidade de objetos:', total_objetos;

if __name__ == '__main__': 
    if (len(argv) == 1):
        print 'Passe o caminho da imagem a ser carregada.';
        exit(1);

    

    caminho_arquivo = argv[1];
    img = carregar_imagem(caminho_arquivo);
    
    ret, imgT = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    mostrar_imagem('original-binaria', imgT);
    
    
    contar_objetos(imgT);
    mostrar_imagem('original-tons-cinza', img);
    mostrar_imagem('pintada', imgT);

    n,bins,patches = plt.hist(imgT.ravel(), 256, [1, 255])
    plt.show()

    bloquear_execucao();
