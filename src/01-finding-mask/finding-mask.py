import cv2


thresholds = {
    'min_blue':  0,
    'min_green':  0,
    'min_red':  0,
    'max_blue':  0,
    'max_green':  0,
    'max_red':  0
}

def min_blue_changed(x):
    global thresholds
    thresholds['min_blue'] = x
    thresholds_changed(thresholds)

def min_green_changed(x):
    global thresholds
    thresholds['min_green'] = x
    thresholds_changed(thresholds)

def min_red_changed(x):
    global thresholds
    thresholds['min_red'] = x
    thresholds_changed(thresholds)

def max_blue_changed(x):
    global thresholds
    thresholds['max_blue'] = x
    thresholds_changed(thresholds)

def max_green_changed(x):
    global thresholds
    thresholds['max_green'] = x
    thresholds_changed(thresholds)

def max_red_changed(x):
    global thresholds
    thresholds['max_red'] = x
    thresholds_changed(thresholds)



trackbar_window_name = 'track bars'

cv2.namedWindow(trackbar_window_name, cv2.WINDOW_NORMAL)

cv2.createTrackbar('min_blue', trackbar_window_name, 0, 255, min_blue_changed)
cv2.createTrackbar('min_green', trackbar_window_name, 0, 255, min_green_changed)
cv2.createTrackbar('min_red', trackbar_window_name, 0, 255, min_red_changed)

cv2.createTrackbar('max_blue', trackbar_window_name, 0, 255, max_blue_changed)
cv2.createTrackbar('max_green', trackbar_window_name, 0, 255, max_green_changed)
cv2.createTrackbar('max_red', trackbar_window_name, 0, 255, max_red_changed)


bgr_img = cv2.imread('objects-to-detect.jpg')
bgr_img = cv2.resize(bgr_img, (600, 426))

o_image_window_name = 'original image'
cv2.namedWindow(o_image_window_name, cv2.WINDOW_NORMAL)
cv2.imshow(o_image_window_name, bgr_img)

hsv_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)

hsv_image_window_name = 'HSV image'
cv2.namedWindow(hsv_image_window_name, cv2.WINDOW_NORMAL)
cv2.imshow(hsv_image_window_name, hsv_img)


mask_window_name = 'Image with Mask'
cv2.namedWindow(mask_window_name, cv2.WINDOW_NORMAL)

def thresholds_changed(thresholds):
    print(thresholds)
    mask = cv2.inRange(hsv_img,
                       (thresholds['min_blue'], thresholds['min_green'], thresholds['min_red']),
                       (thresholds['max_blue'], thresholds['max_green'], thresholds['max_red']))
    
    cv2.imshow(mask_window_name, mask)

while True:
    if cv2.waitKey(0):
        break