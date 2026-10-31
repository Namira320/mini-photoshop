# Mini Photoshop (SnapFilter Pro) 📷

A professional desktop-based digital image processing application built with Python featuring 40+ image processing features, real-time image enhancement, geometric transformations, edge detection, color space manipulation, and machine learning integration.

---

## 📺 Demo Video
[![Watch the video](https://img.youtube.com/vi/mBY7YgPAT2c/hqdefault.jpg)](https://youtu.be/mBY7YgPAT2c)

---

## 📄 Project Documentation

[mini-photoshop](./mini-photoshop.pdf)

---

## 🎯 Main Features

### 1. **Image Management** ✅
- Load image (JPG, PNG, BMP, TIFF)
- Save with quality control (0-100)
- Reset to original
- Undo/Redo system (max 20 history states)

### 2. **Image Enhancement** ✅
- Brightness & Contrast adjustment (slider real-time)
- Histogram Equalization (CLAHE)
- Sharpening (kernel-based)
- Gaussian Blur
- Bilateral Filter (edge-preserving blur)

### 3. **Geometric Transformation** ✅
- Rotate (0°-360° with slider)
- Flip Horizontal/Vertical
- Crop (interactive drag-select)
- Resize (scale factor)
- Translation (offset X/Y with slider)
- Affine transformations with interpolation

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
- Save with quality levels (10-100)
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
- Scrollable sidebar with 30+ filter buttons
- Real-time preview
- Slider controls for parameter tuning
- Status bar for feedback
- Dark mode (CustomTkinter)

### 11. **Machine Learning (Bonus)** ✅
- Face Detection with Haar Cascades
- Real-time detection with bounding boxes
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

Or install manually if there are any problems:
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
- Opens matplotlib window with the histogram
- Display RGB channels or grayscale

### Face Detection
- Click "🤖 Face Detection"
- Automatically detects faces and draws bounding boxes
- Shows count in the status bar

## 🔧 Technical Details

### Image Processing Pipeline
1. **Original Master Copy**: `cv_img_original` (read-only reference)
2. **Working Copy**: `cv_img_processed` (editable working image)
3. **History Stack**: Maintains last 20 states for undo/redo

### Filter Categories
- **Enhancement**: Brightness, contrast, histogram, sharpening
- **Geometric**: Rotation, flip, crop, resize, translation
- **Restoration**: Noise reduction, morphological operations
- **Edge Detection**: 6 different edge detectors + morphology
- **Color**: Grayscale, HSV, channel operations
- **Segmentation**: Thresholding, clustering, watershed
- **Analysis**: Histogram, statistics, metadata

### Affine Transformations
- Uses `cv2.getRotationMatrix2D()` for rotation
- `cv2.warpAffine()` for transformation application
- Support for interpolation (nearest/linear)

### Performance Optimizations
- Direct NumPy operations for speed
- Lazy loading from image files
- Efficient memory management
- Real-time preview without lag

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
- Quality: 10 to 100 (for JPEG)
- PNG compression: auto-calculated

## 🎯 Tips & Tricks

1. **Real-time Adjustment**: Slider values apply instantly
2. **Undo/Redo Workflow**: Work non-destructively
3. **Quality Control**: Adjust quality before save for file size
4. **Channel Analysis**: Split channels for debug color problems
5. **Histogram Matching**: Use for before/after comparisons
6. **Batch Operations**: Combine multiple filters for custom effects

## ⚙️ Configuration

### Default Settings
- Appearance: Dark mode
- Color Theme: Blue
- Max History: 20 states
- Default Quality: 95

### Customization
Edit in `main.py`:
```python
ctk.set_appearance_mode("dark")  # Change to "light"
ctk.set_default_color_theme("blue")  # Change theme
```

## 🐛 Troubleshooting

### "Module not found" errors
```bash
pip install --upgrade -r requirements.txt
```

### GUI does not appear
- Check Python version (3.8+)
- Verify tkinter installed: `python -m tkinter`

### Image does not load
- Check format (support JPG, PNG, BMP, TIFF)
- Verify image path valid
- Try smaller resolution

### Filters too slow
- Reduce image resolution
- Use lower quality setting
- Disable live preview for real-time sliders

## 📚 Algorithm References

### Edge Detection
- **Canny**: Multi-stage edge detection with hysteresis
- **Sobel**: Gradient-based using convolution kernels
- **Prewitt**: Similar to Sobel, different kernels
- **Roberts**: 2x2 kernels for fast computation
- **Laplacian**: 2nd derivative for edge enhancement
- **LoG**: Laplacian after Gaussian blur

### Segmentation
- **Threshold**: Binary classification based on intensity
- **K-means**: Iterative clustering algorithm
- **Watershed**: Topological approach for region labeling

### Morphology
- **Erosion**: Removes white regions (with structuring element)
- **Dilation**: Expands white regions
- **Opening**: Erosion then dilation (remove noise)
- **Closing**: Dilation then erosion (fill holes)

## 📝 License & Credits

Built with libraries:
- OpenCV (cv2) - Computer Vision
- Pillow - Image processing
- NumPy - Numerical computing
- Matplotlib - Data visualization
- CustomTkinter - Modern GUI
- Scikit-learn - Machine learning

## 📧 Support

For issues, questions, or suggestions:
1. Check README and Filter Reference
2. Verify Python version and dependencies
3. Test with sample image
4. Check console output for error messages


