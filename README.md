# Using OCR to find 2024 in pictures

Problem: How can I iterate through .jpg files to find all images that are from 2024?

Task: Using a temporary file, temp_ocr.jpb, use Tesseract OCR to convert image_to_string and check if 2024 is in the file. If 2024 is found in the image, use "shutil" to copy the file to the destination folder.

Results: Did not accurartely identify 2024 in the majority of the photos (4/98 files were accurately identified from the sample size). 

Recommendations for future use: upgrade or change the pre-processing methods and/or use another OCR. Perhaps, utilize a GPT model using an API key.
