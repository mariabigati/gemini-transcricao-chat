import sys
import os
import streamlit as st
import youtube_utils
import gemini_utils
from googletrans import Translator

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Cinzel Decorative', serif;
        }

        /* Tornar o cabeçalho transparente e brilhante */
        header {
            background-color: rgba(0, 0, 0, 0.2) !important;
            backdrop-filter: blur(10px) !important;
            box-shadow: 0 4px 10px rgba(0, 255, 255, 0.3) !important;
        }

        .custom-title {
            font-family: 'Cinzel Decorative', serif;
            font-size: 60px;
            text-align: center;
            color: rgba(255, 255, 255, 0.95);
            letter-spacing: 3px;
            margin: 40px 0;
            text-shadow:
                0 0 6px rgba(255, 255, 255, 0.6),
                0 0 12px rgba(173, 216, 230, 0.5),
                0 0 20px rgba(173, 216, 230, 0.4),
                0 0 40px rgba(0, 191, 255, 0.2);
            animation: starlight 3s ease-in-out infinite alternate;
        }

        @keyframes starlight {
            0% {
                text-shadow:
                    0 0 4px rgba(255, 255, 255, 0.3),
                    0 0 10px rgba(173, 216, 230, 0.2),
                    0 0 18px rgba(173, 216, 230, 0.2),
                    0 0 30px rgba(0, 191, 255, 0.1);
            }
            100% {
                text-shadow:
                    0 0 10px rgba(255, 255, 255, 0.8),
                    0 0 20px rgba(173, 216, 230, 0.6),
                    0 0 30px rgba(173, 216, 230, 0.4),
                    0 0 50px rgba(0, 191, 255, 0.3);
            }
        }

        .stApp {
            position: relative;
            background-image: url(https://i.gifer.com/5cU5.gif);
            background-repeat: no-repeat;
            background-size: cover;
            height: 100vh;
        }

        .stApp::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.5);
            z-index: 0;
        }

        .stButton>button {
            background-color: rgba(255, 255, 255, 0.0); 
            color: white;
            border-radius: 12px;
            padding: 12px 25px;
            font-size: 16px;
            border: 2px solid rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(10px);
            animation: pulseGlow 2.5s ease-in-out infinite;
            transition: all 0.3s ease;
            background-color: rgba(255, 255, 255, 0.2);
        }

        .stButton>button:hover {
            background-color: rgba(102, 255, 204, 0.1); 
            transform: scale(1.1);
            color: white !important;
            border: 2px solid rgba(102, 255, 204, 1);
            box-shadow: 0 0 30px rgba(102, 255, 204, 0.9);
            backdrop-filter: blur(5px);
        }

        .stButton>button:focus,
        .stButton>button:active {
            border: 2px solid rgba(72, 201, 176, 1);
            background-color: rgba(255, 255, 255, 0.05);
            box-shadow: 0 0 25px rgba(72, 201, 176, 0.8);
            color: white !important;
            backdrop-filter: blur(5px);
        }

        .stTextInput>div>input {
            background-color: rgba(255, 255, 255, 0.05);
            color: white;
            font-size: 16px;
            padding: 12px 20px;
            border-radius: 12px;
            border: 2px solid rgba(255, 255, 255, 0.6);
            box-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(6px);
            transition: all 0.3s ease;
        }

        .stTextInput>div>input:focus {
            outline: none;
            border: 2px solid rgba(102, 255, 204, 0.8);
            box-shadow: 0 0 20px rgba(102, 255, 204, 0.7);
            background-color: rgba(255, 255, 255, 0.08);
        }

        .transcript-card {
            background-color: rgba(255, 255, 255, 0.2); 
            padding: 25px;
            border-radius: 12px;
            margin-top: 20px;
            border: 1px solid rgba(255, 255, 255, 0.3); 
            color: white;
            font-family: 'Arial', sans-serif; 
            font-size: 14px; 
            line-height: 1.8; 
            text-align: center; 
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7); 
            box-shadow: 0 0 15px rgba(255, 255, 255, 0.3);
            backdrop-filter: blur(5px); 
            word-wrap: break-word; 
            white-space: pre-wrap; 
        }

        .stButton {
            margin-top: 25px;
        }

        .corner-image {
            position: fixed;
            bottom: 0;
            z-index: 1;
            opacity: 0.95;
        }

        .corner-image.right {
            right: 0;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="corner-image right">
        <img src="https://i.gifer.com/yuD.gif" width="300">
    </div>
""", unsafe_allow_html=True)


def main():
    st.markdown('<div class="custom-title">Sailor Transcripts</div>', unsafe_allow_html=True)

    video_url = st.text_input("Insira a URL do vídeo do Youtube:", "https://www.youtube.com/watch?v=3LqKXV1-6R4")

    if video_url:
        try:
            video_id = youtube_utils.extract_video_id(video_url)
            video_title = youtube_utils.get_video_title(video_url)
            transcript = youtube_utils.get_transcript(video_id)

            if not transcript:
                st.error("Não foi possível obter a transcrição do vídeo.")
                return

            if video_title:
                st.subheader(f"Título do Vídeo: {video_title}")

            st.subheader("Transcrição (Inglês)")
            st.markdown(
                f'<div class="transcript-card">{transcript.replace("\n", "<br>")}</div>',
                unsafe_allow_html=True
            )

            if st.button("Traduzir para Português"):
                translator = Translator()
                translated = translator.translate(transcript, src='en', dest='pt').text

                st.subheader("Tradução (Português)")
                st.markdown(
                    f'<div class="transcript-card">{translated.replace("\n", "<br>")}</div>',
                    unsafe_allow_html=True
                )

            if st.button("Gerar Resumo com Gemini"):
                gemini_utils.configure_gemini()
                summary = gemini_utils.generate_summary(transcript)

                if summary:
                    st.subheader("Resumo Gerado por Gemini:")
                    st.markdown(
                        f'<div class="transcript-card">{summary.replace("\n", "<br>")}</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.error("Falha ao gerar o resumo com Gemini.")

        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")


if __name__ == "__main__":
    main()
