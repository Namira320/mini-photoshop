"""
Image processing filters dan algorithms untuk SnapFilter Pro
"""
import cv2
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


# ============================================
# 1. IMAGE ENHANCEMENT
# ============================================

def adjust_brightness_contrast(img, brightness=0, contrast=1.0):
    """Adjust brightness and contrast using linear transformation"""
    return np.clip(cv2.convertScaleAbs(img, alpha=contrast, beta=brightness), 0, 255).astype(np.uint8)


def histogram_equalization(img):
    """Apply histogram equalization (CLAHE for color images)"""
    if len(img.shape) == 3:
        # Convert to LAB for better result
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        lab = cv2.merge([l, a, b])
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    else:
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        return clahe.apply(img)


def sharpen_image(img, kernel_size=3):
    """Sharpen image using kernel-based convolution"""
    if kernel_size == 3:
        kernel = np.array([[-1, -1, -1],
                          [-1, 9, -1],
                          [-1, -1, -1]]) / 2.0
    elif kernel_size == 5:
        kernel = np.array([[-1, -1, -1, -1, -1],
                          [-1, 9, 9, -1, -1],
                          [-1, 9, 17, 9, -1],
                          [-1, -1, 9, -1, -1],
                          [-1, -1, -1, -1, -1]]) / 8.0
    else:
        kernel = np.array([[-1, -1, -1],
                          [-1, 9, -1],
                          [-1, -1, -1]]) / 2.0
    
    return cv2.filter2D(img, -1, kernel)


def gaussian_blur(img, kernel_size=5):
    """Apply Gaussian blur for smoothing"""
    kernel_size = max(3, kernel_size if kernel_size % 2 == 1 else kernel_size + 1)
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)


def bilateral_filter(img, diameter=9, sigma_color=75, sigma_space=75):
    """Bilateral filtering for edge-preserving blur"""
    return cv2.bilateralFilter(img, diameter, sigma_color, sigma_space)


# ============================================
# 2. GEOMETRIC TRANSFORMATIONS
# ============================================

def rotate_image(img, angle):
    """Rotate image with angle in degrees (0-360)"""
    angle = angle % 360
    h, w = img.shape[:2]
    center = (w / 2, h / 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    # Calculate new dimensions
    cos = np.abs(rotation_matrix[0, 0])
    sin = np.abs(rotation_matrix[0, 1])
    new_w = int((h * sin) + (w * cos))
    new_h = int((h * cos) + (w * sin))
    
    rotation_matrix[0, 2] += (new_w / 2) - center[0]
    rotation_matrix[1, 2] += (new_h / 2) - center[1]
    
    return cv2.warpAffine(img, rotation_matrix, (new_w, new_h), 
                         borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))


def flip_image(img, direction='horizontal'):
    """Flip image horizontally or vertically"""
    if direction == 'horizontal':
        return cv2.flip(img, 1)  # 1 = horizontal
    elif direction == 'vertical':
        return cv2.flip(img, 0)  # 0 = vertical
    elif direction == 'both':
        return cv2.flip(img, -1)  # -1 = both
    return img


def resize_image(img, width=None, height=None, scale=None, interpolation='linear'):
    """Resize image with width/height or scale factor"""
    h, w = img.shape[:2]
    
    if scale:
        new_w = int(w * scale)
        new_h = int(h * scale)
    elif width and height:
        new_w, new_h = width, height
    elif width:
        ratio = width / w
        new_h = int(h * ratio)
        new_w = width
    elif height:
        ratio = height / h
        new_w = int(w * ratio)
        new_h = height
    else:
        return img
    
    inter_method = cv2.INTER_LINEAR if interpolation == 'linear' else cv2.INTER_NEAREST
    return cv2.resize(img, (new_w, new_h), interpolation=inter_method)


def translate_image(img, tx, ty):
    """Translate image by offset (tx, ty)"""
    h, w = img.shape[:2]
    translation_matrix = np.float32([[1, 0, tx], [0, 1, ty]])
    return cv2.warpAffine(img, translation_matrix, (w, h))


