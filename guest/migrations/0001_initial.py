# Generated by Django 4.2.7 on 2023-12-03 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MelonTest',
            fields=[
                ('kode_melon', models.TextField(max_length=10, primary_key=True, serialize=False, verbose_name='kode melon')),
                ('image', models.ImageField(blank=True, null=True, upload_to='melon/raw')),
                ('crop', models.ImageField(blank=True, null=True, upload_to='melon/crop')),
                ('edge', models.ImageField(blank=True, null=True, upload_to='melon/edge')),
                ('edge_resize', models.ImageField(blank=True, null=True, upload_to='melon/resize')),
                ('predicted_class', models.TextField(choices=[('MM', 'mature'), ('TM', 'raw'), ('BM', 'not melon')])),
                ('actual_class', models.TextField(choices=[('MM', 'mature'), ('TM', 'raw'), ('BM', 'not melon')])),
                ('pub_date', models.DateField()),
            ],
        ),
    ]