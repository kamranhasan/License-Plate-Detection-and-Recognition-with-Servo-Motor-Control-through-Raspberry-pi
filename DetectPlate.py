from skimage.io import imread
from skimage.filters import threshold_otsu
import matplotlib.pyplot as plt
import cv2
from skimage import measure
from skimage.measure import regionprops
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import imutils

def detection(filename):
    car_image = imread(filename, as_gray=True)
    gray_car_image = car_image * 255
    threshold_value = threshold_otsu(gray_car_image)
    binary_car_image = gray_car_image > threshold_value

    label_image = measure.label(binary_car_image)

    plate_dimensions = (0.03*label_image.shape[0], 0.08*label_image.shape[0], 0.15*label_image.shape[1], 0.3*label_image.shape[1])
    plate_dimensions2 = (0.08*label_image.shape[0], 0.2*label_image.shape[0], 0.15*label_image.shape[1], 0.4*label_image.shape[1])
    min_height, max_height, min_width, max_width = plate_dimensions
    plate_objects_cordinates = []
    plate_like_objects = []
    flag = 0
    for region in regionprops(label_image):
        if region.area < 50:
            continue
        min_row, min_col, max_row, max_col = region.bbox

        region_height = max_row - min_row
        region_width = max_col - min_col

        if region_height >= min_height and region_height <= max_height and region_width >= min_width and region_width <= max_width and region_width > region_height:
            flag = 1
            plate_like_objects.append(binary_car_image[min_row:max_row,
                                      min_col:max_col])
            plate_objects_cordinates.append((min_row, min_col,
                                             max_row, max_col))
    if (flag==1):
        return False
    if(flag==0):
        min_height, max_height, min_width, max_width = plate_dimensions2
        plate_objects_cordinates = []
        plate_like_objects = []
        for region in regionprops(label_image):
            if region.area < 50:
                continue
            min_row, min_col, max_row, max_col = region.bbox
            region_height = max_row - min_row
            region_width = max_col - min_col

            if region_height >= min_height and region_height <= max_height and region_width >= min_width and region_width <= max_width and region_width > region_height:
                plate_like_objects.append(binary_car_image[min_row:max_row,
                                          min_col:max_col])
                plate_objects_cordinates.append((min_row, min_col,
                                                 max_row, max_col))
                dimensions = [min_row, max_row, min_col, max_col]
        image = cv2.imread(filename)
        plate = image[dimensions[0]:dimensions[1], dimensions[2]:dimensions[3]]
        cv2.imwrite("./plate.png", plate)
        return True
