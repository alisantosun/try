pip install pandas streamlit openpyxl
import pandas as pd

# Excel dosyasını okuma
file_path = '/mnt/data/Guncel_veriler (1).xlsx'
df = pd.read_excel(file_path)

# Veri çerçevesinin ilk birkaç satırını gösterme
print(df.head())
df['carbon_footprint'] = df['fuel_consumption'] * df['emission_factor']

# İşlenmiş verilerin ilk birkaç satırını gösterme
print(df.head())

import streamlit as st

# Başlık ve giriş
st.title("Karbon Ayak İzi Hesaplayıcı")
st.write("Bu uygulama, çeşitli aktivitelerinizin karbon ayak izini hesaplamanıza yardımcı olur.")

# Excel dosyasını yükleme
uploaded_file = st.file_uploader("Excel dosyasını yükleyin", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write(df.head())

    # Hesaplamalar ve sonuçlar
    df['carbon_footprint'] = df['fuel_consumption'] * df['emission_factor']
    st.write("Hesaplanan Karbon Ayak İzleri")
    st.write(df)

    # Kullanıcı girdileri
    activity = st.selectbox("Aktivite Seçin", df['activity'].unique())
    fuel_consumption = st.number_input("Yakıt Tüketimi (litre)")
    emission_factor = df[df['activity'] == activity]['emission_factor'].values[0]

    if st.button("Karbon Ayak İzini Hesapla"):
        carbon_footprint = fuel_consumption * emission_factor
        st.write(f"Seçilen aktivitenin karbon ayak izi: {carbon_footprint} kg CO2e")

streamlit run app.py
