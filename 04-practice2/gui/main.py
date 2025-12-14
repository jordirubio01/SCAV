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
        ["Tots els fitxers", "Info", "Transformacions", "BBB Container", "Còdecs", "Encoding ladder", "Algoritmes"]
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
    st.subheader("📦 Fitxers disponibles a /videos")
    try:
        files = sorted(os.listdir("/data"))
        if files:
            for filename in files:
                st.caption(f"📄 {filename}")
        else:
            st.warning("No s'han trobat fitxers a /data")
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
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Durada (s)", resp.get("duration_seconds"))
                st.metric("Mida (bytes)", f"{int(resp.get('size_bytes')):,}")
                st.metric("Bitrate (bps)", f"{int(resp.get('bit_rate')):,}")
            with col2:
                st.metric("Còdec de vídeo", resp.get("video_codec"))
                st.metric("Resolució", f"{resp.get('width')}x{resp.get('height')}")
            with col3:
                st.metric("Còdec d'àudio", resp.get("audio_codec"))
                sample_rate = resp.get("sample_rate")
                try:
                    sr_value = f"{int(sample_rate):,}"
                except (ValueError, TypeError):
                    sr_value = str(sample_rate)
                st.metric("Sample rate (Hz)", sr_value)
            resp_tracks = api_get(f"/video/tracks/{filename}")
            st.metric("Nombre de pistes", resp_tracks["num_tracks"])
            st.write(f"Tipus de pistes: {', '.join(resp_tracks['track_types'])}")
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
                    st.success("✔ Imatge redimensionada correctament")
                    st.write(f"Nou fitxer: **{resp.get('output_file','?')}**")
            with colB:
                st.caption("Submostreig de chroma")
                subs = st.selectbox("pix_fmt", ["yuv420p", "yuv422p", "yuv444p"])
                if st.button("Aplicar chroma"):
                    resp = api_post(f"/video/chroma-subsampling/{filename}", {"subsampling": subs})
                    st.success("✔ Submostreig de chroma aplicat")
                    st.write(f"Format de píxel: **{resp.get('pix_fmt','?')}**")
            with colC:
                st.caption("Compressió BN / Superposicions")
                if st.button("Comprimir BN"):
                    resp = api_post(f"/image/bw-compression/{filename}")
                    st.success("✔ Compressió en blanc i negre feta")
                    st.write(f"Fitxer de sortida: **{resp.get('output_file','?')}**")
                if st.button("Mostrar vectors de moviment"):
                    resp = api_post(f"/video/show-motion/{filename}")
                    st.success("✔ Vídeo amb vectors de moviment generat")
                    st.write(f"Fitxer de sortida: **{resp.get('output_file','?')}**")
                if st.button("Mostrar histograma YUV"):
                    resp = api_post(f"/video/yuv-histogram/{filename}")
                    st.success("✔ Histograma YUV generat")
                    st.write(f"Fitxer de sortida: **{resp.get('output_file','?')}**")
    except Exception:
        st.info("No es pot accedir a /data.")

# Secció BBB Container
elif section == "BBB Container":
    st.subheader("Crear contenidor Big Buck Bunny")
    try:
        files = sorted(os.listdir("/data"))
        filename = st.selectbox("Fitxer", files, key="bbbfile") if files else None
        if filename and st.button("Crear BBB Container"):
            resp = api_post(f"/video/create-bbb-container/{filename}")
            st.success("✔ Contenidor BBB creat")
            st.write(f"Fitxer de sortida: **{resp.get('output_file','?')}**")
            st.write(f"Durada: {resp.get('duration')}")
            st.write(f"Pistes d'àudio: {', '.join(resp.get('audio_tracks', []))}")
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
            st.success("✔ Conversió a múltiples còdecs completada")
            for codec, result in resp.items():
                st.write(f"**{codec.upper()}** → {result.get('output_file','?')} (estat: {result.get('status','?')})")
    except Exception:
        st.info("No es pot accedir a /data.")

