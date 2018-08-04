from read_image import read_image
from find_plates import find_plates
from find_plate_number import iterate_found_plates

def main():
    plate_like_objects = read_image('./testers/car3.jpg', show=True)
    plates, column_lists = find_plates(plate_like_objects, show=True)
    found = iterate_found_plates(plates, column_lists)
    print(found)


if __name__ == '__main__':
    main()