import streamlit as st
import requests
import os

API_BASE = os.environ.get("API_BASE", "http://api:8000")

# Configuració de la pàgina
st.set_page_config(page_title="Laboratori Multimèdia", page_icon="🎛️", layout="wide")

# Títol inicial
st.title("Pràctica Multimèdia — Monster API GUI")

# Barra lateral amb les opcions
with st.sidebar:
    st.header("Menú")
    section = st.radio(
        "Selecciona secció",
        ["Tots els fitxers", "Info", "Transformacions", "Còdecs", "Escala d'encoding", "Algoritmes"]
    )

def api_get(path):
    r = requests.get(f"{API_BASE}{path}")
    r.raise_for_status()
    return r.json()

def api_post(path, json=None):
    r = requests.post(f"{API_BASE}{path}", json=json)
    r.raise_for_status()
    return r.json()

# Secció Fitxers
if section == "Tots els fitxers":
    st.subheader("📦 Fitxers disponibles a /data")
    try:
        files = sorted(os.listdir("/data"))
        st.write(files if files else "No s'han trobat fitxers a /data")
    except Exception:
        st.info("Munta ./videos a /data dins del contenidor GUI per llistar fitxers.")

# Secció Info
elif section == "Info":
    st.subheader("Informació del vídeo")
    try:
        files = sorted(os.listdir("/data"))
        filename = st.selectbox("Selecciona fitxer", files) if files else None
        if filename and st.button("Obtenir informació"):
            resp = api_get(f"/video/info/{filename}")
            col1, col2 = st.columns(2)
            with col1:
                st.json(resp)
            with col2:
                st.metric("Resolució", f"{resp.get('width')}x{resp.get('height')}")
                st.metric("Durada (s)", resp.get("duration_seconds"))
                st.metric("Bitrate (bps)", resp.get("bit_rate"))
    except Exception:
        st.info("No es pot accedir a /data.")

# Secció Transformacions
elif section == "Transformacions":
    st.subheader("Redimensionar / Chroma / BN / Superposicions")
    try:
        files = sorted(os.listdir("/data"))
        filename = st.selectbox("Fitxer", files, key="tfile") if files else None
        if filename:
            colA, colB, colC = st.columns(3)
            with colA:
                st.caption("Redimensionar")
                w = st.number_input("Amplada", 64, 4096, 1280)
                h = st.number_input("Alçada", 64, 4096, 720)
                if st.button("Redimensionar"):
                    resp = api_post(f"/image/resize/{filename}", {"width": w, "height": h})
                    st.success(resp)
            with colB:
                st.caption("Submostreig de chroma")
                subs = st.selectbox("pix_fmt", ["yuv420p", "yuv422p", "yuv444p"])
                if st.button("Aplicar chroma"):
                    resp = api_post(f"/video/chroma-subsampling/{filename}", {"subsampling": subs})
                    st.success(resp)
            with colC:
                st.caption("Compressió BN / Superposicions")
                if st.button("Comprimir BN"):
                    resp = api_post(f"/image/bw-compression/{filename}")
                    st.success(resp)
                if st.button("Mostrar vectors de moviment"):
                    resp = api_post(f"/video/show-motion/{filename}")
                    st.success(resp)
                if st.button("Mostrar histograma YUV"):
                    resp = api_post(f"/video/yuv-histogram/{filename}")
                    st.success(resp)
    except Exception:
        st.info("No es pot accedir a /data.")

# Secció Còdecs
elif section == "Còdecs":
    st.subheader("Convertir a VP8 / VP9 / H.265 / AV1")
    try:
        files = sorted(os.listdir("/data"))
        filename = st.selectbox("Fitxer", files, key="cfile") if files else None
        if filename and st.button("Convertir"):
            resp = api_post(f"/video/convert-codecs/{filename}")
            st.success(resp)
    except Exception:
        st.info("No es pot accedir a /data.")

# Secció Escala d'encoding
elif section == "Escala d'encoding":
    st.subheader("Escala d'encoding")
    try:
        files = sorted(os.listdir("/data"))
        filename = st.selectbox("Fitxer", files, key="lfile") if files else None
        if filename and st.button("Generar escala"):
            resp = api_post(f"/video/encoding-ladder/{filename}")
            st.success(resp)
            rows = []
            for r in resp["results"]:
                v = r["variant"]
                out = r["result"].get("output_file")
                rows.append({"variant": v, "output_file": out, "status": r["result"].get("status", "error")})
            st.table(rows)
    except Exception:
        st.info("No es pot accedir a /data.")

# Secció Algoritmes
elif section == "Algoritmes":
    st.subheader("Zona d'algoritmes")
    col1, col2 = st.columns(2)
    with col1:
        st.caption("RGB → YUV")
        r = st.number_input("R", 0, 255, 128)
        g = st.number_input("G", 0, 255, 128)
        b = st.number_input("B", 0, 255, 128)
        if st.button("Convertir"):
            resp = api_post("/converter/rgb-to-yuv", {"r": r, "g": g, "b": b})
            st.success(resp)
    with col2:
        st.caption("RLE")
        seq = st.text_input("Seqüència (separada per comes)", "1,0,0,0,3,0,2")
        if st.button("Executar RLE"):
            data = [int(x.strip()) for x in seq.split(",") if x.strip()]
            resp = api_post("/algorithm/rle", {"data": data})
            st.success(resp)
    st.caption("Serpentine / DCT / DWT")
    mat_text = st.text_area("Matriu (files separades per ;)", "1,2,3;4,5,6;7,8,9")
    matrix = [[float(y.strip()) for y in row.split(",")] for row in mat_text.split(";") if row.strip()]
    c1, c2, c3 = st.columns(3)
    if c1.button("Serpentine"):
        resp = api_post("/algorithm/serpentine", {"matrix": matrix})
        st.success(resp)
    if c2.button("DCT"):
        resp = api_post("/algorithm/dct", {"matrix": matrix})
        st.success(resp)
    if c3.button("DWT"):
        resp = api_post("/algorithm/dwt", {"matrix": matrix})