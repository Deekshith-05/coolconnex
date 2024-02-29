import cv2
import csv
import os
import webbrowser
# import datetime
from datetime import date
from datetime import datetime
from datetime import timedelta
from tabulate import tabulate
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def sendmail(text, html, data, subject, header):
    me = 'coolconnex901@gmail.com'
    password = "vuva lisc ajlh psqq"
    server = 'smtp.gmail.com:587'
    #you = input()
    you = ['20311a04b0@sreenidhi.edu.in','20311a04b1@sreenidhi.edu.in','20311a04a9@sreenidhi.edu.in']

    #sorting in order of expiry
    data=(sorted(data, key = lambda x: x[len(x)-1]))

    text = text.format(table=tabulate(data, headers=header, tablefmt="grid"))
    html = html.format(table=tabulate(data, headers=header, tablefmt="html"))

    path=os.path.abspath('sample.html')
    url='file://' +path

    with open(path,'w') as f:
        f.write(html)
    webbrowser.open(url)

    message = MIMEMultipart(
        "alternative", None, [MIMEText(text), MIMEText(html,'html')])
    message['Subject'] = subject
    message['From'] = me
    message['To'] = ",".join(you)
    server = smtplib.SMTP(server)
    server.ehlo()
    server.starttls()
    server.login(me, password)
    server.sendmail(me, you, message.as_string())
    server.quit()

def maillist():
    text = """
    Hello, User.
    Here is your data:
    {table}
    Regards,
    Smart Fridge"""

    html = """
    <html><body><p>Hello, User.</p>
    <p>Here is your data:</p>
    {table}
    <p>Regards,</p>
    <p>Smart Fridge</p>
    </body></html>
    """

    with open('items_list.csv') as input_file:
        reader = csv.reader(input_file)
        data = list(reader)
    header="firstrow"
    subject="Items in your fridge"
    sendmail(text,html,data,subject,header)
    print("=>  Mail Sent  <=")


def alert():
    text = """
    Hello, User.
    Here is the list of Items about to expire:
    {table}
    Regards,
    Smart Fridge"""

    html = """
    <html><body><p>Hello, User.</p>
    <p>Here is the list of Items about to expire:</p>
    {table}
    <p>Regards,</p>
    <p>Smart Fridge</p>
    </body></html>
    """

    with open('items_list.csv') as input_file:
        reader = csv.reader(input_file)
        ldata = list(reader)
    #alert prior to expiry
    alertdays=2
    #sorting in order of expiry
    ldata=(sorted(ldata, key = lambda x: x[2]))
    data=[]
    for i in range(1,len(ldata)):
        datestr=(datetime.strptime(ldata[i][2][:10],"%Y-%m-%d"))
        #print(type(datestr))
        p=datetime.combine(date.today(),datetime.min.time())
        x=datestr-p
        if(x.days>alertdays):
            break
        data.append([ldata[i][0],ldata[i][2]])

    if(len(data)>=1):
        subject= "Alert!! Items about to Expire"
        header = ["Item Name","Date of Expiry"]
        sendmail(text, html, data, subject, header)
        print("=>  Alert Sent  <=")
        #prevdate=date.today()
    else:
        print("Your Fridge is Fresh!")

