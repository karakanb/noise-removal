import cv2
import numpy as np
import time

IMAGES_DIRECTORY = 'images/'


def read_image(image_name):
    image = cv2.imread(image_name)

    return image


def get_mean_with_kernel(image_channel, row, column, kernel, middle_point):
    filter_area = image_channel[row - middle_point:row + middle_point + 1,
                  column - middle_point:column + middle_point + 1]

    # Fastest solution to multiply the matrices and get the result.
    return np.einsum('ijk,ik->i', filter_area, kernel)

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


def mean_filter(image):
    # Get the image size for the kernel looping.
    height, width = image.shape[:2]
    height -= 2
    width -= 2

    # Set the kernel.
    kernel = np.ones((3, 3), np.float32) / 9
    kernel_height, kernel_width = kernel.shape[:2]
    middle_point = int(kernel_height / 2)

    for row in range(height):
        for column in range(width):
            res = get_mean_with_kernel(image, row + 1, column + 1, kernel, middle_point)
            image[row + 1][column + 1] = res

    return image


def filter_image(image, filtering_function):
    # Add 1px reflected padding to allow kernels to work properly.
    image = cv2.copyMakeBorder(image, 1, 1, 1, 1, cv2.BORDER_REFLECT)

    return filtering_function(image)


def main():
    images = [
        'cameramanN1.jpg',
        'cameramanN2.jpg',
        'cameramanN3.jpg',
    ]

    for image_name in images:
        # Read and print the original image.
        image = cv2.imread(IMAGES_DIRECTORY + image_name)
        cv2.imshow('Original Image: %s' % image_name, image)

        # Calculate the mean and print the resulting image.
        print("Calculating mean filter for %s" % image_name)
        start_time = time.time()
        image = filter_image(image, mean_filter)
        print("Successfully calculated mean filter for %s in %s seconds" % (image_name, str(time.time() - start_time)))
        cv2.imshow('Mean filtered Image: %s' % image_name, image)

    print("Completed all of the images.")
    # Destroy all the images on any key press.
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
