import os
import shutil
import subprocess
import random
from pathlib import Path

# Configuration
REPO_URL = "https://github.com/spMohanty/PlantVillage-Dataset.git"
TEMP_DIR = "temp_dataset_repo"
TARGET_DIR = "ml_models/tomato/dataset"
CLASSES_OF_INTEREST = ["Tomato"]

def setup_data():
    print("Starting dataset setup...")
    
    # 1. Clone Repository (Sparse checkout if possible, but full clone is safer for structure)
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    
    print(f"Cloning {REPO_URL}...")
    subprocess.run(["git", "clone", "--depth", "1", REPO_URL, TEMP_DIR], check=True)
    
    # 2. Locate Source Images
    source_root = Path(TEMP_DIR) / "raw" / "color"
    if not source_root.exists():
        print("Error: Could not find raw/color directory in repo.")
        return

    # 3. Create Target Structure
    train_dir = Path(TARGET_DIR) / "train"
    val_dir = Path(TARGET_DIR) / "val"
    
    if os.path.exists(TARGET_DIR):
        shutil.rmtree(TARGET_DIR)
    
    os.makedirs(train_dir)
    os.makedirs(val_dir)
    
    # 4. Filter and Move Files
    print("Processing images...")
    found_classes = []
    
    for category_path in source_root.iterdir():
        if not category_path.is_dir():
            continue
            
        folder_name = category_path.name
        
        # Check if folder matches our interest (e.g., starts with "Tomato")
        if any(interest in folder_name for interest in CLASSES_OF_INTEREST):
            print(f"  Found class: {folder_name}")
            found_classes.append(folder_name)
            
            # Create class folders in train/val
            (train_dir / folder_name).mkdir()
            (val_dir / folder_name).mkdir()
            
            # Get all images
            images = list(category_path.glob("*"))
            random.shuffle(images)
            
            # Split 80/20
            split_idx = int(len(images) * 0.8)
            train_imgs = images[:split_idx]
            val_imgs = images[split_idx:]
            
            # Copy images
            for img in train_imgs:
                shutil.copy(img, train_dir / folder_name / img.name)
                
            for img in val_imgs:
                shutil.copy(img, val_dir / folder_name / img.name)
                
    print(f"Processed {len(found_classes)} classes.")
    
    # 5. Cleanup
    print("Cleaning up temporary files...")
    shutil.rmtree(TEMP_DIR)
    
    print(f"Dataset setup complete. Data located at {TARGET_DIR}")

if __name__ == "__main__":
    setup_data()
