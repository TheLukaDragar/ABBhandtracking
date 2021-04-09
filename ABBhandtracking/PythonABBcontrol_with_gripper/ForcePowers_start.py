import cv2
import numpy as np
import time
import socket
import threading
import config




# ABB Robot movement control using camera object tracking and packets
# Made by Luka Dragar 
#
# Follow me at @thelukadragar
# 
# Thanks to ABB forum and @amarlearningiamarpandey for handtracking
# 
# Enjoy!
#
# Change the config.py if needed
#
#
#
#
#
#
#

























hand_hist = None
traverse_point = []
total_rectangle = 9
hand_rect_one_x = None
hand_rect_one_y = None

hand_rect_two_x = None
hand_rect_two_y = None

corlist = ["0", "0","0"]
corlistold = ["0", "0","0"]
corxold = corlistold[0]
coryold = corlistold[1]
corzold= corlistold[2]
runthread=None

isdeafultareaset=None
defaultarea=0

sock=socket
isthreadrunning=None
firstoperatingmode=None
switchmode=False

connectionerror = False
outofframe = False
shutdown=False

grab=False


def rescale_frame(frame, wpercent=config.livefeedwindowscalex, hpercent=config.livefeedwindowscaley):
    width = int(frame.shape[1] * wpercent / 100)
    height = int(frame.shape[0] * hpercent / 100)
    return cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)


def contours(hist_mask_image):
    gray_hist_mask_image = cv2.cvtColor(hist_mask_image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray_hist_mask_image, 0, 255, 0)
    cont, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return cont


def max_contour(contour_list):
    max_i = 0
    max_area = 0
   
    for i in range(len(contour_list)):
        cnt = contour_list[i]
        

        area_cnt = cv2.contourArea(cnt)
       

        if area_cnt > max_area:
            max_area = area_cnt
            max_i = i

    return contour_list[max_i]





def draw_rect(frame):
    rows, cols, _ = frame.shape
    global total_rectangle, hand_rect_one_x, hand_rect_one_y, hand_rect_two_x, hand_rect_two_y

    hand_rect_one_x = np.array(
        [6 * rows / 20, 6 * rows / 20, 6 * rows / 20, 9 * rows / 20, 9 * rows / 20, 9 * rows / 20, 12 * rows / 20,
         12 * rows / 20, 12 * rows / 20], dtype=np.uint32)

    hand_rect_one_y = np.array(
        [9 * cols / 20, 10 * cols / 20, 11 * cols / 20, 9 * cols / 20, 10 * cols / 20, 11 * cols / 20, 9 * cols / 20,
         10 * cols / 20, 11 * cols / 20], dtype=np.uint32)

    hand_rect_two_x = hand_rect_one_x + 10
    hand_rect_two_y = hand_rect_one_y + 10

    for i in range(total_rectangle):
        cv2.rectangle(frame, (hand_rect_one_y[i], hand_rect_one_x[i]),
                      (hand_rect_two_y[i], hand_rect_two_x[i]),
                      (0, 255, 0), 1)

    return frame


def hand_histogram(frame):
    global hand_rect_one_x, hand_rect_one_y

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    roi = np.zeros([90, 10, 3], dtype=hsv_frame.dtype)

    for i in range(total_rectangle):
        roi[i * 10: i * 10 + 10, 0: 10] = hsv_frame[hand_rect_one_x[i]:hand_rect_one_x[i] + 10,
                                          hand_rect_one_y[i]:hand_rect_one_y[i] + 10]

    hand_hist = cv2.calcHist([roi], [0, 1], None, [180, 256], [0, 180, 0, 256])
    return cv2.normalize(hand_hist, hand_hist, 0, 255, cv2.NORM_MINMAX)


def hist_masking(frame, hist):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv], [0, 1], hist, [0, 180, 0, 256], 1)

    disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31))
    cv2.filter2D(dst, -1, disc, dst)

    ret, thresh = cv2.threshold(dst, 150, 255, cv2.THRESH_BINARY)

    # thresh = cv2.dilate(thresh, None, iterations=5)

    thresh = cv2.merge((thresh, thresh, thresh))

    return cv2.bitwise_and(frame, thresh)


def centroid(max_contour):
    global corlist
    

    moment = cv2.moments(max_contour)
    if moment['m00'] != 0:
        cx = str(int(moment['m10'] / moment['m00']))
        cy = str(int(moment['m01'] / moment['m00']))

        coordinates=["0","0"]
        coordinates[0] = str(round(int(cx)*config.cormultiplyx))
        coordinates[1] = str(round(int(cy)*config.cormultiplyy))

        corlist[0] = str(round(int(cx)*config.cormultiplyx))
        corlist[1] = str(round(int(cy)*config.cormultiplyy))

        return coordinates
    else:
        coordinates=["0","0"]
        coordinates[0]=0
        coordinates[1]=0
        return coordinates



def centroid2(max_contour):
    moment = cv2.moments(max_contour)
    if moment['m00'] != 0:
        cx = int(moment['m10'] / moment['m00'])
        cy = int(moment['m01'] / moment['m00'])

        return cx,cy
    else:
        
        return None



