from datasets import load_dataset
import pandas as pd
from pathlib import Path
import base64
from io import BytesIO

# Load dataset from HuggingFace
print("Loading product dataset...")
try:
    # Try loading the dataset
    dataset = load_dataset("ashraq/fashion-product-images-small", split="train[:5]")
    print(f"✓ Loaded {len(dataset)} products")
    print(dataset)
    # print(dataset[0]['image'].show()) # show first example image
    products_df = pd.DataFrame(dataset)
    print(f"Dataset columns: {products_df.columns.to_list()}")
    
except Exception as e:
    print(f"⚠ Could not load HuggingFace dataset: {e}")
    print("Using local images instead...")
    # Alternative: Use local images
    # Create a products.json file with product information
    products_data = [
        {
            "id": 1,
            "name": "Wireless Headphones",
            "price": 79.99,
            "category": "Electronics",
            "image_path": "images/product1.jpg"
        },
        # Add more products...
    ]
    
    products_df = pd.DataFrame(products_data)

DATA_DIR = Path("data")
# Create images directory
images_dir = DATA_DIR / "product_images"
images_dir.mkdir(parents=True, exist_ok=True)
 
print(f"\n✓ Dataset prepared!")
print(f"Total products: {len(products_df)}")

def encode_image_to_base64(image_path):
    """Encode an image file to base64 string."""
    # following steps are needed to save jpeg file otherwise: 
    # TypeError: expected str, bytes or os.PathLike object, not JpegImageFile
    
    # binary buffer to hold image data 
    buffered = BytesIO()
    # save image to buffer
    image_path.save(buffered, format="JPEG")
    # get the raw bytes from the buffer and encode them
    encoded = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    """with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode("utf-8") """
    return encoded 

# Example usage
sample_path = products_df.iloc[0]["image"]
encoded_image = encode_image_to_base64(sample_path)
print(f"Encoded image length: {len(encoded_image)} characters")
print(f"Encoded prefix: {encoded_image[:40]}...")