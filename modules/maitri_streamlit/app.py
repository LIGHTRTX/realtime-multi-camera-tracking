import streamlit as st
import sqlite3
import datetime
import os
import cv2
import tempfile
import matplotlib.pyplot as plt
import av

from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
from process_frame import ArmCurlAnalyzer


DB_PATH="astronauts.db"

st.set_page_config(page_title="MAITRI Wellness",layout="wide")


# ---------------- DATABASE ----------------

def init_db():
    conn=sqlite3.connect(DB_PATH)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS diary(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        astronaut TEXT,
        text TEXT,
        emotion TEXT,
        stress TEXT,
        reply TEXT,
        date TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()


def log_entry(a,t,e,s,r):
    conn=sqlite3.connect(DB_PATH)
    conn.execute(
    "INSERT INTO diary (astronaut,text,emotion,stress,reply,date) VALUES (?,?,?,?,?,?)",
    (a,t,e,s,r,str(datetime.datetime.now())))
    conn.commit()
    conn.close()


def get_history(a):
    conn=sqlite3.connect(DB_PATH)
    rows=conn.execute(
    "SELECT text,emotion,stress,reply,date FROM diary WHERE astronaut=? ORDER BY id DESC LIMIT 20",
    (a,)).fetchall()
    conn.close()
    return rows[::-1]


# ---------------- EMOTION DETECTION ----------------

def detect_emotion(text):

    t=text.lower()

    if any(w in t for w in ["sad","lonely","miss"]):
        return "Sad","Medium"

    if any(w in t for w in ["stress","overwhelm","pressure"]):
        return "Stressed","High"

    if any(w in t for w in ["happy","good","great"]):
        return "Positive","Stable"

    if any(w in t for w in ["tired","sleep","fatigue"]):
        return "Fatigued","Low"

    return "Neutral","Stable"


# ---------------- MAITRI RESPONSE ENGINE ----------------

def call_llm(messages,system):

    user_text=messages[-1]["content"].lower()

    if "sad" in user_text or "lonely" in user_text:

        return (
        "I hear the weight in your words. Long missions can amplify feelings of isolation.\n\n"
        "Remember that emotional cycles are normal during extended spaceflight. Even the most experienced astronauts "
        "report moments where the silence of space feels overwhelming.\n\n"
        "Let's try a small grounding exercise together:\n"
        "• inhale slowly for 4 seconds\n"
        "• hold for 4 seconds\n"
        "• exhale gently for 6 seconds\n\n"
        "Repeat that three times while focusing on something stable around you — perhaps the hum of the station or "
        "the steady rhythm of your breathing.\n\n"
        "You are not alone in this mission. I'm here with you."
        )

    if "stress" in user_text or "overwhelm" in user_text:

        return (
        "It sounds like the workload might be building up. High-pressure environments can trigger cognitive overload.\n\n"
        "A quick technique used in astronaut training is called **task segmentation**.\n"
        "Instead of seeing everything at once, isolate the next small action.\n\n"
        "For example:\n"
        "1. identify the immediate task\n"
        "2. ignore everything else temporarily\n"
        "3. complete that step calmly\n\n"
        "Once the first step is finished, the rest often becomes clearer."
        )

    if "happy" in user_text or "good" in user_text:

        return (
        "That's wonderful to hear. Positive emotional states are extremely valuable during long-duration missions.\n\n"
        "Moments like this reinforce psychological resilience and help maintain crew morale.\n\n"
        "If you'd like, we can log this as a positive checkpoint in your mission diary. "
        "Tracking these moments helps maintain balance over time."
        )

    if "tired" in user_text or "sleep" in user_text:

        return (
        "Fatigue is very common during space missions due to circadian rhythm disruptions.\n\n"
        "Try this short reset:\n"
        "• close your eyes for 30 seconds\n"
        "• take three slow breaths\n"
        "• gently relax your shoulders and neck\n\n"
        "Even short micro-breaks can restore focus and improve cognitive clarity."
        )

    return (
    "I'm here listening. Whether it's mission pressure, emotional stress, or something on your mind, "
    "we can work through it step by step.\n\n"
    "Tell me more about what you're experiencing right now."
    )


# ---------------- WEBCAM PROCESSOR ----------------

class VideoProcessor(VideoProcessorBase):

    def __init__(self):
        self.analyzer=ArmCurlAnalyzer()

    def recv(self,frame):

        img=frame.to_ndarray(format="bgr24")
        img=self.analyzer.process(img)

        return av.VideoFrame.from_ndarray(img,format="bgr24")


# ---------------- VIDEO ANALYSIS ----------------

def run_arm_analysis(video_path):

    cap=cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return None,None

    analyzer=ArmCurlAnalyzer()

    while True:

        ret,frame=cap.read()

        if not ret:
            break

        analyzer.process(frame)

    cap.release()

    summary=analyzer.summary()
    angles=analyzer.angle_history

    return summary,angles


# ---------------- ASTRONAUT PROFILES ----------------

PROFILES={
"Meera":"empathetic emotional astronaut",
"Kabir":"analytical calm astronaut",
"Zara":"energetic optimistic astronaut"
}


# ---------------- SESSION STATE ----------------

if "messages" not in st.session_state:
    st.session_state.messages=[]


# ---------------- SIDEBAR ----------------

st.sidebar.title("MAITRI")

astronaut=st.sidebar.selectbox("Astronaut",list(PROFILES.keys()))

page=st.sidebar.radio("Page",["Chat","Arm Analyzer","Logs"])


st.title("MAITRI Wellness System")


# ================= CHAT PAGE =================

if page=="Chat":

    for m in st.session_state.messages:
        st.chat_message(m["role"]).write(m["content"])

    prompt=st.chat_input("Message MAITRI")

    if prompt:

        emotion,stress=detect_emotion(prompt)

        system=f"You are MAITRI AI wellness companion for astronaut {astronaut}"

        messages=[{"role":m["role"],"content":m["content"]} for m in st.session_state.messages]

        messages.append({"role":"user","content":prompt})

        reply=call_llm(messages,system)

        st.session_state.messages.append({"role":"user","content":prompt})
        st.session_state.messages.append({"role":"assistant","content":reply})

        log_entry(astronaut,prompt,emotion,stress,reply)

        st.rerun()


# ================= ARM ANALYZER =================

elif page=="Arm Analyzer":

    st.header("Live Webcam Exercise Analysis")

    webrtc_streamer(
    key="webcam",
    video_processor_factory=VideoProcessor
    )

    st.header("Upload Video")

    uploaded=st.file_uploader("Upload exercise video")

    if uploaded:

        t=tempfile.NamedTemporaryFile(delete=False)
        t.write(uploaded.read())

        summary,angles=run_arm_analysis(t.name)

        if summary:

            st.write("Reps:",summary["reps"])
            st.write("Range:",summary["range_motion"])

            if angles:

                fig,ax=plt.subplots()
                ax.plot(angles)
                st.pyplot(fig)


# ================= LOG PAGE =================

elif page=="Logs":

    logs=get_history(astronaut)

    for l in logs:

        st.write("User:",l[0])
        st.write("AI:",l[3])
        st.write("---")