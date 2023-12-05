from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

import cv2
import numpy as np

from django.http import HttpResponse, JsonResponse
from .models import MelonTest
from tensorflow.keras.models import load_model
from django.core.files.storage import default_storage
from django.utils import timezone
from keras.preprocessing import image
from django.views.decorators.csrf import csrf_exempt

from ssm.models import Melon
from .forms import MelonTestForm

def melon_test_view(request):
    if request.method == 'POST':
        form = MelonTestForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = MelonTestForm()
    return render(request, 'guest/test_predict.html', {'form': form})

    
def landing(request):
    return render(request,"guest/landingpage.html")

@csrf_exempt
def predict_test(request):
    model = load_model("ssm\modelmodel-edge_ann.h5")
    response = JsonResponse
    data = {
        "kode_melon":"",
        "kelas":""
    }
    if request.method == 'POST':
        actual_class = int(request.POST.get('kelas'))
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
            categories = [MelonTest.BUKAN_MELON,MelonTest.MATANG,MelonTest.MENTAH]
            predicted_category = categories[predicted_category_index]
            
            kode_melon = str(MelonTest.generate_kode_melon(predicted_category))
            print(kode_melon)
            
            crop_path = f"melon\crop\{kode_melon}.png"
            edge_path = f"melon\edge\{kode_melon}.png"
            edge_resize_path = f"melon\\resize\{kode_melon}.png"
            cv2.imwrite("storage\\"+edge_path,edge_rgb)
            cv2.imwrite("storage\\"+crop_path,croped_img)
            cv2.imwrite("storage\\"+edge_resize_path,edge_rgb_sized)
            
            actual_class = categories[actual_class]
            
            melon = MelonTest.objects.create(
                kode_melon=kode_melon,
                image=file_path,
                crop= crop_path,
                edge = edge_path,
                edge_resize = edge_resize_path,
                predicted_class=predicted_category,
                actual_class="TM",
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
