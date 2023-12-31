from torch.utils.data import Dataset
from PIL import Image
import os
import numpy as np

class drivedataset(Dataset):
    def __init__(self, images_dir, masks_dir, transform):
        self.images_dir = images_dir
        self.masks_dir = masks_dir
        self.transform = transform
        self.images = os.listdir(images_dir)
        
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, index):
        img_path = os.path.join(self.images_dir, self.images[index])
        mask_path = os.path.join(self.masks_dir, self.images[index].replace("_training.tif", "_manual1.gif")).replace("_test.tif", "_manual1.gif")
        image = np.array(Image.open(img_path).convert("RGB"))
        # image = np.array(Image.open(img_path).convert("L"))
        mask = np.array(Image.open(mask_path).convert("L"), dtype = np.float32)
        mask[mask==255.0] = 1.0
        
        if self.transform is not None:
            augmentations = self.transform(image=image, mask=mask)
            image = augmentations["image"]
            mask = augmentations["mask"]
    
        return image, mask
        
