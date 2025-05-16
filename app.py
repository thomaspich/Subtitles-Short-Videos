import os
import json
import whisper
import streamlit as st
from moviepy import VideoFileClip, CompositeVideoClip
from extensions.MoviePyExtension import TextClip

# --- Fonctions utiles ---

def split_segments_into_short_segments(segments, max_words=5):
    new_segments = []
    for segment in segments:
        words = segment['text'].strip().split()
        start_time = segment['start']
        end_time = segment['end']
        duration = end_time - start_time

        if not words:
            continue

        duration_per_word = duration / len(words)

        for i in range(0, len(words), max_words):
            chunk_words = words[i:i + max_words]
            chunk_text = " ".join(chunk_words)
            chunk_start = start_time + (i * duration_per_word)
            chunk_end = chunk_start + (len(chunk_words) * duration_per_word)

            new_segments.append({
                "start": round(chunk_start, 2),
                "end": round(chunk_end, 2),
                "text": chunk_text
            })
    return new_segments

def create_subtitle_clips(segments, video_width, video_height, font_path="Montserrat-Bold", font_size=60, style="classique"):
    subtitle_clips = []
    for segment in segments:
        if style == "classique (blanc + contour noir)":
            txt_clip = (TextClip(text=segment['text'].upper(),
                                font=font_path,
                                font_size=font_size,
                                color='white',
                                stroke_color='black',
                                stroke_width=5,
                                method='caption',
                                size=(int(video_width * 0.8), None),
                                text_align='center')
                                    .with_start(segment['start'])
                                    .with_end(segment['end'])
                                    .with_position(("center", video_height * 0.65)))
            subtitle_clips.append(txt_clip)
        
        elif style == "bulle blanche arrondie (style TikTok)":
            txt_clip = (TextClip(text=segment['text'],
                                font=font_path,
                                font_size=font_size,
                                color='black',
                                bg_color='white',
                                method='caption',
                                size=(int(video_width * 0.6), None),
                                corner_radius=20,
                                padding=(20,20,20,20),
                                text_align='center')
                                    .with_start(segment['start'])
                                    .with_end(segment['end'])
                                    .with_position(("center", video_height * 0.65)))
            subtitle_clips.append(txt_clip)
            
    return subtitle_clips

def add_subtitles_to_video(video_path, segments, output_path, font_path="Montserrat-Bold", font_size=60, style="classique", logger=None):
    video = VideoFileClip(video_path)
    subtitles = create_subtitle_clips(segments, video.w, video.h, font_path=font_path, font_size=font_size, style=style)
    final = CompositeVideoClip([video] + subtitles)
    final.write_videofile(output_path, codec="libx264", fps=30, audio_codec="aac", preset="medium", logger=logger)

# --- Interface Streamlit ---

st.set_page_config(layout="centered", page_title="Subtitles for Short Content")
st.title("📝 Éditeur de sous-titres avec Whisper & MoviePy")

video_file = st.file_uploader("🎥 Téléverse ta vidéo", type=["mp4", "mov"])
font_path = st.text_input("🔤 Chemin de la police (.ttf ou .otf)", value="/Library/Fonts/insolent.otf")

if video_file:
    os.makedirs("temp", exist_ok=True)
    video_temp_path = f"temp/temp_video.{video_file.name.split('.')[-1]}"
    with open(video_temp_path, "wb") as f:
        f.write(video_file.read())

    audio_path = "temp/temp_audio.wav"
    video = VideoFileClip(video_temp_path)
    video.audio.write_audiofile(audio_path)

    if "segments" not in st.session_state:
        st.info("⏳ Transcription en cours avec Whisper...")
        model = whisper.load_model("large")
        result = model.transcribe(audio_path)
        segments = split_segments_into_short_segments(result["segments"])
        st.session_state["segments"] = segments
        st.success("✅ Transcription terminée. Tu peux corriger les sous-titres.")

    c1, c2 = st.columns(2)

    with c1:
        subtitle_style = st.selectbox(
            "🎨 Style des sous-titres",
            ["classique (blanc + contour noir)", "bulle blanche arrondie (style TikTok)"]
        )
    with c2:
        font_size = st.slider("🔠 Taille de la police", min_value=30, max_value=100, value=60, step=2)

    col1, col2 = st.columns(2)
    edited_segments = []

    # --- Colonne de gauche : édition + boutons
    with col1:
        st.subheader("✍️ Édition des sous-titres")
        with st.container(height=500):
            for i, seg in enumerate(st.session_state["segments"]):
                key = f"segment_{i}"
               # if key not in st.session_state:
                    #st.session_state[key] = seg["text"]
                start_key = f"start_{i}"
                end_key = f"end_{i}"
                if start_key not in st.session_state:
                    st.session_state[start_key] = seg["start"]
                if end_key not in st.session_state:
                    st.session_state[end_key] = seg["end"]
                
                col_start, col_end = st.columns([1, 1])

                start_time = col_start.number_input("⏱️ Début (s)", value=st.session_state[start_key], key=start_key, step=0.1, format="%.2f")
                end_time = col_end.number_input("⏱️ Fin (s)", value=st.session_state[end_key], key=end_key, step=0.1, format="%.2f")

                if key not in st.session_state:
                    st.session_state[key] = seg["text"]
                
                text = st.text_area("💬 Texte", value=st.session_state[key], key=key, height=80)
                #start_time = st.number_input("⏱️ Début (s)", value=st.session_state[start_key], key=start_key, step=0.1, format="%.2f")
                #end_time = st.number_input("⏱️ Fin (s)", value=st.session_state[end_key], key=end_key, step=0.1, format="%.2f")
                st.markdown("""
   
                """, unsafe_allow_html=True)
                #text = st.text_input(
                 #   f"[{seg['start']}s → {seg['end']}s]",
                  #  value=st.session_state[key],
                   # key=key
                #)
                edited_segments.append({
                    "start": start_time,
                    "end": end_time,
                    "text": text
                })

    # --- Colonne de droite : aperçu vidéo + sous-titres dynamiques
    with col2:
        st.subheader("🎬 Vidéo")
        st.video(video_temp_path)
    # --- Boutons d'action
    st.markdown("---")
    col_left, col_right = st.columns(2)

    with col_left:
        if st.button("💾 Sauvegarder les sous-titres en JSON"):
            with open("subtitles_edited.json", "w", encoding="utf-8") as f:
                json.dump(edited_segments, f, ensure_ascii=False, indent=2)
            st.success("✅ Sous-titres sauvegardés dans subtitles_edited.json")

    with col_right:
        if st.button("🎥 Générer la vidéo finale"):
            st.info("⏳ La vidéo est en cours de génération")
            output_path = "video_sous_titres.mp4"
            add_subtitles_to_video(video_temp_path, edited_segments, output_path, font_path, font_size=font_size, style=subtitle_style)
            st.success("✅ Vidéo générée avec succès !")
            st.video(output_path)
            with open(output_path, "rb") as f:
                st.download_button(
                    label="📥 Télécharger la vidéo",
                    data=f.read(),
                    file_name="video_sous_titres.mp4",
                    mime="video/mp4"
                )