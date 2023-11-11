import cv2
import numpy as np
from PIL import Image
import io
from django.http import HttpResponse
from .feature_extractor import extract_glcm_features_all_angles
from django.views.decorators.csrf import csrf_exempt

def index(request):
    path = "prediction\storage\Copy of m6.png"
    # Read the image
    img = cv2.imread(path)
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect edges
    edges = cv2.Canny(gray, 100, 200)
    # Convert to binary
    _, binary = cv2.threshold(edges, 127, 255, cv2.THRESH_BINARY)
    # Convert to PIL images
    img_pil = Image.fromarray(img)
    binary_pil = Image.fromarray(binary)
    # Create a BytesIO object
    img_io = io.BytesIO()
    # Save the images to the BytesIO object
    img_pil.save(img_io, 'PNG')
    binary_pil.save(img_io, 'PNG')
    # Seek to the beginning of the BytesIO object
    img_io.seek(0)
    # Return a HttpResponse with the image data and the content type
    return HttpResponse(img_io, content_type='image/png')

def coba(request):
    image = cv2.imread("prediction\storage\Copy of m6.png")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Deteksi tepi menggunakan metode Canny
    edges = cv2.Canny(gray, 100, 200)
    
    img_io = io.BytesIO()
    
    
    return HttpResponse(edges, content_type='image/png')

@csrf_exempt
def upload(request):
    response = ""
    if request.method == 'POST':
        image_file = request.FILES['image']  # get the image file from the POST request
        image_data = image_file.read()  # read the image data
        nparr = np.fromstring(image_data, np.uint8)  # convert string data to numpy array
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        try:
            img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            glcm = extract_glcm_features_all_angles(img_gray)
            response = str(glcm)
        except(cv2.error):
            response = "eror encoding img"
        
        
    return HttpResponse(response)