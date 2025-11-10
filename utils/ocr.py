# ocr_utils.py
# This file handles Optical Character Recognition (OCR) to extract text from images
# It processes exam question images and converts them to readable text for analysis

# Import necessary libraries for image processing and OCR
import cv2  # OpenCV for image processing and manipulation
import numpy as np  # NumPy for numerical operations on image arrays
import easyocr  # EasyOCR library for text recognition from images
from PIL import Image  # Python Imaging Library for image format conversions
from typing import List  # Type hints for better code documentation

# Global variable to store the OCR reader instance
# We initialize it once to avoid reloading the model multiple times (which is slow)
_reader = None

def init_reader(lang_list=["en"], gpu: bool = True):
    """
    Initializes the EasyOCR reader with specified languages and GPU settings.
    
    This function creates an OCR reader instance that can recognize text in the
    specified languages. The reader is cached globally to avoid reloading the
    model on every OCR operation, which would be very slow.
    
    Args:
        lang_list (list): List of language codes for text recognition (default: ["en"])
        gpu (bool): Whether to use GPU acceleration if available (default: True)
    
    Returns:
        easyocr.Reader: Initialized OCR reader instance
    """
    global _reader
    # Only initialize the reader if it hasn't been created yet
    # This prevents reloading the model multiple times
    if _reader is None:
        # Create the EasyOCR reader with specified languages and GPU setting
        # First initialization is slow as it downloads and loads the model
        _reader = easyocr.Reader(lang_list, gpu=gpu)
    return _reader

def preprocess_image(path: str, resize_width: int = 1600) -> np.ndarray:
    """
    Preprocesses an image to improve OCR accuracy.
    
    This function applies various image processing techniques to enhance text
    readability for the OCR engine. It handles resizing, grayscale conversion,
    dark background detection, noise reduction, and adaptive thresholding.
    
    Args:
        path (str): File path to the input image
        resize_width (int): Target width for image resizing (default: 1600)
    
    Returns:
        np.ndarray: Preprocessed image as a NumPy array ready for OCR
    
    Raises:
        FileNotFoundError: If the image file cannot be found or loaded
    """
    # Load the image from the specified path
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Image not found: {path}")
    
    # Get image dimensions (height, width)
    h, w = img.shape[:2]
    
    # Resize image if it's smaller than the target width
    # This helps improve OCR accuracy on small images
    if w < resize_width:
        scale = resize_width / w  # Calculate scaling factor
        # Resize image maintaining aspect ratio
        img = cv2.resize(img, (int(w*scale), int(h*scale)), interpolation=cv2.INTER_LINEAR)
    
    # Convert image to grayscale for better text processing
    # Grayscale images are easier for OCR engines to process
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Detect if the image has dark background with light text
    # Calculate average brightness of the image
    mean_intensity = np.mean(gray)
    if mean_intensity < 100:  # If image is dark (dark background)
        # Invert colors: dark background becomes light, light text becomes dark
        # This helps OCR engines that expect dark text on light background
        gray = cv2.bitwise_not(gray)
    
    # Save intermediate result for debugging purposes
    cv2.imwrite("outputs/preprocessed-gray.jpg", gray)
    
    # Apply bilateral filter to reduce noise while preserving edges
    # This smooths the image while keeping text edges sharp
    # Parameters: image, diameter, sigmaColor, sigmaSpace
    blur = cv2.bilateralFilter(gray, 9, 15, 15)
    
    # Save blurred result for debugging
    cv2.imwrite("outputs/preprocessed-blur.jpg", blur)
    
    # Apply adaptive thresholding to create binary image (black and white)
    # This converts grayscale to pure black text on white background
    # Adaptive thresholding works better than fixed threshold for varying lighting
    th = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY, 15, 8)
    
    # Save final preprocessed image for debugging
    cv2.imwrite("outputs/preprocessed.jpg", th)
    
    # Return the preprocessed binary image
    return th

def image_to_text(path: str, lang_list=["en"], gpu: bool = True) -> str:
    """
    Extracts text from an image using OCR (Optical Character Recognition).
    
    This function takes an image file, preprocesses it to improve text recognition,
    and then uses EasyOCR to extract all readable text from the image. It's
    specifically designed to handle exam question images.
    
    Args:
        path (str): File path to the image containing text to extract
        lang_list (list): List of language codes for text recognition (default: ["en"])
        gpu (bool): Whether to use GPU acceleration if available (default: True)
    
    Returns:
        str: Extracted text from the image, with multiple text blocks joined by newlines
    """
    # Initialize or get the cached OCR reader
    reader = init_reader(lang_list=lang_list, gpu=gpu)
    
    # Preprocess the image to improve OCR accuracy
    # This applies filtering, thresholding, and other enhancements
    prep = preprocess_image(path)
    
    # Convert the preprocessed NumPy array to PIL Image format
    # EasyOCR can work with various formats, but PIL ensures compatibility
    pil = Image.fromarray(prep)
    
    # Perform OCR on the preprocessed image
    # detail=0 returns only text (no bounding boxes or confidence scores)
    # paragraph=True groups text into logical paragraphs
    results = reader.readtext(np.array(pil), detail=0, paragraph=True)
    
    # Join all extracted text pieces into a single string
    # Filter out empty strings and strip whitespace from each piece
    # Each text block is separated by a newline character
    text = "\n".join([r.strip() for r in results if r.strip()])
    
    # Return the complete extracted text
    return text