#def farthest_point(defects, contour, centroid):
 #   if defects is not None and centroid is not None:
  #      s = defects[:, 0][:, 0]
   #     cx, cy = centroid

    #    x = np.array(contour[s][:, 0][:, 0], dtype=np.float)
     #   y = np.array(contour[s][:, 0][:, 1], dtype=np.float)

      #  xp = cv2.pow(cv2.subtract(x, cx), 2)
       # yp = cv2.pow(cv2.subtract(y, cy), 2)
        #dist = cv2.sqrt(cv2.add(xp, yp))

#        dist_max_i = np.argmax(dist)

#        if dist_max_i < len(s):
 #           farthest_defect = s[dist_max_i]
  #          farthest_point = tuple(contour[farthest_defect][0])
   #         return farthest_point
    #    else:
     #       return None


def draw_circles(frame, traverse_point):
    if traverse_point is not None:
        for i in range(len(traverse_point)):
            cv2.circle(frame, traverse_point[i], int(5 - (5 * i * 3) / 100), [0, 255, 255], -1)


def manage_image_opr(frame, hand_hist):
    global isdeafultareaset
    global defaultarea
    global corlist
    hist_mask_image = hist_masking(frame, hand_hist)
    contour_list = contours(hist_mask_image)
    max_cont = max_contour(contour_list)
    myarea = ((cv2.contourArea(max_cont)/config.areatocompare)*config.zrange)+config.zoffsetcamera

    if isdeafultareaset==False:

        defaultarea = cv2.contourArea(max_cont)        
        isdeafultareaset= True
       
    myz = round(int(myarea)*config.cormultiplyz)
    corlist[2]=str(myz)

    cnt_centroid2 = centroid2(max_cont)
    cv2.circle(frame, cnt_centroid2, 5, [255, 0, 255], -1)

    if max_cont is not None:

        hull = cv2.convexHull(max_cont, returnPoints=False)
        defects = cv2.convexityDefects(max_cont, hull)
        cordinateee=centroid(max_cont)
        #FARPOINT CODE CAN USE FOR FINGER TRACKING
        #far_point = farthest_point(defects, max_cont, cnt_centroid)
        #print("Centroid : x=" +cordinateee[0] +" y=" +cordinateee[1]+ ", farthest Point : not used")
        #str(far_point)
       # cv2.circle(frame, far_point, 5, [0, 0, 255], -1)
       # if len(traverse_point) < 20:
        #    traverse_point.append(far_point)
        #else:
         #   traverse_point.pop(0)
          #  traverse_point.append(far_point)

        draw_circles(frame, traverse_point)

def mythread():
    global corxold
    global coryold
    global corlistold
    global corlist
    global isthreadrunning
    global sock
    global firstoperatingmode
    global switchmode
    global connectionerror
    global shutdown
    global grab

    isthreadrunning=True
   
    if runthread:
    
        corx = str(int(corlist[0]) + config.xoffset)
        cory = str(int(corlist[1]) + config.yoffset)
        corz = str(int(corlist[2]) + config.zoffset)

        corxold = str(int(corlistold[0]) + config.xoffset)
        coryold = str(int(corlistold[1]) + config.yoffset)
        corzold = str(int(corlistold[2]) + config.zoffset)


        diffx = int(corx)-int(corxold)
        diffy = int(cory)-int(coryold)
        diffz = int(corz)-int(corzold)

        #check if object moved 
        xrange= range(config.xmin, config.xmax)
        yrange= range(config.ymin, config.ymax)
        zrange = range(config.zmin, config.zmax)

        inframeoflimits= (int(corx) in xrange) and (int(cory) in yrange) and (int(corz) in zrange)

        if((diffx > 1 or diffx < -1 or diffy > 1 or diffy < -1 or diffz > 1 or diffz < -1)and inframeoflimits):
            corxold = str(int(corlist[0]) + config.xoffset)
            coryold = str(int(corlist[1]) + config.yoffset)
            corzold = str(int(corlist[2])+ config.zoffset)
            corlistold[0] = corlist[0]
            corlistold[1] = corlist[1]
            corlistold[2] = corlist[2]

           
            try:
                if switchmode==True:
                     sock.send(bytes(firstoperatingmode, 'UTF-8'))
                     switchmode=False
                if grab:
                    sock.send(bytes("g", 'UTF-8'))
                    grab=False
                         
            
                if firstoperatingmode=="xy"and switchmode == False:
                    print("sending coordinates x=" + corx+" y= " + cory)
                    sock.send(bytes(corx+";"+cory, 'UTF-8'))

                if firstoperatingmode == "xyz" and switchmode == False:
                    print("sending coordinates x=" +corx+" y= " + cory+" z= " + corz)
                    sock.send(bytes(corx+";"+cory+";"+corz, 'UTF-8'))

            except socket.error:
                connectionerror=True
        else:
           if inframeoflimits==False:
               print("out of limits")
    if shutdown==False:
        threading.Timer(config.sendinginterval, mythread).start()

    