def crop_image(img, x1, y1, x2, y2):
    """Crop image using coordinates"""
    return img[y1:y2, x1:x2]


def perspective_transform(img, src_points, dst_points):
    """Apply perspective transformation using 4 corner points"""
    h, w = img.shape[:2]
    matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    return cv2.warpPerspective(img, matrix, (w, h))


# ============================================
# 3. NOISE REDUCTION & RESTORATION
# ============================================

def median_blur(img, kernel_size=5):
    """Median blur for salt & pepper noise removal"""
    kernel_size = max(3, kernel_size if kernel_size % 2 == 1 else kernel_size + 1)
    return cv2.medianBlur(img, kernel_size)


def morphological_denoise(img, kernel_size=5, operation='open'):
    """Morphological operations for denoising"""
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
    
    if operation == 'open':  # Erosion then dilation
        return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    elif operation == 'close':  # Dilation then erosion
        return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    elif operation == 'gradient':
        return cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)
    else:
        return img


def erode_image(img, kernel_size=5):
    """Erosion operation"""
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
    return cv2.erode(img, kernel, iterations=1)


def dilate_image(img, kernel_size=5):
    """Dilation operation"""
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
    return cv2.dilate(img, kernel, iterations=1)


# ============================================
# 4. EDGE DETECTION
# ============================================

def canny_edge(img, threshold1=100, threshold2=200):
    """Canny edge detection"""
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    return cv2.Canny(gray, threshold1, threshold2)


def sobel_edge(img, direction='both'):
    """Sobel edge detection (X, Y, or both)"""
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    
    if direction == 'x':
        magnitude = np.abs(sobelx)
    elif direction == 'y':
        magnitude = np.abs(sobely)
    else:  # both
        magnitude = np.sqrt(sobelx**2 + sobely**2)
    
    return np.uint8(magnitude)


def prewitt_edge(img):
    """Prewitt edge detection"""
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    
    kernelx = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.float32)
    kernely = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]], dtype=np.float32)
    
    prewitt_x = cv2.filter2D(gray, cv2.CV_64F, kernelx)
    prewitt_y = cv2.filter2D(gray, cv2.CV_64F, kernely)
    
    magnitude = np.sqrt(prewitt_x**2 + prewitt_y**2)
    return np.uint8(magnitude)


def roberts_edge(img):
    """Roberts edge detection"""
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    
    kernelx = np.array([[1, 0], [0, -1]], dtype=np.float32)
    kernely = np.array([[0, 1], [-1, 0]], dtype=np.float32)
    
    roberts_x = cv2.filter2D(gray, cv2.CV_64F, kernelx)
    roberts_y = cv2.filter2D(gray, cv2.CV_64F, kernely)
    
    magnitude = np.sqrt(roberts_x**2 + roberts_y**2)
    return np.uint8(magnitude)


def laplacian_edge(img):
    """Laplacian edge detection"""
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    return np.uint8(np.absolute(laplacian))


def laplacian_of_gaussian(img, sigma=1.0):
    """Laplacian of Gaussian (LoG) edge detection"""
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    
    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (5, 5), sigma)
    # Apply Laplacian
    log = cv2.Laplacian(blurred, cv2.CV_64F)
    return np.uint8(np.absolute(log))


# ============================================
# 5. THRESHOLDING & BINARY
# ============================================

def threshold_binary(img, threshold=127, method='simple'):
    """Binary thresholding"""
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    
    if method == 'simple':
        _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    elif method == 'otsu':
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    elif method == 'adaptive':
        binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY, 11, 2)
    else:
        _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    
    return binary


# ============================================
# 6. COLOR PROCESSING
# ============================================

def to_grayscale(img):
    """Convert to grayscale"""
    if len(img.shape) == 3:
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img


def split_channels(img):
    """Split BGR channels"""
    if len(img.shape) == 3:
        b, g, r = cv2.split(img)
        return {'B': b, 'G': g, 'R': r}
    return {'Gray': img}


