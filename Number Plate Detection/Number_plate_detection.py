                        #vehicle Number Plate Detection using Python(OpenCv & pytesseract)
import cv2
import numpy as np
import imutils #to resize image
import pytesseract
import sqlite3

con=sqlite3.connect('NumberPlates.db')  #connection to database
cur=con.cursor()


pytesseract.pytesseract.tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe" #pytesseract path

img=cv2.imread('C://python//car2.jpg')      #takes Image
img=imutils.resize(img,width=300)           #convert Image Size
cv2.imshow("Original Image",img)
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)   #Convert Normal Image To gray Scale Image
cv2.imshow("Gray Image",gray)

flter=cv2.bilateralFilter(gray,11,15,15)    #Removes unwanted Noise From Gray Scale Image
cv2.imshow("Cleard Gray Image",flter)

edged=cv2.Canny(flter,170,200)              #Detect only edge of img with min and max threshold value
cv2.imshow("Edges of Iamge",edged)

contor,href=cv2.findContours(edged,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)   #Finds all Possible Contours
ctn=sorted(contor,key=cv2.contourArea,reverse=True)[:30]                    #Takes only largest 30 Contours
numberplate_count=None

temp=img.copy()
cv2.drawContours(temp,ctn,-1,(255,0,0),2)      #Draw all Possible Contours
cv2.imshow("Best 30 Contours In Img",temp)



count=0
name=1  #name of croped images


for c in ctn:
    peri=cv2.arcLength(c,True)                      #Perimeter 
    epsilon=0.02*peri
    approx=cv2.approxPolyDP(c,epsilon,True)
             
    if len(approx)==4:
        numberplate_count=approx
        x,y,w,h=cv2.boundingRect(c)         #draw rectangle
        crp_img=img[y:y+h,x:x+w]            #Takes only Number plate part of Image(Croped Image)

        cv2.imwrite(str(name)+'.png',crp_img)   #saves croped Image
        name+=1
        break
cv2.drawContours(img,[numberplate_count],-1,(255,0,0),2)    #draw contorous(Polygon) on only Number plate
cv2.waitKey(0)


crp_img_loc='1.png' 
cv2.imshow("Number Plate",cv2.imread(crp_img_loc))  #Load the croped Image
cv2.waitKey(0)                                      #hold for some time


text1=pytesseract.image_to_string(crp_img_loc,lang='eng')   #pytesseract to convert image to string with english lang
print("Number is",text1)
cv2.waitKey(0)
#cur.execute('''DROP TABLE IF EXISTS Number_plate''')
#cur.execute('''CREATE TABLE Number_plate(Number TEXT)''')
cur.execute('''INSERT INTO Number_plate(Number)VALUES(?)''',(text1,))   #insert number plate text in database
con.commit()
cur.close()