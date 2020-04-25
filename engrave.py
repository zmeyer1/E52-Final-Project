import sys
import numpy as np
import cv2
import simple_gcode as sg

def findNextPixel(x,y,data):
    for x_o in [-1,0,1]:
        for y_o in [-1,0,1]:
            if (data[x+x_o,y+y_o] == 0):
                return x+x_o,y+y_o
    return -1,-1

def main():
    #Handle arguments
    try:
        filename = sys.argv[1]
    except:
        print("Usage: python engrave.py filename")
        sys.exit(1)

    data = cv2.imread(filename,cv2.IMREAD_GRAYSCALE)

    cv2.imshow("Engraving",data)
    cv2.waitKey()

    h,w = data.shape

    CUT_DEPTH = -2

    print("Shape:",data.shape)

    x0 = 0
    y0 = 0



    program = [
        sg.PREAMBLE,
        sg.tool_change(102),
        sg.spindle_on(9500), #9500 RPM
        ''
    ]

    for i in range(w):
        for j in range(h):
            if(data[i,j] == 0):
                #found one!
                print("found one!", i,j)
                x,y = i,j
                #start engraving
                program.append(sg.motion(mtype='rapid', x=x, y=y))
                program.append(sg.motion(mtype='linear', feedrate=800, z= CUT_DEPTH))
                while True:
                    data[x,y] = 255
                    print("Just removed:",x,y,data[x,y])
                    x_prime, y_prime = findNextPixel(x,y,data)
                    print("Next pixel to cut to is: ", x_prime,y_prime)
                    if(x_prime == -1):
                        break

                    #draw line from x,y to x_prime,y_prime
                    program.append(sg.motion(mtype='linear', feedrate=800, x = x_prime, y = y_prime))
                    x,y = x_prime,y_prime
                #get out of the danger zone
                program.append(sg.motion(mtype='linear', feedrate=800, z = 15))

    for i in range(w):
        for j in range(h):
            if(data[i,j] == 0):
                print("\t\tYa Missed one:",i,j,"\n")

    end = [
    '',
    sg.motion(mtype='rapid', z=15),
    sg.SPINDLE_OFF,
    sg.CONCLUSION
    ]

    program.extend(end)


    writer = open('engraving.nc', 'w')

    writer.write('\n'.join(program)) #Write program to file

    writer.close()
    print("All done!")



if __name__ == "__main__":
    main()
