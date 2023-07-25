# ActionLearningAIS4
Repository for ActionLearning Group 4


# Identify Your Own Voice

This code uses a simple deep learning model (Sequential model) to identify whether a provided audio file is from a human or another source. It extracts the MFCC (Mel Frequency Cepstral Coefficient) features from the audio data and uses them as input to the model.

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

