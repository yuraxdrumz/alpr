import numpy as np
from skimage.transform import resize
from skimage import measure
from skimage.measure import regionprops
import matplotlib.patches as patches
import matplotlib.pyplot as plt

MIN_CHAR_HEIGHT = 0.1
MAX_CHAR_HEIGHT = 0.8
MIN_CHAR_WIDTH = 0.01
MAX_CHAR_WIDTH = 0.2

def get_char_dimensions(license_plate):
    character_dimensions = (MIN_CHAR_HEIGHT*license_plate.shape[0], MAX_CHAR_HEIGHT*license_plate.shape[0], MIN_CHAR_WIDTH*license_plate.shape[1], MAX_CHAR_WIDTH*license_plate.shape[1])
    return character_dimensions


def find_valid_plates_in_marked_objects(plate_like_objects):
    plates = [ [] for y in range(len(plate_like_objects)) ]
    column_lists = [ [] for y in range(len(plate_like_objects)) ]

    for idx, plate in enumerate(plate_like_objects):
        license_plate = np.invert(plate)
        labelled_plate = measure.label(license_plate)
        character_dimensions = get_char_dimensions(license_plate)
        plate, column_list = find_characters_in_valid_regions(labelled_plate, license_plate, character_dimensions)
        plates[idx] = plate
        column_lists[idx] = column_list

    return (plates, column_lists)



def find_characters_in_valid_regions(labelled_plate, license_plate,  character_dimensions):
    plate = []
    column_list = []
    fig, ax1 = plt.subplots(1)
    ax1.imshow(license_plate, cmap="gray")
    min_height, max_height, min_width, max_width = character_dimensions
    for regions in regionprops(labelled_plate):
        y0, x0, y1, x1 = regions.bbox
        region_height = y1 - y0
        region_width = x1 - x0
        if region_height > min_height and region_height < max_height and region_width > min_width and region_width < max_width:
            # draw a red bordered rectangle over the character.
            rect_border = patches.Rectangle((x0, y0), x1 - x0, y1 - y0, edgecolor="red",linewidth=2, fill=False)
            ax1.add_patch(rect_border)
            roi = license_plate[y0:y1, x0:x1]
            # resize the characters to 20X20 and then append each character into the characters list
            resized_char = resize(roi, (20, 20))
            plate.append(resized_char)
            # this is just to keep track of the arrangement of the characters
            column_list.append(x0)

    return (plate, column_list)

def find_plates(plate_like_objects, show = False):
    plates, column_lists = find_valid_plates_in_marked_objects(plate_like_objects)
    if show:
        plt.show()
    return (plates, column_lists)