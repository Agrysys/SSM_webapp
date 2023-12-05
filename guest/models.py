from django.db import models

# Create your models here.

class MelonTest(models.Model):
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
    predicted_class = models.TextField(choices=CLASS_MELON)
    actual_class = models.TextField(choices=CLASS_MELON)
    pub_date = models.DateField()
    
    def generate_kode_melon(kode):
        print(kode)
        if MelonTest.objects.filter(kode_melon__startswith="T"+kode).exists():
            last_melon = MelonTest.objects.filter(kode_melon__startswith="T"+kode).order_by('kode_melon').last()
            print(f"Last melon: {last_melon}")
        else:
            return "T"+kode+"0000001"
        
        if last_melon is not None:
            kode_counter = int(last_melon.kode_melon[3:])
            print(f"Kode counter 1: {kode_counter}")
            kode_counter += 1
            s_kosong = str("")
            print(f"Kode counter 2: {kode_counter}")
            for kosong in range(7-len(str(kode_counter))):
                s_kosong += str(0)
            return "T"+kode+s_kosong+str(kode_counter)
        else:
            print("No last melon found.")
    