<<<<<<< HEAD
# SnapFilter Pro - Mini Photoshop Application

Aplikasi image editing profesional dengan 40+ fitur pemrosesan citra dan machine learning integration.

## 🎯 Fitur Utama

### 1. **Image Management** ✅
- Load gambar (JPG, PNG, BMP, TIFF)
- Save dengan quality control (0-100)
- Reset ke original
- Undo/Redo system (max 20 history states)

### 2. **Image Enhancement** ✅
- Brightness & Contrast adjustment (slider real-time)
- Histogram Equalization (CLAHE)
- Sharpening (kernel-based)
- Gaussian Blur
- Bilateral Filter (edge-preserving blur)

### 3. **Geometric Transformation** ✅
- Rotate (0°-360° dengan slider)
- Flip Horizontal/Vertical
- Crop (interactive drag-select)
- Resize (scale factor)
- Translation (offset X/Y dengan slider)
- Affine transformations dengan interpolasi

### 4. **Image Restoration** ✅
- Gaussian Blur
- Median Filter
- Bilateral Filter
- Morphological operations (open/close/erode/dilate)

### 5. **Binary & Edge Processing** ✅
**Edge Detectors:**
- Canny
- Sobel (X, Y, Both directions)
- Prewitt
- Roberts
- Laplacian
- Laplacian of Gaussian (LoG)

**Thresholding:**
- Simple binary
- Otsu's method
- Adaptive thresholding

**Morphology:**
- Erosion
- Dilation
- Morphological Opening
- Morphological Closing

### 6. **Color Processing** ✅
- RGB → Grayscale
- Channel Splitting (R, G, B analysis)
- HSV Adjustment (Hue, Saturation, Value sliders)
- Color space transformations

### 7. **Image Segmentation** ✅
- Threshold-based segmentation
- K-means clustering (2-10 clusters)
- Watershed segmentation
- Region extraction

### 8. **Image Compression** ✅
- Save dengan quality levels (10-100)
- Format support (JPG, PNG, BMP)
- RLE compression simulation
- Compression ratio calculation

### 9. **Histogram Analysis** ✅
- Grayscale histogram display
- RGB channel histograms
- Interactive matplotlib visualization
- Before/After comparison

### 10. **User Interface** ✅
- Menu bar (File, Edit, Filter, Transform, Analysis)
- Scrollable sidebar dengan 30+ filter buttons
- Real-time preview
- Slider controls untuk parameter tuning
- Status bar untuk feedback
- Dark mode (CustomTkinter)

### 11. **Machine Learning (Bonus)** ✅
- Face Detection menggunakan Haar Cascades
- Real-time detection dengan bounding boxes
- Confidence visualization

## 📋 Requirements

```
customtkinter>=5.0.0
opencv-python>=4.8.0
pillow>=10.0.0
numpy>=1.24.0
matplotlib>=3.8.0
scikit-learn>=1.3.0
scipy>=1.11.0
```

## 🚀 Installation

### Step 1: Create Virtual Environment (Recommended)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

Atau install manually jika ada masalah:
```bash
pip install customtkinter opencv-python pillow numpy matplotlib scikit-learn scipy
```

### Step 3: Run Application
```bash
python main.py
```

## 📁 File Structure
```
miniPhotoshop/
├── main.py              # Main GUI application (38KB)
├── filters.py           # Image processing functions (15KB)
├── requirements.txt     # Python dependencies
└── README.md           # Documentation (this file)
```

## 🎮 How to Use

### Opening an Image
1. Click "📂 Buka Gambar" button
2. Select an image file (JPG, PNG, BMP, TIFF)
3. Image loads and displays in canvas

### Applying Filters
1. Use sidebar buttons or menu bar
2. For sliders: drag to adjust, see live preview
3. Image updates in real-time

### Saving Results
1. Adjust quality slider (10-100)
2. Click "💾 Simpan Hasil"
3. Choose format (JPG, PNG, BMP)
4. Enter filename

### Undo/Redo
- Click "↶ Undo" to revert last change
- Click "↷ Redo" to restore change
- Max 20 history states

### Histogram Analysis
- Click "Show Histogram" button
- Opens matplotlib window dengan histogram
- Display RGB channels atau grayscale

### Face Detection
- Click "🤖 Face Detection"
- Automatically detects faces dan draws bounding boxes
- Shows count di status bar

