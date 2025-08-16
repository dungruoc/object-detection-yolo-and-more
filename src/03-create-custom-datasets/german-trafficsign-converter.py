import sys
import os
import pandas as pd
import cv2
import glob


trafficsigns_dataset_path = sys.argv[1]
output_path = sys.argv[2]

input_annotations = pd.read_csv(
    os.path.join(trafficsigns_dataset_path, 'gt.txt'),
    sep=';',
    header=None,
    index_col=None
)

input_annotations.columns = [
    'fileName',
    'x_left',
    'y_left',
    'x_right',
    'y_right',
    'classLabel'
]

input_annotations['x_center'] = input_annotations.apply(lambda row: (row['x_right'] + row['x_left'])/2.0, axis=1)
input_annotations['y_center'] = input_annotations.apply(lambda row: (row['y_right'] + row['y_left'])/2.0, axis=1)
input_annotations['b_width'] = input_annotations.apply(lambda row: (row['x_right'] - row['x_left']) * 1.0, axis=1)
input_annotations['b_height'] = input_annotations.apply(lambda row: (row['y_right'] - row['y_left'])* 1.0, axis=1)

print(input_annotations.head())


for ppm_path in glob.glob(f"{trafficsigns_dataset_path}/*.ppm"):
    ppm_image = cv2.imread(ppm_path)
    ppm_name = os.path.split(ppm_path)[1]
    image_annotation = input_annotations.loc[input_annotations['fileName'] == ppm_name].copy()
    h, w = ppm_image.shape[:2]
    print(ppm_name, h, w)
    image_annotation['x_center'] = image_annotation['x_center'] / w
    image_annotation['y_center'] = image_annotation['y_center'] / h
    image_annotation['b_width'] = image_annotation['b_width'] / w
    image_annotation['b_height'] = image_annotation['b_height'] / h
    image_annotation = image_annotation[[
        'classLabel',
        'x_center',
        'y_center',
        'b_width',
        'b_height'
    ]]
    # print(image_annotation)
    image_name = ppm_name[:-4]
    cv2.imwrite(os.path.join(output_path, image_name) + '.jpg', ppm_image)
    image_annotation.to_csv(os.path.join(output_path, image_name) + '.txt', header=False, index=None, sep=' ')
    # break

