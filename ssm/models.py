from django.db import models
from skimage.feature import graycomatrix, graycoprops

import numpy as np
import random
import string

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
    image = models.ImageField(upload_to="melon/", default="melon/no_im.jpeg")
    object_class = models.TextField(choices=CLASS_MELON)
    pub_date = models.DateField()
    Glcm = models.OneToOneField("Glcm",on_delete=models.CASCADE)
    
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

    
class Glcm(models.Model):
    contrast_0 = models.FloatField()
    contrast_45 = models.FloatField()
    contrast_90 = models.FloatField()
    contrast_135 = models.FloatField()
    dissimilarity_0 = models.FloatField()
    dissimilarity_45 = models.FloatField()
    dissimilarity_90 = models.FloatField()
    dissimilarity_135 = models.FloatField()
    homogeneity_0 = models.FloatField()
    homogeneity_45 = models.FloatField()
    homogeneity_90 = models.FloatField()
    homogeneity_135 = models.FloatField()
    energy_0 = models.FloatField()
    energy_45 = models.FloatField()
    energy_90 = models.FloatField()
    energy_135 = models.FloatField()
    correlation_0 = models.FloatField()
    correlation_45 = models.FloatField()
    correlation_90 = models.FloatField()
    correlation_135 = models.FloatField()
    asm_0 = models.FloatField()
    asm_45 = models.FloatField()
    asm_90 = models.FloatField()
    asm_135 = models.FloatField()
    
    def extract_glcm_features_all_angles(image):
        image = np.array(image)
        distances = [1]
        angles = [0, 45, 90, 135]
        glcm = graycomatrix(image, distances=distances, angles=angles, levels=256, symmetric=True, normed=True)
        properties = ['contrast', 'dissimilarity', 'homogeneity', 'energy', 'correlation', 'ASM']
        features = [np.array([])]
        for prop in properties:
            for index in range(len(angles)):
                features = np.append(features,graycoprops(glcm,prop)[0,index])
        return features