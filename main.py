# filepath: c:\Users\Boazoma\Downloads\miniPhotoshop\main.py
import customtkinter as ctk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import cv2
import numpy as np
import cvlib as cv
from cvlib.object_detection import draw_bbox
import os
from filters import *
import matplotlib.pyplot as plt
import threading


# Set tampilan ke Dark Mode 
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MiniPhotoshop(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SnapFilter Pro - PCD 2026")
        self.geometry("1400x850")
        self.resizable(True, True)

        # Variabel penyimpan memori gambar
        self.cv_img_original = None
        self.cv_img_processed = None
        self.image_history = []  # Undo/Redo stack
        self.history_index = -1
        
        # Current file info
        self.current_file = None
        self.current_dir = os.path.expanduser("~")

        # === Status Fitur Interactive Crop (Ala Photoshop) ===
        self.mode_crop_aktif = False 
        self.crop_rect_id = None    
        self.crop_handle_ids = []    
        self.start_x = None          
        self.start_y = None          
        self.current_crop_rect = None 
        
        # Binding Mouse ditunda, akan dipanggil saat kanvas sudah dibuat di display_image

        # --- PENGATURAN LAYOUT UTAMA ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # === MENU BAR ===
        #self.create_menu_bar()

        # === STATUS BAR ===
        self.status_frame = ctk.CTkFrame(self, height=30, fg_color="#1a1a1a")
        self.status_frame.grid(row=2, column=0, columnspan=2, sticky="ew")
        self.status_label = ctk.CTkLabel(self.status_frame, text="Ready", text_color="gray")
        self.status_label.pack(side="left", padx=10, pady=5)

        # === PANEL SIDEBAR (KIRI) ===
        self.sidebar = ctk.CTkScrollableFrame(self, width=280, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")

        # Judul Aplikasi
        self.label = ctk.CTkLabel(self.sidebar, text="SnapFilter Pro", 
                                  font=("Urbanist", 20, "bold"), text_color="#3b82f6")
        self.label.pack(pady=15)

        # File Management
        self.create_file_buttons()

        # Image Enhancement
        self.create_enhancement_section()

        # Geometric Transformation
        self.create_geometric_section()

        # Restoration & Noise
        self.create_restoration_section()

        # Edge & Binary
        self.create_edge_section()

        # Color Processing
        self.create_color_section()

        # Segmentation
        self.create_segmentation_section()



        # Compression & Analysis
        self.create_analysis_section()

        # === PANEL CANVAS (KANAN: BEFORE - AFTER) ===
        self.canvas_frame = ctk.CTkFrame(self)
        self.canvas_frame.grid(row=0, column=1, rowspan=2, padx=15, pady=15, sticky="nsew")
        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(1, weight=1) # Tambahan untuk kolom kedua

        # Kanvas Kiri (Original)
        self.canvas_original = ctk.CTkLabel(self.canvas_frame, text="Original", font=("Inter", 16), fg_color="#020617", text_color="gray")
        self.canvas_original.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Kanvas Kanan (Processed)
        self.canvas = ctk.CTkLabel(self.canvas_frame, text="Processed", font=("Inter", 16), fg_color="#020617", text_color="gray")
        self.canvas.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # === FRAME UNTUK HISTOGRAM (DI BAWAH GAMBAR) ===
        self.hist_frame_original = ctk.CTkFrame(self.canvas_frame, height=150, fg_color="#1e1e1e")
        self.hist_frame_original.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        
        self.hist_frame_processed = ctk.CTkFrame(self.canvas_frame, height=150, fg_color="#1e1e1e")
        self.hist_frame_processed.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        self.bind("<Button-1>", self.on_canvas_click)
        self.bind("<B1-Motion>", self.on_canvas_drag)
        self.bind("<ButtonRelease-1>", self.on_canvas_release)
        
        # Panggil Menu Bar Native
        self.create_menu_bar()


    def create_menu_bar(self):
        """Membuat Menu Toolbar Native (Drop-down standar desktop)"""
        import tkinter as tk 
        
        menubar = tk.Menu(self)
        
        # === 1. Menu FILE ===
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Buka Gambar", command=self.open_image)
        file_menu.add_command(label="Simpan Hasil", command=self.save_image) # Asumsi nama fungsimu save_image
        file_menu.add_separator()
        file_menu.add_command(label="Keluar", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # === 2. Menu EDIT ===
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.undo) 
        edit_menu.add_command(label="Redo", command=self.redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Reset Original", command=self.reset_image) # Asumsi nama fungsimu reset_image
        menubar.add_cascade(label="Edit", menu=edit_menu)
        
        # === 3. Menu FILTER ===
        filter_menu = tk.Menu(menubar, tearoff=0)
        filter_menu.add_command(label="Grayscale", command=self.apply_grayscale)
        filter_menu.add_command(label="Gaussian Blur", command=self.apply_gaussian_blur)
        filter_menu.add_command(label="Edge Detection (Canny)", command=self.apply_canny_edge)
        menubar.add_cascade(label="Filter", menu=filter_menu)
        
        # === 4. Menu TRANSFORM ===
        transform_menu = tk.Menu(menubar, tearoff=0)
        transform_menu.add_command(label="Flip Horizontal", command=self.apply_flip_h)
        transform_menu.add_command(label="Flip Vertical", command=self.apply_flip_v)
        menubar.add_cascade(label="Transform", menu=transform_menu)

        # Pasang menubar otomatis menempel ke atas window utama
        self.configure(menu=menubar)


    def create_file_buttons(self):
        """File management buttons"""
        lbl = ctk.CTkLabel(self.sidebar, text="📁 File Management", font=("", 12, "bold"))
        lbl.pack(pady=(15, 10))

        btn_open = ctk.CTkButton(self.sidebar, text="Buka Gambar", command=self.open_image)
        btn_open.pack(pady=5, padx=20, fill="x")

        btn_save = ctk.CTkButton(self.sidebar, text="Simpan Hasil", command=self.save_image,
                                fg_color="#10b981", hover_color="#059669")
        btn_save.pack(pady=5, padx=20, fill="x")

        btn_reset = ctk.CTkButton(self.sidebar, text="Reset Original", command=self.reset_image,
                                 fg_color="#ef4444", hover_color="#b91c1c")
        btn_reset.pack(pady=5, padx=20, fill="x")

        btn_undo = ctk.CTkButton(self.sidebar, text="↶ Undo", command=self.undo)
        btn_undo.pack(pady=5, padx=20, fill="x")

        btn_redo = ctk.CTkButton(self.sidebar, text="↷ Redo", command=self.redo)
        btn_redo.pack(pady=5, padx=20, fill="x")


    def create_enhancement_section(self):
        """Image Enhancement section"""
        lbl = ctk.CTkLabel(self.sidebar, text="🌟 Enhancement", font=("", 12, "bold"))
        lbl.pack(pady=(15, 10))

        # Brightness
        ctk.CTkLabel(self.sidebar, text="Brightness:").pack(anchor="w", padx=20)
        slider_bright = ctk.CTkSlider(self.sidebar, from_=-100, to=100,
                                      command=lambda v: self.update_brightness(float(v)))
        slider_bright.set(0)
        slider_bright.pack(pady=5, padx=20, fill="x")

        # Contrast
        ctk.CTkLabel(self.sidebar, text="Contrast:").pack(anchor="w", padx=20)
        slider_contrast = ctk.CTkSlider(self.sidebar, from_=0.5, to=3.0,
                                        command=lambda v: self.update_contrast(float(v)))
        slider_contrast.set(1.0)
        slider_contrast.pack(pady=5, padx=20, fill="x")

        btn_hist_eq = ctk.CTkButton(self.sidebar, text="Histogram Equalization",
                                   command=self.apply_histogram_equalization)
        btn_hist_eq.pack(pady=5, padx=20, fill="x")

        btn_sharp = ctk.CTkButton(self.sidebar, text="Sharpening", command=self.apply_sharpen)
        btn_sharp.pack(pady=5, padx=20, fill="x")

        # Label & Slider untuk Gaussian Blur
        lbl_gaussian = ctk.CTkLabel(self.sidebar, text="Gaussian Blur Level:")
        lbl_gaussian.pack(anchor="w", padx=20, pady=(5, 0))

        slider_gaussian = ctk.CTkSlider(self.sidebar, from_=0, to=31, command=self.apply_gaussian_blur_slider)
        slider_gaussian.set(0) # Default di angka 0 (tidak nge-blur)
        slider_gaussian.pack(pady=(0, 10), padx=20, fill="x")

        btn_smoothing = ctk.CTkButton(self.sidebar, text="Smoothing (Blur)", 
                                      command=self.apply_smoothing)
        btn_smoothing.pack(pady=5, padx=20, fill="x")

        btn_bilateral = ctk.CTkButton(self.sidebar, text="Bilateral Filter",
                                     command=self.apply_bilateral_filter)
        btn_bilateral.pack(pady=5, padx=20, fill="x")


    def create_geometric_section(self):
        """Geometric Transformation section"""
        lbl = ctk.CTkLabel(self.sidebar, text="🔄 Transform", font=("", 12, "bold"))
        lbl.pack(pady=(15, 10))

        # Rotation
        ctk.CTkLabel(self.sidebar, text="Rotate (°):").pack(anchor="w", padx=20)
        slider_rotate = ctk.CTkSlider(self.sidebar, from_=0, to=360,
                                      command=lambda v: self.apply_rotation(float(v)))
        slider_rotate.set(0)
        slider_rotate.pack(pady=5, padx=20, fill="x")

        btn_flip_h = ctk.CTkButton(self.sidebar, text="Flip Horizontal",
                                  command=lambda: self.apply_flip_h())
        btn_flip_h.pack(pady=5, padx=20, fill="x")

        btn_flip_v = ctk.CTkButton(self.sidebar, text="Flip Vertical",
                                  command=lambda: self.apply_flip_v())
        btn_flip_v.pack(pady=5, padx=20, fill="x")

        # Tombol pemicu mode Interactive Crop
        self.btn_interactive_crop = ctk.CTkButton(
            self.sidebar, 
            text="Interactive Crop ✂️", 
            fg_color=["#3B8ED0", "#1F6AA5"],
            command=self.toggle_crop_mode
        )
        self.btn_interactive_crop.pack(pady=5, padx=20, fill="x")

        # Slider untuk Resize (Scale)
        ctk.CTkLabel(self.sidebar, text="Resize (Scale):").pack(anchor="w", padx=20)
        self.slider_resize = ctk.CTkSlider(self.sidebar, from_=0.1, to=3.0, 
                                           command=lambda v: self.update_resize(float(v)))
        self.slider_resize.set(1.0)
        self.slider_resize.pack(pady=5, padx=20, fill="x")

        # Translation
        ctk.CTkLabel(self.sidebar, text="Translate X:").pack(anchor="w", padx=20)
        slider_tx = ctk.CTkSlider(self.sidebar, from_=-200, to=200,
                                  command=lambda v: self.apply_translation(float(v), None))
        slider_tx.set(0)
        slider_tx.pack(pady=5, padx=20, fill="x")

        ctk.CTkLabel(self.sidebar, text="Translate Y:").pack(anchor="w", padx=20)
        slider_ty = ctk.CTkSlider(self.sidebar, from_=-200, to=200,
                                  command=lambda v: self.apply_translation(None, float(v)))
        slider_ty.set(0)
        slider_ty.pack(pady=5, padx=20, fill="x")


        # Slider untuk Transformasi Matriks Affine (Shear)
        ctk.CTkLabel(self.sidebar, text="Affine Shear X:").pack(anchor="w", padx=20)
        self.slider_shear_x = ctk.CTkSlider(self.sidebar, from_=-1.0, to=1.0, 
                                            command=lambda v: self.update_affine_shear())
        self.slider_shear_x.set(0.0)
        self.slider_shear_x.pack(pady=5, padx=20, fill="x")

        ctk.CTkLabel(self.sidebar, text="Affine Shear Y:").pack(anchor="w", padx=20)
        self.slider_shear_y = ctk.CTkSlider(self.sidebar, from_=-1.0, to=1.0, 
                                            command=lambda v: self.update_affine_shear())
        self.slider_shear_y.set(0.0)
        self.sidebar_shear_y_pack = self.slider_shear_y.pack(pady=5, padx=20, fill="x")


    def create_restoration_section(self):
        """Noise Reduction section"""
        lbl = ctk.CTkLabel(self.sidebar, text="🧹 Restoration", font=("", 12, "bold"))
        lbl.pack(pady=(15, 10))

        btn_median = ctk.CTkButton(self.sidebar, text="Median Filter", command=self.apply_median_filter)
        btn_median.pack(pady=5, padx=20, fill="x")

        btn_spatial = ctk.CTkButton(self.sidebar, text="Noise Removal", command=self.apply_salt_pepper_removal)
        btn_spatial.pack(pady=5, padx=20, fill="x")

        btn_morph_open = ctk.CTkButton(self.sidebar, text="Morph Open", command=self.apply_morph_open)
        btn_morph_open.pack(pady=5, padx=20, fill="x")

        btn_morph_close = ctk.CTkButton(self.sidebar, text="Morph Close", command=self.apply_morph_close)
        btn_morph_close.pack(pady=5, padx=20, fill="x")


    def create_edge_section(self):
        """Edge Detection section"""
        lbl = ctk.CTkLabel(self.sidebar, text="✏️ Edge Detection", font=("", 12, "bold"))
        lbl.pack(pady=(15, 10))

        btn_canny = ctk.CTkButton(self.sidebar, text="Canny", command=self.apply_canny_edge)
        btn_canny.pack(pady=5, padx=20, fill="x")

        btn_sobel = ctk.CTkButton(self.sidebar, text="Sobel", command=self.apply_sobel_edge)
        btn_sobel.pack(pady=5, padx=20, fill="x")

        btn_prewitt = ctk.CTkButton(self.sidebar, text="Prewitt", command=self.apply_prewitt_edge)
        btn_prewitt.pack(pady=5, padx=20, fill="x")

        btn_roberts = ctk.CTkButton(self.sidebar, text="Roberts", command=self.apply_roberts_edge)
        btn_roberts.pack(pady=5, padx=20, fill="x")

        btn_laplacian = ctk.CTkButton(self.sidebar, text="Laplacian", command=self.apply_laplacian_edge)
        btn_laplacian.pack(pady=5, padx=20, fill="x")

        btn_log = ctk.CTkButton(self.sidebar, text="Laplacian of Gaussian",
                               command=self.apply_log_edge)
        btn_log.pack(pady=5, padx=20, fill="x")

        # Morphology
        btn_erode = ctk.CTkButton(self.sidebar, text="Erosion", command=self.apply_erode)
        btn_erode.pack(pady=5, padx=20, fill="x")

        btn_dilate = ctk.CTkButton(self.sidebar, text="Dilation", command=self.apply_dilate)
        btn_dilate.pack(pady=5, padx=20, fill="x")

       # Thresholding (Binary Image) - Untuk Poin No. 5
        btn_threshold = ctk.CTkButton(self.sidebar, text="Threshold (Binary)", command=self.apply_simple_threshold)
        btn_threshold.pack(pady=5, padx=20, fill="x")


    def create_color_section(self):
        """Color Processing section"""
        lbl = ctk.CTkLabel(self.sidebar, text="🎨 Color", font=("", 12, "bold"))
        lbl.pack(pady=(15, 10))

        btn_gray = ctk.CTkButton(self.sidebar, text="Grayscale", command=self.apply_grayscale)
        btn_gray.pack(pady=5, padx=20, fill="x")

        # Label & Dropdown untuk Split Channels ala Photoshop
        lbl_split = ctk.CTkLabel(self.sidebar, text="Split Channels:")
        lbl_split.pack(anchor="w", padx=20, pady=(5, 0))

        self.option_split = ctk.CTkOptionMenu(
            self.sidebar, 
            values=["Original (RGB)", "Red Channel", "Green Channel", "Blue Channel"],
            command=self.apply_split_channels_dropdown
        )
        self.option_split.set("Original (RGB)")
        self.option_split.pack(pady=(0, 10), padx=20, fill="x")

        # === HSV Adjustment ===
        # Label Text
        ctk.CTkLabel(self.sidebar, text="Hue:").pack(anchor="w", padx=20)

        # 1. Generate gambar gradasi pelangi otomatis (tanpa perlu file eksternal)
        from PIL import Image
        import colorsys
        width, height = 200, 8
        img = Image.new("RGB", (width, height))
        for x in range(width):
            # Rumus matematika untuk mengubah rentang 0-1 menjadi warna RGB pelangi
            r, g, b = colorsys.hsv_to_rgb(x / width, 1.0, 1.0)
            for y in range(height):
                img.putpixel((x, y), (int(r * 255), int(g * 255), int(b * 255)))
        
        # Ubah jadi format yang bisa dibaca CustomTkinter
        hue_img = ctk.CTkImage(light_image=img, dark_image=img, size=(200, 8))
        
        # 2. Tempel gambar pelangi persis di atas slider
        ctk.CTkLabel(self.sidebar, text="", image=hue_img, height=8).pack(pady=(5, 0))

        # 3. Slider Hue Utama
        slider_hue = ctk.CTkSlider(self.sidebar, from_=-180, to=180,
                                   command=lambda v: self.apply_hsv_adjust(float(v), None, None))
        slider_hue.set(0)
        slider_hue.pack(pady=(2, 10), padx=20, fill="x")

        ctk.CTkLabel(self.sidebar, text="Saturation:").pack(anchor="w", padx=20)
        slider_sat = ctk.CTkSlider(self.sidebar, from_=0.5, to=2.0,
                                   command=lambda v: self.apply_hsv_adjust(None, float(v), None))
        slider_sat.set(1.0)
        slider_sat.pack(pady=5, padx=20, fill="x")

        ctk.CTkLabel(self.sidebar, text="Value:").pack(anchor="w", padx=20)
        slider_val = ctk.CTkSlider(self.sidebar, from_=0.5, to=2.0,
                                   command=lambda v: self.apply_hsv_adjust(None, None, float(v)))
        slider_val.set(1.0)
        slider_val.pack(pady=5, padx=20, fill="x")


    def create_segmentation_section(self):
        """Segmentation section"""
        lbl = ctk.CTkLabel(self.sidebar, text="🔍 Segmentation", font=("", 12, "bold"))
        lbl.pack(pady=(15, 10))

        btn_seg_threshold = ctk.CTkButton(self.sidebar, text="Threshold-Based Segmentation",
                                         command=self.apply_threshold_segmentation)
        btn_seg_threshold.pack(pady=5, padx=20, fill="x")

        # Label & Slider untuk K-Means
        lbl_kmeans = ctk.CTkLabel(self.sidebar, text="K-Means Clusters (k):")
        lbl_kmeans.pack(anchor="w", padx=20, pady=(5, 0))

        # from_=2 karena cluster minimal harus 2. number_of_steps=10 agar slider nge-snap ke angka bulat.
        slider_kmeans = ctk.CTkSlider(self.sidebar, from_=2, to=12, number_of_steps=10, command=self.apply_kmeans_slider)
        slider_kmeans.set(3) # Default awal di angka 3 cluster
        slider_kmeans.pack(pady=(0, 10), padx=20, fill="x")

        btn_watershed = ctk.CTkButton(self.sidebar, text="Watershed", command=self.apply_watershed)
        btn_edge_seg = ctk.CTkButton(self.sidebar, text="Edge-Based Segmentation", 
                                     command=self.edge_based_segmentation)
        btn_edge_seg.pack(pady=5, padx=20, fill="x")
        btn_watershed.pack(pady=5, padx=20, fill="x")

        btn_region = ctk.CTkButton(self.sidebar, text="Region-Based", command=self.apply_region_based)
        btn_region.pack(pady=5, padx=20, fill="x")

    def create_analysis_section(self):
        """Analysis & Compression section"""
        lbl = ctk.CTkLabel(self.sidebar, text="📊 Analysis", font=("", 12, "bold"))
        lbl.pack(pady=(15, 10))

        

        # Quality slider for compression dengan indikator angka
        self.lbl_quality = ctk.CTkLabel(self.sidebar, text="Save Quality: 100%")
        self.lbl_quality.pack(anchor="w", padx=20)

        def update_quality_label(value):
            self.lbl_quality.configure(text=f"Save Quality: {int(value)}%")

        self.slider_quality = ctk.CTkSlider(self.sidebar, from_=1, to=100, command=update_quality_label)
        self.slider_quality.set(100)
        self.slider_quality.pack(pady=5, padx=20, fill="x")

        # Tombol Simulasi Kompresi
        btn_simulasi = ctk.CTkButton(self.sidebar, text="Simulasi Kompresi JPEG", command=self.apply_compression_simulation)
        btn_simulasi.pack(pady=10, padx=20, fill="x")

        btn_face = ctk.CTkButton(self.sidebar, text="🤖 Object Detection CNN", 
                                fg_color="#8b5cf6", hover_color="#6d28d9", 
                                command=self.detect_object_cnn)
        btn_face.pack(pady=5, padx=20, fill="x")

    # ==========================================
    # --- IMAGE MANAGEMENT ---
    # ==========================================

    def open_image(self):
        """Open image file"""
        path = filedialog.askopenfilename(
            initialdir=self.current_dir,
            filetypes=[("Image Files", "*.jpg *.png *.bmp *.jpeg *.tiff"), ("All Files", "*.*")]
        )
        if path:
            self.cv_img_original = cv2.imread(path)
            if self.cv_img_original is None:
                messagebox.showerror("Error", "Cannot open image!")
                return
            
            self.current_file = path
            self.current_dir = os.path.dirname(path)
            self.cv_img_processed = self.cv_img_original.copy()
            self.image_history = [self.cv_img_processed.copy()]
            self.history_index = 0
            self.display_image_original(self.cv_img_original)
            self.display_image(self.cv_img_processed)
            self.update_status(f"Loaded: {os.path.basename(path)}")
            self.update_histograms_auto(is_new_image=True)


    def save_image(self):
        """Save image with quality control"""
        if self.cv_img_processed is None:
            messagebox.showwarning("Warning", "No image to save!")
            return

        path = filedialog.asksaveasfilename(
            initialdir=self.current_dir,
            defaultextension=".jpg",
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("BMP", "*.bmp")]
        )
        if path:
            quality = int(self.slider_quality.get())
            save_with_quality(path, self.cv_img_processed, quality)
            messagebox.showinfo("Success", f"Saved with quality {quality}!")
            self.update_status(f"Saved: {os.path.basename(path)} (Quality: {quality})")


    def reset_image(self):
        """Reset to original image"""
        if self.cv_img_original is not None:
            self.cv_img_processed = self.cv_img_original.copy()
            self.image_history = [self.cv_img_processed.copy()]
            self.history_index = 0
            self.display_image(self.cv_img_processed)
            self.update_status("Reset to original")


    def undo(self):
        """Undo last operation"""
        if self.history_index > 0:
            self.history_index -= 1
            self.cv_img_processed = self.image_history[self.history_index].copy()
            self.display_image(self.cv_img_processed)
            self.update_status(f"Undo (Step {self.history_index + 1})")


    def redo(self):
        """Redo operation"""
        if self.history_index < len(self.image_history) - 1:
            self.history_index += 1
            self.cv_img_processed = self.image_history[self.history_index].copy()
            self.display_image(self.cv_img_processed)
            self.update_status(f"Redo (Step {self.history_index + 1})")


    def push_history(self):
        """Push current state to history"""
        if len(self.image_history) > self.history_index + 1:
            self.image_history = self.image_history[:self.history_index + 1]
        self.image_history.append(self.cv_img_processed.copy())
        self.history_index += 1
        if len(self.image_history) > 20:  # Limit history
            self.image_history.pop(0)
            self.history_index -= 1


    # ==========================================
    # --- IMAGE ENHANCEMENT ---
    # ==========================================

    def update_brightness(self, value):
        """Update brightness"""
        if self.cv_img_original is None:
            return
        value = int(value)
        self.cv_img_processed = adjust_brightness_contrast(self.cv_img_original, brightness=value)
        self.display_image(self.cv_img_processed)


    def update_contrast(self, value):
        """Update contrast"""
        if self.cv_img_original is None:
            return
        value = float(value)
        self.cv_img_processed = adjust_brightness_contrast(self.cv_img_original, contrast=value)
        self.display_image(self.cv_img_processed)


    def apply_histogram_equalization(self):
        """Apply histogram equalization"""
        if self.cv_img_original is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return
        self.cv_img_processed = histogram_equalization(self.cv_img_original)
        self.push_history()
        self.display_image(self.cv_img_processed)
        self.update_status("Applied histogram equalization")


    def apply_sharpen(self):
        """Apply sharpening"""
        if self.cv_img_original is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return
        self.cv_img_processed = sharpen_image(self.cv_img_original)
        self.push_history()
        self.display_image(self.cv_img_processed)
        self.update_status("Applied sharpening")


    def apply_gaussian_blur(self):
        """Apply Gaussian blur"""
        if self.cv_img_original is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return
        kernel = simpledialog.askinteger("Gaussian Blur", "Kernel size (odd number):", initialvalue=5)
        if kernel:
            self.cv_img_processed = gaussian_blur(self.cv_img_original, kernel)
            self.push_history()
            self.display_image(self.cv_img_processed)
            self.update_status("Applied Gaussian blur")

    def apply_gaussian_blur_slider(self, value):
        """Fungsi real-time Gaussian Blur via Slider"""
        if self.cv_img_original is None: 
            return

        # Trik Gaib: Ubah value slider menjadi bilangan INT ganjil (Syarat mutlak OpenCV)
        val = int(value)
        k_size = val if val % 2 != 0 else val + 1

        if k_size <= 1:
            # Jika slider ditarik mentok ke kiri (0 atau 1), kembalikan ke gambar tajam asli
            self.cv_img_processed = self.cv_img_original.copy()
            self.update_status("Gaussian Blur dinonaktifkan")
        else:
            import cv2
            self.cv_img_processed = cv2.GaussianBlur(self.cv_img_original, (k_size, k_size), 0)
            self.update_status(f"Applied Gaussian Blur (Kernel: {k_size}x{k_size})")

        # Lempar ke layar, dan biarkan "fungsi hantu" histogram yang kita buat tadi bekerja otomatis!
        self.display_image(self.cv_img_processed)

    def apply_bilateral_filter(self):
        """Apply bilateral filter"""
        if self.cv_img_original is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return
        self.cv_img_processed = bilateral_filter(self.cv_img_original)
        self.push_history()
        self.display_image(self.cv_img_processed)
        self.update_status("Applied bilateral filter")


    # ==========================================
    # --- GEOMETRIC TRANSFORMATIONS ---
    # ==========================================

    def apply_rotation(self, angle):
        """Apply rotation"""
        if self.cv_img_original is None:
            return
        self.cv_img_processed = rotate_image(self.cv_img_original, angle)
        self.display_image(self.cv_img_processed)

    def update_resize(self, scale):
        """Mengubah ukuran gambar menggunakan slider secara realtime"""
        if self.cv_img_original is None:
            return

        # Ambil dimensi asli gambar
        height, width = self.cv_img_original.shape[:2]
        
        # Hitung ukuran baru berdasarkan nilai scale dari slider
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        # Eksekusi resize menggunakan OpenCV
        self.cv_img_processed = cv2.resize(self.cv_img_original, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
        
        # Tampilkan ke layar
        self.display_image(self.cv_img_processed)
        self.update_status(f"Resize Scale: {scale:.2f}x")

    def update_affine_shear(self):
        """Menerapkan transformasi matriks affine (Shearing) secara realtime"""
        if self.cv_img_original is None:
            return

        # 1. Ambil nilai pergeseran sudut dari kedua slider
        shear_x = float(self.slider_shear_x.get())
        shear_y = float(self.slider_shear_y.get())

        # 2. Ambil dimensi lebar dan tinggi gambar asli
        rows, cols = self.cv_img_original.shape[:2]

        # 3. Susun Matriks Affine 2x3 (M) menggunakan NumPy
        # [ 1      shear_x  0 ]
        # [ shear_y   1     0 ]
        M = np.float32([
            [1, shear_x, 0],
            [shear_y, 1, 0]
        ])

        # 4. Transformasikan gambar menggunakan matriks M tersebut
        self.cv_img_processed = cv2.warpAffine(self.cv_img_original, M, (cols, rows))

        # 5. Tampilkan hasilnya ke canvas GUI
        self.display_image(self.cv_img_processed)
        self.update_status(f"Affine Matrix Applied -> Shear X: {shear_x:.2f}, Shear Y: {shear_y:.2f}")

    def apply_flip_h(self):
        """Flip horizontal"""
        if self.cv_img_processed is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return
        self.cv_img_processed = flip_image(self.cv_img_processed, 'horizontal')
        self.push_history()
        self.display_image(self.cv_img_processed)
        self.update_status("Flipped horizontally")


    def apply_flip_v(self):
        """Flip vertical"""
        if self.cv_img_processed is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return
        self.cv_img_processed = flip_image(self.cv_img_processed, 'vertical')
        self.push_history()
        self.display_image(self.cv_img_processed)
        self.update_status("Flipped vertically")


    def start_crop_mode(self):
        """Enable crop mode"""
        if self.cv_img_original is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return
        self.crop_mode = True
        self.update_status("Crop mode enabled - Click and drag to select area")


    def apply_crop(self, x1, y1, x2, y2):
        """Apply crop"""
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        
        if x1 >= x2 or y1 >= y2:
            messagebox.showwarning("Warning", "Invalid crop area!")
            return
        
        self.cv_img_processed = crop_image(self.cv_img_processed, x1, y1, x2, y2)
        self.push_history()
        self.display_image(self.cv_img_processed)
        self.update_status("Applied crop")
        self.crop_mode = False


    


    def apply_translation(self, tx, ty):
        """Apply translation"""
        if self.cv_img_original is None:
            return
        
        # Store last values
        if not hasattr(self, '_last_tx'):
            self._last_tx = 0
            self._last_ty = 0
        
        if tx is None:
            tx = self._last_tx
        if ty is None:
            ty = self._last_ty
        
        self._last_tx = tx
        self._last_ty = ty
        
        self.cv_img_processed = translate_image(self.cv_img_original, int(tx), int(ty))
        self.display_image(self.cv_img_processed)


    # ==========================================
    # --- RESTORATION & NOISE ---
    # ==========================================

    def apply_median_filter(self):
        """Apply median filter"""
        if self.cv_img_processed is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return
        self.cv_img_processed = median_blur(self.cv_img_processed)
        self.push_history()
        self.display_image(self.cv_img_processed)
        self.update_status("Applied median filter")

    def apply_salt_pepper_removal(self):
        """Menyamarkan Salt & Pepper noise menggunakan teknik Kernel Convolution (Spatial Filtering)"""
        if self.cv_img_original is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return

        self.update_status("Applying Kernel Convolution...")
        self.update()

        # TEKNIS: 1. Membuat custom Kernel 3x3 untuk Spatial Filtering (Average/Mean Filter)
        # Matriks kernel diisi angka 1, lalu dibagi 9.0 agar kecerahan gambar tidak berubah
        kernel_convolution = np.ones((3, 3), np.float32) / 9.0

        # TEKNIS: 2. Menerapkan konvolusi kernel ke gambar menggunakan cv2.filter2D
        self.cv_img_processed = cv2.filter2D(self.cv_img_processed, -1, kernel_convolution)

        self.push_history()
        self.display_image(self.cv_img_processed)
        self.update_status("Kernel Convolution berhasil diaplikasikan!")

    def apply_morph_open(self):
        """Apply morphological opening"""
        if self.cv_img_processed is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return
        self.cv_img_processed = morphological_denoise(self.cv_img_processed, operation='open')
        self.push_history()
        self.display_image(self.cv_img_processed)
        self.update_status("Applied morphological opening")


    def apply_morph_close(self):
        """Apply morphological closing"""
        if self.cv_img_processed is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return
        self.cv_img_processed = morphological_denoise(self.cv_img_processed, operation='close')
        self.push_history()
        self.display_image(self.cv_img_processed)
        self.update_status("Applied morphological closing")


    # ==========================================
    # --- EDGE DETECTION ---
    # ==========================================

    def apply_canny_edge(self):
        """Apply Canny edge detection"""
        if self.cv_img_original is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return
        self.cv_img_processed = canny_edge(self.cv_img_original)
        self.push_history()
        self.display_image(self.cv_img_processed)
        self.update_status("Applied Canny edge detection")


    def apply_sobel_edge(self):
        """Apply Sobel edge detection"""
        if self.cv_img_original is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return
        self.cv_img_processed = sobel_edge(self.cv_img_original)
        self.push_history()
        self.display_image(self.cv_img_processed)
        self.update_status("Applied Sobel edge detection")


    def apply_prewitt_edge(self):
        """Apply Prewitt edge detection"""
        if self.cv_img_original is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return
        self.cv_img_processed = prewitt_edge(self.cv_img_original)
        self.push_history()
        self.display_image(self.cv_img_processed)
        self.update_status("Applied Prewitt edge detection")


    def apply_roberts_edge(self):
        """Apply Roberts edge detection"""
        if self.cv_img_original is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return
        self.cv_img_processed = roberts_edge(self.cv_img_original)
        self.push_history()
        self.display_image(self.cv_img_processed)
        self.update_status("Applied Roberts edge detection")


    def apply_laplacian_edge(self):
        """Apply Laplacian edge detection"""
        if self.cv_img_original is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return
        self.cv_img_processed = laplacian_edge(self.cv_img_original)
        self.push_history()
        self.display_image(self.cv_img_processed)
        self.update_status("Applied Laplacian edge detection")


    def apply_log_edge(self):
        """Apply Laplacian of Gaussian"""
        if self.cv_img_original is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return
        self.cv_img_processed = laplacian_of_gaussian(self.cv_img_original)
        self.push_history()
        self.display_image(self.cv_img_processed)
        self.update_status("Applied Laplacian of Gaussian")


    def apply_erode(self):
        """Apply erosion"""
        if self.cv_img_processed is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return
        self.cv_img_processed = erode_image(self.cv_img_processed)
        self.push_history()
        self.display_image(self.cv_img_processed)
        self.update_status("Applied erosion")


    def apply_dilate(self):
        """Apply dilation"""
        if self.cv_img_processed is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return
        self.cv_img_processed = dilate_image(self.cv_img_processed)
        self.push_history()
        self.display_image(self.cv_img_processed)
        self.update_status("Applied dilation")

    def apply_simple_threshold(self):
        """Mengeksekusi fitur Thresholding menjadi gambar Biner (Hitam-Putih)"""
        if self.cv_img_original is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return

        self.update_status("Applying Threshold...")
        self.update()

        # 1. Thresholding WAJIB menggunakan gambar Grayscale
        if len(self.cv_img_processed.shape) == 3:
            gray_img = cv2.cvtColor(self.cv_img_processed, cv2.COLOR_BGR2GRAY)
        else:
            gray_img = self.cv_img_processed

        # 2. Eksekusi Thresholding (Otsu Otomatis agar hasil selalu tajam)
        _, result_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # 3. Simpan dan tampilkan hasilnya ke layar
        self.cv_img_processed = result_img
        self.push_history()
        self.display_image(self.cv_img_processed)
        self.update_status("Thresholding berhasil diaplikasikan!")

    


    # ==========================================
    # --- COLOR PROCESSING ---
    # ==========================================

    def apply_grayscale(self):
        """Convert to grayscale"""
        if self.cv_img_original is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return
        self.cv_img_processed = to_grayscale(self.cv_img_original)
        self.push_history()
        self.display_image(self.cv_img_processed)
        self.update_status("Converted to grayscale")

    def apply_split_channels(self):
        """Membagi channel R, G, B dan menampilkannya dengan label di luar (bawah) gambar"""
        if self.cv_img_original is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return

        self.update_status("Splitting Channels (R | G | B)...")
        self.update()

        # 1. Ambil copy dari gambar yang sedang diproses
        img = self.cv_img_processed.copy()
        
        # 2. Cek apakah gambar punya 3 channel (Warna), kalau iya kita pisah
        if len(img.shape) == 3:
            b, g, r = cv2.split(img)
        else:
            # Kalau gambar udah grayscale, nilainya disamakan semua
            b = g = r = img

        # 3. Ubah ke 3-channel grayscale agar aman saat digabung
        r_3ch = cv2.merge([r, r, r])
        g_3ch = cv2.merge([g, g, g])
        b_3ch = cv2.merge([b, b, b])

        # 4. Buat area hitam (kanvas) di bawah masing-masing gambar khusus untuk teks
        h, w = r.shape[:2]
        bar_height = 100  # Tinggi kotak hitam di bawah gambar
        
        import numpy as np # Jaga-jaga panggil numpy
        # Bikin kotak hitam pekat seukuran lebar gambar
        bar_r = np.zeros((bar_height, w, 3), dtype=np.uint8)
        bar_g = np.zeros((bar_height, w, 3), dtype=np.uint8)
        bar_b = np.zeros((bar_height, w, 3), dtype=np.uint8)

        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 1.5
        thickness = 3
        color = (255, 255, 255) # Teks warna putih
        
        # Kalkulasi otomatis agar teks pas berada di tengah kotak hitam
        x_r = (w - cv2.getTextSize("Red Channel", font, scale, thickness)[0][0]) // 2
        x_g = (w - cv2.getTextSize("Green Channel", font, scale, thickness)[0][0]) // 2
        x_b = (w - cv2.getTextSize("Blue Channel", font, scale, thickness)[0][0]) // 2
        
        # Lukis teks ke dalam kotak hitam (bukan ke gambar aslinya)
        cv2.putText(bar_r, "Red Channel", (x_r, 55), font, scale, color, thickness, cv2.LINE_AA)
        cv2.putText(bar_g, "Green Channel", (x_g, 55), font, scale, color, thickness, cv2.LINE_AA)
        cv2.putText(bar_b, "Blue Channel", (x_b, 55), font, scale, color, thickness, cv2.LINE_AA)

        # Sambungkan gambar utama dengan kotak hitam di bawahnya secara vertikal (Atas-Bawah)
        r_final = cv2.vconcat([r_3ch, bar_r])
        g_final = cv2.vconcat([g_3ch, bar_g])
        b_final = cv2.vconcat([b_3ch, bar_b])

        # 5. Gabungkan ketiga channel secara horizontal (Kiri-Kanan)
        result_img = cv2.hconcat([r_final, g_final, b_final])

        # 6. Tampilkan langsung ke layar utama
        self.cv_img_processed = result_img
        self.push_history()
        self.display_image(self.cv_img_processed)
        self.update_status("Channel R | G | B dengan label berhasil ditampilkan!")
    
    def apply_split_channels_dropdown(self, choice):
        """Fungsi ala Photoshop untuk split channel tanpa bikin gambar gepeng"""
        if self.cv_img_original is None:
            self.option_split.set("Original (RGB)")
            return

        import cv2

        if choice == "Original (RGB)":
            # Kembalikan ke gambar processed terakhir atau salinan original
            self.cv_img_processed = self.cv_img_original.copy()
            self.update_status("Kembali ke tampilan RGB Original")
        
        elif choice == "Red Channel":
            # OpenCV membaca format BGR (Index 0: Blue, 1: Green, 2: Red)
            b, g, r = cv2.split(self.cv_img_original)
            self.cv_img_processed = r
            self.update_status("Menampilkan Red Channel (Grayscale)")
            
        elif choice == "Green Channel":
            b, g, r = cv2.split(self.cv_img_original)
            self.cv_img_processed = g
            self.update_status("Menampilkan Green Channel (Grayscale)")
            
        elif choice == "Blue Channel":
            b, g, r = cv2.split(self.cv_img_original)
            self.cv_img_processed = b
            self.update_status("Menampilkan Blue Channel (Grayscale)")

        # Lempar hasil ke kanvas kanan & update histogram secara otomatis!
        self.display_image(self.cv_img_processed)

    def apply_region_based(self):
        """Region-based sederhana menggunakan teknik Masking & Region Extraction"""
        if self.cv_img_original is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return

        self.update_status("Applying Region-based Segmentation...")
        self.update()

        # 1. Ambil copy dari gambar yang sedang diproses
        img = self.cv_img_processed.copy()

        # 2. Konversi ke Grayscale untuk memudahkan pembuatan Mask
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img.copy()

        # 3. Bikin Thresholding (Otsu) untuk memisahkan objek dan background sementara
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # 4. Cari area/region objek (Contours)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # Cari region dengan area paling besar (asumsi: itu adalah objek utamanya)
            c = max(contours, key=cv2.contourArea)

            # Bikin kanvas hitam kosong (Ini yang disebut Masking)
            mask = np.zeros_like(gray)

            # Warnai region objek utama di kanvas masking menjadi putih (255)
            cv2.drawContours(mask, [c], -1, 255, thickness=cv2.FILLED)

            # 5. Extract Region! (Tempelkan mask ke gambar asli pakai Bitwise AND)
            if len(img.shape) == 3:
                # Kalau gambar asli berwarna, mask-nya harus di-copy jadi 3 channel
                mask_3ch = cv2.merge([mask, mask, mask])
                result_img = cv2.bitwise_and(img, mask_3ch)
            else:
                result_img = cv2.bitwise_and(img, mask)
        else:
            # Kalau kebetulan gambarnya nggak punya region jelas, balikan ke threshold
            result_img = thresh

        # 6. Tampilkan hasilnya langsung ke layar utama
        self.cv_img_processed = result_img
        self.push_history()
        self.display_image(self.cv_img_processed)
        self.update_status("Region-based (Masking & Extraction) berhasil diaplikasikan!")

    def apply_compression_simulation(self):
        """Simulasi Kompresi JPEG langsung ke layar utama tanpa pop-up"""
        if self.cv_img_original is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return

        self.update_status("Menjalankan Simulasi Kompresi JPEG...")
        self.update()

        img = self.cv_img_processed.copy()
        quality = int(self.slider_quality.get())

        # 1. Proses Kompresi (Kuantisasi, RLE, dan Huffman berjalan di sini)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        result, encimg = cv2.imencode('.jpg', img, encode_param)
        
        # 2. Decode untuk langsung diupdate ke layar utama (efek pecah/burik langsung kelihatan)
        decimg = cv2.imdecode(encimg, 1)
        self.cv_img_processed = decimg
        self.display_image(self.cv_img_processed)

        # 3. Hitung ukuran hasil kompresi
        comp_size_kb = len(encimg) / 1024
        
        # 4. Tampilkan info ukuran hanya di status bar bawah aplikasimu
        self.update_status(f"Simulasi JPEG Selesai! Kualitas: {quality}% | Ukuran: {comp_size_kb:.2f} KB")

    def apply_hsv_adjust(self, hue, sat, val):
        """Apply HSV adjustment"""
        if self.cv_img_original is None:
            return

        if not hasattr(self, '_hsv_h'):
            self._hsv_h = 0
            self._hsv_s = 1.0
            self._hsv_v = 1.0

        if hue is not None:
            self._hsv_h = int(hue)
        if sat is not None:
            self._hsv_s = sat
        if val is not None:
            self._hsv_v = val

        self.cv_img_processed = adjust_hsv(self.cv_img_original, self._hsv_h, self._hsv_s, self._hsv_v)
        self.display_image(self.cv_img_processed)


    # ==========================================
    # --- SEGMENTATION ---
    # ==========================================

    def apply_threshold_segmentation(self):
        """Apply threshold-based segmentation"""
        if self.cv_img_original is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return
        self.cv_img_processed = threshold_segmentation(self.cv_img_original, 127)
        self.push_history()
        self.display_image(self.cv_img_processed)
        self.update_status("Applied threshold segmentation")


    def apply_kmeans_segmentation(self):
        """Apply K-means segmentation"""
        if self.cv_img_original is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return

        k = simpledialog.askinteger("K-means", "Number of clusters:", initialvalue=3, minvalue=2, maxvalue=10)
        if k:
            self.cv_img_processed = kmeans_segmentation(self.cv_img_original, k)
            self.push_history()
            self.display_image(self.cv_img_processed)
            self.update_status(f"Applied K-means with {k} clusters")

    def apply_kmeans_slider(self, value):
        """Fungsi real-time K-Means Clustering via Slider"""
        if self.cv_img_original is None:
            return

        import cv2
        import numpy as np

        # Slider CustomTkinter mengembalikan nilai float, kita wajib paksa jadi integer
        k = int(value)

        # Ubah format gambar menjadi array 2D yang bisa dihitung oleh K-Means
        img_data = self.cv_img_original.reshape((-1, 3))
        img_data = np.float32(img_data)

        # Kriteria berhenti (maksimal 10 iterasi biar aplikasimu nggak lag saat slider digeser)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        
        # Eksekusi algoritma K-Means (pakai RANDOM_CENTERS agar prosesnya lebih cepat)
        ret, label, center = cv2.kmeans(img_data, k, None, criteria, 1, cv2.KMEANS_RANDOM_CENTERS)

        # Kembalikan array menjadi format gambar kembali
        center = np.uint8(center)
        res = center[label.flatten()]
        self.cv_img_processed = res.reshape((self.cv_img_original.shape))

        self.update_status(f"Applied K-Means Clustering (k={k})")
        
        # Lempar ke layar, dan biarkan "fungsi hantu" histogram yang kita buat tadi bekerja otomatis!
        self.display_image(self.cv_img_processed)

    def apply_watershed(self):
        """Apply watershed segmentation"""
        if self.cv_img_original is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return
        self.cv_img_processed = watershed_segmentation(self.cv_img_original)
        self.push_history()
        self.display_image(self.cv_img_processed)
        self.update_status("Applied watershed segmentation")


    # ==========================================
    # --- ANALYSIS & VISUALIZATION ---
    # ==========================================

    def update_histograms_auto(self, is_new_image=False):
        """Fungsi background untuk update histogram secara real-time"""
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        import cv2

        def draw(image, frame, title):
            if image is None: return
            
            # Bersihkan frame
            for widget in frame.winfo_children():
                widget.destroy()
            
            fig = Figure(figsize=(5, 2), dpi=80)
            fig.patch.set_facecolor('#1e1e1e') 
            ax = fig.add_subplot(111)
            ax.set_facecolor('#1e1e1e')
            ax.tick_params(colors='gray', labelsize=8)
            
            ax.set_title(title, color='#3498db', fontsize=10, fontweight='bold')
            ax.spines['bottom'].set_color('gray')
            ax.spines['left'].set_color('gray')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

            if len(image.shape) == 2:
                hist = cv2.calcHist([image], [0], None, [256], [0, 256])
                ax.plot(hist, color='white', linewidth=1.5)
                ax.fill_between(range(256), hist.flatten(), color='white', alpha=0.3)
            else:
                colors = ('b', 'g', 'r')
                plot_colors = {'b': 'blue', 'g': 'green', 'r': 'red'}
                for i, col in enumerate(colors):
                    hist = cv2.calcHist([image], [i], None, [256], [0, 256])
                    ax.plot(hist, color=plot_colors[col], linewidth=1.2)

            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        # 1. Jika ini saat BUKA GAMBAR BARU (Update Kiri & Kanan sama)
        if is_new_image:
            if self.cv_img_original is None: return
            draw(self.cv_img_original, self.hist_frame_original, "BEFORE HISTOGRAM")
            draw(self.cv_img_original, self.hist_frame_processed, "AFTER HISTOGRAM")
            
        # 2. Jika lagi nge-klik FILTER (Update Kanan aja secara real-time)
        else:
            if self.cv_img_processed is not None:
                draw(self.cv_img_processed, self.hist_frame_processed, "AFTER HISTOGRAM")


    def detect_object_cnn(self):
        """Object detection using CNN (cvlib/YOLO) - FILTERED"""
        if self.cv_img_original is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return

        self.update_status("Processing AI CNN... Mohon tunggu sebentar.")
        self.update() 

        # Pakai yolov3-tiny untuk memancing download file baru yang bersih dari error
        bbox, label, conf = cv.detect_common_objects(self.cv_img_original, model='yolov3-tiny')
        
        # FILTERING: Tentukan target spesifik sesuai spesifikasi proyek!
        # Saat ini disetel ke 'person' (Manusia). Bisa diganti misal 'car', 'cat', dll.
        target_objek = ['person'] 
        
        filtered_bbox = []
        filtered_label = []
        filtered_conf = []
        
        # Proses penyaringan agar AI hanya fokus ke target spesifik
        for i, lbl in enumerate(label):
            if lbl in target_objek:
                filtered_bbox.append(bbox[i])
                filtered_label.append(lbl)
                filtered_conf.append(conf[i])
        
        # Menggambar kotak HANYA untuk objek yang lolos filter
        img_copy = draw_bbox(self.cv_img_original.copy(), filtered_bbox, filtered_label, filtered_conf)

        self.cv_img_processed = img_copy
        self.push_history()
        self.display_image(self.cv_img_processed)
        self.update_status(f"CNN berhasil mendeteksi {len(filtered_label)} target utama!")


    # ==========================================
    # --- DISPLAY & UI ---
    # ==========================================

    def display_image(self, img):
        """Display image on canvas"""
        if img is None:
            return

        # Convert to RGB for display
        if len(img.shape) == 3:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        else:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

        img_pil = Image.fromarray(img_rgb)

        # Fit to canvas
        canvas_width, canvas_height = 1080, 600
        img_pil.thumbnail((canvas_width, canvas_height), Image.Resampling.LANCZOS)

        img_tk = ImageTk.PhotoImage(img_pil)

        self.canvas.configure(image=img_tk, text="")
        self.canvas.image = img_tk
        
        # Store for crop mode
        self._display_img = img_pil

        self.update_histograms_auto(is_new_image=False)

        # Pasang sensor mouse untuk fitur Interactive Crop di kanvas kanan (hasil edit)
        self.canvas.bind("<ButtonPress-1>", self.on_crop_start)
        self.canvas.bind("<B1-Motion>", self.on_crop_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_crop_end)

    def display_image_original(self, img):
        """Display original image on left canvas"""
        if img is None: return
        if len(img.shape) == 3:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        else:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

        img_pil = Image.fromarray(img_rgb)
        canvas_width, canvas_height = 540, 600 # Ukuran layarnya dibagi dua
        img_pil.thumbnail((canvas_width, canvas_height), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img_pil)

        self.canvas_original.configure(image=img_tk, text="")
        self.canvas_original.image = img_tk

    def update_status(self, message):
        """Update status bar"""
        self.status_label.configure(text=message)


    def on_canvas_click(self, event):
        """Handle canvas click for crop mode"""
        if not self.crop_mode:
            return
        self.crop_start = (event.x, event.y)


    def on_canvas_drag(self, event):
        """Handle canvas drag"""
        if not self.crop_mode or self.crop_start is None:
            return


    def on_canvas_release(self, event):
        """Handle canvas release for crop"""
        if not self.crop_mode or self.crop_start is None:
            return
        
        self.crop_end = (event.x, event.y)
        x1, y1 = self.crop_start
        x2, y2 = self.crop_end
        
        if x1 != x2 and y1 != y2:
            self.apply_crop(x1, y1, x2, y2)
        
        self.crop_start = None
        self.crop_end = None


    # ==========================================
    # --- MENU FUNCTIONS ---
    # ==========================================

    def show_file_menu(self):
        """Show file menu (placeholder)"""
        messagebox.showinfo("File Menu", "Use the sidebar buttons for file operations")


    def show_edit_menu(self):
        """Show edit menu"""
        messagebox.showinfo("Edit Menu", "Undo/Redo available in sidebar")


    def show_filter_menu(self):
        """Show filter menu"""
        messagebox.showinfo("Filter Menu", "Check Enhancement, Restoration, and Color sections")


    def show_transform_menu(self):
        """Show transform menu"""
        messagebox.showinfo("Transform Menu", "Check the Transform section in sidebar")


    def show_analysis_menu(self):
        """Show analysis menu"""
        messagebox.showinfo("Analysis Menu", "Check the Analysis section in sidebar")

    def edge_based_segmentation(self):
        """Segmentasi memisahkan objek dari background berbasis deteksi tepi (Edge-based)"""
        if self.cv_img_original is None:
            messagebox.showwarning("Warning", "Silakan buka gambar terlebih dahulu!")
            return

        self.update_status("Processing Edge-based Segmentation...")
        self.update()

        # 1. Ubah ke Grayscale dan beri Blur agar noise hilang
        gray = cv2.cvtColor(self.cv_img_original, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # 2. Deteksi tepi menggunakan Canny
        edges = cv2.Canny(blurred, 50, 150)

        # 3. Operasi Morfologi (Closing) untuk menyambungkan garis tepi yang terputus
        import numpy as np
        kernel = np.ones((5, 5), np.uint8)
        closed_edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

        # 4. Mencari kontur (bentuk objek) dari garis tepi yang sudah tertutup
        contours, _ = cv2.findContours(closed_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 5. Membuat kanvas hitam murni (masking)
        mask = np.zeros_like(gray)
        
        # 6. Menggambar kontur yang ditemukan menjadi warna putih pekat (mengisi ruang objek)
        cv2.drawContours(mask, contours, -1, (255), thickness=cv2.FILLED)

        # 7. Memotong (menggabungkan) gambar asli dengan kanvas masking
        # Hasilnya: Objek utama tetap berwarna, background jadi hitam
        segmented_img = cv2.bitwise_and(self.cv_img_original, self.cv_img_original, mask=mask)

        # 8. Tampilkan ke layar
        self.cv_img_processed = segmented_img
        self.push_history()
        self.display_image(self.cv_img_processed)
        self.update_status("Edge-based Segmentation berhasil diaplikasikan!")

    def apply_smoothing(self):
        """Menerapkan filter rata-rata (Average Smoothing/Blur) pada gambar"""
        if self.cv_img_original is None:
            messagebox.showwarning("Warning", "Silakan buka gambar terlebih dahulu!")
            return

        self.update_status("Processing Smoothing (Blur)...")
        self.update()

        # Menggunakan algoritma Average Blur standar dari OpenCV dengan kernel 5x5
        smoothed_img = cv2.blur(self.cv_img_processed, (5, 5))

        self.cv_img_processed = smoothed_img
        self.push_history()
        self.display_image(self.cv_img_processed)
        self.update_status("Smoothing (Blur) berhasil diaplikasikan!")

    def toggle_crop_mode(self):
        """Pemicu mode pemotongan interaktif"""
        if self.cv_img_processed is None: 
            self.update_status("Error: Buka gambar terlebih dahulu!")
            return
            
        self.mode_crop_aktif = not self.mode_crop_aktif
        
        if self.mode_crop_aktif:
            self.update_status("Crop Mode AKTIF: Klik dan seret di kanvas KANAN untuk memotong")
            self.btn_interactive_crop.configure(fg_color="orange") 
            self._clear_crop_ui()
        else:
            self.update_status("Crop Mode NONAKTIF")
            self.btn_interactive_crop.configure(fg_color=["#3B8ED0", "#1F6AA5"]) 
            self._clear_crop_ui()

    def _clear_crop_ui(self):
        """Trik hacker: Membersihkan UI kotak crop di atas Label"""
        if hasattr(self, 'crop_lines'):
            for line in self.crop_lines: line.destroy()
        if hasattr(self, 'crop_handles'):
            for h in self.crop_handles: h.destroy()
        self.crop_lines = []
        self.crop_handles = []

    # --- Mouse Event Handlers ---
    def on_crop_start(self, event):
        if not self.mode_crop_aktif: return
        self.start_x = event.x
        self.start_y = event.y
        
        self._clear_crop_ui()
        
        # Buat 4 garis solid putih dinamis
        self.crop_lines = [
            ctk.CTkFrame(self.canvas, fg_color="white", height=2, corner_radius=0), # Atas
            ctk.CTkFrame(self.canvas, fg_color="white", height=2, corner_radius=0), # Bawah
            ctk.CTkFrame(self.canvas, fg_color="white", width=2, corner_radius=0),  # Kiri
            ctk.CTkFrame(self.canvas, fg_color="white", width=2, corner_radius=0)   # Kanan
        ]
        # Buat 4 pegangan sudut biru aesthetic ala Photoshop
        self.crop_handles = [
            ctk.CTkFrame(self.canvas, fg_color="#3B8ED0", width=8, height=8, corner_radius=0) for _ in range(4)
        ]

    def on_crop_drag(self, event):
        if not self.mode_crop_aktif: return
        cur_x = max(0, min(self.canvas.winfo_width(), event.x))
        cur_y = max(0, min(self.canvas.winfo_height(), event.y))
        
        x1, x2 = min(self.start_x, cur_x), max(self.start_x, cur_x)
        y1, y2 = min(self.start_y, cur_y), max(self.start_y, cur_y)
        
        w, h = x2 - x1, y2 - y1

        if w > 0 and h > 0 and hasattr(self, 'crop_lines'):
            # Posisikan garis
            self.crop_lines[0].place(x=x1, y=y1, width=w, height=2)
            self.crop_lines[1].place(x=x1, y=y2, width=w, height=2)
            self.crop_lines[2].place(x=x1, y=y1, width=2, height=h)
            self.crop_lines[3].place(x=x2, y=y1, width=2, height=h)

            # Posisikan pegangan sudut
            self.crop_handles[0].place(x=x1-4, y=y1-4)
            self.crop_handles[1].place(x=x2-4, y=y1-4)
            self.crop_handles[2].place(x=x1-4, y=y2-4)
            self.crop_handles[3].place(x=x2-4, y=y2-4)

    def on_crop_end(self, event):
        if not self.mode_crop_aktif: return
        end_x, end_y = (event.x, event.y)
        
        cx1, cy1 = min(self.start_x, end_x), min(self.start_y, end_y)
        cx2, cy2 = max(self.start_x, end_x), max(self.start_y, end_y)
        
        if abs(cx1 - cx2) < 10 or abs(cy1 - cy2) < 10:
            self.update_status("Interactive Crop dibatalkan (kotak terlalu kecil)")
            self.toggle_crop_mode() 
            return

        self.current_crop_rect = [cx1, cy1, cx2, cy2]
        self.update_status("Merender pemotongan...")
        self._execute_opencv_crop()

    def _execute_opencv_crop(self):
        import cv2
        from PIL import Image as PILImage
        
        cx1, cy1, cx2, cy2 = self.current_crop_rect
        current_img = self.cv_img_processed 
        
        orig_pil = PILImage.fromarray(cv2.cvtColor(current_img, cv2.COLOR_BGR2RGB))
        orig_w, orig_h = orig_pil.size
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()

        ratio = min(canvas_w / orig_w, canvas_h / orig_h)
        displayed_w = int(orig_w * ratio)
        displayed_h = int(orig_h * ratio)

        offset_x = (canvas_w - displayed_w) / 2
        offset_y = (canvas_h - displayed_h) / 2

        px1 = max(0, min(orig_w, int((cx1 - offset_x) / ratio)))
        py1 = max(0, min(orig_h, int((cy1 - offset_y) / ratio)))
        px2 = max(0, min(orig_w, int((cx2 - offset_x) / ratio)))
        py2 = max(0, min(orig_h, int((cy2 - offset_y) / ratio)))

        fx1, fx2 = min(px1, px2), max(px1, px2)
        fy1, fy2 = min(py1, py2), max(py1, py2)

        self.cv_img_processed = current_img[fy1:fy2, fx1:fx2].copy()
        
        if hasattr(self, 'push_history'):
            self.push_history()
            
        self.display_image(self.cv_img_processed)
        self.toggle_crop_mode()
        self.update_status(f"Interactive Crop berhasil: {fx2-fx1}x{fy2-fy1} piksel")

if __name__ == "__main__":
    app = MiniPhotoshop()
    app.mainloop()

    