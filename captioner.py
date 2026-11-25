
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration


class SceneCaptioner:

    def __init__(self):

        print("Loading image captioning model...")

        self.processor = BlipProcessor.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )

        self.model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )

        print("Scene description model is ready!")

    def generate_caption(self, image):

        inputs = self.processor(
            images=image,
            return_tensors="pt"
        )

        with torch.no_grad():

            output = self.model.generate(
                **inputs,
                max_new_tokens=60
            )

        caption = self.processor.decode(
            output[0],
            skip_special_tokens=True
        )

        return caption


if __name__ == "__main__":

    from PIL import Image

    captioner = SceneCaptioner()

    image = Image.open("test.jpg").convert("RGB")

    description = captioner.generate_caption(image)

    print("\nScene Description:")
    print(description)