def merge_channels(channels_dict):
    """Merge BGR channels back"""
    if 'B' in channels_dict and 'G' in channels_dict and 'R' in channels_dict:
        return cv2.merge([channels_dict['B'], channels_dict['G'], channels_dict['R']])
    return channels_dict.get('Gray', None)


def adjust_hsv(img, hue=0, saturation=1.0, value=1.0):
    """Adjust Hue, Saturation, Value"""
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
    
    hsv[:, :, 0] = (hsv[:, :, 0] + hue) % 180
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * saturation, 0, 255)
    hsv[:, :, 2] = np.clip(hsv[:, :, 2] * value, 0, 255)
    
    return cv2.cvtColor(np.uint8(hsv), cv2.COLOR_HSV2BGR)


# ============================================
# 7. IMAGE SEGMENTATION
# ============================================

def threshold_segmentation(img, threshold=127):
    """Threshold-based segmentation"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    _, seg = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    return seg


def kmeans_segmentation(img, k=3):
    """K-means clustering for segmentation"""
    data = img.reshape(-1, img.shape[-1] if len(img.shape) == 3 else 1)
    data = np.float32(data)
    
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    centers = np.uint8(centers)
    result = centers[labels.flatten()]
    return result.reshape(img.shape)


def watershed_segmentation(img):
    """Watershed-based segmentation"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=2)
    
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
    
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    
    _, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0
    
    markers = cv2.watershed(img, markers)
    result = img.copy()
    result[markers == -1] = [0, 0, 255]
    
    return result


# ============================================
# 8. HISTOGRAM & ANALYSIS
# ============================================

def calculate_histogram(img, channels=None):
    """Calculate histogram for image channels"""
    if len(img.shape) == 3:
        if channels is None:
            channels = ['B', 'G', 'R']
        histograms = {}
        for i, ch in enumerate(channels):
            hist = cv2.calcHist([img], [i], None, [256], [0, 256])
            histograms[ch] = hist.flatten()
        return histograms
    else:
        hist = cv2.calcHist([img], [0], None, [256], [0, 256])
        return {'Gray': hist.flatten()}


def plot_histogram(img, title="Histogram"):
    """Plot histogram using matplotlib"""
    if len(img.shape) == 3:
        colors = ('B', 'G', 'R')
        for i, color in enumerate(colors):
            hist = cv2.calcHist([img], [i], None, [256], [0, 256])
            plt.plot(hist, color=color.lower(), label=color)
    else:
        hist = cv2.calcHist([img], [0], None, [256], [0, 256])
        plt.plot(hist, color='gray')
    
    plt.title(title)
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid()


# ============================================
# 9. COMPRESSION & QUALITY
# ============================================

def save_with_quality(filename, img, quality=95):
    """Save image with specific quality level (0-100)"""
    quality = max(1, min(100, quality))
    if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
        cv2.imwrite(filename, img, [cv2.IMWRITE_JPEG_QUALITY, quality])
    elif filename.lower().endswith('.png'):
        cv2.imwrite(filename, img, [cv2.IMWRITE_PNG_COMPRESSION, (100 - quality) // 10])
    else:
        cv2.imwrite(filename, img)


def rle_compression(img_flat):
    """Simple RLE (Run-Length Encoding) compression simulation"""
    compressed = []
    if len(img_flat) == 0:
        return compressed
    
    current_val = img_flat[0]
    count = 1
    
    for i in range(1, len(img_flat)):
        if img_flat[i] == current_val and count < 255:
            count += 1
        else:
            compressed.append((current_val, count))
            current_val = img_flat[i]
            count = 1
    
    compressed.append((current_val, count))
    return compressed


def get_image_stats(img):
    """Get image statistics"""
    stats = {
        'shape': img.shape,
        'dtype': str(img.dtype),
        'min': img.min(),
        'max': img.max(),
        'mean': img.mean(),
        'std': img.std()
    }
    return stats
