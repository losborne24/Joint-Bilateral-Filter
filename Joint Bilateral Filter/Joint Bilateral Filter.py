import numpy as np
import cv2
import argparse

parser = argparse.ArgumentParser(description="Flash and no flash image pair(s) of interest")
parser.add_argument('images', nargs='+')
args = parser.parse_args()


def gaussian(x, sigma):     # gaussian function
    return np.exp(-(x ** 2) / (2 * sigma ** 2)) / (np.sqrt(2 * np.pi) * sigma)


def distance(x, y, i, j):   # calculate distance between neighbour pixel and centred pixel
    return np.sqrt((x - i)**2 + (y - j)**2)


def joint_bilateral_filter(no_flash_image, flash_image, d, sigma_r, sigma_s):
    height, width = no_flash_img.shape[:2]  # find dimensions of image
    new_image = np.zeros((height, width, 3), np.uint8)  # create a black output image
    for x in range(height):  # for each pixel in the image, apply bilateral filter and store pixel in new image.
        for y in range(width):

            filtered_image = 0
            wp = 0
            height, width = no_flash_image.shape[:2]
            for i in range(d):  # for each pixel in neighbourhood, calculate sigmaColour and sigmaSpace
                for j in range(d):
                    x_loc = int(x - ((d/2) - i))  # x location of neighbour pixel
                    y_loc = int(y - ((d/2) - j))  # y location of neighbour pixel
                    if x_loc < height:  # only perform gaussian function on pixels within image
                        if y_loc < width:
                            if x_loc >= 0:
                                if y_loc >= 0:
                                    gr = gaussian(flash_image[x_loc][y_loc] - flash_image[x][y], sigma_r)
                                    gs = gaussian(distance(x_loc, y_loc, x, y), sigma_s)
                                    w = gr * gs
                                    filtered_image += no_flash_image[x_loc][y_loc] * w
                                    wp += w
            filtered_image = filtered_image / wp    # normalise and round result
            new_image[x][y] = np.round(filtered_image)
    return new_image


if __name__ == '__main__':
    # for each no flash and flash image pair
    for no_flash_str, flash_str in zip(args.images[0::2], args.images[1::2]):
        # read images from file
        no_flash_img = cv2.imread('../images/' + no_flash_str, cv2.IMREAD_COLOR).astype(float)
        flash_img = cv2.imread('../images/' + flash_str, cv2.IMREAD_COLOR).astype(float)
        split_image_str = ""
        ext = ""
        if '.' in str(no_flash_str):
            split_image_str, ext = str(no_flash_str).rsplit('.', 1)
        else:
            print("File type not specified.")
            exit()
        if no_flash_img is not None:
            if flash_img is not None:
                max_range = (np.max(no_flash_img) - np.min(no_flash_img)) * 0.001  # 0.236 in this case
                output_image = joint_bilateral_filter(no_flash_img, flash_img, 5, max_range, 5)
                # write image to file
                cv2.imwrite('../images/' + split_image_str + "_output." + ext, output_image)
            else:
                print("No image file successfully loaded.")
        else:
            print("No image file successfully loaded.")
