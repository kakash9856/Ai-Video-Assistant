


import streamlit as st
import os
import tempfile
from pathlib import Path

from dotenv import load_dotenv
from main import run_pipeline
from core.rag_engine import ask_question

load_dotenv()

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
    }

    .main-title {
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        color: #ffffff;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #a0aec0;
        font-size: 16px;
        margin-bottom: 30px;
    }

    .section-heading {
        font-size: 23px;
        font-weight: 700;
        color: #ffffff;
        margin-top: 10px;
    }

    div[data-testid="stMetric"] {
        background-color: #1c2333;
        border: 1px solid #30394d;
        padding: 15px;
        border-radius: 12px;
    }

    .stButton button {
        border-radius: 10px;
        font-weight: 600;
    }

    .info-card {
        background-color: #1c2333;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #30394d;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)


# ---------------- SESSION STATE ----------------

if "result" not in st.session_state:
    st.session_state.result = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ---------------- HEADER ----------------

st.markdown(
    '<div class="main-title">🎬 AI Video Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Transform videos and meetings into intelligent insights'
    '</div>',
    unsafe_allow_html=True
)


# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("⚙️ Settings")

    st.markdown("---")

    st.subheader("🌐 Language")

    language = st.selectbox(
        "Select transcription language",
        ["english", "hinglish"],
        index=0
    )

    st.markdown("---")

    st.subheader("📌 Features")

    st.write("🎙️ Whisper Transcription")
    st.write("📝 AI Summarization")
    st.write("✅ Action Item Extraction")
    st.write("🔑 Key Decision Extraction")
    st.write("💬 RAG-based Chat")

    st.markdown("---")

    if st.button("🗑️ Clear All Data", use_container_width=True):
        st.session_state.result = None
        st.session_state.chat_history = []
        st.rerun()


# ---------------- INPUT SECTION ----------------

st.markdown(
    '<div class="section-heading">📥 Upload Your Video or Audio</div>',
    unsafe_allow_html=True
)

input_type = st.radio(
    "Choose input method",
    ["YouTube URL", "Upload Audio / Video"],
    horizontal=True
)

source = None
uploaded_file = None

if input_type == "YouTube URL":

    source = st.text_input(
        "Enter YouTube video URL",
        placeholder="https://www.youtube.com/watch?v=..."
    )

else:

    uploaded_file = st.file_uploader(
        "Upload your audio or video file",
        type=[
            "mp3", "wav", "m4a",
            "mp4", "mkv", "webm",
            "mpeg", "mpga"
        ]
    )


# ---------------- PROCESSING ----------------

if st.button(
    "🚀 Generate AI Insights",
    type="primary",
    use_container_width=True
):

    final_source = None

    if input_type == "YouTube URL":

        if not source or not source.strip():
            st.error("Please enter a valid YouTube URL.")

        elif not (
            "youtube.com/" in source.lower()
            or "youtu.be/" in source.lower()
        ):
            st.error("Please enter a valid YouTube URL.")

        else:
            final_source = source.strip()

    else:

        if uploaded_file is None:
            st.error("Please upload an audio or video file.")

        else:
            try:
                os.makedirs("uploads", exist_ok=True)

                suffix = Path(uploaded_file.name).suffix

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=suffix,
                    dir="uploads"
                ) as temp_file:

                    temp_file.write(uploaded_file.getbuffer())
                    final_source = temp_file.name

            except Exception as e:
                st.error(f"File upload failed: {e}")

    if final_source:

        try:
            with st.status(
                "AI is processing your video...",
                expanded=True
            ) as status:

                st.write("📥 Processing audio/video...")
                st.write("🎙️ Generating transcription...")
                st.write("🧠 Creating AI summary...")
                st.write("📌 Extracting action items and decisions...")
                st.write("🔍 Building RAG knowledge base...")

                result = run_pipeline(
                    final_source,
                    language
                )

                status.update(
                    label="Processing completed successfully!",
                    state="complete",
                    expanded=False
                )

            st.session_state.result = result
            st.session_state.chat_history = []

            st.success("Your AI Video Assistant report is ready!")

        except Exception as e:
            st.error(f"Processing failed: {str(e)}")


# ---------------- RESULTS SECTION ----------------

result = st.session_state.result

if result:

    st.markdown("---")

    st.markdown(
        f'<div class="main-title" style="font-size:28px;">'
        f'📌 {result["title"]}</div>',
        unsafe_allow_html=True
    )

    st.markdown("")

    # ---------------- TABS ----------------

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Summary",
        "✅ Action Items",
        "🔑 Decisions",
        "🎙️ Transcript",
        "💬 Chat with Video"
    ])

    # ---------------- SUMMARY ----------------

    with tab1:

        st.subheader("📝 AI Generated Summary")

        st.markdown(
            f'<div class="info-card">{result["summary"]}</div>',
            unsafe_allow_html=True
        )

        st.download_button(
            "⬇️ Download Summary",
            data=str(result["summary"]),
            file_name="ai_summary.txt",
            mime="text/plain"
        )

    # ---------------- ACTION ITEMS ----------------

    with tab2:

        st.subheader("✅ Action Items")

        st.markdown(result["action_items"])

        st.markdown("---")

        st.subheader("❓ Open Questions")

        st.markdown(result["open_questions"])

    # ---------------- KEY DECISIONS ----------------

    with tab3:

        st.subheader("🔑 Key Decisions")

        st.markdown(result["key_decisions"])

    # ---------------- TRANSCRIPT ----------------

    with tab4:

        st.subheader("🎙️ Full Transcript")

        st.text_area(
            "Transcribed Content",
            value=result["transcript"],
            height=450
        )

        st.download_button(
            "⬇️ Download Transcript",
            data=result["transcript"],
            file_name="transcript.txt",
            mime="text/plain"
        )

    # ---------------- RAG CHAT ----------------

    with tab5:

        st.subheader("💬 Chat with Your Video")

        st.caption(
            "Ask questions about your video or meeting transcript."
        )

        # Display previous messages

        for message in st.session_state.chat_history:

            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input

        question = st.chat_input(
            "Ask something about your video..."
        )

        if question:

            st.session_state.chat_history.append({
                "role": "user",
                "content": question
            })

            with st.chat_message("user"):
                st.markdown(question)

            with st.chat_message("assistant"):

                with st.spinner("Thinking..."):

                    try:
                        answer = ask_question(
                            result["rag_chain"],
                            question
                        )

                        st.markdown(answer)

                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": str(answer)
                        })

                    except Exception as e:

                        st.error(f"Chat error: {str(e)}")

            st.rerun()


# ---------------- FOOTER ----------------

st.markdown("---")

st.markdown(
    "<center style='color:#8492a6;'>"
    "Built with Python | Streamlit | Whisper | LangChain | RAG"
    "</center>",
    unsafe_allow_html=True
)
