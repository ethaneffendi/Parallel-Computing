import cmath
from PIL import Image
import math
import multiprocessing
import time

# checks whehter or not the input c is a member of the Mandelbrot set (returns what color c should be in a Mandelbrot set visualization)
def isInMandelbrotSet(c, maxIterations = 1000, maxModulus = 10 ** 6 + 1):
    # seed is zero
    x_0 = 0
    # iteration counter
    iterations = 0
    # tracks what the last iteration produced
    x_n = x_0
    # tracks the modulus of the last x_n
    modulus = abs(x_n)
    # iteration
    while iterations < maxIterations and modulus < maxModulus:
        iterations += 1
        # try to produce the next x_n, but if it is too big (OverflowError), break
        try:
            x_n = (x_n ** 2) + c
            modulus = abs(x_n)
        except OverflowError:
            break
    #test for divergence (c is a part of the Mandelbrot set, so it should graphically be colored black)
    if iterations >= maxIterations:
        return (0,0,0)
    #test for divergence (c is not a part of the Mandelbrot set, so it should graphically be colored white)
    elif abs(x_n) > maxModulus:
        return (255, 255, 255)

# receives a list of complex numbers and returns a list containing what color each complex number should be colored on a Mandelbrot set visualization
def computeMandelbrotSet_with_multiprocessing(inputList, maxIterations = 1000, maxModulus = 10 ** 6 + 1):
    pool = multiprocessing.Pool()
    outputList = pool.map(isInMandelbrotSet, inputList)
    pool.close()
    pool.join()
    return outputList

# produces an x by y image of the Mandelbrot set using the colors specified in inputList
def visualizeMandelbrotSet(inputList, x, y):
    # make a new image using PIL.Image
    im = Image.new(mode = 'RGB', size = (x, y))
    # plot the pixel colors specified in inputList onto im
    for i in range(x):
        for j in range(y):
            im.putpixel((i,j), inputList[j * x + i])
    # show im
    im.show()

# produces the list of complex numbers to be tested when real values are tested from -2 to 0.5 and imaginary values are tested from -1.5 to 1.5 (for x by y image)
def produceCList(x, y):
    outputList = []
    xIncrement = abs(-2 - 0.5) / x
    yIncrement = abs(-1.5 - 1.5) / y
    for j in range(y):
        for i in range(x):
            outputList.append(complex(-2 + i * xIncrement, 1.5 - j * yIncrement))
    return outputList

# putting it all together
if __name__ == '__main__':
    inputList = produceCList(250, 300)
    start_time = time.perf_counter()
    inputList = computeMandelbrotSet_with_multiprocessing(inputList)
    end_time = time.perf_counter()
    print(end_time-start_time)
    visualizeMandelbrotSet(inputList, 250, 300)
