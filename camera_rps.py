import random
import time
import numpy as np
import cv2
from keras.models import load_model
import keyboard

# Load the pre-trained Keras model for predicting hand gestures
model = load_model('keras_model.h5')

# Open the webcam. Change the index if necessary to correspond to the correct camera.
cap = cv2.VideoCapture(4)

# Create a data buffer for the image in the shape required by the model
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# List of options corresponding to the possible hand gestures
options = ['rock', 'paper', 'scissors', 'false reading']


class RockPaperScissors:
    """Class for playing a game of Rock, Paper, Scissors against the computer."""

    def __init__(self):
        """Initialize the game with counters for wins and losses."""
        self.num_wins = 0
        self.num_loss = 0

    def get_cpu_choice(self):
        """Randomly select a choice for the CPU."""
        return random.randint(0, 2)

    def get_winner(self, user_choice, cpu_choice):
        """
        Determine the winner of a round.

        Args:
            user_choice (int): The choice of the user (0: Rock, 1: Paper, 2: Scissors).
            cpu_choice (int): The choice of the CPU (0: Rock, 1: Paper, 2: Scissors).

        Returns:
            str: 'draw', 'player', or 'CPU' indicating the winner.
        """
        if user_choice == cpu_choice:
            return "draw"
        elif (user_choice == 0 and cpu_choice == 2) or \
                (user_choice == 1 and cpu_choice == 0) or \
                (user_choice == 2 and cpu_choice == 1):
            self.num_wins += 1
            return "player"
        else:
            self.num_loss += 1
            return "CPU"

    def get_prediction(self):
        """
        Capture webcam input and use the model to predict the user's choice.

        Returns:
            int: The predicted choice (0: Rock, 1: Paper, 2: Scissors, 3: Invalid).
        """
        start_time = time.time()

        while True:
            # Capture frame-by-frame from the webcam
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame from the webcam.")
                break

            # Resize the frame to match the model's input size
            resized_frame = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)
            image_np = np.array(resized_frame)
            normalized_image = (image_np.astype(np.float32) / 127.0) - 1  # Normalize the image
            data[0] = normalized_image
            prediction = model.predict(data)
            rounded_prediction = np.round(prediction, 2)
            print(rounded_prediction)

            # Countdown timer for user to make a gesture
            countdown_time = 5.5
            running_time = time.time() - start_time
            running_time_inverse = abs(countdown_time - running_time)

            # Show the countdown on the webcam frame
            cv2.putText(frame, str(round(running_time_inverse, 0)), (450, 450),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 5)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) and running_time > countdown_time:
                break

            max_prediction = np.argmax(prediction)
        return max_prediction

    def play(self):
        """Start the Rock Paper Scissors game and manage the game loop."""
        print("Welcome to Rock Paper Scissors!")

        play_again = True

        while play_again:
            cpu_choice = self.get_cpu_choice()
            user_choice = self.get_prediction()

            # Exit loop if invalid choice is made
            if user_choice > 2:
                break

            print(f"\nTimes up! You chose {options[user_choice].capitalize()}.")
            time.sleep(2)
            print(f"CPU chose {options[cpu_choice].capitalize()}.\n")

            winner = self.get_winner(user_choice, cpu_choice)

            # Print the outcome of the round
            if winner == "draw":
                print("It's a draw!")
            elif winner == "player":
                print("You win!")
            else:
                print("You lost.")

            # Check if the game has reached a winning condition
            if self.num_wins >= 3 or self.num_loss >= 3:
                print(f"\n{winner.capitalize()} wins!")
                break
            else:
                print(f"Wins: {self.num_wins}, Losses: {self.num_loss}")
                print("\nPress c to continue. Press another key to quit")
                if keyboard.read_key() == "c":
                    print("You pressed 'c'.")
                    play_again = True
                    time.sleep(2)
                else:
                    break


def find_cv2_backends():
    """List available OpenCV Video Backends."""
    available_backends = [cv2.videoio_registry.getBackendName(b) for b in cv2.videoio_registry.getBackends()]
    print("Available OpenCV Video Backends:", available_backends)


def find_camera_index(max_cameras=10):
    """
    Print the list of available camera indices.

    Args:
        max_cameras (int): Maximum number of camera indices to check.
    """
    for i in range(max_cameras):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"Camera index {i} is available")
            cap.release()
        else:
            print(f"No camera found at index {i}")


if __name__ == "__main__":
    game = RockPaperScissors()
    game.play()

    # Cleanup resources after the game is over
    cap.release()  # Release the webcam
    cv2.destroyAllWindows()  # Close all open windows
