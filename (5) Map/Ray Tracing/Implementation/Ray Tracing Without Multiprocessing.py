import numpy as np
import math
from PIL import Image
import time

# sphere class
class Sphere:
    def __init__(self, center, radius, color):
        self.center = center
        self.radius = radius
        self.color = color

# return the point on the viewport that corresponds to the pixel (imageX, imageY) in the image to be produced
def canvasToViewport(imageX, imageY, viewportWidth, viewportHeight, imageWidth, imageHeight):
    return np.array([(imageX) * (viewportWidth / imageWidth), (imageY) * (viewportHeight / imageHeight), 1])

# return the direction of a ray that passes through O and V
def direction(O, V):
    return V-O

# returns when a given ray intersects with a given sphere
def intersectionOfRayAndSphere(O, V, sphere):

    r = sphere.radius
    CO = O - sphere.center
    D = direction(O, V)

    a = np.dot(D, D)
    b = 2 * np.dot(CO, D)
    c = np.dot(CO, CO) - (r**2)

    discriminant = b * b - 4 * a * c

    if discriminant < 0:
        return "none"
    else:
        if (-b + math.sqrt(discriminant)) / (2 * a) == (-b - math.sqrt(discriminant)) / (2 * a):
            return
        else:
            if (-b + math.sqrt(discriminant)) / (2 * a) < (-b - math.sqrt(discriminant)) / (2 * a):
                return (-b + math.sqrt(discriminant)) / (2 * a)
            else:
                return (-b - math.sqrt(discriminant)) / (2 * a)

# trace a ray through V (What color should V be?)
def traceRay(O, V, spheres, d):
    closest_t = None
    closest_sphere = None

    # safely initialize closest_t and closest_sphere
    for i in range(len(spheres)):
        if intersectionOfRayAndSphere(np.array([0,0,0]), V, spheres[i]) != "none":
            closest_t = intersectionOfRayAndSphere(np.array([0,0,0]), V, spheres[i])
            closest_sphere = spheres[i]

    #find the closest closest_t and closest_sphere
    for i in range(len(spheres)-1):
        if intersectionOfRayAndSphere(np.array([0,0,0]), V, spheres[i+1]) != "none" and intersectionOfRayAndSphere(np.array([0,0,0]), V, spheres[i+1]) < closest_t:
            closest_t = intersectionOfRayAndSphere(np.array([0,0,0]), V, spheres[i+1])
            closest_sphere = spheres[i+1]

    if closest_sphere != None:
        return closest_sphere.color
    else:
        return (255, 255, 255)

# ray tracing without multiprocessing (image must be of even height and width)
def rayTracing_without_multiprocessing(viewportWidth, viewportHeight, imageWidth, imageHeight, spheres):
    outputList = []
    O = np.array([0,0,0])
    for y in range(imageHeight // 2, -imageHeight // 2, -1):
        for x in range(-imageWidth // 2, imageWidth // 2):
            viewportPoint = canvasToViewport(x, y, viewportWidth, viewportHeight, imageWidth, imageHeight)
            color = traceRay(O, viewportPoint, spheres, 1)
            outputList.append(color)
    return outputList

def visualizeRayTracedImage(imageWidth, imageHeight, inputList):
    im = Image.new(mode = 'RGB', size = (imageWidth, imageHeight))
    # plot the pixel colors specified in inputList onto im
    for y in range(imageHeight):
        for x in range(imageWidth):
            im.putpixel((x,y), inputList[y * imageWidth + x])
    # show im
    im.show()

# putting it all together
spheres = [Sphere(np.array([0, -1, 3]), 1, (255,0,0)), Sphere(np.array([2, 0, 4]), 1, (0, 0, 255)), Sphere(np.array([-2, 0, 4]), 1, (0, 255, 0))]
start_time = time.perf_counter()
imagePixelsList = rayTracing_without_multiprocessing(2, 2, 1000, 1000, spheres)
end_time  = time.perf_counter()
print(end_time - start_time)
visualizeRayTracedImage(1000, 1000, imagePixelsList)
