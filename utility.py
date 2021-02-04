from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import math


#the same proces function in part 1 of the project
# this is method the main provider of the denoised version of the matrix
# process of denoising
def process(k, img):
    U, S, V = np.linalg.svd(img.copy())
    #Taking SVD computation as A= U D (V^T), For U, D, V = np.linalg.svd(A), this function returns V in Vᵗ form already.
    height, width = img.shape
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
    
def get_main_function():
    x = np.linspace(0, math.pi * 3 / 2, 30)
    y = np.linspace(0, math.pi * 3 / 2, 30)
    X, Y = np.meshgrid(x, y)
    return np.sin(X * Y)

def get_function():
    return make_function_noisy(get_main_function())


def make_function_noisy(z):
    max_noise = 0.1
    t = 2 * np.random.rand(30 * 30) * max_noise - max_noise
    t = t.reshape(30, 30)
    
    return np.add(z, t)


def show_my_matrix(Z, name):
    x = np.linspace(0, math.pi * 3 / 2, 30)
    y = np.linspace(0, math.pi * 3 / 2, 30)
    X, Y = np.meshgrid(x, y)
    ax = plt.axes(projection='3d')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                    cmap='viridis', edgecolor='black')
    ax.set_title(name)
    ax.view_init(60, 35)
    plt.show()


def show_main():
    Z = get_main_function()
    show_my_matrix(Z, 'surface')


def show_noisy():
    # Z = get_function()
    x = np.linspace(0, math.pi * 3 / 2, 30)
    y = np.linspace(0, math.pi * 3 / 2, 30)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(X * Y)
    show_my_matrix(Z, 'surface')


def showAllDenoised():
    output = get_function()
    for k in range(0,30):
        newDenoisedVersion = process(k, output)
        newName = ".\\SecondPart\\format1\\F1__"+str(k+1)+".jpg"
        plt.imsave(newName, newDenoisedVersion)
        print("the image was saved as",newName)
        show_my_matrix(newDenoisedVersion, 'surface'+str(k+1))


#if we un-comment the next line we will get a view of all of the figures and how they look, after analysing we cant tell k=13+1 is the closer one
# showAllDenoised()


#to show the original figure
show_main()
#to show the dinoised one using the svd method
show_my_matrix(process(13, get_function()), 'surface'+str(13))