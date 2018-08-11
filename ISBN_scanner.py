from __future__ import print_function
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import time
import re

cap = cv2.VideoCapture(0)
 
def decode(im) : 
  # Find barcodes and QR codes
  decodedObjects = pyzbar.decode(im)
  
  # Print results
  for obj in decodedObjects:
    print('Type : ', obj.type)
    print('Data : ', obj.data,'\n')

  return decodedObjects
 
 
# Display barcode and QR code location  
def display(im, decodedObjects):
 
  # Loop over all decoded objects
  for decodedObject in decodedObjects: 
    points = decodedObject.polygon
 
    # If the points do not form a quad, find convex hull
    if len(points) > 4 : 
      hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
      hull = list(map(tuple, np.squeeze(hull)))
    else : 
      hull = points;
     
    # Number of points in the convex hull
    n = len(hull)
 
    # Draw the convext hull
    for j in range(0,n):
      cv2.line(im, hull[j], hull[ (j+1) % n], (255,0,0), 3)
 
  # Display results 
  cv2.imshow("Results", im);
  cv2.waitKey(0);
 


  

# Main 
if __name__ == '__main__':

  # 顯示現在時間
  utc_data = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()) 
  #print(utc_data)  



  # 開啟鏡頭
  while(cap.isOpened()):
    ret, frame = cap.read()
    cv2.imshow('frame',frame) 
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
    if cv2.waitKey(1) & 0xFF == ord('s'):
      utc_data = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()) 
      cv2.imwrite(utc_data + '.jpg', frame)
      break

  cap.release()
  cv2.destroyAllWindows()


  # 讀取影像
  im = cv2.imread(utc_data + '.jpg')
  # 解碼讀入的影像
  decodedObjects = decode(im)
  display(im, decodedObjects)

  