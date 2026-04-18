from rembg import remove
from PIL import Image
import io

def process_remove_bg(input_bytes):
    # Image ko process karke background remove karna
    result = remove(input_bytes)
    return result