import cv2
import numpy as np
import math
from matplotlib import pyplot as plt

def imgSegment(img):
    crop = img[1:119, 1:90]
    height, width = crop.shape[:2]
    blur = cv2.GaussianBlur(crop,(5,5),0)
    edges = cv2.Canny(blur,30,170)
    return edges

def UmaxFind(edges):
    Umaxflag =False
    rows,cols = edges.shape
    print("엣지: y   x")
    print(rows,cols)
    for y in range(rows):
        for x in range(cols):
            if Umaxflag==False:
                k = edges[y,x]
                if k==255:
                    Umaxflag=True
                    Umax = (y,x) # Umax 행,열 좌표
                    return Umax

def DrawOrigin(img):
    crop = img[1:119, 1:90]
    height, width = crop.shape[:2]
    blur = cv2.GaussianBlur(crop,(5,5),0)
    edges = cv2.Canny(blur,30,170)
    plt.subplot(122),plt.imshow(blur),plt.title('Blurred')
    plt.xticks([]), plt.yticks([])
    plt.subplot(121),plt.imshow(edges),plt.title('Canny Edged')
    plt.xticks([]), plt.yticks([])
    plt.show()

def Draw(img):
    plt.imshow(img)
    plt.show()

#input이 튜플 과 x좌표,y좌표일 때
def Euclidean1(A,x2,y2):
    x1=A[1]
    y1=A[0]
    #print("x1 : {0}, y1 : {1}, x2 : {2}, y2 : {3}".format(x1,y1,x2,y2))
    return math.sqrt(((x2-x1)**2)+((y2-y1)**2))

#input이 튜플과 튜플일 때
def Euclidean2(A,B):
    x1=A[1]
    y1=A[0]
    x2=B[1]
    y2=B[0]
    #print("x1 : {0}, y1 : {1}, x2 : {2}, y2 : {3}".format(x1,y1,x2,y2))
    return math.sqrt(((x2-x1)**2)+((y2-y1)**2))

def sum(x,y):
    return x+y

def LmaxFind(edges,Umax):
    rows,cols=edges.shape
    max_length=0
    Lmax=(0,0)
    for i in range(rows):
        for j in range(cols):
            k=edges[i,j]
            if k==255:
                if max_length<Euclidean1(Umax,i,j): #Umax와 엣지 좌표간의 거리
                    Lmax=(i,j)
            else :
                pass
    return Lmax


#Ulb는 왼쪽위에서 아래로 향하면서 검사
def UlbFind(edges,Umax,T):
    Ulbflag=False
    rows,cols =edges.shape
    for x in range(cols):
        for y in range(rows):
            k=edges[y,x]
            dist=Euclidean1(Umax,x,y)
            if Ulbflag==False and (T-1)< dist and dist<(T+1) and k==255:
                Ulbflag=True
                Ulb = (y,x) # Umax 행(y),열(x) 좌표
                return Ulb
            else :
                continue

#Urb는 오른쪽 위에서 아래로 향하면서 검사
def UrbFind(edges,Umax,T):
    Urbflag = False
    rows,cols = edges.shape
    for x in range(cols):
        for y in range(rows):
            k=edges[y,cols-x-1]
            dist=Euclidean1(Umax,cols-x-1,y)
            if Urbflag==False and (T-1)< dist and dist<(T+1) and k==255:
                Urbflag=True
                Urb=(y,cols-x-1)
                return Urb



#Llb를 찾을 떄 귀의 기울어짐을 고려하여 이미지 가장 아래에서 부터 위로 보았을 때 1/3지점까지만 검사
#Llb는 왼쪽아래에서 위로 향하면서 검사
def LlbFind(edges,Lmax,T):
    Llbflag=False
    rows,cols =edges.shape
    for x in range(cols):
        for y in range(rows):
            k=edges[rows-y-1,x]
            dist=Euclidean1(Lmax,x,rows-y-1)
            if Llbflag==False and (T-1)< dist and dist<(T+1) and k==255:
                Llbflag=True
                Llb=(rows-y-1,x)
                return Llb




def main():
    img = cv2.imread('./image/0015.jpg')
    edges=imgSegment(img)
    Umax=UmaxFind(edges)
    Lmax=LmaxFind(edges,Umax)
    print("Umax: y    x")
    print(Umax)
    print("Lmax: y    x")
    print(Lmax)
    
    T = 10
    
    Ulb = UlbFind(edges,Umax,T)
    print("Ulb:  y    x")
    print(Ulb)
    Urb = UrbFind(edges,Umax,T)
    print("Urb:  y    x")
    print(Urb)
    
    Llb = LlbFind(edges,Lmax,T)
    print("Llb:  y    x")
    print(Llb)
    DrawOrigin(img)

main()
