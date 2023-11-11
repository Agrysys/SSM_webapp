import cv2
import numpy as np
from skimage.feature import graycomatrix, graycoprops
import os

def extract_edge_features(image):
    # Ubah gambar ke skala abu-abu
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Terapkan Canny edge detection
    edges = cv2.Canny(gray, 100, 200)
    
    # Hitung jumlah piksel tepi yang terdeteksi
    edge_pixel_count = np.sum(edges) / 255  # Normalisasi
    
    return edge_pixel_count

def extract_glcm_feature(image):
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    glcm = graycomatrix(image, distances=[5], angles=[0], levels=256, symmetric=True, normed=True)
    cs = graycoprops(glcm, 'contrast')[0,0]
    hom = graycoprops(glcm, 'homogeneity')[0,0]
    eng = graycoprops(glcm, 'energy')[0,0]
    kor = graycoprops(glcm, 'correlation')[0,0]
    fitur = [cs, hom, eng, kor]
    return fitur






# Fungsi untuk ekstraksi fitur warna
def extract_hsv_features(image):
    # Ubah gambar ke format HSV (Hue, Saturation, Value)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Ambil histogram dari channel Hue (warna)
    hist_hue = cv2.calcHist([hsv], [0], None, [256], [0, 256])
    
    return hist_hue.flatten()

# Function to extract RGB color features
def extract_color_features(image):
    # Split the image into its Red, Green, and Blue components
    b, g, r = cv2.split(image)

    # Calculate histograms for Red, Green, and Blue channels
    hist_red = cv2.calcHist([r], [0], None, [256], [0, 256])
    hist_green = cv2.calcHist([g], [0], None, [256], [0, 256])
    hist_blue = cv2.calcHist([b], [0], None, [256], [0, 256])

    # Flatten and concatenate the histograms
    all_features = np.concatenate([hist_red.flatten(), hist_green.flatten(), hist_blue.flatten()])

    return all_features

def glcm_hsv_extractor(dataset_path):
    categories = ['Matang', 'Mentah']

# Menyiapkan list untuk menyimpan fitur dan label
    x_test = []
    labels = []

# Loop melalui setiap kategori (matang dan mentah)
    for category in categories:
        path = os.path.join(dataset_path, category)
        label = categories.index(category)  # Label kategori
    
    # Loop melalui setiap gambar dalam setiap kategori
        for img_name in os.listdir(path):
            img_path = os.path.join(path, img_name)
            image = cv2.imread(img_path)
            image = cv2.resize(image, (100, 100))  # Resize gambar ke ukuran yang sama
        
        # Ekstraksi fitur warna dan edge
            glcm_feature = extract_glcm_feature(image)
            color_features = extract_hsv_features(image)
        
        # Gabungkan fitur-fitur
            all_features = np.concatenate([color_features, glcm_feature])
        
        # Simpan fitur dan label
            x_test.append(all_features)
            labels.append(label)


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
# Ubah ke format numpy
    
# path = "dataset\Test\Matang\Copy of m1.png"
# img = cv2.imread(path)
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# # print(extract_glcm_features_all_angles(gray))
# for glcm in extract_glcm_features_all_angles(gray):
#     print(str(round(glcm,4)))