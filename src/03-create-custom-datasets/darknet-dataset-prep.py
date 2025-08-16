import sys
import os
import glob
import random

label_names_path = sys.argv[1]
image_set_path = sys.argv[2]
output_path = sys.argv[3]

label_names_path = os.path.abspath(label_names_path)

labels = [l.strip() for l in open(label_names_path, 'r').readlines()]

image_set_path = os.path.abspath(image_set_path)

all_input_images = []
for image_file in glob.glob(f"{image_set_path}/*.jpg"):
    if os.path.exists(image_file[:-4] + '.txt'):
        all_input_images.append(image_file)

random.shuffle(all_input_images)

split = int(0.7 * len(all_input_images))

train = all_input_images[:split]
test = all_input_images[split:]

train_txt_file = os.path.abspath(os.path.join(output_path, 'train.txt'))
test_txt_file = os.path.abspath(os.path.join(output_path, 'test.txt'))
class_name_file = os.path.abspath(os.path.join(output_path, 'classes.names'))
dataset_data_file = os.path.abspath(os.path.join(output_path, 'ts_data.data'))

with open(train_txt_file, 'w') as f:
    f.write('\n'.join(train))

with open(test_txt_file, 'w') as f:
    f.write('\n'.join(test))

with open(class_name_file, 'w') as f:
    f.write('\n'.join(labels))

data = [
    f"classes = {len(labels)}",
    f"train = {train_txt_file}",
    f"valid = {test_txt_file}",
    f"names = {class_name_file}",
    "backup = backup"
]

with open(dataset_data_file, 'w') as f:
    f.write("\n".join(data))
