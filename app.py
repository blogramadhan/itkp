# Import Core PKGS
import streamlit as st

# Import Fungsi ITKP
from itkp import run_itkp

def main():
    # Setting Halaman
    st.set_page_config(page_title="Dashboard ITKP Prov. Kalbar", layout="wide")

    st.title("DASHBOARD ITKP")
    daerah = ["HOME", "PROV. KALBAR", "KOTA PONTIANAK", "KAB. KUBU RAYA", "KAB. MEMPAWAH", "KOTA SINGKAWANG", "KAB. SAMBAS", "KAB. BENGKAYANG", "KAB. LANDAK", 
              "KAB. SANGGAU", "KAB. SEKADAU", "KAB. SINTANG", "KAB. MELAWI", "KAB. KAPUAS HULU", "KAB. KAYONG UTARA", "KAB. KETAPANG"]
    pilih = st.selectbox("Pilih Daerah yang Diinginkan :", daerah)
    
    if pilih == "HOME":
        st.subheader("Tentang ITKP Provinsi Kalimantan Barat")
        st.write("")
    else:
        run_itkp(pilih)

if __name__ == '__main__':
    main()