# SnapFilter Pro - Complete Setup Guide

## ⚙️ Prerequisites

- Python 3.8+ (tested dengan 3.10, 3.11, 3.12, 3.14)
- Windows / macOS / Linux
- ~500MB disk space untuk dependencies
- Tkinter (biasanya included dengan Python)

## 📥 Installation Steps

### Option 1: Using Virtual Environment (RECOMMENDED)

#### Step 1: Navigate ke project directory
```bash
cd c:\Users\<YourUsername>\Downloads\miniPhotoshop
```

#### Step 2: Create virtual environment
```bash
# Windows
python -m venv venv

# macOS/Linux
python3 -m venv venv
```

#### Step 3: Activate virtual environment
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

Status: Anda akan lihat `(venv)` di awal command prompt

#### Step 4: Install dependencies
```bash
pip install -r requirements.txt
```

Alternative jika ada issue:
```bash
pip install --upgrade pip
pip install customtkinter opencv-python pillow numpy matplotlib scikit-learn scipy
```

#### Step 5: Run aplikasi
```bash
python main.py
```

---

### Option 2: System-wide Installation (NOT RECOMMENDED)

```bash
cd c:\Users\<YourUsername>\Downloads\miniPhotoshop
pip install -r requirements.txt
python main.py
```

⚠️ **Warning**: Ini bisa conflict dengan other Python projects

---

### Option 3: Using UV (Fast Package Manager)

Jika sudah install UV:
```bash
uv pip install -r requirements.txt --break-system-packages
python main.py
```

---

## 🔧 Troubleshooting Installation

### "ModuleNotFoundError: No module named 'customtkinter'"

**Solution:**
```bash
# Make sure virtual environment is activated
pip install customtkinter

# Atau reinstall semua
pip install -r requirements.txt --force-reinstall
```

### "python: command not found"

**Windows:**
- Use `python.exe` instead of `python`
- Or use `py` shortcut: `py main.py`

**macOS/Linux:**
- Use `python3` instead of `python`
- Or create alias: `alias python=python3`

### "ImportError: No module named 'tkinter'"

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**macOS:**
- Tkinter usually included with Python
- If missing, reinstall Python from python.org

**Windows:**
- Check "tcl/tk and IDLE" during Python installation
- Or reinstall Python with this option selected

### "ERROR: externally-managed-environment"

