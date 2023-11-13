import cv2
import io
import numpy as np
import json

from PIL import Image
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import Glcm, Melon
from tensorflow.keras.models import load_model
from django.core.files.storage import default_storage
from django.utils import timezone
from datetime import date, timedelta
from django.db.models import Count
from django.db.models.functions import Trunc


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
            
            kode_melon = str(Melon.generate_kode_melon(predicted_category))
            melon = Melon.objects.create(
                kode_melon=kode_melon,
                image=file_path,
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
        
    
def data_melons(request):
    melon = Melon.objects.all
    return render(request,"ssm/data_melons.html",{'melons':melon})

def dashboard(request):
    total = Melon.objects.count()
    matang = Melon.objects.filter(object_class = Melon.MATANG).count()
    mentah = Melon.objects.filter(object_class = Melon.MENTAH).count()
    bukan = Melon.objects.filter(object_class = Melon.BUKAN_MELON).count()
    
    label = []
    data = []
    
    # start_date = date(2023, 11, 13)  # replace with your start date
    # end_date = timezone.now().date()
    # delta = timedelta(days=1)
    # context = {}
    # while start_date <= end_date:
    #     label = label.append(start_date)
    #     melon_count = Melon.objects.filter(pub_date = start_date).count()
    #     data = data.append(melon_count)
    #     start_date += delta
    
    # melons = Melon.objects.order_by("pub_date")
    # for melon in melons:
    #     tanggl = str(melon.pub_date)
    #     print(melon.pub_date)
    #     label = label.append(tanggl)
    #     data = Melon.objects.filter(pub_date = tanggl).count()
    melons = Melon.objects.annotate(date=Trunc('pub_date', 'day')).values('date').annotate(count=Count('kode_melon')).order_by('date')

    for melon in melons:
        data.append(melon['count'])
        label.append(melon['date'].strftime('%Y-%m-%d'))
    
    
    context = {
        "jumlah_total":total,
        "jumlah_matang":matang,
        "jumlah_mentah":mentah,
        "jumlah_bukan":bukan,
        "label_chart" : json.dumps(label),
        "data_chart" : json.dumps(data)
        
    }
    
    return render(request=request, template_name="ssm/dashboard.html", context=context)

def get_glcm(request, pk):
    glcm = Glcm.objects.get(pk=pk)
    data = {
        0 : {
            "contrast" : glcm.contrast_0,
            "dissimilarity" : glcm.dissimilarity_0,
            "homogenity" : glcm.homogeneity_0,
            "energy" : glcm.energy_0,
            "corelation" : glcm.correlation_0,
            "asm" : glcm.asm_0
        },
        45 : {
            "contrast" : glcm.contrast_45,
            "dissimilarity" : glcm.dissimilarity_45,
            "homogenity" : glcm.homogeneity_45,
            "energy" : glcm.energy_45,
            "corelation" : glcm.correlation_45,
            "asm" : glcm.asm_45
        },
        90 : {
            "contrast" : glcm.contrast_90,
            "dissimilarity" : glcm.dissimilarity_90,
            "homogenity" : glcm.homogeneity_90,
            "energy" : glcm.energy_90,
            "corelation" : glcm.correlation_90,
            "asm" : glcm.asm_90
        },
        135 : {
            "contrast" : glcm.contrast_135,
            "dissimilarity" : glcm.dissimilarity_135,
            "homogenity" : glcm.homogeneity_135,
            "energy" : glcm.energy_135,
            "corelation" : glcm.correlation_135,
            "asm" : glcm.asm_135
        }
    }
    return JsonResponse(data)