import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np

# Set tampilan ke Dark Mode 
ctk.set_appearance_mode("dark")

class MiniPhotoshop(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SnapFilter Pro - PCD 2026")
        self.geometry("1100x650")

        # Variabel penyimpan memori gambar
        self.cv_img_original = None   # Master copy (Tidak boleh berubah)
        self.cv_img_processed = None  # Copy yang sudah diedit untuk ditampilkan

        # --- PENGATURAN LAYOUT UTAMA ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # === PANEL SIDEBAR (KIRI) ===
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Judul Aplikasi
        self.label = ctk.CTkLabel(self.sidebar, text="SnapFilter Pro", font=("Urbanist", 24, "bold"), text_color="#3b82f6")
        self.label.pack(pady=20)

        # 1. Tombol Buka & Simpan
        self.btn_open = ctk.CTkButton(self.sidebar, text="📂 Buka Gambar", command=self.open_image)
        self.btn_open.pack(pady=10, padx=20)

        self.btn_save = ctk.CTkButton(self.sidebar, text="💾 Simpan Hasil", command=self.save_image, fg_color="#10b981", hover_color="#059669")
        self.btn_save.pack(pady=10, padx=20)

        self.btn_reset = ctk.CTkButton(self.sidebar, text="🔄 Reset Original", command=self.reset_image, fg_color="#ef4444", hover_color="#b91c1c")
        self.btn_reset.pack(pady=10, padx=20)

        # Label Pemisah
        #self.lbl_filters = ctk.CTkLabel(self.sidebar, text="--- Filter Wajib ---", text_color="gray")
        #self.lbl_filters.pack(pady=10)

        # 2. Tombol Efek & Geometri
        self.btn_gray = ctk.CTkButton(self.sidebar, text="⚫ Grayscale", command=self.apply_grayscale)
        self.btn_gray.pack(pady=5, padx=20)

        self.btn_blur = ctk.CTkButton(self.sidebar, text="💧 Blur (Median)", command=self.apply_blur)
        self.btn_blur.pack(pady=5, padx=20)

        self.btn_edge = ctk.CTkButton(self.sidebar, text="✏️ Sketsa (Canny)", command=self.apply_edge)
        self.btn_edge.pack(pady=5, padx=20)

        self.btn_rotate = ctk.CTkButton(self.sidebar, text="🔁 Putar 90°", command=self.apply_rotate)
        self.btn_rotate.pack(pady=5, padx=20)

        # 3. Slider Kecerahan
        self.lbl_bright = ctk.CTkLabel(self.sidebar, text="Kecerahan (Brightness):")
        self.lbl_bright.pack(pady=(15, 0))
        self.slider_bright = ctk.CTkSlider(self.sidebar, from_=-100, to=100, command=self.update_brightness)
        self.slider_bright.set(0) # Posisi slider di tengah
        self.slider_bright.pack(pady=5, padx=20)

        # Label Pemisah Bonus
        #self.lbl_ai = ctk.CTkLabel(self.sidebar, text="--- Fitur Nilai Tambah ---", text_color="gray")
        #self.lbl_ai.pack(pady=10)

        # 4. Tombol AI
        self.btn_face = ctk.CTkButton(self.sidebar, text="🤖 Deteksi Wajah AI", command=self.detect_face, fg_color="#8b5cf6", hover_color="#6d28d9")
        self.btn_face.pack(pady=5, padx=20)

        # === PANEL CANVAS (KANAN) ===
        import tkinter as tk
        self.canvas = tk.Canvas(self, bg="#020617", highlightthickness=0)
        self.canvas.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")


    # ==========================================
    # --- KUMPULAN FUNGSI (LOGIKA PROGRAM) ---
    # ==========================================

    def open_image(self):
        # Membuka jendela dialog untuk memilih file
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.bmp *.jpeg")])
        if path:
            self.cv_img_original = cv2.imread(path)
            self.cv_img_processed = self.cv_img_original.copy()
            self.slider_bright.set(0)
            self.display_image(self.cv_img_processed)

    def save_image(self):
        if self.cv_img_processed is None:
            messagebox.showwarning("Peringatan", "Tidak ada gambar yang bisa disimpan!")
            return
            
        path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")])
        if path:
            cv2.imwrite(path, self.cv_img_processed)
            messagebox.showinfo("Sukses", "Gambar berhasil disimpan!")

    def reset_image(self):
        if self.cv_img_original is not None:
            self.cv_img_processed = self.cv_img_original.copy()
            self.slider_bright.set(0)
            self.display_image(self.cv_img_processed)

    def apply_grayscale(self):
        if self.cv_img_original is not None:
            self.cv_img_processed = cv2.cvtColor(self.cv_img_original, cv2.COLOR_BGR2GRAY)
            self.display_image(self.cv_img_processed)

    def apply_blur(self):
        if self.cv_img_original is not None:
            # Median blur untuk menghilangkan noise / bintik
            self.cv_img_processed = cv2.medianBlur(self.cv_img_original, 9)
            self.display_image(self.cv_img_processed)

    def apply_edge(self):
        if self.cv_img_original is not None:
            # Canny edge detection
            self.cv_img_processed = cv2.Canny(self.cv_img_original, 100, 200)
            self.display_image(self.cv_img_processed)

    def apply_rotate(self):
        if self.cv_img_original is not None:
            self.cv_img_processed = cv2.rotate(self.cv_img_original, cv2.ROTATE_90_CLOCKWISE)
            # Update master copy agar jika ditekan lagi, dia berputar terus
            self.cv_img_original = self.cv_img_processed.copy()
            self.display_image(self.cv_img_processed)

    def update_brightness(self, value):
        if self.cv_img_original is not None:
            # Mengatur kecerahan menggunakan convertScaleAbs
            val = int(value)
            self.cv_img_processed = cv2.convertScaleAbs(self.cv_img_original, alpha=1, beta=val)
            self.display_image(self.cv_img_processed)

    def detect_face(self):
        if self.cv_img_original is not None:
            # Menggunakan pre-trained model bawaan OpenCV (Haar Cascades)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(self.cv_img_original, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            
            img_copy = self.cv_img_original.copy()
            # Menggambar kotak hijau di area wajah yang terdeteksi
            for (x, y, w, h) in faces:
                cv2.rectangle(img_copy, (x, y), (x+w, y+h), (0, 255, 0), 3)
            
            self.cv_img_processed = img_copy
            self.display_image(self.cv_img_processed)

    def display_image(self, img):
        # Mencegah error jika gambar kosong
        if img is None:
            return

        # OpenCV menggunakan format warna BGR, sedangkan layar komputer butuh RGB
        # Kita cek apakah gambarnya berwarna (3 channel) atau hitam putih/biner (2 dimensi)
        if len(img.shape) == 3:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        else:
            img_rgb = img # Kalau grayscale/canny, biarkan saja

        # Konversi array OpenCV menjadi gambar yang bisa ditampilkan di antarmuka (Tkinter)
        img_pil = Image.fromarray(img_rgb)
        
        # Hitung ukuran agar pas di tengah layar tanpa merusak rasio (aspect ratio)
        canvas_width, canvas_height = 800, 600
        img_pil.thumbnail((canvas_width, canvas_height))

        from PIL import ImageTk # Jaga-jaga buat mastiin library-nya kepanggil
        
        # Konversi ke format yang bisa dibaca Canvas murni
        img_tk = ImageTk.PhotoImage(img_pil)
        
        # Bersihkan sisa gambar lama
        self.canvas.delete("all")
        
        # Tempel gambar tepat di tengah kanvas (400, 300 adalah titik tengah dari 800x600)
        self.canvas.create_image(400, 300, anchor="center", image=img_tk)
        
        # Wajib ada biar gambarnya nggak hilang dimakan "Garbage Collector" Python!
        self.canvas.image = img_tk

    def toggle_crop_mode(self):
        if self.cv_img_processed is None: return
        self.mode_crop_aktif = not self.mode_crop_aktif
        
        if self.mode_crop_aktif:
            self.update_status("Crop Mode AKTIF: Klik dan seret di kanvas untuk memotong")
            self.btn_interactive_crop.configure(fg_color="orange") 
            if hasattr(self, 'crop_rect_id') and self.crop_rect_id: self.canvas.delete(self.crop_rect_id)
        else:
            self.update_status("Crop Mode NONAKTIF")
            self.btn_interactive_crop.configure(fg_color=["#3B8ED0", "#1F6AA5"]) 
            if hasattr(self, 'crop_rect_id') and self.crop_rect_id: self.canvas.delete(self.crop_rect_id)

    def on_crop_start(self, event):
        if not hasattr(self, 'mode_crop_aktif') or not self.mode_crop_aktif: return
        self.start_x = event.x
        self.start_y = event.y
        if hasattr(self, 'crop_rect_id') and self.crop_rect_id: self.canvas.delete(self.crop_rect_id)
        
        self.crop_rect_id = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline="white", dash=(8, 8), width=2
        )

    def on_crop_drag(self, event):
        if not hasattr(self, 'mode_crop_aktif') or not self.mode_crop_aktif: return
        cur_x = max(0, min(self.canvas.winfo_width(), event.x))
        cur_y = max(0, min(self.canvas.winfo_height(), event.y))
        if hasattr(self, 'crop_rect_id'):
            self.canvas.coords(self.crop_rect_id, self.start_x, self.start_y, cur_x, cur_y)

    def on_crop_end(self, event):
        if not hasattr(self, 'mode_crop_aktif') or not self.mode_crop_aktif: return
        end_x, end_y = (event.x, event.y)
        cx1, cy1 = min(self.start_x, end_x), min(self.start_y, end_y)
        cx2, cy2 = max(self.start_x, end_x), max(self.start_y, end_y)
        
        if abs(cx1 - cx2) < 10 or abs(cy1 - cy2) < 10:
            if hasattr(self, 'crop_rect_id') and self.crop_rect_id: self.canvas.delete(self.crop_rect_id)
            self.toggle_crop_mode() 
            return
        self.current_crop_rect = [cx1, cy1, cx2, cy2]
        self._execute_opencv_crop()

    def _execute_opencv_crop(self):
        import cv2
        from PIL import Image as PILImage
        cx1, cy1, cx2, cy2 = self.current_crop_rect
        current_img = self.cv_img_processed
        orig_pil = PILImage.fromarray(cv2.cvtColor(current_img, cv2.COLOR_BGR2RGB))
        orig_w, orig_h = orig_pil.size
        canvas_w, canvas_h = self.canvas.winfo_width(), self.canvas.winfo_height()
        ratio = min(canvas_w / orig_w, canvas_h / orig_h)
        
        # Hitung offset tengah kanvas
        displayed_w, displayed_h = int(orig_w * ratio), int(orig_h * ratio)
        offset_x, offset_y = (canvas_w - displayed_w) / 2, (canvas_h - displayed_h) / 2

        px1 = max(0, min(orig_w, int((cx1 - offset_x) / ratio)))
        py1 = max(0, min(orig_h, int((cy1 - offset_y) / ratio)))
        px2 = max(0, min(orig_w, int((cx2 - offset_x) / ratio)))
        py2 = max(0, min(orig_h, int((cy2 - offset_y) / ratio)))

        self.cv_img_processed = current_img[min(py1, py2):max(py1, py2), min(px1, px2):max(px1, px2)].copy()
        if hasattr(self, 'push_history'): self.push_history()
        self.display_image(self.cv_img_processed)
        if hasattr(self, 'crop_rect_id') and self.crop_rect_id: self.canvas.delete(self.crop_rect_id)
        self.toggle_crop_mode()

if __name__ == "__main__":
    app = MiniPhotoshop()
    app.mainloop()