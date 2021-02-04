#Using OpenCV
import cv2 as cv
import sys
import numpy as np


img = None

def readFile():
    global img
    #if you change the input image, rememmber to changed the name of file in the line bellow 
    #change the file format(.png .jpg .bmp ...) of the output file -in method saveImg()- accordingly
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
    global img
    imageChannel = img[:,:,rgbChannel]
    U, S, V = np.linalg.svd(imageChannel)
    #Taking SVD computation as A= U D (V^T), For U, D, V = np.linalg.svd(A), this function returns V in Vᵗ form already.
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
    
def saveImg(newChannels):
    print("press s key to save the file, if you dont want to save it press any other key")
    cv.imshow("Final Denoised Version of the image", newChannels)
    k = cv.waitKey(0)
    if k == ord("s"):
        cv.imwrite("newClean.jpg", newChannels)
        print("the image was saved as clean.jpg")
        return
    else: 
        print("Was not saved")
        return

def putInMatrix(newChannels, newMatx, channel):
    height, width = newMatx.shape
    for i in range(0, height):
        for j in range(0, width):
            newChannels[i][j][channel]= int(newMatx[i][j])
    return


def main():
    global img
    if readFile():
        #get input form user
        k = -1
        while True :
            try:
                k = int(input("Please enter k:"))
                break
            except ValueError:
                print("Please enter a number")
                continue

        height, width, numChannels = img.shape
        newChannels = np.zeros((height, width, numChannels), dtype=np.uint8)
        for i in range( 0, numChannels):
            newMatx = process(k, i)
            
            putInMatrix(newChannels, newMatx, i)
            #you can also use the line above to put the output image into each channel but the method putInMatrix has casting integrated
            # so its preferable to use the method putInMatrix  
            # newChannels[:,:,i]=newMatx

            # if you want to see the process of denoising each of the channels, un-comment the following lines
            # cv.imshow("new Channel Dinoised", newChannels)
            # key = cv.waitKey(0)
        saveImg(newChannels)
    else:
        return


main()
