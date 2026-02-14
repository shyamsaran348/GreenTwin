import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, models, transforms
import os
import copy

# Configuration
DATA_DIR = 'ml_models/tomato/dataset'
MODEL_SAVE_PATH = 'model.pth'
NUM_EPOCHS = 10
BATCH_SIZE = 32
LEARNING_RATE = 0.001

def train_model():
    # Data Augmentation
    data_transforms = {
        'train': transforms.Compose([
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
        'val': transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
    }

    # Load Data
    image_datasets = {x: datasets.ImageFolder(os.path.join(DATA_DIR, x), data_transforms[x]) 
                      for x in ['train', 'val']}
    dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=BATCH_SIZE, shuffle=True, num_workers=4)
                   for x in ['train', 'val']}
    
    class_names = image_datasets['train'].classes
    
    # Select Device: MPS (Mac GPU) > CUDA (NVIDIA) > CPU
    if torch.backends.mps.is_available():
        device = torch.device("mps")
        print("Using Device: MPS (Mac GPU) 🚀")
    elif torch.cuda.is_available():
        device = torch.device("cuda:0")
        print("Using Device: CUDA (NVIDIA GPU) 🚀")
    else:
        device = torch.device("cpu")
        print("Using Device: CPU 🐢")

    # Load Pretrained MobileNetV2
    model = models.mobilenet_v2(pretrained=True)
    
    # Freeze weights
    for param in model.parameters():
        param.requires_grad = False
        
    # Replace last layer
    num_ftrs = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(num_ftrs, len(class_names))
    
    model = model.to(device)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
    
    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0

    # Training Loop
    for epoch in range(NUM_EPOCHS):
        print(f'Epoch {epoch+1}/{NUM_EPOCHS}')
        print('-' * 10)
        
        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()
            else:
                model.eval()
                
            running_loss = 0.0
            running_corrects = 0
            
            for inputs, labels in dataloaders[phase]:
                inputs = inputs.to(device)
                labels = labels.to(device)
                
                optimizer.zero_grad()
                
                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)
                    
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()
                        
                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)
            
            epoch_loss = running_loss / len(image_datasets[phase])
            epoch_acc = running_corrects.float() / len(image_datasets[phase])
            
            print(f'{phase} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}')
            
            # Deep copy the model
            if phase == 'val' and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_model_wts = copy.deepcopy(model.state_dict())
                torch.save(model.state_dict(), 'best_model.pth')
                print(f"New best model saved with Acc: {best_acc:.4f}")

    print(f'Best val Acc: {best_acc:4f}')
    
    # Load best model weights
    model.load_state_dict(best_model_wts)
    
    # Save Final Model
    torch.save(model.state_dict(), MODEL_SAVE_PATH)
    print(f"Final model saved to {MODEL_SAVE_PATH}")
    
    # Save Classes
    import json
    with open('classes.json', 'w') as f:
        json.dump(class_names, f)

if __name__ == '__main__':
    # This is a template. User needs to provide data path.
    # print("Please configure DATA_DIR before running.")
    train_model()
