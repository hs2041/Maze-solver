import cv2
import numpy as np
import sys
import math
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file_name", help="Enter the file no. (1 to 9)")
args = parser.parse_args()
# name = str(args.echo)
print("Selected image no.:"+args.file_name)
# print("got1")

name = str(args.file_name)
#sys.setrecursionlimit(10000)
dir_in = 'examples/'
dir_out = 'results/'
# print("got2")
##################
##################


png = '.png'
img = cv2.imread(dir_in + name + png)
start = [0,0]
end = [0,0]
# print("got3")
rows,cols,channel =img.shape
last_point = [[-1 for i in range(cols)] for j in range(rows)]
# print("got4")
last_pose = [[[] for i in range(cols)] for j in range(rows)]
count = 0
her = []
# print("got5")
def find(point,rows,cols):
    global img
    count = 0
    for i in range(0,cols):
        if img[point][i][0] == [255]:
            break
    return [point,i]

def create_heuristic(rows,cols):
    global img,end,her
    heur = np.zeros((rows,cols))
    for i in range(rows):
        for j in range(cols):
            heur[i][j] = abs(end[1]-j)+abs(end[0]-i)
    her = heur
def open_p_updater(open_points):
    # print("111")
    least_score = 0
    least_point = []
    flag = True
    pos_goodpoint_del = 0
    for i in range(len(open_points)):
        good_point = [open_points[i][0],open_points[i][1]]
        if(flag == True):
            flag = False
            least_score = her[good_point[0]][good_point[1]]
            least_point = good_point
            pos_goodpoint_del = i
        else:
            if(least_score> her[good_point[0]][good_point[1]]):
                least_score = her[good_point[0]][good_point[1]]
                least_point = good_point
                pos_goodpoint_del = i
    open_points.pop(pos_goodpoint_del)

    return open_points,least_point

def mover(start,end,open_points):
    #first find which point out of open_points is the best

    #img is the image, start and end are start and end points
    #heur is heuristics
    #last_point: stores the score to reach a point
    #last_pose: point where it came from
    #open_points is the list of points that are open
    global last_pose,last_point
    global count
    least_point=[-1,-1]

    while(least_point[0]!=end[0] or least_point[1]!=end[1]):

        open_points,least_point = open_p_updater(open_points)
        count+=1
        # print(count)
        # print(least_point)

        #update the score of this point
        if least_point[0]==end[0] and least_point[1]==end[1]:
            # print("ljkdsljsd")
            return #start,end,open_points
        if least_point[0] == start[0] and least_point[1] == start[1]:
            open_points = [[start[0]+1,start[1]]]
            last_point[start[0]+1][start[1]]=1+her[start[0]+1][start[1]]
            last_pose[start[0]+1][start[1]] = [start[0],start[1]]

        else:
            #now our current point is least_point
            #check point above least_point
            if(img[least_point[0]][least_point[1]-1][0] == 255):
                if(last_point[least_point[0]][least_point[1]-1] == -1) or ((last_point[least_point[0]][least_point[1]-1])>(last_point[least_point[0]][least_point[1]]+1+her[least_point[0]][least_point[1]-1])):
                    last_point[least_point[0]][least_point[1]-1] = last_point[least_point[0]][least_point[1]]+1+her[least_point[0]][least_point[1]-1]
                    last_pose[least_point[0]][least_point[1]-1] = [least_point[0],least_point[1]]
                    open_points.append([least_point[0],least_point[1]-1])

            if(img[least_point[0]][least_point[1]+1][0] == 255):
                if(last_point[least_point[0]][least_point[1]+1] == -1) or ((last_point[least_point[0]][least_point[1]+1])>(last_point[least_point[0]][least_point[1]]+1+her[least_point[0]][least_point[1]+1])):
                    last_point[least_point[0]][least_point[1]+1] = last_point[least_point[0]][least_point[1]]+1+her[least_point[0]][least_point[1]+1]
                    last_pose[least_point[0]][least_point[1]+1] = [least_point[0],least_point[1]]
                    open_points.append([least_point[0],least_point[1]+1])

            if(img[least_point[0]+1][least_point[1]][0] == 255):
                # print(len(last_point))
                # print(len(least_point))
                #print(img[least_point[0]+1][least_point[1]][0])
                if(last_point[least_point[0]+1][least_point[1]] == -1) or ((last_point[least_point[0]+1][least_point[1]])>(last_point[least_point[0]][least_point[1]]+1+her[least_point[0]+1][least_point[1]])):
                    last_point[least_point[0]+1][least_point[1]] = last_point[least_point[0]][least_point[1]]+1+her[least_point[0]+1][least_point[1]]
                    last_pose[least_point[0]+1][least_point[1]] = [least_point[0],least_point[1]]
                    open_points.append([least_point[0]+1,least_point[1]])

            if(img[least_point[0]-1][least_point[1]][0] == 255):
                if(last_point[least_point[0]-1][least_point[1]] == -1) or ((last_point[least_point[0]-1][least_point[1]])>(last_point[least_point[0]][least_point[1]]+1+her[least_point[0]-1][least_point[1]])):
                    last_point[least_point[0]-1][least_point[1]] = last_point[least_point[0]][least_point[1]]+1+her[least_point[0]-1][least_point[1]]
                    last_pose[least_point[0]-1][least_point[1]] = [least_point[0],least_point[1]]
                    open_points.append([least_point[0]-1,least_point[1]])


            #check if its white

    #last_point is the point we want to go forward with
    #conditions we need to check
    #for each point you send in open points, you need to set it's last score and last pose
    #1) if its a new check the -1 condition
    #2) check in all 4 directions
    #3) if the point you are checking has already been discovered or not
    #4) for each point discovered or new path assign weight and trailing point
    #5) also need to check if the position is black or white
    #6) add the good ones to open_points
    #7) if the point is a dead end, simply remove it from the good_points list
    #8)

