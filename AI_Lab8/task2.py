import torch
import torch.nn as nn
import torch.optim as optim
import time
import numpy
import random
import os
from torch.utils.data import Dataset, DataLoader
from PIL import Image
from torchvision import datasets, models, transforms


class ImageClassifierDataset(Dataset):
    def __init__(self, image_classes = ['face', 'not']):
        self.images = []
        self.labels = []
        self.classes = list(set(image_classes))
        self.class_to_label = {c: i for i, c in
        enumerate(self.classes)}
        self.image_size = 224
        self.transforms = transforms.Compose([
        transforms.Resize(self.image_size),
        transforms.CenterCrop(self.image_size),
        transforms.ToTensor(),
        transforms.Normalize((0.5,0.5,0.5), (0.5,0.5,0.5))
        ])


    def load_data(self):
        for subdirectory in os.listdir('images'):
            if not subdirectory.startswith('.') and (subdirectory.startswith("female_faces") or subdirectory.startswith("male_faces")):
                self.load_from_directory(f'images/{subdirectory}', 'face')
        for subdirectory in os.listdir('images'):
            if not subdirectory.startswith('.') and subdirectory.startswith('animals'):
                self.load_from_directory(f'images/{subdirectory}', 'not')


    def process_images(self, image_list, image_classes):
        for image, image_class in zip(image_list, image_classes):
            transformed_image = self.transforms(image)
            self.images.append(transformed_image)
            label = self.class_to_label[image_class]
            self.labels.append(label)

    def load_from_directory(self, directory_name, label):
        images = []
        directory_images = [file_name for file_name in os.listdir(directory_name) if not file_name.startswith('.')]
        numpy.random.shuffle(directory_images)

        for image in directory_images:
            images.append(Image.open(f"{directory_name}/{image}").convert('RGB'))

        self.process_images(images, [label for _ in images])

    def split(self):
        images_labels = list(zip(self.images, self.labels))
        numpy.random.shuffle(images_labels)
        indexes = list(range(len(images_labels)))
        train_indexes = []
        validation_indexes = []
        for index in indexes:
            if random.random() < 0.7:
                train_indexes.append(index)
            else:
                validation_indexes.append(index)

        train_set = ImageClassifierDataset()
        train_set.images = torch.tensor([])
        train_set.labels = torch.tensor([])
        train_set.images = [images_labels[i][0] for i in train_indexes]
        train_set.labels = [torch.tensor([images_labels[i][1]]) for i in train_indexes]

        train_set.images = torch.stack(train_set.images)
        train_set.labels = torch.stack(train_set.labels)

        test_set = ImageClassifierDataset()
        test_set.images = torch.tensor([])
        test_set.labels = torch.tensor([])
        test_set.images = [images_labels[i][0] for i in validation_indexes]
        test_set.labels = [torch.tensor([images_labels[i][1]]) for i in validation_indexes]

        test_set.images = torch.stack(test_set.images)
        test_set.labels = torch.stack(test_set.labels)

        return train_set, test_set

    def __getitem__(self, index):
        return self.images[index], self.labels[index]
    def __len__(self):
        return len(self.images)



dataset = ImageClassifierDataset()
dataset.load_data()
print(len(dataset.images))
dataset.split()