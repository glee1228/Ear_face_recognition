import cv2
import numpy as np
import math
from matplotlib import pyplot as plt

def imgSegment(img):
    rows,cols=img.shape[0:2]
    crop = img[1:rows-10, 1:cols]
    height, width = crop.shape[:2]
    blur = cv2.GaussianBlur(crop,(5,5),0)
    edges = cv2.Canny(blur,70,170)
    return edges

def UmaxFind(edges):
    Umaxflag =False
    rows,cols = edges.shape
    #print("엣지: y   x")
    #print(rows,cols)
    for y in range(rows):
        for x in range(cols):
            if Umaxflag==False:
                k = edges[y,x]
                if k==255:
                    Umaxflag=True
                    Umax = (y,x) # Umax 행,열 좌표
                    return Umax
def checkFeature(edges,Ulb,Umax,Urb,Llb,Lmax,Cmax,Ilb):
    rows,cols=edges.shape
    for y in range(rows):
        for x in range(cols):
            l=(y,x)
            if l==Ulb or l==Umax or l==Urb or l==Llb or l==Lmax or l==Cmax or l==Ilb :
                edges[y,x]=100
    return edges
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
    for y in range(rows):
        for x in range(cols):
            k=edges[y,x]
            if k==255:
                if max_length<Euclidean1(Umax,x,y): #Umax와 엣지 좌표간의 거리
                    Lmax=(y,x)
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
#왼쪽 나선영역 리스트로 저장(나중에 Umax와 Lmax사이 중간지점 Cmax로 부터 왼쪽 나선영역 간의 최단거리인 Cl을 구하기 위함)
def LlbFind(edges,Lmax,T):
    Llbflag=False
    rows,cols =edges.shape
    leftlist = []    #왼쪽 외곽선 나선영역 좌표점을 저장하는 리스트
    
    for x in range(cols):
        for y in range(rows):
            k=edges[rows-y-1,x]
            dist=Euclidean1(Lmax,x,rows-y-1)
            Llb_and_leftList=[]
            if Llbflag==False and (T-1)< dist and dist<(T+1) and k==255:
                Llbflag=True
                Llb=(rows-y-1,x)
                Llb_and_leftList.append(Llb)
                Llb_and_leftList.append(leftlist)
                return Llb_and_leftList
            elif k==255:
                leftloc=(y,x)
                leftlist.append(leftloc)
                break

def FV2Find(edges,Ulb,Umax,Urb,Llb,Lmax):
    FV2flag = False
    #Umax의 y좌표 : Uy1, Ulb와 Urb 둘 중 더 큰(낮게 위치한) y좌표 : Uy2 , Ulb의 x좌표 : Ux1 ,Urb의 x좌표 : Ux2
    Uy1,Uy2,Ux1,Ux2=Umax[0],Ulb[0] if Ulb[0]>=Urb[0] else Urb[0],Ulb[1],Urb[1]
    #print(Uy1,Uy2,Ux1,Ux2)
    
    #Llb의 y좌표 : Ly1, Lmax의 y좌표 : Ly2, Llb의 x좌표 : Lx1, Lmax의 x좌표 : Lx2
    Ly1,Ly2,Lx1,Lx2= Llb[0],Lmax[0],Llb[1],Lmax[1]
    #print(Ly1,Ly2,Lx1,Lx2)

    #Ux,Uy로 이루어진 upper영역에 존재하는 점(외곽선)들과 Lx,Ly로 이루어진 lower영역안에 존재하는 점(외곽선)들 사이의 최단거리를 FV2로 한다.
    Ulist=[]        #upper영역에 존재하는 외곽선 좌표들
    Llist=[]        #lower영역에 존재하는 외곽선 좌표들
    for y in range(Uy1,Uy2+1):
        for x in range(Ux1,Ux2+1):
            k=edges[y,x]
            if k==255:
                Uloc=(y,x)
                Ulist.append(Uloc)
    for y in range(Ly1,Ly2+1):
        for x in range(Lx1,Lx2+1):
            k=edges[y,x]
            if k==255:
                Lloc=(y,x)
                Llist.append(Lloc)
    FV2=1000000
    Umin=(0,0)
    Lmin=(0,0)
    result=[]
    for i in Ulist:
        for j in Llist:
            dist=Euclidean2(i,j)
            if dist<FV2:
                Umin=(i[1],i[0])
                Lmin=(j[1],j[0])
                FV2=dist
    result.append(Umin)
    result.append(Lmin)
    result.append(FV2)
    return result

