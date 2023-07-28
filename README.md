# ActionLearningAIS4

Repository for ActionLearning Group 4


# Speech Detection

This code uses a simple deep learning model (Sequential model) to identify whether a provided audio file is from a human or another source. It extracts the MFCC (Mel Frequency Cepstral Coefficient) features from the audio data and uses them as input to the model.
This script is a sound classification pipeline that trains a neural network to classify audio files as either "human" or "other". The pipeline includes preprocessing steps such as silence removal and audio augmentation, as well as feature extraction, training the model, evaluating it, and saving the model for future use.

1. **Model Used:** 
The model used is a simple feed-forward neural network (also known as a multi-layer perceptron) implemented with Keras. The model has three layers: 
    - The first layer has 100 neurons and uses the ReLU activation function.
    - The second layer has 50 neurons and also uses the ReLU activation function.
    - The final layer is a single neuron with a sigmoid activation function, which will output the probability that the input audio is classified as "human".
    
2. **Feature Extraction:**
The script extracts four different types of features from each audio file:
    - MFCC (Mel Frequency Cepstral Coefficients): This is a type of spectral feature that is widely used in speech and audio processing.
    - Chroma-STFT: This represents the short-term power spectrum of sound.
    - Spectral Contrast: This measures the difference in amplitude between peaks and valleys in a sound spectrum.
    - Tonnetz: This is used to represent harmonic relations between different pitches.
These features are then concatenated into a single feature vector for each audio file.

3. **Data Augmentation:** 
The script uses the Audiomentations library to augment the audio data, adding variety to the training data and helping the model generalize better. The augmentations include adding Gaussian noise, time stretching, pitch shifting, and shifting the audio.

4. **Data Preparation:**
The script reads audio files from a specified path, removes silence from the audio, optionally applies data augmentation, extracts features from the audio, and then splits the resulting feature vectors and labels into training and validation sets. The labels are also encoded as integers using sklearn's LabelEncoder.

5. **Training:**
The model is trained using the Adam optimizer and binary cross entropy loss (since this is a two-class classification problem). Early stopping is used to prevent overfitting, stopping the training if the validation loss doesn't decrease for 10 consecutive epochs.

6. **Evaluation:**
After training, the model is evaluated on the validation set, producing a confusion matrix and classification report (which includes precision, recall, and f1-score for each class, as well as overall accuracy).

7. **Prediction:**
The script includes a function to use the trained model to classify a single audio file.

8. **Saving the Model and Label Encoder:**
The trained model and the label encoder (used to convert between class labels and integers) are saved to disk using Keras' model saving functionality and joblib, respectively.

In terms of how the code works, the logic flows from data loading, augmentation and feature extraction, through to data splitting, model creation, training, evaluation, and finally saving.


The model uses the trained weights to make predictions based on the features extracted from new, unseen audio data. For instance, if you have a new audio file and you want to classify it as "human" or "other"
## Requirements
- Python 3.6 or above
- Keras 2.4.3 or above
- Librosa 0.8.0 or above

## How To Run
1. Clone the repository to your local machine.
2. Navigate to the directory containing the code.
3. Install the necessary libraries mentioned in requirements.
4. Prepare your dataset. The dataset should be arranged in two folders: `train` and `test`. The `train` folder should contain two subfolders: `human` and `other` for human voice and other sounds respectively. The `test` folder should contain the audio files to be tested.
5. You can customize `DATA_PATH_TRAIN`, `DATA_PATH_TEST`, `SAMPLE_RATE`, and `MFCC_COUNT` based on your dataset and requirements.
6. Run the script. The script will train the model on the training data, evaluate it on the test data and print out a confusion matrix and a classification report. It will also save the trained model in a folder named `my_model`.

## Dataset
The dataset used in this project is a collection of audio files, separated into two categories: human and other. The `human` folder contains voice recordings from humans, while the `other` folder contains various other sounds. 

## Model
The model used is a simple neural network model with 2 hidden layers, 100 and 50 neurons respectively, with SELU (Scaled Exponential Linear Unit) activation and Lecun normal initializer. The output layer uses sigmoid activation for binary classification.

## Performance Metrics
The performance of the model is evaluated using the confusion matrix and the classification report, which provides precision, recall and F1-score. Additionally, the accuracy and loss of the model on the validation set are also computed.

## Results
After training, the model was evaluated on a validation set. The results are as follows:

- Confusion Matrix:

|   | Predicted: No | Predicted: Yes |
|---|---|---|
| Actual: No | 292 | 33 |
| Actual: Yes | 98 | 1304 |

- Classification Report:

|   | Precision | Recall | F1-score |
|---|---|---|---|
| Class 0 | 0.75 | 0.90 | 0.82 |
| Class 1 | 0.98 | 0.93 | 0.95 |
| Accuracy |  |  | 0.92 |
| Macro Avg | 0.86 | 0.91 | 0.88 |
| Weighted Avg | 0.93 | 0.92 | 0.93 |

- Model Accuracy: 92.41%
- Model Loss: 0.22



# Noise Detection System
This project consists of a noise detection system, implemented using Python and Keras. The goal is to predict whether an audio file is 'clean' or contains 'noise'. This classification problem is approached using a neural network which takes as input the MFCCs (Mel Frequency Cepstral Coefficients) of the audio files.

# System Requirements
To run this project, you'll need to have the following libraries installed:

Python 3.6 or above
librosa
numpy
Keras
scikit-learn
joblib