# Secció Encoding Ladder
elif section == "Encoding ladder":
    st.subheader("Encoding ladder")
    try:
        files = sorted(os.listdir("/data"))
        filename = st.selectbox("Fitxer", files, key="lfile") if files else None
        if filename and st.button("Generar encoding ladder"):
            resp = api_post(f"/video/encoding-ladder/{filename}")
            st.success("✔ Encoding ladder generat")
            rows = []
            for r in resp["results"]:
                v = r["variant"]
                out = r["result"].get("output_file")
                rows.append({"Variant": v, "Fitxer de sortida": out, "Estat": r["result"].get("status", "error")})
            st.table(rows)
    except Exception:
        st.info("No es pot accedir a /data.")

# Secció Algoritmes
elif section == "Algoritmes":
    st.subheader("Zona d'algoritmes")

    # RGB a YUV
    st.caption("RGB a YUV")
    r = st.number_input("R", 0, 255, 128)
    g = st.number_input("G", 0, 255, 128)
    b = st.number_input("B", 0, 255, 128)
    if st.button("Convertir RGB a YUV"):
        resp = api_post("/converter/rgb-to-yuv", {"r": r, "g": g, "b": b})
        yuv = resp["output_yuv"]
        col1, col2, col3 = st.columns(3)
        col1.metric("Y", f"{yuv['y']:.2f}")
        col2.metric("U", f"{yuv['u']:.2f}")
        col3.metric("V", f"{yuv['v']:.2f}")

    # YUV a RGB
    st.caption("YUV a RGB")
    y = st.number_input("Y", 0.0, 255.0, 128.0)
    u = st.number_input("U", 0.0, 255.0, 128.0)
    v = st.number_input("V", 0.0, 255.0, 128.0)
    if st.button("Convertir YUV a RGB"):
        resp = api_post("/converter/yuv-to-rgb", {"y": y, "u": u, "v": v})
        rgb = resp["output_rgb"]
        col1, col2, col3 = st.columns(3)
        col1.metric("R", f"{rgb['r']:.2f}")
        col2.metric("G", f"{rgb['g']:.2f}")
        col3.metric("B", f"{rgb['b']:.2f}")

    # RLE
    st.caption("Run Length Encoding")
    seq = st.text_input("Seqüència (separada per comes)", "1,0,0,0,3,0,2")
    if st.button("Executar RLE"):
        data = [int(x.strip()) for x in seq.split(",") if x.strip()]
        resp = api_post("/algorithm/rle", {"data": data})
        st.write(f"Longitud original: {resp['input_length']}")
        st.write(f"Longitud codificada: {resp['encoded_length']}")
        st.write(f"Ratio compressió: {resp['compression_ratio_percent']}%")
        st.text(f"Seqüència codificada: {resp['encoded_data']}")

    # Serpentine / DCT / DWT
    st.caption("Serpentine / DCT / DWT")
    mat_text = st.text_area("Matriu (files separades per ';')", "1,2,3;4,5,6;7,8,9")
    matrix = [[float(y.strip()) for y in row.split(",")] for row in mat_text.split(";") if row.strip()]
    c1, c2, c3 = st.columns(3)
    if c1.button("Serpentine"):
        resp = api_post("/algorithm/serpentine", {"matrix": matrix})
        st.write("Resultat Serpentine:")
        st.text(resp["result"])
    if c2.button("DCT"):
        resp = api_post("/algorithm/dct", {"matrix": matrix})
        st.write("Coeficients DCT:")
        st.table(resp["dct_coefficients"])
    if c3.button("DWT"):
        resp = api_post("/algorithm/dwt", {"matrix": matrix})
        st.write("Coeficients DWT:")
        st.table(resp["dwt_coefficients"])

# Peu de pàgina
st.markdown("---")
st.caption("\n\nUniversitat Pompeu Fabra (UPF), Curs 2025-26, Sistemes de Codificació d'Àudio i Vídeo.")
st.caption("Autors: Jordi Rubio Arbona (NIA 266981) i Lluc Sayols Hidalgo (NIA 267172)")