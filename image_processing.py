from google.cloud import vision
import io

def process_image(image_path):
    # Initialize Vision API client
    client = vision.ImageAnnotatorClient()

    # Read the image file
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    # Perform label detection
    response = client.label_detection(image=image)
    labels = response.label_annotations

    if response.error.message:
        raise Exception(f"Google Vision API error: {response.error.message}")

    # Extract label descriptions
    label_list = [label.description.lower() for label in labels]
    print("Detected labels:", label_list)
    return label_list
