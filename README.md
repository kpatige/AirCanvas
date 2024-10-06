# **Interactive Air Canvas with Hand Tracking**

## **Project Overview**

This project is an **Interactive Air Canvas** that allows users to draw in real-time using hand gestures. By utilizing **OpenCV** for video processing and **MediaPipe** for hand tracking, the application enables users to interact with a virtual canvas without needing any physical drawing tools. The user's hand movements are tracked, and gestures like fingertip movement allow them to draw on the canvas. Users can also change colors and clear the canvas through intuitive gestures.

## **Features**

- **Real-Time Hand Tracking**: The project uses MediaPipe’s hand tracking module to detect hand landmarks and track the movement of the index finger, enabling gesture-based drawing on the canvas.
  
- **Color Selection via UI**: A simple color palette with predefined colors (red, green, blue, cyan, magenta, white) is displayed at the top of the screen. Users can hover their finger over a color box to select a new drawing color.

- **Drawing on Canvas**: By moving the index finger over the canvas area, users can draw lines. The color of the drawing changes based on the selected color from the color palette.

- **Canvas Clearing Gesture**: The "Clear" option allows the user to reset the canvas by hovering over the clear box in the palette, erasing all drawings and starting fresh.

- **Dual Output Views**: The application shows two outputs side by side:
  - A **white canvas** where the user’s drawing is displayed in full on a blank background.
  - A **combined frame** that overlays the drawing on the live webcam feed for a more interactive visual experience.
