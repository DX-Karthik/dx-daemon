import base64
from PIL import Image, UnidentifiedImageError
import io

def main(image_base64: str):
    try:
        # Decode the base64 encoded image
        image_data = base64.b64decode(image_base64)

        # Convert the binary data to an image
        image = Image.open(io.BytesIO(image_data))

        # Compress the image
    
        # The "optimize" flag can be used to reduce the file size without losing any quality.
        with io.BytesIO() as output:
            image.save(
                output, format="PNG", optimize=True
            )  # Using optimize flag for PNG compression
            compressed_data = output.getvalue()

        # Encode the compressed image to base64
        compressed_base64 = base64.b64encode(compressed_data).decode("utf-8")

        # Return the base64 encoded compressed image
        return {
                    "file": {
                        "content": compressed_base64,
                        "filename": "compressed_image.png",
                    }
                }

    except UnidentifiedImageError:
        # Handle the case where the image cannot be identified
        return "Error: The provided data does not represent a valid image."