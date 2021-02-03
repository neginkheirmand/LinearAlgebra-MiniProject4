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
            R[i][i]=S[i][i]
        else:
            break
    output = np.dot(U, R)
    output = np.dot(output, V)
    return output    
        
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
        k = -1
        while True :
            try:
                k = int(input("Please enter k:"))
                break
            except ValueError:
                print("Please enter a number")
                continue
        cv.imshow("Noisy -starting- Image", img)
        s = cv.waitKey(0)
        height, width, numChannels = img.shape
        newChannels = np.zeros((height, width, numChannels))
        for i in range( 0, numChannels):
            newMatx = process(k, i)
            np.add(newChannels, newMatx)
    else:
        return


# main()

A = np.array([[4, 11, 14], [8, 7, 2]])
U, S, V = np.linalg.svd(A)
print(U)
print()
print(S)
print()
print(V)
