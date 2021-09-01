import imghdr
import cv2
from os import listdir

for file in listdir("presivir/Games by Gameness/Not Game/"):  
    image = cv2.imread("presivir/Games by Gameness/Not Game/" + file)
    file_type = imghdr.what("presivir/Games by Gameness/Not Game/" + file)
    if file_type != 'jpeg':  
        print(file +  " - invalid - " +  str(file_type))  
        cv2.imwrite("presivir/Games by Gameness/Not Game/" + file, image)