
import cv2
import numpy as np
from numpy import mean
def roi(img,Txl,Tyl,Txu,Tyu):  
    gr=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gr1=np.array(gr[Tyl:Tyu,Txl:Txu])
    print("size of gr1")
    print(np.shape(gr1))
    M = cv2.moments(gr1)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    return cX,cY
def predict(c,d,Txl,Tyl,Txu,Tyu):
    c=np.array(c)
    d=np.array(d)
    s= np.linalg.norm(c-d)
    mx=c[0]-d[0]
    my=c[1]-d[1]
    if(mx>0):
        Txu=int(Txu+(1.25*s))
        Txl=int(Txl-(0.75*s))
    else:
        Txu=int(Txu+(0.75*s))
        Txl=int(Txl-(1.25*s))
    if(my>0):
        Tyu=int(Tyu+(1.25*s))
        Tyl=int(Tyl-(0.75*s))
    else:
        Txu=int(Txu+(0.75*s))
        Txl=int(Txl-(1.25*s))
    return(Txl,Tyl,Txu,Tyu)
def mean1(cr,Txl,Tyl,Txu,Tyu):
    cr1=cr[Tyl:Tyu,Txl:Txu]
    #print(cr1.shape)
    def max_dev(r):
        r=np.array(r)
        r=r.flatten()
        dev=[]
        for i in range(len(r)):
            d=abs(r[i]-np.mean(r))
            dev.append(d)
        return(max(dev))
    b,g,r=cv2.split(cr1)
    m=cv2.mean(cr)
    m=np.mean(m)
    mb=max_dev(b)
    mg=max_dev(g)
    mr=max_dev(r)
    #print(mr,mg,mb)
    w,h=cr1.shape[:2]
    px=[]
    for i in range(w):
        for j in range(h):
            pix=cr1[i,j]
            b1=bool(abs(pix[0]-m)<mb)
            b2=bool(abs(pix[1]-m)<mg)
            b3=bool(abs(pix[2]-m)<mr)
            if(b1 and b2 and b3):
                px.append(int(0))
            else:
                px.append(int(1))
    px=np.array(px)
    op=np.reshape(px,(w,h))
    print(np.shape(op))    
    p=np.nonzero(op)
    p=np.array(p)
    ymin,xmin=p.min(axis=1)
    #co-ordinate transformation 
    xmin=int(xmin+Txl)
    ymin=int(ymin+Tyl)
    ymax,xmax=p.max(axis=1)
    xmax=int(xmax+Txl)
    ymax=int(ymax+Tyl)
    return(xmin,ymin,xmax,ymax)
#takes first frame here
def track(t,Txl,Tyl,Txu,Tyu):
    t=t+1
    if(t==53):
        return None
    else:
        print("Currently at frame {}".format(t))
        cap.set(1,t)
        ret,fr=cap.read()
        sg=cv2.imread(r'C:\Users\vandana\Documents\spatio\spat\spat%d.jpg'%(t))
        a=roi(fr,Txl,Tyl,Txu,Tyu)
        print("Centroid of t")
        print(c)
        sg=cv2.imread(r'C:\Users\vandana\Documents\spatio\spat\spat%d.jpg'%(t-1))
        d=roi(sg,Txl,Tyl,Txu,Tyu)
        print("Centroid of t-1")
        print(d)
        Txl,Txu,Tyl,Tyu=predict(c,d,Txl,Tyl,Txu,Tyu)
        #print(Txl,Txu,Tyl,Tyu)
        #final detected coordinates here
        Txl,Tyl,Txu,Tyu=mean1(fr,Txl,Txu,Tyl,Tyu)
        #plot the coordinates
        print(Txl,Tyl,Txu,Tyu)
        #adjustments in frame
        if(17<t<=30):
            a=cv2.rectangle(fr,(Txl-15,Tyl-15),(Txu+15,Tyu+15),(255,0,0),2)
        if(30<t<40):
            a=cv2.rectangle(fr,(Txl-25,Tyl-25),(Txu+25,Tyu+25),(255,0,0),2)
        # cv2.imwrite(r'C:\Users\vandana\Documents\spatio\op\frame%d.jpg'%(t),a)
        cv2.imshow("frame",a)
        cv2.waitKey(0)
        cv2.destroyWindow("frame") 
        track(t,Txl,Tyl,Txu,Tyu)
t=int(35)
cap=cv2.VideoCapture(r'C:\Users\vandana\Documents\spatio\carsq.mp4')
cap.set(1,t)
ret,fr=cap.read()
r = cv2.selectROI('roi select',fr,showCrosshair=False)
cv2.waitKey(0)
cv2.destroyWindow('roiselect')
print('Checking roi is selected ')
print(r)
cr=np.array(fr[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])])
sg=cv2.imread(r'C:\Users\vandana\Documents\spatio\spat\spat%d.jpg'%(t))
Txl=r[0]
Txu=r[0]+r[2]
Tyl=r[1]
Tyu=r[1]+r[3]
c=roi(sg,Txl,Tyl,Txu,Tyu)
print("Centroid of t")
print(c)
sg=cv2.imread(r'C:\Users\vandana\Documents\spatio\spat\spat%d.jpg'%(t-1))
d=roi(sg,Txl,Tyl,Txu,Tyu)
print("Centroid of t-1")
print(d)
Txl,Txu,Tyl,Tyu=predict(c,d,Txl,Tyl,Txu,Tyu)
print("predicted coordiates are")
print(Txl,Txu,Tyl,Tyu)
cap.set(1,t+1)
ret,fr=cap.read()
#final object coordinates are found here
Txl,Tyl,Txu,Tyu=mean1(fr,Txl,Txu,Tyl,Tyu)
print(Txl,Tyl,Txu,Tyu)
a=cv2.rectangle(fr,(Txl,Tyl),(Txu,Tyu),(255,0,0),2)
cv2.imshow("44",a)
cv2.waitKey(0)
cv2.destroyWindow("44")
track(t,Txl,Tyl,Txu,Tyu)
#next iteration
#try recursive functions
# t=t+1
# print(t)
# cap.set(1,t)
# ret,fr=cap.read()
# sg=cv2.imread(r'C:\Users\vandana\Documents\spatio\spat\spat%d.jpg'%(t))
# a=roi(fr,Txl,Tyl,Txu,Tyu)
# print("Centroid of t")
# print(c)
# sg=cv2.imread(r'C:\Users\vandana\Documents\spatio\spat\spat%d.jpg'%(t-1))
# d=roi(sg,Txl,Tyl,Txu,Tyu)
# print("Centroid of t-1")
# print(d)
# Txl,Txu,Tyl,Tyu=predict(c,d,Txl,Tyl,Txu,Tyu)
# print(Txl,Txu,Tyl,Tyu)
# #final detected coordinates here
# Txl,Tyl,Txu,Tyu=mean1(fr,Txl,Txu,Tyl,Tyu)
# a=cv2.rectangle(fr,(Txl,Tyl),(Txu,Tyu),(255,0,0),2)
# cv2.imshow("45",a)
# cv2.waitKey(0)
# cv2.destroyWindow("45") 
        


