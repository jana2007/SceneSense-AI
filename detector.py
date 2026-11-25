
from ultralytics import YOLO
import cv2


class SceneDetector:

    def __init__(self):
        print("Loading YOLO model...")

        self.model = YOLO("yolov8n.pt")

        print("SceneSense object detector is ready!")

    def detect_objects(self, image):

        results = self.model(image)

        detected_objects = []

        for result in results:

            for box in result.boxes:

                class_id = int(box.cls[0])
                confidence = float(box.conf[0])

                object_name = self.model.names[class_id]

                detected_objects.append({
                    "name": object_name,
                    "confidence": round(confidence * 100, 2)
                })

        return results[0].plot(), detected_objects


if __name__ == "__main__":

    detector = SceneDetector()

    image = cv2.imread("test.jpg")

    if image is None:
        print("Please place an image named test.jpg in the project folder.")

    else:
        output_image, objects = detector.detect_objects(image)

        print("\nDetected Objects:")

        for obj in objects:
            print(f"{obj['name']} - {obj['confidence']}%")

        cv2.imshow("SceneSense - Object Detection", output_image)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