def CmaxFind(Umax,Lmax):
    y1,y2,x1,x2 = Umax[0],Lmax[0],Umax[1],Lmax[1]
    midy=int((y1+y2)/2)
    midx=int((x1+x2)/2)
    Cmax=(midy,midx)
    return Cmax

def ClFind(leftlist,Cmax):  # 왼쪽 나선영역 외곽선과 Cmax간의 최단거리 Cl
    min_length=1000000
    Ilb=(0,0)
    Cl_Ilb=[]
    for i in leftlist:
        dist=Euclidean2(i,Cmax)
        y=i[0]
        x=i[1]
        if dist<min_length:
            min_length=dist
            Ilb=(y,x)
    Cl_Ilb.append(min_length)
    Cl_Ilb.append(Ilb)
    return Cl_Ilb

def extract_feature(path,label,T):  # 이미지 경로 : path / 레이블 : label / 피쳐 추출할 T 포인트(임의의 수 대략 10~ 20정도) : T
    img = cv2.imread(path)
    edges=imgSegment(img)
    Umax=UmaxFind(edges)            # Umax = 귀의 제일 상단점
    Lmax=LmaxFind(edges,Umax)   # Lmax = Umax와 가장 멀리 떨어진 귀의 외곽선 중 좌표점 / Umax와 Lmax간의 거리 : FV1
#    print("Umax: y    x")
#    print("     ",Umax)
#    print("Lmax: y    x")
#    print("     ",Lmax)
#
    Ulb = UlbFind(edges,Umax,T)     # Ulb = T에서 T+1 사이의 값(거리)만큼 떨어진 Umax왼쪽에 위치한 외곽선중 한점
#    print("Ulb:  y    x")
#    print("     ",Ulb)
    Urb = UrbFind(edges,Umax,T)     # Urb = T에서 T+1 사이의 값(거리)만큼 떨어진 Umax오른쪽에 위치한 외곽선중 한점
#    print("Urb:  y    x")
#    print("     ",Urb)

    Llb_and_leftList = LlbFind(edges,Lmax,T)
    Llb=Llb_and_leftList[0]         # Llb = T에서 T+1 사이의 값(거리)만큼 떨어진 Lmax왼쪽에 위치한 외곽선중 한점
    leftlist=Llb_and_leftList[1]  #왼쪽 나선영역 외곽선 좌표점 리스트
#    print("Llb:  y    x")
#    print("     ",Llb)
    FV1=Euclidean2(Umax,Lmax)
    result=FV2Find(edges,Ulb,Umax,Urb,Llb,Lmax)
    Umin=result[0]
    Lmin=result[1]
    FV2=result[2]
#    print("FV1(Umax와 Lmax의 직선거리) :",FV1)
#    print("FV2(Ulb와 Urb사이영역과 Llb와 Lmax사이영역 간 최단 직선 거리) :",FV2)
    FV3=FV1+FV2
    FV4=FV2/FV1
#    print("FV3(FV1+FV2) : ",FV3)
#    print("FV4(FV2/FV1) : ",FV4)
    Cmax=CmaxFind(Umax,Lmax)     #Umax와 Cmax를 잇는 선분의 중점
#    print("Cmax : ",Cmax)
    Cl_Ilb=ClFind(leftlist,Cmax)
    Cl = Cl_Ilb[0]
    Ilb = Cl_Ilb[1]
#    print("Cl : ",Cl)
    FV5=Cl/FV1
    FV6=Cl/FV2
#    print("FV5(Cl/FV1) : ",FV5)
#    print("FV6(Cl/FV2) : ",FV6)
    FV=[]
    FV.append(FV1)
    FV.append(FV2)
    FV.append(FV3)
    FV.append(FV4)
    FV.append(FV5)
    FV.append(FV6)
    FV.append(label)
    drawedge=checkFeature(edges,Ulb,Umax,Urb,Llb,Lmax,Cmax,Ilb)
    Draw(drawedge)
#    DrawOrigin(img)
    return FV

def main() :
    img_num = 35
    label = 3
    T = 10 # Umax와 Lmax에서 T만큼 떨어진 외곽선 Ulb,Urb,Llb를 정하는 임의의 수
    for i in range(0,img_num+1):
        image_path = "./image/%04d.jpg"%i
        print(image_path)
        FV=extract_feature(image_path,label,T)
        feature = ','.join(str(v) for v in FV)
        print(feature)


main()


















