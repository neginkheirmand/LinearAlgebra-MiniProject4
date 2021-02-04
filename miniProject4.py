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
    img = cv.imread("noisy.jpg",1)
    if img is None:
        sys.exit("Could not read the image.")
        return False
    cv.imshow("Noisy -starting- Image", img)
    print("To continue press any key")
    k = cv.waitKey(0)
    return True
    
#the rgb value is the index of the channel under process
def process(k, rgbChannel ):
    #U*R*Vᵗ = Cleared
    #U*S*Vᵗ = Noisy_Matrix
    global U, S, V
    global img
    imageChannel = img[:,:,rgbChannel]
    U, S, V = np.linalg.svd(imageChannel)
    height, width = imageChannel.shape
    R = np.zeros((height, width))
    r = min(height, width)
    #we now that the number of non zero diagonal values are r and r is less than/equal to the min of height and wifth 
    for i in range(0, r):
        if i<=k:
            R[i][i]=S[i]
        else:
            break
    output = np.dot(U, R)
    output = np.dot(output, V)
    return output    
        
def saveFile(matrix):
    print("press s key to save the file, if you dont want to save it press any other key")
    cv.imshow("Final Denoised Version of the image", matrix)
    k = cv.waitKey(0)
    if k == ord("s"):
        print("the image was save as clean.jpg")
        
        cv.imwrite("newClean.jpg", matrix)
        exit()
    else: 
        print("Was not saved")
        exit()

def putInMatrix(newChannels, newMatx, channel):
    height, width = newMatx.shape
    for i in range(0, height):
        for j in range(0, width):
            newChannels[i][j][channel]= newMatx[i][j]
    return

def main():
    global img
    if readFile():
        k = -1
        while True :
            try:
                k = int(input("Please enter k:"))
                break
            except ValueError:
                print("Please enter a number")
                continue
        height, width, numChannels = img.shape
        newChannels = np.zeros((height, width, numChannels))
        for i in range( 0, numChannels):
            newMatx = process(k, i)
            putInMatrix(newChannels, newMatx, i)
            cv.imshow("new Channel Dinoised", newChannels)
            key = cv.waitKey(0)
        saveFile(newChannels)
    else:
        return


main()
