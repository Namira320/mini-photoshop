# Mini Photoshop (SnapFilter Pro) 📷

A desktop-based digital image processing application built with Python, featuring real-time image enhancement, geometric transformations, edge detection, color space manipulation, and AI-powered object detection.

---

## 📄 Project Documentation

[mini-photoshop](./mini-photoshop.pdf)

---

## 🚀 Key Features

* **File Management & Preview:** Load standard image formats (`.jpg`, `.png`, `.bmp`) with side-by-side comparison for **Original** and **Processed** workspaces.
* **Basic Adjustments & Filters:** Real-time controls for Brightness, Contrast, Truncation, Grayscale, and Sharpening.
* **Interactive Transformations & Crop:** Dynamic image resizing, rotation, translation, affine shearing, and an **Interactive Crop** feature directly on the canvas.
* **Noise Reduction & Edge Detection:** Built-in filters including Median Filter, Noise Removal, Canny, Roberts, Prewitt, Sobel, Laplacian of Gaussian (LoG), and Thresholding.
* **Color Processing & Segmentation:** Color space splitting (RGB/HSV), threshold adjustments, K-Means clustering, and edge-based segmentation.
* **AI Object Detection:** Integrated Convolutional Neural Network (YOLOv3-tiny via `cvlib`) to automatically detect and draw bounding boxes around specific objects (such as "person").
* **History Management:** Fully supported Undo, Redo, and Reset operations using a memory stack approach.

---

## 🛠️ Tech Stack & Libraries

* **GUI Framework:** CustomTkinter (CTK) & Native Tkinter Canvas
* **Core Logic / Image Processing:** Python 3, OpenCV (`cv2`), NumPy
* **AI & Deep Learning:** `cvlib` with OpenCV DNN Backend
* **Data Visualization:** Matplotlib (integrated for real-time color histograms)

---

## 📋 System Requirements

* **Operating System:** Windows, macOS, or Linux
* **Python Version:** Python 3.10 or higher
* **RAM:** Minimum 4 GB (recommended for undo/redo stack memory management)

