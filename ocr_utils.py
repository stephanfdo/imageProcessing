# ocr_utils.py
import cv2
import numpy as np
import pytesseract
import re
import csv
from skimage.filters import threshold_local

def four_point_transform(image, pts):
    """Applies a four-point perspective transform to an image."""
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped

def order_points(pts):
    """Orders points in a consistent way for perspective transforms."""
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect


#text extraction 
def text_extraction(warped):
    
    # Extract text using OCR
    config = r'--oem 3 -l eng --psm 6'
    text = pytesseract.image_to_string(warped, config=config)
    print("Extracted Text:", text)

    # Clean and extract data from text
    extracted_data = clean_and_extract_data(text)

    output_csv="extracted_data.csv"

    # Write extracted data to CSV
    if extracted_data:
        write_to_csv(extracted_data, output_csv)
        print(f"Data written to {output_csv}")
    else:
        print("No data extracted.")
    
    
    

def clean_and_extract_data(text):
    """
    Cleans the OCR-extracted text and extracts relevant data.
    Returns a list of dictionaries with keys 'Item', 'Qty', 'Total', 'Category'.
    """
    lines = text.splitlines()
    extracted_data = []

    for line in lines:
        # Use regex to find lines with item details (Item, Qty, Total)
        match = re.match(r'(.+?)\s+(\d+)\s+([\d.]+)', line)
        if match:
            item = match.group(1).strip()
            qty = int(match.group(2).strip())
            total = float(match.group(3).strip())
            
            extracted_data.append({
                'Item': item,
                'Qty': qty,
                'Total': total
                
            })
    return extracted_data

def write_to_csv(extracted_data, output_csv):
    """
    Writes the extracted data to a CSV file.
    """
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Item', 'Qty', 'Total', 'Category'])
        writer.writeheader()
        for data in extracted_data:
            writer.writerow(data)
