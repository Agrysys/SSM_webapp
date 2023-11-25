from django.db import models
from skimage.feature import graycomatrix, graycoprops
import cv2

import numpy as np
import cv2
# Create your models here.
class Melon(models.Model):
    MATANG = "MM"
    MENTAH = "TM"
    BUKAN_MELON = "BM"
    
    CLASS_MELON = [
        (MATANG,"mature"),
        (MENTAH,"raw"),
        (BUKAN_MELON,"not melon")
    ]
    kode_melon = models.TextField(verbose_name="kode melon",primary_key=True,max_length=10)
    image = models.ImageField(upload_to="melon/raw", blank=True, null=True)
    crop = models.ImageField(upload_to="melon/crop",blank=True,null=True)
    edge = models.ImageField(upload_to="melon/edge", blank=True, null=True)
    edge_resize = models.ImageField(upload_to="melon/resize", blank=True, null=True)
    object_class = models.TextField(choices=CLASS_MELON)
    pub_date = models.DateField()
    
    def generate_kode_melon(kode):
        if Melon.objects.filter(kode_melon__startswith=kode).exists():
            last_melon = Melon.objects.filter(kode_melon__startswith=kode).order_by('kode_melon').last()
            print(f"Last melon: {last_melon}")
        else:
            return kode+"00000001"
        
        if last_melon is not None:
            kode_counter = int(last_melon.kode_melon[2:])
            print(f"Kode counter 1: {kode_counter}")
            kode_counter += 1
            s_kosong = str("")
            print(f"Kode counter 2: {kode_counter}")
            for kosong in range(8-len(str(kode_counter))):
                s_kosong += str(0)
            return kode+s_kosong+str(kode_counter)
        else:
            print("No last melon found.")
            

    def canny_edge(img):
            canny = cv2.Canny(img, 100, 200)
            resized_canny = cv2.resize(canny, (150, 150))
            # Convert the single-channel image back to a three-channel image
            return resized_canny
    
    def crop_otomatis(image):
        input_image = image

        height = input_image.shape[0]
        width = input_image.shape[1]

        # Checking image is grayscale or not. If image shape is 2 then gray scale otherwise not
        if len(input_image.shape) == 2:
            gray_input_image = input_image.copy()
        else:
            # Converting BGR image to grayscale image
            gray_input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

        # # To find upper threshold, we need to apply Otsu's thresholding
        upper_threshold, thresh_input_image = cv2.threshold(
            gray_input_image, thresh=0, maxval=255, type=cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        # # Calculate lower threshold
        lower_threshold = 0.5 * upper_threshold

        # Apply canny edge detection
        canny = cv2.Canny(input_image, lower_threshold, upper_threshold)
        # canny = cv2.Canny(input_image, 100, 200)
        # Finding the non-zero points of canny
        pts = np.argwhere(canny > 0)

        # Finding the min and max points
        y1, x1 = pts.min(axis=0)
        y2, x2 = pts.max(axis=0)

        # Crop ROI from the givn image
        output_image = input_image[y1:y2, x1:x2]
        return output_image


