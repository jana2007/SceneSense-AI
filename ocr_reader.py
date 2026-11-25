
import easyocr


class SceneOCR:

    def __init__(self):
        print("Loading OCR model...")

        self.reader = easyocr.Reader(['en'], gpu=False)

        print("SceneSense OCR is ready!")

    def extract_text(self, image):

        results = self.reader.readtext(image)

        extracted_text = []

        for result in results:

            text = result[1]
            confidence = round(result[2] * 100, 2)

            extracted_text.append({
                "text": text,
                "confidence": confidence
            })

        return extracted_text


if __name__ == "__main__":

    import cv2

    image = cv2.imread("test.jpg")

    if image is None:
        print("Please place an image named test.jpg in the project folder.")

    else:
        ocr = SceneOCR()

        results = ocr.extract_text(image)

        print("\nExtracted Text:")

        for item in results:
            print(f"{item['text']} - {item['confidence']}% confidence")
