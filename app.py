import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pandas as pd
import streamlit as st
import json

def normalize_data(_data):
    data = {
            'USER_ID': [], 
            'AUDIO_SRC': [], 
            'TEST_DIRECTION': [],
            'audio': [],
            'isCorrect': [],
            'responseTime': [],
            'selectedSpeaker': [],
            'timeOfRecord': [],
            }

    for k_id, v_id in _data.items():
        # print("key_id = {key}".format(key=k_id))
        # data['USER_ID'].append(k_id)
        for k_src, v_src in v_id.items():
            # data['AUDIO_SRC'].append(k_src)
            for k_dir, v_dir in v_src.items():
                # data['TEST_DIRECTION'].append(k_dir)
                for k_trial, v_trial in v_dir.items():
                    for k_item, v_item in v_trial.items():
                        data['USER_ID'].append(k_id)
                        data['AUDIO_SRC'].append(k_src)
                        data['TEST_DIRECTION'].append(k_dir)
                        data['audio'].append(v_item['audio'])
                        data['isCorrect'].append(v_item['isCorrect'])
                        data['responseTime'].append(v_item['responseTime'])
                        data['selectedSpeaker'].append(v_item['selectedSpeaker'])
                        data['timeOfRecord'].append(v_item['timeOfRecord'])

    return data

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

        if firebase_admin._apps:
            firebase_admin.delete_app(firebase_admin.get_app())

        cred = credentials.Certificate(json.loads(fb_credentails.getvalue().decode("utf-8")))
        firebase_admin.initialize_app(cred, {
            'databaseURL': fb_database_url
        })

        ref = db.reference('tests')
        logs = ref.get()
        # st.json(logs)

        current_datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = "vr_logs_" + current_datetime

        json_str = json.dumps(logs, indent=2)

        data = normalize_data(logs)
        st.dataframe(data)

        st.download_button(
            label="Download logs as JSON",
            data=json_str,
            file_name=file_name + ".json",
            mime="application/json")

        df = pd.DataFrame(data)
        csv = df.to_csv(index=True).encode('utf-8')
        
        st.download_button(
            label="Download logs as CSV",
            data=csv,
            file_name=file_name + ".csv",
            mime="text/csv")

    
if __name__ == '__main__':
    main()