import os
import numpy as np
import cv2
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import db  # Import your Pinecone initialization module

# Define paths
images_folder = './images'
categories = ['Tops', 'Dresses']

# Preprocess images


def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))  # Resize to 224x224
    img = img_to_array(img)
    img = img / 255.0  # Normalize
    return img


# Create a list of image paths and labels
image_paths = []
labels = []

for category in categories:
    category_path = os.path.join(images_folder, category)
    for img_file in os.listdir(category_path):
        if img_file.endswith(('jpg', 'jpeg', 'png')):
            image_paths.append(os.path.join(category_path, img_file))
            labels.append(category)  # Use folder name as label

# Encode labels
label_encoder = LabelEncoder()
labels = label_encoder.fit_transform(labels)
labels = to_categorical(labels)

# Split dataset
train_paths, val_paths, train_labels, val_labels = train_test_split(
    image_paths, labels, test_size=0.2, random_state=42)

# Build the CNN model
model = Sequential([
    Input(shape=(224, 224, 3)),
    Conv2D(32, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(name='flatten'),
    Dense(512, activation='relu'),
    Dropout(0.5),
    Dense(len(label_encoder.classes_), activation='softmax')  # Number of classes
])

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy',
              metrics=['accuracy'])

# Data generator


def data_generator(image_paths, labels, batch_size=32):
    while True:
        for start in range(0, len(image_paths), batch_size):
            end = min(start + batch_size, len(image_paths))
            batch_paths = image_paths[start:end]
            batch_labels = labels[start:end]

            images = []
            for img_path in batch_paths:
                img = preprocess_image(img_path)
                images.append(img)
            yield np.array(images), np.array(batch_labels)


# Train the model
batch_size = 32
train_generator = data_generator(train_paths, train_labels, batch_size)
val_generator = data_generator(val_paths, val_labels, batch_size)

model.fit(train_generator, steps_per_epoch=len(train_paths)//batch_size, epochs=10,
          validation_data=val_generator, validation_steps=len(val_paths)//batch_size)

model.save('./my_model.h5')
