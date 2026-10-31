# SnapFilter Pro - Quick Start Guide

## ⚡ 3-Minute Setup

### 1️⃣ Install Dependencies (1 minute)
```bash
cd c:\Users\Boazoma\Downloads\miniPhotoshop
pip install customtkinter opencv-python pillow numpy matplotlib scikit-learn scipy
```

### 2️⃣ Run Application (instant)
```bash
python main.py
```

### 3️⃣ Open an Image (instant)
- Click "📂 Buka Gambar"
- Select any JPG, PNG, or BMP file
- Click "Open"

---

## 🎯 10 Essential Features You Must Try

### 1. Brightness Control
```
👉 Slide "Brightness" slider left/right
✓ See instant live preview
```

### 2. Edge Detection
```
👉 Click "Canny" button
✓ Sketch-like image effect
```

### 3. Face Detection
```
👉 Click "🤖 Face Detection"
✓ Green boxes appear around faces
```

### 4. Rotate Image
```
👉 Drag "Rotate (°)" slider to 45°
✓ Image rotates in real-time
```

### 5. Black & White
```
👉 Click "⚫ Grayscale"
✓ Instant B&W conversion
```

### 6. Flip Image
```
👉 Click "↔️ Flip Horizontal" atau "↕️ Flip Vertical"
✓ Image flipped
```

### 7. Show Histogram
```
👉 Click "📈 Show Histogram"
✓ Matplotlib window shows pixel distribution
```

### 8. Sharpen Image
```
👉 Click "🔪 Sharpen"
✓ Image becomes more crisp
```

### 9. Blur Background
```
👉 Click "💧 Gaussian Blur"
✓ Soft, blurry effect
```

### 10. Undo/Redo
```
👉 Click "↶ Undo" to revert
👉 Click "↷ Redo" to restore
✓ Max 20 history states
```

---

## 💾 Saving Your Work

### Save with Quality Control
```
1. Adjust "Save Quality" slider (10=low, 100=high)
2. Click "💾 Simpan Hasil"
3. Choose format: JPG, PNG, or BMP
4. Enter filename
5. Click "Save"
```

### Example
```
Filename: my_photo_edited
Format: JPEG
Quality: 85
Result: my_photo_edited.jpg (smaller file size, good quality)
```

---

## 🎨 Filter Quick Reference

| Category | Best For | Example |
|----------|----------|---------|
| **Brightness** | Dark/Bright fixes | Adjust slider |
| **Histogram Eq** | Improve contrast | One-click enhancement |
| **Canny Edge** | Sketch/outline | Edge detection |
| **Grayscale** | B&W effect | Instant conversion |
| **Blur** | Soft effect | Gaussian blur |
| **Sharpen** | Crisp image | Detail enhancement |
| **Flip** | Mirror effect | H/V flip |
| **Rotate** | Turn image | 0-360° rotation |
| **Crop** | Focus area | Drag to select |
| **K-means** | Color reduction | Artistic effect |

---

## 🐛 Troubleshooting

### Image Not Loading?
```bash
# Check file format - must be: JPG, PNG, BMP, or TIFF
# Try with a different image file
```

### Slow Performance?
```bash
# Use smaller image resolution
# Try lower quality images
# Close other applications
```

### GUI Won't Start?
```bash
# Reinstall dependencies:
pip install -r requirements.txt --force-reinstall

# Or use:
python -m pip install --upgrade customtkinter
```

### Module Not Found?
```bash
# Install missing module
pip install customtkinter opencv-python pillow numpy matplotlib scikit-learn scipy
```

---

## 🎮 Keyboard & Mouse

| Action | How To | Result |
|--------|--------|--------|
| **Open Image** | Click "📂 Buka Gambar" | File dialog opens |
| **Apply Filter** | Click button | Filter applied instantly |
| **Adjust Slider** | Drag slider | Live preview updates |
| **Crop** | Click crop, drag on image | Select area to keep |
| **Undo** | Click "↶ Undo" | Revert last change |
| **Save** | Click "💾 Simpan Hasil" | Save dialog opens |

---

## 📊 Expert Tips

### Tip 1: Combine Filters
```
1. Apply Gaussian Blur
2. Then apply Sharpen
3. Result: Soft with preserved edges
```

### Tip 2: Compare Filters
```
1. Apply Canny edge detection
2. Click Undo
3. Try Sobel instead
4. Compare results
```

### Tip 3: Color Exploration
```
1. Adjust Hue slider
2. Watch colors change
3. Adjust Saturation
4. Adjust Value
5. Find perfect color balance
```

### Tip 4: Histogram Analysis
```
1. Apply histogram equalization
2. Click "Show Histogram"
3. See improved distribution
4. Compare before/after
```

### Tip 5: Quality Control
```
- JPG @ 95: Best quality, larger file
- JPG @ 75: Good quality, medium file
- JPG @ 50: Acceptable, small file
- Experiment to find sweet spot!
```

---

## 🚀 Advanced Features

### Face Detection
```
1. Load image dengan faces
2. Click "🤖 Face Detection"
3. Green boxes appear around each face
4. Count shown di status bar
5. Status bar: "Detected X face(s)"
```

### Image Segmentation
```
1. Load image
2. Click "🎯 K-means Clustering"
3. Choose number of clusters (2-10)
4. Image becomes color-segmented
5. Try different cluster counts untuk comparison
```

### Channel Analysis
```
1. Load color image
2. Click "🌈 Split Channels"
3. Matplotlib shows R, G, B channels separately
4. Analyze individual color information
```

---

## ❓ FAQ

**Q: Apa itu histogram equalization?**
A: Teknik meningkatkan contrast dengan mendistribusikan ulang pixel intensity. Result: Lebih kontras image.

**Q: Bagaimana cara crop image?**
A: Click "✂️ Crop", then drag on image untuk select area, release untuk apply.

**Q: Berapa maksimal undo?**
A: Max 20 history states. Lebih dari itu, history paling lama akan dihapus.

**Q: Format apa yang supported?**
A: Load: JPG, PNG, BMP, TIFF. Save: JPG, PNG, BMP.

**Q: Apa beda Canny vs Sobel?**
A: Canny = lebih akurat edge detection. Sobel = faster, lebih tebal edges.

**Q: Gimana cara face detection?**
A: Click "🤖 Face Detection". Automatic detect & draw green boxes.

---

## 📱 System Requirements

- Python 3.8+
- 4GB RAM
- 500MB disk space
- Windows / Mac / Linux

---

## 📞 Getting Help

1. Check README.md untuk overview
2. Check SETUP_GUIDE.md untuk setup issues
3. Check FEATURES.md untuk feature details
4. Check console output untuk error messages
5. Try dengan different image file

---

## 🎉 You're Ready!

```
✅ Dependencies installed
✅ Application running
✅ Image loaded
✅ Filters working
✅ Saving successful

👉 Now go create amazing images! 🎨
```

---

**Need more info? See full documentation files:**
- README.md - Complete overview
- SETUP_GUIDE.md - Installation help
- FEATURES.md - All features listed
- IMPLEMENTATION_SUMMARY.md - Technical details

**Enjoy SnapFilter Pro! 🚀**
