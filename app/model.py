import torch
from torchvision import transforms
from PIL import Image


class ToolRecognitionModel:
    def __init__(self):
        self.model = torch.load('model.pth')  # Загрузка обученной модели
        self.model.eval()  # Перевод модели в режим оценки

        # Трансформации для обработки изображений
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def recognize(self, image_path):
        # Открытие и преобразование изображения
        image = Image.open(image_path)
        image = self.transform(image).unsqueeze(0)

        # Прогоняем изображение через модель
        with torch.no_grad():
            output = self.model(image)

        # Получаем предсказанный класс (инструмент)
        predicted_class = output.argmax(dim=1).item()

        # Рассчитываем уверенность (вероятность)
        probabilities = torch.nn.functional.softmax(output, dim=1)
        confidence = probabilities[0][predicted_class].item() * 100

        # Возвращаем предсказанный инструмент и уверенность
        return f"Tool {predicted_class}", confidence
