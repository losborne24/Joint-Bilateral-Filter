import cv2
import argparse

parser = argparse.ArgumentParser(description="Image(s) of interest")
parser.add_argument('images', nargs='+')
args = parser.parse_args()


for image_str in args.images:
    # read images from file
    img = cv2.imread('../images/' + image_str, cv2.IMREAD_COLOR)
    split_image_str = ""
    ext = ""
    if '.' in image_str:
        split_image_str, ext = image_str.rsplit('.', 1)
    else:
        print("File type not specified.")
        exit()
    # check images have loaded
    if img is not None:
        # apply filter
        bilateral_filter1 = cv2.bilateralFilter(img, 7, 30, 30)
        bilateral_filter2 = cv2.bilateralFilter(img, 9, 60, 60)
        # write images to file
        cv2.imwrite('../images/' + split_image_str + '_output1.' + ext, bilateral_filter1)
        cv2.imwrite('../images/' + split_image_str + '_output2.' + ext, bilateral_filter1)

    else:
        print("No image file successfully loaded.")
