import sys
import os
import pandas as pd
import glob

csv_path = os.path.abspath(sys.argv[1])
image_path = os.path.abspath(sys.argv[2])

labels = ['Car', 'Bicycle wheel', 'Bus']

all_classes = pd.read_csv(os.path.join(csv_path, 'class-descriptions-boxable.csv'),
                      usecols=[0, 1], header=None)

label_ids = []

for label in labels:
    class_id = all_classes.loc[all_classes[1] == label].values[0][0]
    label_ids.append(class_id)

print(label_ids)

annotations = pd.read_csv(os.path.join(csv_path, 'train-annotations-bbox.csv'),
                      usecols=[
                          'ImageID',
                          'LabelName',
                          'XMin',
                          'XMax',
                          'YMin',
                          'YMax'
                      ])
filtered_annotations = annotations.loc[annotations['LabelName'].isin(label_ids)].copy()

label_map = {l: i for i, l in enumerate(label_ids)}

filtered_annotations['classNumber'] = filtered_annotations['LabelName'].apply(lambda l: label_map[l])
filtered_annotations['center_x'] = (filtered_annotations['XMax'] + filtered_annotations['XMin']) / 2.0
filtered_annotations['center_y'] = (filtered_annotations['YMax'] + filtered_annotations['YMin']) / 2.0
filtered_annotations['box_width'] = (filtered_annotations['XMax'] - filtered_annotations['XMin'])
filtered_annotations['box_height'] = (filtered_annotations['YMax'] - filtered_annotations['YMin'])
filtered_annotations = filtered_annotations[[
    'ImageID',
    'classNumber',
    'center_x',
    'center_y',
    'box_width',
    'box_height'
]]

print(filtered_annotations.head())

image_files = glob.glob(f"{image_path}/*.jpg", recursive=True)
for image_file in image_files:
    image_id = os.path.split(image_file)[1][:-4]
    annotation = filtered_annotations.loc[filtered_annotations['ImageID'] == image_id]
    annotation_file = image_file[:-4] + '.txt'
    annotation.loc[:, [
        'classNumber',
        'center_x',
        'center_y',
        'box_width',
        'box_height'
    ]].to_csv(annotation_file, header=False, index=None, sep=' ')