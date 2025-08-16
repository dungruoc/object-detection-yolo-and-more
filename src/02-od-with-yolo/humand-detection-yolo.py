import cv2
import numpy as np
import sys
import time


bgr_img = cv2.imread(sys.argv[1])

original_window = 'Original Image'
cv2.namedWindow(original_window, cv2.WINDOW_NORMAL)
cv2.imshow(original_window, bgr_img)

h, w = bgr_img.shape[:2]
print(h, w)

blob = cv2.dnn.blobFromImage(bgr_img, 1/255.0, (416, 416), swapRB=True, crop=False)
print("blob shape: ", blob.shape)

# blob_img = blob[0, :, :, :].transpose(1, 2, 0)

# blob_window = "Blob Image"
# cv2.namedWindow(blob_window, cv2.WINDOW_NORMAL)
# cv2.imshow(blob_window, cv2.cvtColor(blob_img, cv2.COLOR_RGB2BGR))

with open(sys.argv[2]) as f:
    labels = [line.strip() for line in f]

print(labels)


dnn_model = cv2.dnn.readNetFromDarknet(sys.argv[3], sys.argv[4])
print(dnn_model.getLayerNames())
print(dnn_model.getUnconnectedOutLayers())

output_layer_names = dnn_model.getUnconnectedOutLayersNames()
print('Output Layers:', output_layer_names)

min_probability = 0.5
nonmax_threshold = 0.3


dnn_model.setInput(blob)
start_time = time.time()
output = dnn_model.forward(output_layer_names)
end_time = time.time()

print(f"Yolo took {(end_time - start_time):5f} seconds")

bounding_boxes = []
confidences = []
class_numbers = []

for result in output:
    for detected_objects in result:
        scores = detected_objects[5:]
        class_current = np.argmax(scores)
        confidence_current = scores[class_current]

        if confidence_current > min_probability:
            current_box = detected_objects[0:4] * np.array([w, h, w, h])
            x_center, y_center, b_width, b_height = current_box
            x_min = int(x_center - b_width / 2)
            y_min = int(y_center - b_height / 2)

            bounding_boxes.append([x_min, y_min, int(b_width), int(b_height)])
            confidences.append(confidence_current)
            class_numbers.append(class_current)

print(class_numbers)

nms_results = cv2.dnn.NMSBoxes(bounding_boxes, confidences, min_probability, nonmax_threshold)

count = 1

colors = np.random.randint(0, 255, size=(len(labels), 3), dtype='uint8')

for i in nms_results.flatten():
    class_label = labels[int(class_numbers[i])]
    print("object {0}: {1}".format(count, class_label))
    count += 1

    x_min, y_min, b_w, b_h = bounding_boxes[i]
    box_color = colors[class_numbers[i]].tolist()
    cv2.rectangle(bgr_img, (x_min, y_min), (x_min + b_w, y_min + b_h), box_color, 2)

    text_box = "{}: {:4f}".format(class_label, confidences[i])
    cv2.putText(bgr_img, text_box, (x_min, y_min - 5),
                cv2.FONT_HERSHEY_COMPLEX, 0.7, box_color, 2)

predicted_window = 'Predicted Boxes'
cv2.namedWindow(predicted_window, cv2.WINDOW_NORMAL)
cv2.imshow(predicted_window, bgr_img)


cv2.waitKey(0)
cv2.destroyAllWindows()