def insert():
    #recognition
    thres = 0.70 # Threshold to detect object

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # cap.set(3,1280)
    # cap.set(4,720)
    # cap.set(10,70)
    # print(cap)
    classNames= []
    classFile = 'coco.names'
    with open(classFile,'rt') as f:
        classNames = f.read().rstrip(' ').split('\n')
    # print(classNames)
    configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
    weightsPath = 'frozen_inference_graph.pb'

    net = cv2.dnn_DetectionModel(weightsPath,configPath)
    net.setInputSize(320,320)
    net.setInputScale(1.0/ 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)
    if(True):
        i = 1
        flag = False
        while(True):
            success,img = cap.read()
            # cv2.imshow('',img)
            classIds, confs, bbox = net.detect(img,confThreshold=thres)
                # print(classIds,bbox)

            if len(classIds) != 0:
                for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
                    cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                    prev = 'person'
                    if(classNames[classId-1]!=prev and (classNames[classId-1]=='banana' or classNames[classId-1]=='apple' or classNames[classId-1]=='orange' or classNames[classId-1]=='broccoli' or classNames[classId-1]=='tomato' or classNames[classId-1]=='carrot')):
                        print("added",classNames[classId-1],"list updated")
                        prev = classNames[classId-1]
                        with open('items_list.csv', mode='a',newline='') as items_list:
                            #to avoid extra line gaps
                            items_writer = csv.writer(items_list, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                            today = date.today()
                            dateTimeObj = datetime.now()
                            day = ""
                            day += str(dateTimeObj.day)+"-"+str(dateTimeObj.month)+"-"+str(dateTimeObj.year)+" "+str(dateTimeObj.hour)+":"+str(dateTimeObj.minute)
                            # date = datetime.datetime().strftime(today,"%d-%m-%Y, %H:%M")
                            if(classNames[classId-1]=='banana'):
                                expiry = today + timedelta(days=4)
                                items_writer.writerow([classNames[classId-1], day, expiry])
                            elif(classNames[classId-1]=='apple'):
                                expiry = today + timedelta(days=6)
                                items_writer.writerow([classNames[classId-1], day, expiry])
                            elif(classNames[classId-1]=='carrot'):
                                expiry = today + timedelta(days=7)
                                items_writer.writerow([classNames[classId-1], day, expiry])
                            elif(classNames[classId-1]=='orange'):
                                expiry = today + timedelta(days=5)
                                items_writer.writerow([classNames[classId-1], day, expiry])
                            elif(classNames[classId-1]=='broccoli'):
                                expiry = today + timedelta(days=3)
                                items_writer.writerow([classNames[classId-1], day, expiry])    
                            else:
                                expiry = today + timedelta(days=4)
                                items_writer.writerow([classNames[classId-1], day, expiry])
                            
                        flag = True
                        break
                    # cv2.putText(img,classNames[classId-1],(box[0]+10,box[1]+30),
                    # cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    # cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                    # cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
            if(flag == True):
                break
            cv2.imshow('Output',img)
            cv2.waitKey(1)

def delete():
    #store csv file data into list
    with open('items_list.csv') as input_file:
        reader = csv.reader(input_file)
        data = list(reader)
    #recognition
    thres = 0.70 # Threshold to detect object

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # cap.set(3,1280)
    # cap.set(4,720)
    # cap.set(10,70)
    # print(cap)
    classNames= []
    classFile = 'coco.names'
    with open(classFile,'rt') as f:
        classNames = f.read().rstrip(' ').split('\n')
    # print(classNames)
    configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
    weightsPath = 'frozen_inference_graph.pb'

    net = cv2.dnn_DetectionModel(weightsPath,configPath)
    net.setInputSize(320,320)
    net.setInputScale(1.0/ 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)
    if(True):
        i = 1
        flag = False
        while(True):
            success,img = cap.read()
            # cv2.imshow('',img)
            classIds, confs, bbox = net.detect(img,confThreshold=thres)
                # print(classIds,bbox)

            if len(classIds) != 0:
                for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
                    cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                    prev = 'person'
                    if(classNames[classId-1]!=prev and (classNames[classId-1]=='banana' or classNames[classId-1]=='apple' or classNames[classId-1]=='orange' or classNames[classId-1]=='broccoli' or classNames[classId-1]=='tomato' or classNames[classId-1]=='carrot')):
                        prev = classNames[classId-1]
                        with open('items_list.csv', mode='a',newline='') as items_list:
                            items_writer = csv.writer(items_list, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                            today = date.today()
                            dateTimeObj = datetime.now()
                            day = ""
                            day += str(dateTimeObj.day)+"-"+str(dateTimeObj.month)+"-"+str(dateTimeObj.year)+" "+str(dateTimeObj.hour)+":"+str(dateTimeObj.minute)
                            # date = datetime.datetime().strftime(today,"%d-%m-%Y, %H:%M")
                            #delete oldest occurance of the item
                            for idx in range(len(data)):
                                if(data[idx][0]==classNames[classId-1]):
                                      print("deleted",data[idx][0],"inserted on",data[idx][1])
                                      data.remove(data[idx])
                                      break 
                            with open('items_list.csv', 'w', newline='') as writeFile:
                                writer = csv.writer(writeFile)
                                writer.writerows(data)

                        flag = True
                        break
                    # cv2.putText(img,classNames[classId-1],(box[0]+10,box[1]+30),
                    # cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    # cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                    # cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
            if(flag == True):
                break
            cv2.imshow('Output',img)
            cv2.waitKey(1)

#main code
k = input("Enter your choice\n \ti to insert\td to delete\tm to mail\ta to alert\ts to stop\n")
if(k=='i'):
    while(k=='i'):
        insert()
        k = input("Enter your choice\n\ti to insert\ts to stop\n")
elif(k=='m'):
    maillist()
elif(k=='a'):
    alert()
elif(k=='d'):
    while(k=='d'):
        delete()
        k = input("Enter your choice\n\td to insert\ts to stop\n")
else:
    exit(0)