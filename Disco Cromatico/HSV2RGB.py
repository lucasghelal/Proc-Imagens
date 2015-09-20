import cv2
import numpy as np

def Trabalho1_CirculoHSV2RGB(ImagemQuadrada, Raio):

	imagem = np.ones((ImagemQuadrada, ImagemQuadrada,3), np.float32)
	ll, cc = np.indices((ImagemQuadrada, ImagemQuadrada))
	circulo = (ll - ImagemQuadrada/2) ** 2 + (cc - ImagemQuadrada/2) ** 2
	
	arctan_ll = (ll.astype(np.float32)-ImagemQuadrada/2)
	arctan_cc = (cc.astype(np.float32)-ImagemQuadrada/2)
	#Hue
	H = np.rad2deg(np.arctan2(arctan_ll, arctan_cc)) 
	#Saturation
	S = (circulo.astype(np.float32))/(Raio)**2
	#Value
	#V = np.ones((ImagemQuadrada, ImagemQuadrada), np.float32) 
	#V[circulo > (Raio/1.5)**2] = 0.5
	
	imagem[:,:,0] = H 
	imagem[:,:,1] = S
	#imagem[:,:,2] = V
	
	imagem[circulo > Raio**2] = [0,0,0]
	imagem = cv2.cvtColor(imagem, cv2.COLOR_HSV2BGR)

	cv2.imshow("CirculoHSV2RGB", imagem)
	cv2.waitKey(0)
	cv2.destroyAllWindows()


Trabalho1_CirculoHSV2RGB(400,180)
