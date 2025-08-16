import sys
import os
import cv2
import numpy as np

label_names_path = sys.argv[1]
image_path = sys.argv[2]
annotation_path = image_path[:-4] + '.txt'


def read_annotations(label_names_path, ann_path):
    with open(label_names_path, 'r') as f:
        label_names = [line.strip() for line in f.readlines()]
    boxes = []
    with open(ann_path, 'r') as f:
        boxes = [line.strip().split(' ') for line in f.readlines()]
        boxes = [(label_names[int(c)], float(x), float(y), float(w), float(h)) for (c, x, y, w, h) in boxes]

    return boxes


def draw_boxes(input_img, boxes):

    colors = np.random.randint(0, 255, size=(len(boxes), 3), dtype='uint8')

    for i, (c, bx, by, bw, bh) in enumerate(boxes):
        print("object {0}: {1}".format(i, c), input_img.shape)
        h, w = input_img.shape[:2]
        bx, by, bw, bh = int(bx * w), int(by * h), int(bw * w), int(bh * h)
        bx, by = bx - bw // 2, by - bh // 2
        box_color = colors[i].tolist()
        print(box_color, bx, by, bw, bh)
        cv2.rectangle(input_img, (bx, by), (bx + bw, by + bh), box_color, 2)

        text_box = "{}".format(c)
        cv2.putText(input_img, text_box, (bx, by - 5),
                    cv2.FONT_HERSHEY_COMPLEX, 0.7, box_color, 2)
        
    mask_window_name = 'Image with Mask'
    cv2.namedWindow(mask_window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(mask_window_name, input_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return input_img


boxes = read_annotations(label_names_path, annotation_path)
print(boxes)
img = cv2.imread(image_path)
img = draw_boxes(img, boxes)
# image_name = os.path.split(image_path)[1]
# cv2.imwrite(f'./annotated-{image_name}', img)