def connectplease():
     global sock
     global connectionerror
     sock = socket.socket(socket.AF_INET, socket.TCP_NODELAY)
     sock.connect((config.myIP, config.myPort))
     print("conected")
     print(sock.recv(4096).decode('UTF-8'))
     connectionerror = False
     

def tryconnect():
    tries = 3

    for i in range(tries):
        try:
            connectplease()
            
        except Exception as e:
            if i < tries - 1:  # i is zero indexed
                print(e)
                connectionerror=True
                print("reconecting....")
                sock.close()

                continue
            else:
                input("could not connect press any key to retry")
                tryconnect()
                
        break   


staticmethod
def __draw_label(img, text, pos, bg_color):
    font_face = cv2.FONT_HERSHEY_PLAIN
    scale = 1.2
    color = (0, 0, 0)
    thickness = cv2.FILLED
    margin = 2

    txt_size = cv2.getTextSize(text, font_face, scale, thickness)

    end_x = pos[0] + txt_size[0][0] + margin
    end_y = pos[1] - txt_size[0][1] - margin

    cv2.rectangle(img, pos, (end_x, end_y), bg_color, thickness)
    cv2.putText(img, text, pos, font_face, scale, color, 1, cv2.LINE_AA)





def main():
    print("awaiting connection...")
    global sock
    global firstoperatingmode


    tryconnect()
   


    #sock.send(bytes("0;0;0;0.707106781;0;0;0.707106781;0;0;0;1", 'UTF-8')) full move example x; y; z; ; ; ; ; ; ;..

    firstoperatingmode=config.operatingmode
    print("operating mode ="+firstoperatingmode)

    sock.send(bytes(firstoperatingmode, 'UTF-8'))

    print("starting camera....")


    global hand_hist
    is_hand_hist_created = False
    global corlist
    global corxold
    global coryold
    global runthread
    global isthreadrunning
    global isdeafultareaset
    global switchmode
    pauseme=False
    global connectionerror
    global outofframe
    global shutdown
    isdeafultareaset=False
    shutdown=False

    global grab


    connectionerror = False
    outofframe = False
    runthread=False
    isthreadrunning=False
    mythread()

    #capture = cv2.VideoCapture("http://192.168.64.102:8080/video")

    capture = cv2.VideoCapture(config.cameratouse)
    print("press z to start tracking")

    while capture.isOpened():
        pressed_key = cv2.waitKey(1)
        _, frame = capture.read()

        if pressed_key & 0xFF == ord('z'):
            is_hand_hist_created = True
            hand_hist = hand_histogram(frame)

        if is_hand_hist_created and pauseme==False and outofframe==False and connectionerror==False:
            try:
                manage_image_opr(frame, hand_hist)
                runthread= True
            except Exception as e:
                print(e)
                runthread = False
                print("out of frame")
                outofframe=True
                 
        else:
            frame = draw_rect(frame)


        frm = cv2.flip(rescale_frame(frame),1)

        if pauseme:
            __draw_label(frm, "tracking paused press p to resume", (0,20), (255,255,255))
            runthread=False
        if connectionerror:
            __draw_label(frm, "disconected press e to reconnect", (0, 20), (255, 255, 255))
            
        if outofframe:
            __draw_label(frm, "object out of frame press e to resume", (0, 20), (255, 255, 255))
            
        if is_hand_hist_created==False:
            __draw_label(frm, "press z to capture objects color in green squares", (0, 20), (255, 255, 255))

        if grab:
            __draw_label(frm, "Robot grabbing", (0, 40), (255, 255, 255))
            pass
            

        cv2.imshow("Live Camera Feed", frm)

       
        if pressed_key == 27:#escape key
            runthread = False
            shutdown=True
            break

        if pressed_key == 99:# press c to change config
            
            if firstoperatingmode=="xy":
                firstoperatingmode = "xyz"
                print("switching to xyz")
                switchmode = True
            else:
                if firstoperatingmode == "xyz":
                    firstoperatingmode = "xy"
                    print("switching to xy")
                    switchmode = True


        if pressed_key == 103:# press g to grab/realease
            
            if grab==True:
                
                print("Realising")
                grab=False
            else:
                if grab == False:
                    
                    print("Grabbing")
                    grab=True


        if pressed_key == 112:# p to pause
            if pauseme==True:
                pauseme = False
            else:
                pauseme=True
                runthread=False
                print("tracking paused pres p to resume")
            #input("paused press any key to continue")


        if pressed_key == 114:# restart histogram - key r
            is_hand_hist_created = False
            print(" restarted color maping press z to continue")
            #input("paused press any key to continue")


        if pressed_key == 101:# restart tracking - key e
            if outofframe==True:
                outofframe=False
            else:
                if connectionerror:
                    tryconnect()
                

            
           
            #input("paused press any key to continue")



    cv2.destroyAllWindows()
    capture.release()
    


if __name__ == '__main__':
    main()
    exit
