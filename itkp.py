import streamlit as st
import pandas as pd
from babel.numbers import format_currency

def run_itkp(pilih):
    
    # Setting CSS
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    # Konfigurasi Variabel URL Dataset
    if pilih == "PROV. KALBAR":
        urlFolder = "PROV/" 
    if pilih == "KOTA PONTIANAK":
        urlFolder = "PTK/"
    if pilih == "KAB. KUBU RAYA":
        urlFolder = "KKR/"
    if pilih == "KAB. MEMPAWAH":
        urlFolder = "MPW/"
    if pilih == "KOTA SINGKAWANG":
        urlFolder = "SKW/"
    if pilih == "KAB. SAMBAS":
        urlFolder = "SAMBAS/"
    if pilih == "KAB. BENGKAYANG":
        urlFolder = "BKY/"
    if pilih == "KAB. LANDAK":
        urlFolder = "LDK/"  
    if pilih == "KAB. SANGGAU":
        urlFolder = "SGU/"
    if pilih == "KAB. SEKADAU":
        urlFolder = "SKD/"
    if pilih == "KAB. SINTANG":
        urlFolder = "STG/"
    if pilih == "KAB. MELAWI":
        urlFolder = "MLW/"
    if pilih == "KAB. KAPUAS HULU":
        urlFolder = "KPH/"
    if pilih == "KAB. KAYONG UTARA":
        urlFolder = "KKU/"
    if pilih == "KAB. KETAPANG":
        urlFolder = "KTP/"

    # Dataset
    tglTarik = "2022630"
    urlDataset = "https://storage.googleapis.com/lpse_ramadhan/" + urlFolder

    ## Data RUP Paket Penyedia
    df_pp = pd.read_feather(urlDataset + "sirupdp" + tglTarik + ".ftr")
    df_pp_umumkan = df_pp[df_pp['statusumumkan'].isin(['Terumumkan'])]
    df_pp_belum_umumkan = df_pp[df_pp['statusumumkan'].isin(['Draf', 'Draf Lengkap', 'Final Draft'])]
    df_pp_umumkan_umk = df_pp_umumkan[df_pp_umumkan['statususahakecil'] == 'UsahaKecil']
    df_pp_umumkan_pdn = df_pp_umumkan[df_pp_umumkan['statuspdn'] == 'PDN']

    df_pp_etendering = df_pp_umumkan[df_pp_umumkan['metodepengadaan'].isin(['Tender', 'Tender Cepat', 'Seleksi'])]
    df_pp_tender = df_pp_umumkan[df_pp_umumkan['metodepengadaan'].isin(['Tender'])]
    df_pp_tender_cepat = df_pp_umumkan[df_pp_umumkan['metodepengadaan'].isin(['Tender Cepat'])]
    df_pp_seleksi = df_pp_umumkan[df_pp_umumkan['metodepengadaan'].isin(['Seleksi'])]

    df_pp_non_etendering = df_pp_umumkan[df_pp_umumkan['metodepengadaan'].isin(['Pengadaan Langsung', 'Penunjukan Langsung'])]
    df_pp_pengadaan_langsung = df_pp_umumkan[df_pp_umumkan['metodepengadaan'].isin(['Pengadaan Langsung'])]
    df_pp_penunjukan_langsung = df_pp_umumkan[df_pp_umumkan['metodepengadaan'].isin(['Penunjukan Langsung'])]

    df_pp_ekatalog = df_pp_umumkan[df_pp_umumkan['metodepengadaan'].isin(['e-Purchasing'])]

    ## Data RUP Paket Swakelola
    df_sw = pd.read_feather(urlDataset + "sirupdsw" + tglTarik + ".ftr")
    df_sw_umumkan = df_sw[df_sw['statusumumkan'] == 'Terumumkan']
    df_sw_inisiasi = df_sw[df_sw['statusumumkan'] == 'Terinisiasi']

    ## Data Struktur Anggaran RUP
    df_rsap = pd.read_feather(urlDataset + "sirupdsa_rsap" + tglTarik + ".ftr")

    ## Data Tender
    df_dts = pd.read_feather(urlDataset + "dtender_dts" + tglTarik[0:4] + ".ftr")
    df_dtks = pd.read_feather(urlDataset + "dtender_dtks" + tglTarik[0:4] + ".ftr")

    ## Data Non Tender
    df_dnts = pd.read_feather(urlDataset + "dntender_dnts" + tglTarik[0:4] + ".ftr")

    ## Data Katalog
    df_depep = pd.read_feather(urlDataset + "dkatalog_depep" + tglTarik[0:4] + ".ftr")

    st.title("INDEKS TATA KELOLA PENGADAAN - " + pilih)

    # Tampilan Pemanfaatan SIRUP
    st.markdown("## **PEMANFAATAN SIRUP**")
    ## Struktur Anggaran
    st.markdown("### Struktur Anggaran")
    belanja_pengadaan = df_rsap['belanja_pengadaan'].sum()
    belanja_pengadaan_print = format_currency(belanja_pengadaan, 'Rp. ', locale='id_ID')
    belanja_operasional = df_rsap['belanja_operasi'].sum()
    belanja_operasional_print = format_currency(belanja_operasional, 'Rp. ', locale='id_ID')
    belanja_modal = df_rsap['belanja_modal'].sum()
    belanja_modal_print = format_currency(belanja_modal, 'Rp. ', locale='id_ID')

    sa1, sa2, sa3 = st.columns(3)
    sa1.metric("Belanja Pengadaan", belanja_pengadaan_print)
    sa2.metric("Belanja Operasional", belanja_operasional_print)
    sa3.metric("Belanja Modal", belanja_modal_print)

    ## Posisi Input RUP
    st.markdown("### Posisi Input RUP")
    
    jumlah_total_rup = df_pp_umumkan.shape[0] + df_sw_umumkan.shape[0]
    nilai_total_rup = df_pp_umumkan['jumlahpagu'].sum() + df_sw_umumkan['jumlahpagu'].sum()
    nilai_total_rup_print = format_currency(nilai_total_rup, 'Rp. ', locale='id_ID')

    pir1, pir2, pir3 = st.columns(3)
    pir1.metric("","Jumlah Total")
    pir2.metric("Jumlah Total Paket RUP", jumlah_total_rup)
    pir3.metric("Nilai Total Paket RUP", nilai_total_rup_print)

    jumlah_rup_umumkan = df_pp_umumkan.shape[0]
    nilai_rup_umumkan = df_pp_umumkan['jumlahpagu'].sum()
    nilai_rup_umumkan_print = format_currency(nilai_rup_umumkan, 'Rp. ', locale='id_ID')

    pirpp1, pirpp2, pirpp3 = st.columns(3)
    pirpp1.metric("","Paket Penyedia")
    pirpp2.metric("Jumlah Total Paket RUP", jumlah_rup_umumkan)
    pirpp3.metric("Nilai Total Paket RUP", nilai_rup_umumkan_print)

    jumlah_rup_sw_umumkan = df_sw_umumkan.shape[0]
    nilai_rup_sw_umumkan = df_sw_umumkan['jumlahpagu'].sum()
    nilai_rup_sw_umumkan_print = format_currency(nilai_rup_sw_umumkan, 'Rp. ', locale='id_ID')
    
    pirsw1, pirsw2, pirsw3 = st.columns(3)
    pirsw1.metric("", "Paket Swakelola")
    pirsw2.metric("Jumlah Total Paket RUP", jumlah_rup_sw_umumkan)
    pirsw3.metric("Nilai Total paket RUP", nilai_rup_sw_umumkan_print)

    ## Persentase RUP
    persen_capaian_rup = (nilai_total_rup / belanja_pengadaan)
    persen_capaian_rup_print = "{:.2%}".format(persen_capaian_rup)

    pr1, pr2, pr3 = st.columns(3)
    pr1.metric("", "Persentase Capaian RUP")
    pr2.metric("Persentase Capaian RUP", persen_capaian_rup_print)
    pr3.metric("", "")

    # Tampilan Pemanfaatan E-Tendering
    st.markdown("## **PEMANFAATAN E-TENDERING**")

    ## Pengumuman E-Tendering
    st.markdown("### Pengumuman E-Tendering")

    jumlah_total_etendering = df_pp_etendering.shape[0]
    nilai_total_etendering = df_pp_etendering['jumlahpagu'].sum()
    nilai_total_etendering_print = format_currency(nilai_total_etendering, 'Rp. ', locale='id_ID')

    et1, et2, et3 = st.columns(3)
    et1.metric("", "Jumlah Total")
    et2.metric("Jumlah Total E-Tendering", jumlah_total_etendering)
    et3.metric("Nilai Total E-Tendering", nilai_total_etendering_print)

    jumlah_etendering_tender = df_pp_tender.shape[0]
    nilai_etendering_tender = df_pp_tender['jumlahpagu'].sum()
    nilai_etendering_tender_print = format_currency(nilai_etendering_tender, 'Rp. ', locale='id_ID')

    ett1, ett2, ett3 = st.columns(3)
    ett1.metric("", "E-Tendering (Tender)")
    ett2.metric("Jumlah E-Tendering (Tender)", jumlah_etendering_tender)
    ett3.metric("Nilai E-Tendering (Tender)", nilai_etendering_tender_print)

    jumlah_etendering_tender_cepat = df_pp_tender_cepat.shape[0]
    nilai_etendering_tender_cepat = df_pp_tender_cepat['jumlahpagu'].sum()
    nilai_etendering_tender_cepat_print = format_currency(nilai_etendering_tender_cepat, 'Rp. ', locale='id_ID')

    ettc1, ettc2, ettc3 = st.columns(3)
    ettc1.metric("", "E-Tendering (Tender Cepat)")
    ettc2.metric("Jumlah E-Tendering (Tender Cepat", jumlah_etendering_tender_cepat)
    ettc3.metric("Nilai E-Tendering (Tender Cepat)", nilai_etendering_tender_cepat_print)

    jumlah_etendering_seleksi = df_pp_seleksi.shape[0]
    nilai_etendering_seleksi = df_pp_seleksi['jumlahpagu'].sum()
    nilai_etendering_seleksi_print = format_currency(nilai_etendering_seleksi, 'Rp. ', locale='id_ID')

    ets1, ets2, ets3 = st.columns(3)
    ets1.metric("", "E-Tendering (Seleksi)")
    ets2.metric("Jumlah E-Tendering (Seleksi)", jumlah_etendering_seleksi)
    ets3.metric("Nilai E-Tendering (Seleksi)", nilai_etendering_seleksi_print)

    ## Realisasi E-Tendering
    st.markdown("### Realisasi E-Tendering")

    jumlah_total_realisasi_etendering = df_dts.shape[0]
    nilai_total_realisasi_etendering = df_dts['pagu'].sum()
    nilai_total_realisasi_etendering_print = format_currency(nilai_total_realisasi_etendering, 'Rp. ', locale='id_ID')

    ret1, ret2, ret3 = st.columns(3)
    ret1.metric("", "Realisasi E-Tendering")
    ret2.metric("Jumlah Total Realisasi E-Tendering", jumlah_total_realisasi_etendering)
    ret3.metric("Nilai Total Realisasi E-Tendering", nilai_total_realisasi_etendering_print)

    ## Persentase E-Tendering
    st.markdown("### Persentase E-Tendering")

    persen_capaian_etendering = (nilai_total_realisasi_etendering / nilai_total_etendering)
    persen_capaian_etendering_print = "{:.2%}".format(persen_capaian_etendering)

    pe1, pe2, pe3 = st.columns(3)
    pe1.metric("", "Persentase E-Tendering")
    pe2.metric("Persentase E-Tendering", persen_capaian_etendering_print)
    pe3.metric("", "")

    # Tampilan Pemanfaatan Non E-Tendering
    st.markdown("## **PEMANFAATAN NON E-TENDERING**")

    ## Pengumuman Non E-Tendering
    st.markdown("### Pengumuman Non E-Tendering")

    jumlah_total_non_etendering = df_pp_non_etendering.shape[0]
    nilai_total_non_etendering = df_pp_non_etendering['jumlahpagu'].sum()
    nilai_total_non_etendering_print = format_currency(nilai_total_non_etendering, 'Rp. ', locale='id_ID')

    net1, net2, net3 = st.columns(3)
    net1.metric("", "Jumlah Total")
    net2.metric("Jumlah Total Non E-Tendering", jumlah_total_non_etendering)
    net3.metric("Nilai Total Non E-Tendering", nilai_total_non_etendering_print)

    jumlah_pengadaan_langsung = df_pp_pengadaan_langsung.shape[0]
    nilai_pengadaan_langsung = df_pp_pengadaan_langsung['jumlahpagu'].sum()
    nilai_pengadaan_langsung_print = format_currency(nilai_pengadaan_langsung, 'Rp. ', locale='id_ID')

    netpl1, netpl2, netpl3 = st.columns(3)
    netpl1.metric("", "Pengadaan Langsung")
    netpl2.metric("Jumlah Non E-Tendering (Pengadaan Langsung)", jumlah_pengadaan_langsung)
    netpl3.metric("Nilai Non E-Tendering (Pengadaan Langsung)", nilai_pengadaan_langsung_print)

    jumlah_penunjukan_langsung = df_pp_penunjukan_langsung.shape[0]
    nilai_penunjukan_langsung = df_pp_penunjukan_langsung['jumlahpagu'].sum()
    nilai_penunjukan_langsung_print = format_currency(nilai_penunjukan_langsung, 'Rp. ', locale='id_ID')

    netpnl1, netpnl2, netpnl3 = st.columns(3)
    netpnl1.metric("", "Penunjukan Langsung")
    netpnl2.metric("Jumlah Non E-Tendering (Penunjukan Langsung)", jumlah_penunjukan_langsung)
    netpnl3.metric("Nilai Non E-Tendering (Penunjukan Langsung)", nilai_penunjukan_langsung_print)   

    ## Realisasi Non E-Tendering 
    st.markdown("### Realisasi Non E-Tendering")

    jumlah_total_realisasi_non_etendering = df_dnts.shape[0]
    nilai_total_realisasi_non_etendering = df_dnts['pagu'].sum()
    nilai_total_realisasi_non_etendering_print = format_currency(nilai_total_realisasi_non_etendering, 'Rp. ', locale='id_ID')

    rnet1, rnet2, rnet3 = st.columns(3)
    rnet1.metric("", "Jumlah Total Realisasi")
    rnet2.metric("Jumlah Total Realisasi Non E-Tendering", jumlah_total_realisasi_non_etendering)
    rnet3.metric("Nilai Total Realisasi Non E-Tendering", nilai_total_realisasi_non_etendering_print)

    jumlah_realisasi_non_etendering_pengadaan_langsung = df_dnts[df_dnts['metode_pengadaan'].isin(['Pengadaan Langsung'])].shape[0]
    nilai_realisasi_non_etendering_pengadaan_langsung = df_dnts[df_dnts['metode_pengadaan'].isin(['Pengadaan Langsung'])]['pagu'].sum()
    nilai_realisasi_non_etendering_pengadaan_langsung_print = format_currency(nilai_realisasi_non_etendering_pengadaan_langsung, 'Rp. ', locale='id_ID')

    rnetpl1, rnetpl2, rnetpl3 = st.columns(3)
    rnetpl1.metric("", "Pengadaan Langsung")
    rnetpl2.metric("Jumlah Realisasi Non E-Tendering (Pengadaan Langsung)", jumlah_realisasi_non_etendering_pengadaan_langsung)
    rnetpl3.metric("Nilai Realisasi Non E-Tendering (Pengadaan Langsung)", nilai_realisasi_non_etendering_pengadaan_langsung_print)

    jumlah_realisasi_non_etendering_penunjukan_langsung = df_dnts[df_dnts['metode_pengadaan'].isin(['Penunjukan Langsung'])].shape[0]
    nilai_realisasi_non_etendering_penunjukan_langsung = df_dnts[df_dnts['metode_pengadaan'].isin(['Penunjukan Langsung'])]['pagu'].sum()
    nilai_realisasi_non_etendering_penunjukan_langsung_print = format_currency(nilai_realisasi_non_etendering_penunjukan_langsung, 'Rp. ', locale='id_ID')

    rnetpnl1, rnetpnl2, rnetpnl3 = st.columns(3)
    rnetpnl1.metric("", "Penunjukan Langsung")
    rnetpnl2.metric("Jumlah Realisasi Non E-Tendering (Penunjukan Langsung)", jumlah_realisasi_non_etendering_penunjukan_langsung)
    rnetpnl3.metric("Nilai Realisasi Non E-Tendering (Penunjukan Langsung)", nilai_realisasi_non_etendering_penunjukan_langsung_print)

    ## Persentase Non E-Tendering
    st.markdown("### Persentase Non E-Tendering")

    persen_capaian_non_etendering = (nilai_total_realisasi_non_etendering / nilai_total_non_etendering)
    persen_capaian_non_etendering_print = "{:.2%}".format(persen_capaian_non_etendering)

    pne1, pne2, pne3 = st.columns(3)
    pne1.metric("", "Persentase Non E-Tendering")
    pne2.metric("Persentase Non E-Tendering", persen_capaian_non_etendering_print)
    pne3.metric("", "")   

    # Tampilan Pemanfaatan E-Katalog
    st.markdown("## **PEMANFAATAN E-KATALOG**")

    ## Pengumuman E-Katalog
    jumlah_total_ekatalog = df_depep.shape[0]
    nilai_total_ekatalog = df_depep['total_harga'].sum()
    nilai_total_ekatalog_print = format_currency(nilai_total_ekatalog, 'Rp. ', locale='id_ID')

    pek1, pek2, pek3 = st.columns(3)
    pek1.metric("", "Pengumuman E-Katalog")
    pek2.metric("Jumlah Total E-Katalog", jumlah_total_ekatalog)
    pek3.metric("Nilai Total E-Katalog", nilai_total_ekatalog_print)

    ## Realisasi E-Katalog
    jumlah_realisasi_ekatalog = df_depep[df_depep['paket_status_str'].isin(['Paket Selesai'])].shape[0]
    nilai_realisasi_ekatalog = df_depep[df_depep['paket_status_str'].isin(['Paket Selesai'])]['total_harga'].sum()
    nilai_realisasi_ekatalog_print = format_currency(nilai_realisasi_ekatalog, 'Rp. ', locale='id_ID')

    rek1, rek2, rek3 = st.columns(3)
    rek1.metric("", "Realisasi E-Katalog")
    rek2.metric("Jumlah Realisasi E-Katalog", jumlah_realisasi_ekatalog)
    rek3.metric("Nilai Realisasi E-Katalog", nilai_realisasi_ekatalog_print)

    ## Persentase E-Katalog
    persen_capaian_ekatalog = (nilai_realisasi_ekatalog / nilai_total_ekatalog)
    persen_capaian_ekatalog_print = "{:.2%}".format(persen_capaian_ekatalog)

    prek1, prek2, prek3 = st.columns(3)
    prek1.metric("", "Persentase E-Katalog")
    prek2.metric("Persentase E-Katalog", persen_capaian_ekatalog_print)
    prek3.metric("", "")

    # Tampilan Pemanfaatan E-Kontrak
    st.markdown("## **PEMANFAATAN E-KONTRAK**")

    ## Pengumuman E-Kontrak
    jumlah_total_ekontrak = jumlah_total_realisasi_etendering
    nilai_total_ekontrak = nilai_total_realisasi_etendering
    nilai_total_ekontrak_print = format_currency(nilai_total_ekontrak, 'Rp. ', locale='id_ID')

    pekon1, pekon2, pekon3 = st.columns(3)
    pekon1.metric("", "Pengumuman E-Kontrak")
    pekon2.metric("Jumlah Total E-Kontrak", jumlah_total_ekontrak)
    pekon3.metric("Nilai Total E-Kontrak", nilai_total_ekontrak_print)

    ## Realisasi E-Kontrak
    jumlah_realisasi_ekontrak = df_dtks[df_dtks['status_sppbj'].isin(['Terkirim'])].shape[0]
    nilai_realisasi_ekontrak = df_dtks[df_dtks['status_sppbj'].isin(['Terkirim'])]['nilai_kontrak_sppbj'].sum()
    nilai_realisasi_ekontrak_print = format_currency(nilai_realisasi_ekontrak, 'Rp. ', locale='id_ID')

    rekon1, rekon2, rekon3 = st.columns(3)
    rekon1.metric("", "Realisasi E-Kontrak")
    rekon2.metric("Jumlah Realisasi E-Kontrak", jumlah_realisasi_ekontrak)
    rekon3.metric("Nilai Realisasi E-Kontrak", nilai_realisasi_ekontrak_print)

    ## Persentase E-Kontrak
    persen_capaian_ekontrak = (nilai_realisasi_ekontrak / nilai_total_ekontrak)
    persen_capaian_ekontrak_print = "{:.2%}".format(persen_capaian_ekontrak)

    prekon1, prekon2, prekon3 = st.columns(3)
    prekon1.metric("", "Persentase E-Kontrak")
    prekon2.metric("Persentase E-Kontrak", persen_capaian_ekontrak_print)
    prekon3.metric("", "")