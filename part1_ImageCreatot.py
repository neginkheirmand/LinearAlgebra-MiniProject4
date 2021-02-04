import sys
import numpy as np
import cv2 as cv

def readFile():
    #if you change the input image, rememmber to changed the name of file in the line bellow 
    #change the file format(.png .jpg .bmp ...) of the output file -in method saveImg()- accordingly
    img = cv.imread("noisy.jpg",1)
    if img is None:
        sys.exit("Could not read the image.")
    cv.imshow("Noisy -starting- Image", img)
    print("To continue press any key")
    k = cv.waitKey(0)
    return img
    

def putInMatrix(newChannels, newMatx, channel):
    height, width = newMatx.shape
    for i in range(0, height):
        for j in range(0, width):
            newChannels[i][j][channel]= int(newMatx[i][j])
    return

    
#the rgb value is the index of the channel under process
def process(k, rgbChannel, img ):
    #U*R*Vᵗ = Cleared
    #U*S*Vᵗ = Noisy_Matrix
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
    

def imageCreator():
    #using this function we can see the change for each k given to the scrypt for part 1 of project
    img=readFile()
    height, width, depth = img.shape
    i = 0
    while i< min(height, width):
        k = i
        output = np.zeros((height, width, depth), dtype=np.uint8)
        for j in range(0, depth):
            newChannel = process(k, j, img )
            putInMatrix(output, newChannel, j)
        newName = ".\\firstPartRevolutionOfK\\newClean"+str(i)+".jpg"
        cv.imwrite(newName, output)
        print("the image was saved as",newName)
        i+=5
imageCreator()