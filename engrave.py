import sys
import numpy as np
import cv2
import simple_gcode as gc

def main():
    #Handle argument
    try:
        filename = sys.argv[1]
    except:
        print("Usage: python engrave.py filename")

    data = cv2.imread(filename)

    cv2.imshow("Engraving",data)
    cv2.waitKey()

    #Loop though entire image,
        #If we find a dark pixel, go down, follow its neighbors linearly.
        #Color drawn pixels white.
        #remember where we were looping.






if __name__ == "__main__":
    main()
