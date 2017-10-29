import cv2
import numpy as np
import time
import os

IMAGES_DIRECTORY = 'images/'
OUTPUT_DIRECTORY = 'outputs/'
IMAGE_NAMES = [
    'cameramanN1.jpg',
    'cameramanN2.jpg',
    'cameramanN3.jpg',
]

BALANCE_ALPHA = 0.8


def output_image(display_name, save_name, image):
    cv2.imshow(display_name, image)
    cv2.imwrite(OUTPUT_DIRECTORY + save_name, image)
    print("Image %s is saved." % OUTPUT_DIRECTORY + save_name)


def get_kernel():
    return np.ones((3, 3), np.float32) / 9


def get_mean_with_kernel(filter_area, kernel):
    # Fastest solution to multiply the matrices and get the result.
    return np.sum(np.multiply(kernel, filter_area))

    """
    This is also slower, since it requires this operation to be done for each of the channels.
    average = 0
    for i in range(3):
        average += np.sum(np.multiply(kernel, filter_area))
        
    return average
    """

    """
    Eliminated this loop based averaging, since it takes too much time.
    for krow in range(kernel_height):
        for kcol in range(kernel_width):
            row_index = row - (krow - middle_point)
            col_index = column - (kcol - middle_point)
            average_value += image[row_index][col_index][channel] * kernel[krow][kcol]

    return average_value
    """


def mean_filter(image, height, width):
    # Set the kernel.
    kernel = get_kernel()

    for row in range(1, height + 1):
        for column in range(1, width + 1):
            # Get the area to be filtered with range indexing.
            filter_area = image[row - 1:row + 2, column - 1:column + 2]
            res = get_mean_with_kernel(filter_area, kernel)
            image[row][column] = res

    return image


def get_median(filter_area):
    res = np.median(filter_area)
    return res


def median_filter(image, height, width):
    for row in range(1, height + 1):
        for column in range(1, width + 1):
            filter_area = image[row - 1:row + 2, column - 1:column + 2]
            image[row][column] = get_median(filter_area)

    return image


def mean_median_balanced_filter(image, height, width):
    for row in range(1, height + 1):
        for column in range(1, width + 1):
            filter_area = image[row - 1:row + 2, column - 1:column + 2]
            mean_filter_vector = get_mean_with_kernel(filter_area, get_kernel())
            median_filter_vector = get_median(filter_area)
            image[row][column] = BALANCE_ALPHA * mean_filter_vector + (1 - BALANCE_ALPHA) * median_filter_vector
    return image


def filter_image(image, image_name, filter_name, filtering_function):
    # Get the image size for the kernel looping.
    height, width = image.shape[:2]

    # Add 1px reflected padding to allow kernels to work properly.
    image = cv2.copyMakeBorder(image, 1, 1, 1, 1, cv2.BORDER_REFLECT)

    print("Calculating %s for %s" % (filter_name, image_name))
    start_time = time.time()
    res = filtering_function(image, height, width)
    print("Successfully calculated %s for %s in %s seconds." % (filter_name, image_name, str(time.time() - start_time)))

    return res


def main():
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)

    for image_name in IMAGE_NAMES:
        # Read and print the original image.
        image = cv2.imread(IMAGES_DIRECTORY + image_name, 0)
        cv2.imshow('Original Image: %s' % image_name, image)

        # Calculate the mean and print the resulting image.
        filtered_image = filter_image(image, image_name, 'mean filter', mean_filter)
        output_image('Mean filtered Image: %s' % image_name, '%s_mean.jpg' % image_name, filtered_image)

        filtered_image = filter_image(image, image_name, 'median filter', median_filter)
        output_image('Median filtered Image: %s' % image_name, '%s_median.jpg' % image_name, filtered_image)

        filtered_image = filter_image(image, image_name, 'balanced filter', mean_median_balanced_filter)
        output_image('Mean & Median with balance %s filtered Image: %s' % (BALANCE_ALPHA, image_name),
                     '%s_mean_median%s.jpg' % (image_name, str(BALANCE_ALPHA)), filtered_image)

    print("Completed all of the images.")

    # Destroy all the images on any key press.
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