def placer( start, end):
    global last_pose,last_point
    img2 = img

    img2[end[0]][end[1]][1] = 0
    img2[start[0]][start[1]][1] = 0
    #print(last_pose[end[0]][end[1]])
    #print(start)
    #print(end)
    back_pose = last_pose[end[0]][end[1]]
    while( start[0]!=back_pose[0] or start[1]!=back_pose[1] ):
        img2[back_pose[0]][back_pose[1]][1]=0
        #print("12")
        back_pose = last_pose[back_pose[0]][back_pose[1]]
        #print(back_pose)

    return img2

def a_star(start,end):
    global img,last_point,last_pose
    #heur = her
    rows, cols, channel = img.shape
    # print("got10")
    open_points = [[start[0],start[1]]]
    # print("got11")
    last_point[start[0]][start[1]]=0
    last_pose[start[0]][start[1]]=[start[0],start[1]]
    # print("got12")
    # we need a function which takes in set of open_points
    # determines which one has the lowest score and uncover all its surrounding points

    #start, end,   open_points = mover(start,end,open_points)
    mover(start, end, open_points)
    # print("got20")
    img2 = placer(start, end)
    # print("got21")
    return img2



if __name__ == "__main__":
    #global img, dir_in, dir_out, name, png,start,end,heur


    rows,cols,channel = img.shape
    #print(img.shape)
    # print("got6")
    start = find(0,rows,cols)
    # print("got7")
    end = find(rows-1,rows,cols)
    # print("got8")
    create_heuristic(rows,cols)
    # print("got9")
    img2 = a_star(start,end)

    # print(her)
    #print(start)
    #print(end)
    #print(heur)
    #cv2.imshow('image', img)
    #print(img.shape)
    #cv2.waitKey(0)
    cv2.imwrite(dir_out+name+png,img2)
    print("output image generated")
    #cv2.destroyAllWindows()
    #print(img.shape())