import torch
from torchvision import models, transforms
from PIL import Image
import json
import os
import torch.nn as nn

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Points to backend/
PROJECT_ROOT = os.path.dirname(BASE_DIR) # Points to GreenTwin/

MODEL_PATH = os.path.join(PROJECT_ROOT, "ml_models/tomato/best_model.pth")
CLASSES_PATH = os.path.join(PROJECT_ROOT, "ml_models/tomato/classes.json")

class DiseaseInference:
    def __init__(self):
        self.device = torch.device("cpu")
        self.model = None
        self.classes = []
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        # Try loading
        self.load_model()

    def load_model(self):
        if not os.path.exists(MODEL_PATH) or not os.path.exists(CLASSES_PATH):
            print("Model or classes file not found. Inference will be mocked.")
            return

        try:
            # Load Classes
            with open(CLASSES_PATH, 'r') as f:
                self.classes = json.load(f)

            # Load Model Architecture (MobileNetV2)
            self.model = models.mobilenet_v2(pretrained=False)
            num_ftrs = self.model.classifier[1].in_features
            self.model.classifier[1] = nn.Linear(num_ftrs, len(self.classes))
            
            # Load Weights
            self.model.load_state_dict(torch.load(MODEL_PATH, map_location=self.device))
            self.model.eval()
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Failed to load model: {e}")
            self.model = None

    def predict(self, image_path: str):
        if not self.model:
            # Mock response if model unavailable
            return {"class": "Mock Healthy", "confidence": 0.99}
            
        try:
            image = Image.open(image_path).convert('RGB')
            image_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            with torch.no_grad():
                outputs = self.model(image_tensor)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)
                confidence, predicted = torch.max(probabilities, 1)
                
                predicted_class = self.classes[predicted.item()]
                conf_score = confidence.item()
                
                # Heuristic Override for False Positives
                # If the image is clearly green/healthy but model predicts severe disease, trust the color.
                final_class = self._apply_color_heuristic(image, predicted_class, conf_score)
                
                return {"class": final_class, "confidence": conf_score}
        except Exception as e:
            print(f"Prediction error: {e}")
            return {"class": "Error", "confidence": 0.0}

    def _apply_color_heuristic(self, image: Image.Image, predicted_class: str, confidence: float) -> str:
        """
        Check if pixel stats contradict the model prediction.
        E.g., If Image is >50% Green, it's unlikely to be 'Late_blight' (which turns leaves brown/black).
        """
        try:
            # 1. Resize for speed
            img_small = image.resize((50, 50))
            pixels = list(img_small.getdata())
            
            green_pixels = 0
            total_pixels = len(pixels)
            
            for p in pixels:
                r, g, b = p[0], p[1], p[2]
                # "Healthy Green" definition: Green is dominant channel
                if g > r and g > b and g > 50:
                    green_pixels += 1
            
            green_ratio = green_pixels / total_pixels
            
            # Debug
            print(f"Heuristic Check: Predicted {predicted_class}, Green Ratio: {green_ratio:.2f}")

            # 2. Logic: If prediction is a severe disease but image is excessively green -> Override
            if "healthy" not in predicted_class.lower():
                # If green ratio is very high (>40%), it's likely a false positive
                if green_ratio > 0.45: 
                    print(f"OVERRIDE: Detected {green_ratio:.2f} green. Switching to Healthy.")
                    return "Tomato___healthy"
            
            return predicted_class

        except Exception as e:
            print(f"Heuristic failed: {e}")
            return predicted_class

inference_service = DiseaseInference()
