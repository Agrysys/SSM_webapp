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
    file_path = models.FileField(upload_to="storage/melon")
    object_class = models.TextField(choices=CLASS_MELON)
    pub_date = models.DateField()
    Glcm = models.OneToOneField("Glcm",on_delete=models.CASCADE)
    
    def generate_kode_melon(kode):
        last_melon = Melon.objects.filter(kode_melon__startswith=kode)
        kode_counter = int(last_melon.kode_melon[2:])
        kode_counter += 1
        s_kosong = ""
        for kosong in range(len(str(kode_counter))):
            s_kosong += kosong
        return kode+s_kosong
    
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