from ultralytics import YOLO
import easyocr
import cv2
import re

reader = easyocr.Reader(['en'])
model = YOLO("license_plate_detector.pt")

def is_kz_plate(text):
    patterns = [
        r'^[0-9]{1,3}[A-Z]{3}[0-9]{2}$',       # 744AAA07
        r'^KZ[0-9]{1,3}[A-Z]{3}[0-9]{2}$',     # KZ016KXA16
        r'^[0-9]{1,3}[A-Z]{3}$',               # 314BGI (без региона)
    ]
    return any(re.fullmatch(p, text) for p in patterns)

def detect_and_read_plate(image_path):
    image = cv2.imread(image_path)
    results = model(image_path)[0]

    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        plate_img = image[y1:y2, x1:x2]

        if plate_img.size == 0:
            continue

        try:
            ocr_results = reader.readtext(plate_img)
            if ocr_results:
                parts = []
                for result in ocr_results:
                    text = result[1]
                    cleaned = re.sub(r'[^A-Z0-9]', '', text.upper())
                    if 2 <= len(cleaned) <= 8:
                        parts.append(cleaned)

                combined = ''.join(parts)

                if is_kz_plate(combined):
                    return combined

                matches = re.findall(r'KZ?[0-9]{1,3}[A-Z]{3}[0-9]{2}', combined)
                if matches:
                    return matches[0]

                fallback = re.findall(r'[0-9]{1,3}[A-Z]{3}[0-9]{0,2}', combined)
                if fallback:
                    return fallback[0]

        except Exception as e:
            print("OCR error:", e)
            return "Ошибка OCR"

    return "Номер не найден"
