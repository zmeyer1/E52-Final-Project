import numpy as np
import cv2
import sys

def main():
    a = 255*np.ones((500,500))

    # a[200,100:400] = np.zeros(300)
    # a[100:150, 250] = np.zeros(50)

    #r = 100
    #middle = 250
    #theta = np.arange(0, 2*np.pi, 0.01)
    #for angle in theta:
    #    x = int(2*r * np.cos(angle)) + middle
    #    y = int(r * np.sin(angle)) + middle
    #    a[y,x] = 0

    #cv2.imwrite("circle.jpg",a)
    img = cv2.imread('2cathsign.jpg',0)
    
    edges = cv2.Canny(img,100,200)

    cv2.imwrite("cathsignb&w.jpg",edges)


main()
