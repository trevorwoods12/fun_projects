import os
import shutil
import pytesseract
import cv2
from PIL import Image
import numpy as np
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

SOURCE_FOLDER = "C:\\Users\\...\..."
DEST_FOLDER = "C:\\Users\\...\..."
os.makedirs(DEST_FOLDER, exist_ok=True)

def preprocess_image(image_path):
    # Read image
    img = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Resize if image is small
    if gray.shape[1] < 1000:
        scale = 2
        gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)

    # Gaussian blur to remove noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Adaptive thresholding
    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )

    # Deskew the image
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = thresh.shape
    M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
    deskewed = cv2.warpAffine(thresh, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    # Morphological cleaning (dilate then erode)
    kernel = np.ones((1, 1), np.uint8)
    cleaned = cv2.dilate(deskewed, kernel, iterations=1)
    cleaned = cv2.erode(cleaned, kernel, iterations=1)

    return cleaned

# Process and copy images containing "2024"
for filename in os.listdir(SOURCE_FOLDER):
    if filename.lower().endswith(('.jpg', '.jpeg')):
        file_path = os.path.join(SOURCE_FOLDER, filename)
        try:
            preprocessed_img = preprocess_image(file_path)

            # Save to temporary file for OCR
            temp_path = "temp_ocr.jpg"
            cv2.imwrite(temp_path, preprocessed_img)

            # Run OCR
            text = pytesseract.image_to_string(Image.open(temp_path))

            if "2024" in text:
                print(f"Found 2024 in: {filename}")
                shutil.copy(file_path, os.path.join(DEST_FOLDER, filename))
            else:
                print(f"No 2024 in: {filename}")
        except Exception as e:
            print(f"Error with {filename}: {e}")
