import streamlit as st
import pandas as pd
import numpy as np
from streamlit.components.v1 import html
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
import pickle
import io
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import base64
import seaborn as sns

# CSV dosyasını yükleyin
file_path = '/mnt/data/Guncel_veriler - Worksheet.csv'
data = pd.read_csv(file_path)

# Gelir aralığını sayısal bir değişkene dönüştürme
def gelir_araligi_to_numeric(gelir_araligi):
    if gelir_araligi == "30.000 TL-50.000 TL":
        return 1
    elif gelir_araligi == "50.000 TL-80.000 TL":
        return 2
    elif gelir_araligi == "80.000 TL+":
        return 3
    else:
        return 0  # Bilinmeyen durumlar için varsayılan değer

data['Gelir_Araligi_Numeric'] = data['Aylik_gelir'].apply(gelir_araligi_to_numeric)

# Karbon ayak izi hesaplama için kullanılan emisyon faktörleri (kg CO2/litre)
emission_factors = {
    "Benzin": 2.31,
    "Mazot": 2.68,
    "LPG": 1.51,
    "Elektrik": 0  # Elektrik için varsayılan değer. Ülkeye göre değişebilir.
}

# Karbon ayak izi hesaplama fonksiyonu
def calculate_carbon_footprint(row):
    yakit_tipi = row['Arac_yakit_tipi']
    yakit_miktari = row['Yillik_yakit_miktar']
    
    # Yıllık yakıt miktarı metin olarak gelebilir, bunu sayıya çevirelim
    try:
        yakit_miktari = float(str(yakit_miktari).replace(',', '.'))
    except ValueError:
        yakit_miktari = 0
    
    # Emisyon faktörünü alalım, yakıt tipi mevcut değilse 0 kabul edelim
    emission_factor = emission_factors.get(yakit_tipi, 0)
    
    # Karbon ayak izi hesaplama
    carbon_footprint = yakit_miktari * emission_factor
    return carbon_footprint

# Yeni sütunu oluşturalım
data['Karbon_Ayak_Izi'] = data.apply(calculate_carbon_footprint, axis=1)

# Toplu taşıma sıklığını sayısallaştırmak için önce kategorileri belirleyelim
def toplu_tasima_sikligi_to_numeric(siklik):
    if siklik == "Hiç":
        return 0
    elif siklik == "1-2 kez":
        return 1
    elif siklik == "3-4 kez":
        return 2
    elif siklik == "5-6 kez":
        return 3
    elif siklik == "Her gün":
        return 4
    else:
        return None  # Bilinmeyen durumlar için None değeri

# Yeni sayısal değişkeni ekleyelim
data['Toplu_Tasima_Sikligi_Numeric'] = data['Toplu_tasima_haftalik'].apply(toplu_tasima_sikligi_to_numeric)

# Boxplot ile Karbon Ayak İzi ve Cinsiyet ilişkisinin görselleştirilmesi
plt.figure(figsize=(10, 6))
sns.boxplot(x='Cinsiyet', y='Karbon_Ayak_Izi', data=data)
plt.title('Cinsiyete Göre Karbon Ayak İzi Dağılımı')
plt.xlabel('Cinsiyet')
plt.ylabel('Karbon Ayak İzi (kg CO2)')
plt.show()

# Gelir aralığı sayısal değişkeninin histogramını oluşturalım
plt.figure(figsize=(10, 6))
plt.hist(data['Gelir_Araligi_Numeric'], bins=3, edgecolor='black')
plt.title('Gelir Aralığı Dağılımı')
plt.xlabel('Gelir Aralığı (1: 30-50k, 2: 50-80k, 3: 80k+)')
plt.ylabel('Kişi Sayısı')
plt.show()

# Cinsiyet ve Karbon Ayak İzi ilişkisinin kutu grafiği
plt.figure(figsize=(10, 6))
sns.boxplot(x='Cinsiyet', y='Karbon_Ayak_Izi', data=data)
plt.title('Cinsiyete Göre Karbon Ayak İzi Dağılımı')
plt.xlabel('Cinsiyet')
plt.ylabel('Karbon Ayak İzi (kg CO2)')
plt.show()
