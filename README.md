# SSM Web App

Deskripsi singkat tentang proyek Anda.

## Persyaratan

- Python 3.8 atau lebih tinggi
- Django 3.2 atau lebih tinggi

## Instalasi

1. Clone repositori ini:
    ```
    git clone https://github.com/username/proyek.git
    ```
2. Masuk ke direktori proyek:
    ```
    cd proyek
    ```
3. Buat virtual environment dan aktifkan:

   for mac/linux
    ```
    python3 -m venv env
    ```
    for windows 
    ```
    Set-ExecutionPolicy Unrestricted -Scope Process  
    py -m venv env
    ```
5. Nasuk ke virtual environment
   ```
   env/bin/activate
   ```
6. Install dependensi:
    ```
    pip install -r requirements.txt
    ```
7. Migrasi database
    ```
    py manage.py migrate
    ```
## Penggunaan

Untuk menjalankan server pengembangan Django, gunakan perintah berikut:
```
python manage.py runserver
```
Buka http://127.0.0.1:8000/ di browser Anda untuk melihat aplikasi.