## 🔧 Technical Details

### Image Processing Pipeline
1. **Original Master Copy**: `cv_img_original` (read-only reference)
2. **Working Copy**: `cv_img_processed` (editable working image)
3. **History Stack**: Maintains last 20 states untuk undo/redo

### Filter Categories
- **Enhancement**: Brightness, contrast, histogram, sharpening
- **Geometric**: Rotation, flip, crop, resize, translation
- **Restoration**: Noise reduction, morphological operations
- **Edge Detection**: 6 different edge detectors + morphology
- **Color**: Grayscale, HSV, channel operations
- **Segmentation**: Thresholding, clustering, watershed
- **Analysis**: Histogram, statistics, metadata

### Affine Transformations
- Uses `cv2.getRotationMatrix2D()` untuk rotation
- `cv2.warpAffine()` untuk transformation application
- Support untuk interpolation (nearest/linear)

### Performance Optimizations
- Direct NumPy operations untuk speed
- Lazy loading dari image files
- Efficient memory management
- Real-time preview tanpa lag

## 📊 Filter Reference

### Enhancement Sliders
- Brightness: -100 to +100
- Contrast: 0.5x to 3.0x
- Hue: -180° to +180°
- Saturation: 0.5x to 2.0x
- Value: 0.5x to 2.0x

### Transformation Sliders
- Rotation: 0° to 360°
- Translate X: -200 to +200 pixels
- Translate Y: -200 to +200 pixels

### Compression
- Quality: 10 to 100 (untuk JPEG)
- PNG compression: auto-calculated

## 🎯 Tips & Tricks

1. **Real-time Adjustment**: Slider values apply instantly
2. **Undo/Redo Workflow**: Work non-destructively
3. **Quality Control**: Adjust quality sebelum save untuk file size
4. **Channel Analysis**: Split channels untuk debug color problems
5. **Histogram Matching**: Use untuk perbandingan before/after
6. **Batch Operations**: Combine multiple filters untuk custom effects

## ⚙️ Configuration

### Default Settings
- Appearance: Dark mode
- Color Theme: Blue
- Max History: 20 states
- Default Quality: 95

### Customization
Edit di `main.py`:
```python
ctk.set_appearance_mode("dark")  # Change ke "light"
ctk.set_default_color_theme("blue")  # Change theme
```

## 🐛 Troubleshooting

### "Module not found" errors
```bash
pip install --upgrade -r requirements.txt
```

### GUI tidak muncul
- Check Python version (3.8+)
- Verify tkinter installed: `python -m tkinter`

### Image tidak load
- Check format (support JPG, PNG, BMP, TIFF)
- Verify image path valid
- Try smaller resolution

### Filters terlalu lambat
- Reduce image resolution
- Use lower quality setting
- Disable live preview untuk real-time sliders

## 📚 Algorithm References

### Edge Detection
- **Canny**: Multi-stage edge detection dengan hysteresis
- **Sobel**: Gradient-based using convolution kernels
- **Prewitt**: Similar ke Sobel, different kernels
- **Roberts**: 2x2 kernels untuk fast computation
- **Laplacian**: 2nd derivative untuk edge enhancement
- **LoG**: Laplacian after Gaussian blur

### Segmentation
- **Threshold**: Biner classification berdasarkan intensity
- **K-means**: Iterative clustering algorithm
- **Watershed**: Topological approach untuk region labeling

### Morphology
- **Erosion**: Removes white regions (dengan structuring element)
- **Dilation**: Expands white regions
- **Opening**: Erosion then dilation (remove noise)
- **Closing**: Dilation then erosion (fill holes)

## 📝 License & Credits

**Diadaptasi untuk PCD 2026 Assignment**

Menggunakan libraries:
- OpenCV (cv2) - Computer Vision
- Pillow - Image processing
- NumPy - Numerical computing
- Matplotlib - Data visualization
- CustomTkinter - Modern GUI
- Scikit-learn - Machine learning

## 📧 Support

For issues, questions, atau suggestions:
1. Check README dan Filter Reference
2. Verify Python version dan dependencies
3. Test dengan sample image
4. Check console output untuk error messages

---

**SnapFilter Pro v1.0** - Built for Image Processing Course 2026
=======
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

>>>>>>> 0f82978d557ace535beff4d74f745f059b069c1f
