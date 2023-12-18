## Technologies Used

- **Python:** Main programming language.
- **NumPy:** For numerical operations on arrays and matrices.
- **OpenCV (cv2):** For capturing video frames from the webcam and processing images.
- **Keras:** For loading and utilizing the pre-trained machine learning model.
- **Keyboard:** To capture keyboard inputs during gameplay.

## Features

- **Real-time Gesture Recognition:** The application captures video from the webcam and uses a trained model to recognize hand gestures.
- **Gesture Classification:** Classifies gestures into Rock, Paper, or Scissors, with an additional 'false reading' category.
- **Gameplay Logic:** Includes a class to manage game state, tally wins and losses, and determine game outcomes.

## Repository Structure
```
├── camera_rps.py # Main script with game logic and computer vision processing
├── keras_model.h5 # Pre-trained model file
├── labels.txt
```

## Getting Started

### Prerequisites

- Python 3.x
- NumPy, OpenCV (cv2), Keras, Keyboard

### Installation

```bash
git clone https://github.com/freestyleabg/computer-vision-rock-paper-scissors.git
cd computer-vision-rock-paper-scissors

pip install -r requirements.txt
```
### Usage

Run python camera_rps.py to start the game. Follow on-screen instructions for gameplay.
