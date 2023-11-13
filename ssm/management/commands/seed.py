from django.core.management.base import BaseCommand
from ssm.models import Glcm, Melon
from django.utils import timezone
import random
from ssm.models import Melon, Glcm


class Command(BaseCommand):
    help = 'Seeds the database'

    def handle(self, *args, **options):
        for i in range(10):
            print(f"creating data {i}")
            new_glcm = Glcm(
                contrast_0=random.uniform(0, 1),
                contrast_45=random.uniform(0, 1),
                contrast_90=random.uniform(0, 1),
                contrast_135=random.uniform(0, 1),
                dissimilarity_0=random.uniform(0, 1),
                dissimilarity_45=random.uniform(0, 1),
                dissimilarity_90=random.uniform(0, 1),
                dissimilarity_135=random.uniform(0, 1),
                homogeneity_0=random.uniform(0, 1),
                homogeneity_45=random.uniform(0, 1),
                homogeneity_90=random.uniform(0, 1),
                homogeneity_135=random.uniform(0, 1),
                energy_0=random.uniform(0, 1),
                energy_45=random.uniform(0, 1),
                energy_90=random.uniform(0, 1),
                energy_135=random.uniform(0, 1),
                correlation_0=random.uniform(0, 1),
                correlation_45=random.uniform(0, 1),
                correlation_90=random.uniform(0, 1),
                correlation_135=random.uniform(0, 1),
                asm_0=random.uniform(0, 1),
                asm_45=random.uniform(0, 1),
                asm_90=random.uniform(0, 1),
                asm_135=random.uniform(0, 1)
            )
            
            start_date = timezone.datetime(2023, 1, 1)
            end_date = timezone.datetime(2023, 12, 31)

            time_between_dates = end_date - start_date
            days_between_dates = time_between_dates.days
            random_number_of_days = random.randrange(days_between_dates)

            random_date = start_date + timezone.timedelta(days=random_number_of_days)

            new_glcm.save()
            kelas_melon = random.choice([Melon.BUKAN_MELON,Melon.MENTAH,Melon.MATANG])
            kode_melon = str(Melon.generate_kode_melon(kelas_melon))
            new_melon = Melon.objects.create(
                kode_melon=kode_melon,
                image="melon/no_im.jpeg",
                object_class=kelas_melon,
                pub_date=random_date, 
                Glcm=new_glcm
            )
            
            new_melon.save()
            
