from skimage import measure
from skimage.measure import regionprops
from skimage.io import imread
from skimage.filters import threshold_otsu
import matplotlib.pyplot as plt
import matplotlib.patches as patches

MIN_PLATE_HEIGHT = 0.05
MAX_PLATE_HEIGHT = 0.9
MIN_PLATE_WIDTH = 0.05
MAX_PLATE_WIDTH = 0.9

def create_label_image(image):
    car_image = imread(image, as_grey=True)
    gray_car_image = car_image * 255
    threshold_value = threshold_otsu(gray_car_image)
    binary_car_image = gray_car_image > threshold_value
    # this gets all the connected regions and groups them together
    label_image = measure.label(binary_car_image)
    return (gray_car_image, label_image, binary_car_image)

def get_valid_plate_dimensions(label_image):
    # getting the maximum width, height and minimum width and height that a license plate can be
    plate_dimensions = (MIN_PLATE_HEIGHT*label_image.shape[0], MAX_PLATE_HEIGHT*label_image.shape[0], MIN_PLATE_WIDTH*label_image.shape[1], MAX_PLATE_WIDTH*label_image.shape[1])
    return plate_dimensions

def find_and_mark_valid_regions_in_image(gray_car_image, label_image, binary_car_image, plate_dimensions):
    min_height, max_height, min_width, max_width = plate_dimensions
    plate_like_objects = []
    fig, (ax1) = plt.subplots(1)
    ax1.imshow(gray_car_image, cmap="gray");

    for region in regionprops(label_image):
        if region.area < 50:
            continue
        else:
            min_row, min_col, max_row, max_col = region.bbox
            region_height = max_row - min_row
            region_width = max_col - min_col
            # ensuring that the region identified satisfies the condition of a typical license plate
            if region_height >= min_height and region_height <= max_height and region_width >= min_width and region_width <= max_width and region_width > region_height:
                plate_like_objects.append( binary_car_image[ min_row:max_row, min_col:max_col ] )
                rectBorder = patches.Rectangle( ( min_col, min_row ), max_col-min_col, max_row-min_row, edgecolor="red", linewidth=1, fill=False )
                ax1.add_patch(rectBorder)

    return plate_like_objects


def read_image(image, show = False):
    gray_car_image, label_image, binary_car_image = create_label_image(image)
    plate_dimensions = get_valid_plate_dimensions(label_image)
    plate_like_objects = find_and_mark_valid_regions_in_image(gray_car_image, label_image, binary_car_image, plate_dimensions)
    if show:
        plt.show()
    return plate_like_objects