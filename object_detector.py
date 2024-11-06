import torch
from transformers import ViTFeatureExtractor, ViTForImageClassification
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
from PIL import Image
from googletrans import Translator  # Импорт переводчика
import requests

class ObjectDetector:
    def __init__(self, model_name="google/vit-base-patch16-224"):
        # Инициализация модели и загрузка feature extractor
        self.model = ViTForImageClassification.from_pretrained(model_name)
        self.feature_extractor = ViTFeatureExtractor.from_pretrained(model_name)
        self.translator = Translator()  # Инициализация переводчика

    def detect_object(self, image: Image.Image):
        # Предобработка изображения
        inputs = self.feature_extractor(images=image, return_tensors="pt")
        # Предсказание
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            # Определяем метку с наивысшей вероятностью
            predicted_class_idx = logits.argmax(-1).item()
            predicted_label = self.model.config.id2label[predicted_class_idx]
            confidence = torch.softmax(logits, dim=-1)[0, predicted_class_idx].item()
            
            # Перевод метки на русский
            translated_label = self.translator.translate(predicted_label, src='en', dest='ru').text
        
        return translated_label, confidence

    def capture_screenshot(self):
        # Функция для захвата скриншота
        from PIL import ImageGrab
        screenshot = ImageGrab.grab()
        return screenshot
