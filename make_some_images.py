import numpy as np
import cv2
import sys

def main():
    a = 255*np.ones((500,500))

    a[200,100:400] = np.zeros(300)
    a[100:150, 250] = np.zeros(50)

    cv2.imwrite("simple.jpg",a)

main()
