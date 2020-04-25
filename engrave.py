import sys
import numpy as np
import cv2
import simple_gcode as sg

THRESH = 200

def findNextPixel(x,y,data,h,w):
    for x_o in [0,-1,-2,1,2]:
        for y_o in [0,-1,-2,1,2]:
            idx = x+x_o
            idy = y+y_o
            if(idx < 0 or idy < 0 or idx >= h or idy >= w):
                continue
            if (data[idx,idy] < THRESH):
                return idx,idy
    return -1,-1

def main():
    #Handle arguments
    try:
        filename = sys.argv[1]
        width_out = int(sys.argv[2])
        height_out = int(sys.argv[3])
        tool_no  = int(sys.argv[4])
    except:
        print("Usage: python engrave.py filename width height tool_num")
        sys.exit(1)

    data = cv2.imread(filename,cv2.IMREAD_GRAYSCALE)
    data = cv2.resize(data,(width_out,height_out))

    cv2.imshow("Engraving",data)
    cv2.waitKey()

    w,h = data.shape

    CUT_DEPTH = -2

    print("Shape:",data.shape)

    #print(np.where(data<100))


    program = [
        sg.PREAMBLE,
        sg.tool_change(tool_no),
        sg.spindle_on(9500), #9500 RPM
        ''
    ]

    for i in range(w):
        for j in range(h):
            if(data[i,j] < THRESH):
                #found one!
                print("found one!", i,j)
                x,y = i,j
                #start engraving
                program.append(sg.motion(mtype='rapid', x=x, y=y))
                program.append(sg.motion(mtype='linear', feedrate=800, z= CUT_DEPTH))
                while True:
                    data[x,y] = 255
                    #print("Just removed:",x,y,data[x,y])
                    x_prime, y_prime = findNextPixel(x,y,data,h,w)
                    #print("Next pixel to cut to is: ", x_prime,y_prime)
                    if(x_prime == -1):
                        break
                    #draw line from x,y to x_prime,y_prime
                    program.append(sg.motion(mtype='linear', feedrate=800, x = x_prime, y = y_prime))
                    x,y = x_prime,y_prime
                #get out of the danger zone
                program.append(sg.motion(mtype='linear', feedrate=800, z = 15))

    for i in range(w):
        for j in range(h):
            if(data[i,j] < 30):
                print("\t\tYa Missed one:",i,j,data[i,j],"\n")

    # cv2.imshow('Final Image',data)
    # cv2.waitKey()
    #print(np.where(data<255))


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
