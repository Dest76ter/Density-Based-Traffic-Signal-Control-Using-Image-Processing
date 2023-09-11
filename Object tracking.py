import cv2
import numpy as np
from object_detection import ObjectDetection
import math
import time
import serial
import random


#ser = serial.Serial('COM5', 9600)
# Initialize Object Detection

od = ObjectDetection()
cap =cv2.VideoCapture(0) # Opens the base camera 
# cap = cv2.VideoCapture("http:IP ADDRESS/video") # Can also be used with an IP camera


allowed_objects = ["car", "truck", "bus", "motorbike"]
vehicles_entering = []


center_points_prev_frame = []


def Detect_vehicles(value, lane):

    # pts array is used to create a polygon, to only detect the vehicles present inide it
    pts = np.array([[1150, 100], [1150, 1080],
                [1750, 1080], [1750, 50]],
               np.int32)
    
    pts = pts.reshape((-1, 1, 2))


    center_points_prev_frame = []
    tracking_objects = {}
    tofindmaxlist = []
    mean_list = []
    track_id = 0
    count_time = 0
    count = 0
    # cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture("los_angeles.mp4")

    

    """ 
    If you are using a single camera for multiple lanes, the position of polygon can be different
    So there needs to be manual adjustment for all lanes.

    if lane == 0:
        pts = np.array([[1150, 100], [1150, 1080],
                        [1750, 1080], [1800, 50]],
                       np.int32)
        pts = pts.reshape((-1, 1, 2))

    elif lane == 1:
        pts = np.array([[950, 100], [950, 1080],
                        [1750, 1080], [1750, 50]],
                       np.int32)

        pts = pts.reshape((-1, 1, 2))

    elif lane == 2:
        pts = np.array([[900, 100], [1000, 1080],
                        [1750, 1080], [1750, 50]],
                       np.int32)
        pts = pts.reshape((-1, 1, 2)) """

    while cap.isOpened():
        ret, frame = cap.read()
        count += 1
        count_time += 1
        if count % 3 != 0:
            continue

        # Point current frame
        center_points_cur_frame = []

        # Detect objects on frame
        (class_ids, scores, boxes) = od.detect(frame)
        for box in boxes:
            (x, y, w, h) = box
            cx = int((x + x + w) / 2)
            cy = int((y + y + h) / 2)


            # Helps with the detection of vehicles in the Polygon
            cv2.polylines(frame, [pts], True, (15, 220, 10), 6)
            result = cv2.pointPolygonTest(pts, (int(cx), int(cy)), False)

            if result >= 0:
                center_points_cur_frame.append((cx, cy))
                # print("FRAME N°", count, " ", x, y, w, h)
                class_name = od.classes[class_ids[0]]
                if class_name in allowed_objects and (w * h < 250*250):
                    # cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                    color = od.colors[class_ids[0]]
                    # cv2.putText(frame,"{}".format(class_name), (x,y -15), cv2.FONT_HERSHEY_PLAIN,2,color, 2)
                    cv2.rectangle(frame, (x, y), (x + w, y + h),
                                  (0, 255, 0), 2)

        # Only at the beginning we compare previous and current frame
        if count <= 2:
            for pt in center_points_cur_frame:
                for pt2 in center_points_prev_frame:
                    distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])

                    if distance < 30:
                        tracking_objects[track_id] = pt
                        track_id += 1
        else:

            tracking_objects_copy = tracking_objects.copy()
            center_points_cur_frame_copy = center_points_cur_frame.copy()

            for object_id, pt2 in tracking_objects_copy.items():
                object_exists = False
                for pt in center_points_cur_frame_copy:

                    distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])

                    # Update IDs position
                    if distance < 30:
                        tracking_objects[object_id] = pt
                        object_exists = True
                        if pt in center_points_cur_frame:
                            center_points_cur_frame.remove(pt)
                        continue

                # Remove IDs lost
                if not object_exists:
                    tracking_objects.pop(object_id)

            # Add new IDs found
            for pt in center_points_cur_frame:
                tracking_objects[track_id] = pt
                track_id += 1

        print("Number of vehicles {}".format(len(tracking_objects)))
        imS = cv2.resize(frame, (960, 540))
        cv2.imshow("Frames", imS)
        center_points_prev_frame = center_points_cur_frame.copy()
        mean_list.append(len(tracking_objects))

        getcount(count_time, value, cap)

        key = cv2.waitKey(1)
        if key == 27:
            break


    # print(math.ceil(sum(mean_list)/len(mean_list)))
    return round(sum(mean_list)/len(mean_list))


def getcount(count_time, value, cap):
    if count_time > value:
        cap.release()
        cv2.destroyAllWindows()


def Send_data_to_arduino(y):
    ser.write((str(y) + '\r').encode())
    print(y)


def motor_control():
    ser.write(('Done\r').encode())
    time.sleep(1)
    while ser.in_waiting == 0:
        pass


while True:
    while ser.in_waiting == 0:
        pass
    # print(str(ser.readline(),'utf-8').strip('\r\n') == "Capture")
    if str(ser.readline(), 'utf-8').strip('\r\n') == "Capture":
        for i in range(0, 1):
            vlist = []
            sendinglist = []
            for j in range(0, 3):
                # n = int(input())
                vlist.append(Detect_vehicles(50, j))
                print('\n')
                motor_control()

            time_delay_list = []
            for i in range(len(vlist)):
                if vlist[i] <= 5:
                    time_delay_list.append(vlist[i] * 3000)
                elif vlist[i] <= 10:
                    time_delay_list.append(vlist[i] * 4000)
                elif vlist[i] <= 15:
                    time_delay_list.append(vlist[i] * 5000)
                elif vlist[i] <= 20:
                    time_delay_list.append(vlist[i] * 6000)
                else:
                    time_delay_list.append(vlist[i] * 7000)

            for i in range(3):
                if time_delay_list[i] == 0:
                    time_delay_list[i] = 1000

            print(time_delay_list)
            sorted_indices = sorted(range(len(vlist)), key=lambda i: vlist[i], reverse=True)

            # Use the indices to rearrange list1
            time_delay_list = [time_delay_list[i] for i in sorted_indices]

            # Print the rearranged list1
            print(time_delay_list)
            print(vlist)
            for i in range(0, 3):
                tmp = (vlist.index(max(vlist)))
                # print(tmp)
                sendinglist.append(tmp+1)
                vlist[tmp] = -1

            ser.write((str(10) + '\r').encode())
            for i in sendinglist:
                time.sleep(1)
                Send_data_to_arduino(i)
            for i in time_delay_list:
                time.sleep(1)
                Send_data_to_arduino(i)

            time.sleep(1)