**Solution:**
```bash
# Use virtual environment approach
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## ✅ Verify Installation

Jalankan command berikut untuk verify semua modules:

```bash
python -c "
import customtkinter
import cv2
import numpy as np
import PIL
import matplotlib
import sklearn
import scipy
print('All packages installed successfully!')
"
```

Expected output:
```
All packages installed successfully!
```

---

## 🚀 Running the Application

### Normal Run
```bash
python main.py
```

### With Debug Output
```bash
python -u main.py
```

### With Error Handling
```python
# Create debug.py
import traceback
try:
    from main import MiniPhotoshop
    app = MiniPhotoshop()
    app.mainloop()
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()
```

Then run: `python debug.py`

---

## 📖 First Run Checklist

- [ ] GUI window appears
- [ ] "Buka Gambar" button works
- [ ] Can select an image file
- [ ] Image displays on canvas
- [ ] Brightness slider updates preview live
- [ ] "Simpan Hasil" saves file
- [ ] "Reset Original" works
- [ ] Edge detection filters work
- [ ] Histogram displays in matplotlib window

---

## 🎨 Configuration (Optional)

### Change Theme Color

Edit `main.py` line 8-9:
```python
ctk.set_appearance_mode("dark")  # or "light"
ctk.set_default_color_theme("blue")  # options: blue, green, dark-blue
```

### Change Window Size

Edit `main.py` line 16:
```python
self.geometry("1400x850")  # width x height
```

### Change Image Preview Size

Edit `filters.py` line ~690:
```python
canvas_width, canvas_height = 1080, 600  # adjust preview size
```

---

## 📱 Using Application

### Loading Image
1. Click "📂 Buka Gambar"
2. Select image file (JPG, PNG, BMP, TIFF)
3. Click "Open"

### Applying Filters
1. **Real-time sliders**: Move slider immediately see preview
2. **Button filters**: Click button untuk instant apply
3. **All filters non-destructive**: Original preserved

### Saving Work
1. Adjust "Save Quality" slider (10-100)
2. Click "💾 Simpan Hasil"
3. Choose format (JPG, PNG, BMP)
4. Enter filename
5. Click "Save"

### Advanced Operations
- **Undo/Redo**: Max 20 history states
- **Histogram**: Click "Show Histogram" untuk analysis
- **Face Detection**: Click "🤖 Face Detection" untuk detect
- **Segmentation**: Try K-means, Watershed untuk different results

---

## 🔍 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| GUI tidak muncul | Check tkinter installed, use `python -m tkinter` |
| Slow performance | Use smaller image, lower resolution |
| Image tidak load | Check format (JPG, PNG, BMP), try different file |
| Filter error | Make sure image loaded, check console output |
| Memory error | Reduce image size, clear history (Undo multiple times) |
| Matplotlib error | May need X11 display on macOS/Linux |

---

## 📊 System Requirements

### Minimum
- Python 3.8+
- 4GB RAM
- 500MB disk space

### Recommended
- Python 3.10+
- 8GB+ RAM
- 1GB disk space
- SSD untuk faster I/O

### Tested On
- ✅ Windows 10/11 (Python 3.10+)
- ✅ macOS 12+ (Python 3.10+)
- ✅ Ubuntu 20.04+ (Python 3.10+)
- ✅ Python 3.14.x (latest)

---

## 🐛 Getting Help

### Step 1: Check Error Message
Look at console output (bottom of terminal)

### Step 2: Search README
Check `README.md` untuk feature documentation

### Step 3: Check Implementation Summary
Read `IMPLEMENTATION_SUMMARY.md` untuk detailed info

### Step 4: Verify Environment
```bash
python --version
pip show customtkinter opencv-python
pip list
```

### Step 5: Create Minimal Test
```python
import cv2
import customtkinter as ctk

# Test minimal app
root = ctk.CTk()
label = ctk.CTkLabel(root, text="Test")
label.pack()
root.mainloop()
```

---

## 🔄 Updating Dependencies

```bash
# Update semua packages
pip install -r requirements.txt --upgrade

# Atau specific package
pip install customtkinter --upgrade
```

---

## 🗑️ Cleanup

### Remove Virtual Environment
```bash
# Remove venv directory
# Windows: rmdir venv /s /q
# macOS/Linux: rm -rf venv
```

### Clean Python Cache
```bash
# Remove __pycache__
# Windows: for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"
# macOS/Linux: find . -type d -name __pycache__ -exec rm -r {} +
```

---

## 🎯 Quick Commands Reference

```bash
# Setup
python -m venv venv           # Create environment
venv\Scripts\activate          # Activate (Windows)
source venv/bin/activate       # Activate (macOS/Linux)

# Install
pip install -r requirements.txt

# Run
python main.py

# Test
python -c "import customtkinter; print('OK')"

# Update
pip install -r requirements.txt --upgrade

# Deactivate
deactivate                     # Exit virtual environment
```

---

## ✨ Next Steps

1. **Load sample image** → Open included test image (if available)
2. **Try all filters** → Explore each category
3. **Read algorithm docs** → Understand what each filter does
4. **Combine filters** → Create custom effects
5. **Experiment** → Have fun!

---

## 📚 Additional Resources

- **OpenCV Docs**: https://docs.opencv.org/
- **CustomTkinter**: https://github.com/TomSchimansky/CustomTkinter
- **NumPy**: https://numpy.org/doc/
- **Pillow**: https://pillow.readthedocs.io/
- **Matplotlib**: https://matplotlib.org/

---

**Setup Complete! Enjoy SnapFilter Pro! 🎉**
