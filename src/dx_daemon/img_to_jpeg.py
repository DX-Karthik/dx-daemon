import base64
import io
from pathlib import Path

from PIL import Image, UnidentifiedImageError


# Define the main function with the specified parameter types
def main(image_base64: str):
    try:
        # Decode the base64 encoded image
        image_data = base64.b64decode(image_base64)

        # Convert the binary data to an image
        image = Image.open(io.BytesIO(image_data))

        # Convert the image to JPEG format
        # Note: We use BytesIO to handle the conversion in memory
        with io.BytesIO() as output:
            image.convert("RGB").save(output, format="JPEG")
            jpeg_data = output.getvalue()

        # Encode the JPEG image to base64
        jpeg_base64 = base64.b64encode(jpeg_data).decode("utf-8")

        # Return the base64 encoded JPEG image

        return { "render_all": [ { "file": { "content": jpeg_base64, "filename": "image.jpg" } }, { "jpeg": jpeg_base64 } ]}

    except UnidentifiedImageError:
        # Handle the case where the image cannot be identified
        return "Error: The provided data does not represent a valid image."


def convert_local_file_to_jpeg(source_path: str) -> str:
    """
    Convert a local image file to JPEG and save it to ~/Downloads.

    Supports PNG explicitly, plus other Pillow-readable image formats.
    Returns the output path for the converted file.
    """
    input_path = Path(source_path).expanduser().resolve()
    if not input_path.exists() or not input_path.is_file():
        raise FileNotFoundError(f"Could not find file: {input_path}")

    downloads_dir = Path.home() / "Downloads"
    downloads_dir.mkdir(parents=True, exist_ok=True)
    output_path = downloads_dir / f"{input_path.stem}.jpg"

    with Image.open(input_path) as image:
        image.convert("RGB").save(output_path, format="JPEG")

    return str(output_path)


def prompt_and_convert_local_file() -> None:
    """
    Prompt the user for a local file path, then convert and save to Downloads.
    """
    print("Enter the local image path to convert (PNG supported):")
    source_path = input("> ").strip()
    if not source_path:
        print("No file path provided.")
        return

    try:
        output_path = convert_local_file_to_jpeg(source_path)
        print(f"Converted image saved to: {output_path}")
    except UnidentifiedImageError:
        print("Error: The selected file is not a valid image.")
    except Exception as exc:
        print(f"Error: {exc}")


if __name__ == "__main__":
    prompt_and_convert_local_file()