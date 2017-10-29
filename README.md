# Noise Removal & Edge Detection
This repo contains the sample code for a naive implementation of noise removal filters. The task is to remove noise on the input cameraman images in `images/` directory. There are 3 different cameraman images:
* `cameramanN1.jpg`: Image with Gaussian noise applied.
* `cameramanN2.jpg`: Image with salt-and-pepper noise applied.
* `cameramanN3.jpg`: Image with Gaussian and salt-and-pepper noise combined.

The main aim of this project is to understand basic spatial filtering methods, which is why the project implements naive versions of mean and median filters.

## Noise Removal
The project implements three different noise rmeoval tehcniques, mean filter, median filter, and a combination of both. In order to run the code, you can simply ran `python noise_reduction.py`.

### Mean Filter
In mean filter, the idea is to update the brightness of a pixel by using its neighbor pixels' values. In order to implement this, a simple N×M unit matrix is constructed, and it is convoluted over the image, and the pixel that coresponds to the center of the kernel is updated with the mean of its neighbor' brightness values. A sample kernel can be thought as follows:

![Sample 3-by-3 kernel image](docs/kernel.png)

The kernel above is walked over the whole image, and the corresponding values are multiplied and summed, which is used to determine the value of the orange cell. This way, the resulting values are eliminating the pixels that do not fit to their surroundings, thus reducing the noise.