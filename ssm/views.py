import cv2
import io
import numpy as np
import random

from PIL import Image
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Glcm, Melon
from tensorflow.keras.models import load_model
from django.core.files.storage import default_storage
from django.utils import timezone


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
def predict(request):
    model = load_model("ssm\model_melon_gray_glcm_ep-30_btsz-64_optz-Adam.h5")
    response = JsonResponse
    data = {
        "kode_melon":"",
        "kelas":""
    }
    if request.method == 'POST':
        image_file = request.FILES['image']  # get the image file from the POST request
        image_data = image_file.read()  # read the image data
        nparr = np.fromstring(image_data, np.uint8)  # convert string data to numpy array
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        file_path = default_storage.save('storage/melon/' + image_file.name, image_file)
        try:
            img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            glcm = Glcm.extract_glcm_features_all_angles(img_gray)
            feature = np.array([glcm])
            prediction = model.predict(feature)
            predicted_category_index = np.argmax(prediction)
            categories = [Melon.MATANG,Melon.MENTAH]
            predicted_category = categories[predicted_category_index]
            
            glcm = Glcm.objects.create(
                contrast_0=glcm[0],
                contrast_45=glcm[1],
                contrast_90=glcm[2],
                contrast_135=glcm[3],
                dissimilarity_0=glcm[4],
                dissimilarity_45=glcm[5],
                dissimilarity_90=glcm[6],
                dissimilarity_135=glcm[7],
                homogeneity_0=glcm[8],
                homogeneity_45=glcm[9],
                homogeneity_90=glcm[10],
                homogeneity_135=glcm[11],
                energy_0=glcm[12],
                energy_45=glcm[13],
                energy_90=glcm[14],
                energy_135=glcm[15],
                correlation_0=glcm[16],
                correlation_45=glcm[17],
                correlation_90=glcm[18],
                correlation_135=glcm[19],
                asm_0=glcm[20],
                asm_45=glcm[21],
                asm_90=glcm[22],
                asm_135=glcm[23]
            )
            
            kode_melon = str(random.randrange(0,100000000))
            melon = Melon.objects.create(
                kode_melon=kode_melon,
                file_path=file_path,
                object_class=predicted_category,
                pub_date=timezone.now(), 
                Glcm=glcm
            )
            
            glcm.save()
            melon.save()
            
            data["kelas"] = predicted_category
            data["kode_melon"] = kode_melon
            response = JsonResponse(data=data,status=200)
        except cv2.error as e:
            error = {"error":e}
            response = JsonResponse(data=error,status=500)
        return response
        
    

def generate_kode_melon(kode):
        last_melon = ra
        kode_counter = int(last_melon.kode_melon[2:])
        kode_counter += 1
        s_kosong = ""
        for kosong in range(len(str(kode_counter))):
            s_kosong += kosong
        return kode+s_kosong