import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def get_map(image):
    image_read = cv2.imread(image)
    ret, binary_map = cv2.threshold(image_read, 250, 255, cv2.THRESH_BINARY)
    

    pillowed_image = Image.open(os.path.join(image))


    width, height = pillowed_image.size
    x, y = np.meshgrid(range(width), range(height))
    coordinate_map = np.concatenate([pillowed_image.getdata(), x.reshape(-1, 1), y.reshape(-1, 1)], axis=1)

    
    working_coordinate_map = np.concatenate([pillowed_image.getdata(0)])
    working_coordinate_map = np.reshape(working_coordinate_map, (454, 1167))

    white_pixel_coordinates = []


    for pixel in coordinate_map:
        if pixel[0] > 250:
            pixel[0] = 255
            white_pixel_coordinates.append(tuple(pixel[3:5]))
        else:
            pixel[0] = 0
    

    for row in working_coordinate_map:
        for pixel in range(0, len(row)):
            if row[pixel] > 250:
                row[pixel] = 1
            else:
                row[pixel] = 0   

    
    # for val in white_pixel_coordinates:
    #     for val2 in val:
    #         val2 = int(val2)
    #     print(type(val[0]), type(val[1])) 
    

    #white_pixel_coordinates = np.array(white_pixel_coordinates, dtype=tuple)
    #print(white_pixel_coordinates)
    
    return white_pixel_coordinates, working_coordinate_map, image
