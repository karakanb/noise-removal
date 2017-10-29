import cv2
import numpy as np
import time
import os

IMAGE_PATH = 'images/StairsBuildingsN.png'
OUTPUT_DIRECTORY = 'outputs/'

NORTH = [[-3, -3, -3],
         [-3, 0, -3],
         [5, 5, 5]]

WEST = [[-3, -3, 5],
        [-3, 0, 5],
        [-3, -3, 5]]

SOUTH = [[5, 5, 5],
         [-3, 0, -3],
         [-3, -3, -3]]

EAST = [[5, -3, -3],
        [5, 0, -3],
        [5, -3, -3]]

NORTHWEST = [[-3, -3, -3],
             [-3, 0, 5],
             [-3, 5, 5]]

SOUTHWEST = [[-3, 5, 5],
             [-3, 0, 5],
             [-3, -3, -3]]

SOUTHEAST = [[5, 5, -3],
             [5, 0, -3],
             [-3, -3, -3]]

NORTHEAST = [[-3, -3, -3],
             [5, 0, -3],
             [5, 5, -3]]

DIRECTIONS = [
    {
        "name": "NORTH",
        "direction": NORTH
    },
    {
        "name": "WEST",
        "direction": WEST
    },
    {
        "name": "SOUTH",
        "direction": SOUTH
    },
    {
        "name": "EAST",
        "direction": EAST
    },
    {
        "name": "NORTHWEST",
        "direction": NORTHWEST
    },
    {
        "name": "SOUTHWEST",
        "direction": SOUTHWEST
    },
    {
        "name": "SOUTHEAST",
        "direction": SOUTHEAST
    },
    {
        "name": "NORTHEAST",
        "direction": NORTHEAST
    },
]


def convolution(image, kernel, row, column):
    value = 0
    for i in range(2, -1, -1):
        for j in range(2, -1, -1):
            row_index = row - (i - 1)
            col_index = column - (j - 1)
            value += image[row_index][col_index] * kernel[i][j]

    if value < 0:
        value = 0
    elif value > 255:
        value = 255

    return int(value)


def main():
    # Read and print the original image.
    I = cv2.imread(IMAGE_PATH, 0)
    I = cv2.copyMakeBorder(I, 1, 1, 1, 1, cv2.BORDER_REFLECT)
    cv2.imshow('Stairs Buildings', I)

    height, width = I.shape[:2]

    for direction in DIRECTIONS:
        convolved_image = np.zeros([height, width])

        print("Starting convolution for %s" % direction["name"])
        for row in range(1, height - 1):
            for column in range(1, width - 1):
                convolved_image[row][column] = convolution(I, direction["direction"], row, column)

        print("Completed convolution for %s" % direction["name"])
        cv2.imshow('%s' % direction["name"], convolved_image)

    # Destroy all the images on any key press.
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
