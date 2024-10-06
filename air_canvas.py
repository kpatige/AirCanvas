import cv2
import mediapipe as mp
import numpy as np

# Initialize Mediapipe Hand model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Initialize the canvas for drawing
canvas = None
white_canvas = None

# Define color options and clear option
colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (0, 255, 255), (128, 0, 128), (255, 255, 255)]
color_labels = ["Green", "Blue", "Red", "Yellow", "Purple", "Clear"]
color_index = 0
draw_color = colors[color_index]
prev_x, prev_y = 0, 0

# Start video capture
cap = cv2.VideoCapture(0)

def draw_color_buttons(img):
    for i, color in enumerate(colors):
        cv2.rectangle(img, (i * 100, 0), ((i + 1) * 100, 50), color, -1)
        cv2.rectangle(img, (i * 100, 0), ((i + 1) * 100, 50), (0, 0, 0), 2)  # Border
        cv2.putText(img, color_labels[i], (i * 100 + 10, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0) if color == (255, 255, 255) else (255, 255, 255), 1)
    return img

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    frame = cv2.flip(frame, 1)  # Flip the frame horizontally
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if canvas is None:
        canvas = np.zeros_like(frame)
        white_canvas = np.ones_like(frame) * 255  # Initialize white canvas

    frame = draw_color_buttons(frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

            h, w, _ = frame.shape
            cx, cy = int(index_finger_tip.x * w), int(index_finger_tip.y * h)
            thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)

            # Calculate the distance between index finger tip and thumb tip
            distance = np.sqrt((cx - thumb_x)**2 + (cy - thumb_y)**2)

            if cy < 50:
                color_index = cx // 100
                if color_index == len(colors) - 1:
                    canvas = np.zeros_like(frame)
                    white_canvas = np.ones_like(frame) * 255  # Clear white canvas as well
                else:
                    draw_color = colors[color_index]
            else:
                if distance < 50:  # If index finger and thumb are close, stop drawing
                    prev_x, prev_y = 0, 0
                elif prev_x == 0 and prev_y == 0:
                    prev_x, prev_y = cx, cy
                else:
                    cv2.line(canvas, (prev_x, prev_y), (cx, cy), draw_color, 10)  # Increased thickness
                    cv2.line(white_canvas, (prev_x, prev_y), (cx, cy), draw_color, 10)  # Draw on white canvas
                    prev_x, prev_y = cx, cy

    combined_frame = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)
    
    # Combine the white canvas and combined frame side by side
    final_output = np.hstack((white_canvas, combined_frame))

    cv2.imshow("Air Canvas", final_output)

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'ESC' to exit
        break

cap.release()
cv2.destroyAllWindows()
