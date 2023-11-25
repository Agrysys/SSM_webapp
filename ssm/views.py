import cv2
import io
import numpy as np
import json
import datetime

from PIL import Image
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import Melon
from tensorflow.keras.models import load_model
from django.core.files.storage import default_storage
from django.utils import timezone
from datetime import date, timedelta
from django.db.models import Count
from django.db.models.functions import Trunc
from keras.preprocessing import image
from skimage.feature import graycomatrix, graycoprops



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
def get_count_in_a_week(request):
    # Dapatkan tanggal 7 hari yang lalu
    week_ago = timezone.now() - datetime.timedelta(days=7)

    # Hitung jumlah melon setiap hari dalam seminggu terakhir
    melon_counts = Melon.objects.filter(pub_date__gte=week_ago).annotate(date=models.functions.TruncDate('pub_date')).values('date').annotate(count=Count('kode_melon')).order_by('date')

    for melon_count in melon_counts:
        print(f"Tanggal: {melon_count['date']}, Jumlah Melon: {melon_count['count']}")

@csrf_exempt
def get_glcm(request,kode):
    try:
        melon = Melon.objects.get(kode_melon=kode)
        img_path = str(melon.edge)
        img = cv2.imread("storage\\"+img_path)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Hitung GLCM
        glcm = graycomatrix(img_gray, distances=[1], angles=[0, np.pi/4, np.pi/2, 3*np.pi/4], levels=256, symmetric=True, normed=True)

        # Hitung properti GLCM
        contrast_0 = graycoprops(glcm, 'contrast')[0, 0]
        contrast_135 = graycoprops(glcm, 'contrast')[0, 3]
        dissimilarity_0 = graycoprops(glcm, 'dissimilarity')[0, 0]
        dissimilarity_135 = graycoprops(glcm, 'dissimilarity')[0, 3]
        correlation_0 = graycoprops(glcm, 'correlation')[0, 0]
        correlation_45 = graycoprops(glcm, 'correlation')[0, 1]
        correlation_135 = graycoprops(glcm, 'correlation')[0, 3]
        response = JsonResponse({
            'contrast_0': contrast_0,
            'contrast_135': contrast_135,
            'dissimilarity_0': dissimilarity_0,
            'dissimilarity_135': dissimilarity_135,
            'correlation_0': correlation_0,
            'correlation_45': correlation_45,
            'correlation_135': correlation_135
        })

    except Melon.DoesNotExist:
        response = JsonResponse({'error': 'Melon with given kode_melon does not exist'})

    return response


@csrf_exempt
def predict(request):
    model = load_model("ssm\modelmodel-edge_ann.h5")
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
        file_path = default_storage.save('melon/raw/' + image_file.name, image_file)
        try:
            croped_img = Melon.crop_otomatis(img)
            edge = cv2.Canny(croped_img,100,200)
            edge_rgb = cv2.cvtColor(edge,cv2.COLOR_GRAY2RGB)
            edge_rgb_sized = cv2.resize(edge_rgb,(150,150))
            
            img_keras = image.img_to_array(edge_rgb_sized)
            img_fited_dimension = np.expand_dims(img_keras, axis=0)
            prediction = model.predict(img_fited_dimension)
            predicted_category_index = np.argmax(prediction)
            categories = [Melon.BUKAN_MELON,Melon.MATANG,Melon.MENTAH]
            predicted_category = categories[predicted_category_index]
            
            kode_melon = str(Melon.generate_kode_melon(predicted_category))
            
            
            crop_path = f"melon\crop\{kode_melon}.png"
            edge_path = f"melon\edge\{kode_melon}.png"
            edge_resize_path = f"melon\\resize\{kode_melon}.png"
            cv2.imwrite("storage\\"+edge_path,edge_rgb)
            cv2.imwrite("storage\\"+crop_path,croped_img)
            cv2.imwrite("storage\\"+edge_resize_path,edge_rgb_sized)
            
            melon = Melon.objects.create(
                kode_melon=kode_melon,
                image=file_path,
                crop= crop_path,
                edge = edge_path,
                edge_resize = edge_resize_path,
                object_class=predicted_category,
                pub_date=timezone.now(), 
            )
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
        "jumlah_total":(total- bukan),
        "jumlah_matang":matang,
        "jumlah_mentah":mentah,
        "jumlah_bukan":bukan,
        "label_chart" : json.dumps(label),
        "data_chart" : json.dumps(data)
        
    }
    
    return render(request=request, template_name="ssm/dashboard.html", context=context)