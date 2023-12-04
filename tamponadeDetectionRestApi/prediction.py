import cv2
import numpy as np
import os
from skimage import exposure
from skimage.util import img_as_ubyte
from keras.models import load_model


class TamponadeDetection:
    def __init__(self):
        self.model_path = '../tamponade_detection_model.keras'

    def load_trained_model(self):
        model = load_model(self.model_path)
        return model

    def predict(self, image_path):
        model = self.load_trained_model()
        processed_img = self.process_image(image_path)
        if model is None:
            return {"message": "Model not loaded"}, 0
        try:
            img_array = np.expand_dims(processed_img, axis=0)

            prediction = model.predict(img_array)

            predicted_class = np.argmax(prediction, axis=1)
            confidence = np.max(prediction, axis=1)

            labels = ['Normal', 'Cardiac Tamponade']
            predicted_label = labels[predicted_class[0]]

            confidence_value = confidence[0].item()
            return {"predicted_label": predicted_label, "confidence": confidence_value}

        except Exception as e:
            print(f"Error during prediction: {e}")
            return "Prediction error", 0

    def normalize_image(self, image):
        return (image - np.min(image)) / (np.max(image) - np.min(image))

    def crop_echography(self, image):
        crop_size = int(min(image.shape[:2]) * 0.8)
        start_y = (image.shape[0] - crop_size) // 2
        start_x = (image.shape[1] - crop_size) // 2
        return image[start_y:start_y + crop_size, start_x:start_x + crop_size]

    def process_image(self, image_path):
        try:
            img = cv2.imread(str(image_path))
            if img is None:
                raise Exception("Image not found or invalid image format")
            if len(img.shape) > 2 and img.shape[2] == 3:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cropped_img = self.crop_echography(img)
            normalized_img = self.normalize_image(cropped_img)
            gamma_corrected_img = exposure.adjust_gamma(normalized_img, 1.3)

            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            clahe_img = clahe.apply(np.uint8(255 * gamma_corrected_img))

            log_corrected_img = exposure.adjust_log(clahe_img, 1.2)

            normalized_log_img = self.normalize_image(log_corrected_img)

            log_corrected_img_8bit = img_as_ubyte(normalized_log_img)

            denoised_img = cv2.fastNlMeansDenoising(log_corrected_img_8bit, None, 15, 7, 21)

            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            sharpened_img = cv2.filter2D(denoised_img, -1, kernel)

            input_shape = (256, 256)
            resized_img = cv2.resize(sharpened_img, input_shape, interpolation=cv2.INTER_LINEAR)

            return resized_img

        except Exception as e:
            print(f"Error loading or processing image: {e}")
            raise
