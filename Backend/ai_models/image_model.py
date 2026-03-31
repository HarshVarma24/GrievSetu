import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np

model = tf.keras.models.load_model(
    "/home/harsh/Desktop/UPES/SEM 6/Minor/Saved Models/CBAM_Model_olddatafinal.keras",
    compile=False
)

IMG_SIZE = 224  

class_labels = ["Electricity", "Road", "Sanitation", "Water"]

def predict_image(img_path):
    img = image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    preds = model.predict(img_array, verbose=0)

    pred_class = np.argmax(preds)
    confidence = preds[0][pred_class]

    predicted_label = class_labels[pred_class]

    return predicted_label, float(confidence)

