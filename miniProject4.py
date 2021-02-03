import cv2 as cv
import sys
import numpy as np

img = None
U=None
S=None 
V= None
def readFile():
    global img
    #if you change the input image, rememmber to chaneg the name of file in the line bellow 
    #change the file format(.png .jpg .bmp ...) of the output file -in method saveFile()- accordingly
    img = cv.imread("coffee.png",1)
    if img is None:
        sys.exit("Could not read the image.")
        return False
    return True
    
#the rgb value is the index of the channel under process
def process(k, rgb ):
    #U*R*Vᵗ = Cleared
    #U*S*Vᵗ = Noisy_Matrix
    global U, S, V
    global img
    U, S, V = np.linalg.svd(img)
    bChannel, gChannel, rChannel = cv.split(S)
    height, width = img.shape
    R = np.zeros((height, width))
    r = min(height, width)
    #we now that the number of non zero diagonal values are r and r is less than/equal to the min of height and wifth 
    for i in range(0, r):
        if i<=k:
            R[i][i]=S[i][i]
        else:
            break
    
        






def saveFile():
    global img
    cv.imshow("Display window", img)
    print("press s key to save the file and close the window")
    k = cv.waitKey(0)
    if k == ord("s"):
        print("the image was save as clean.jpg")
        cv.imwrite("clean.jpg", img)

def main():
    global img
    if readFile():
        cv.imshow("Noisy Image", img)
        print(img.shape)        
        k = cv.waitKey(0)

    else:
        return


main()