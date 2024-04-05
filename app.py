import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import streamlit as st
import json

def main():
    st.set_page_config(page_title="Firebase Realtime Database Viewer", page_icon=":face_with_monocle:")
    st.title("Firebase Realtime Database Viewer")

    with st.sidebar:
        fb_credentails = st.file_uploader("Upload Firebase Credential",type=['json'],accept_multiple_files=False)
        fb_database_url = st.text_input("Firebase Database URL")
        process = st.button("Process")

    if process:
        if not fb_credentails:
            st.error("Firebase Credentials is required")
            st.stop()
        if not fb_database_url: 
            st.error("Firebase Database URL is required")
            st.stop()

        if firebase_admin.get_app(name='[DEFAULT]'):    
            firebase_admin.delete_app(name='[DEFAULT]')
        
        cred = credentials.Certificate(json.loads(fb_credentails.getvalue().decode("utf-8")))
        firebase_admin.initialize_app(cred, {
            'databaseURL': fb_database_url
        })

        ref = db.reference('tests')
        logs = ref.get()
        st.json(logs)

        current_datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = "vr_logs_" + current_datetime + ".json"

        json_str = json.dumps(logs, indent=2)
        st.download_button(
            label="Download logs as JSON",
            data=json_str,
            file_name=file_name,
            mime="application/json"
)
    
if __name__ == '__main__':
    main()