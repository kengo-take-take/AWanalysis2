import streamlit as st

st.set_page_config(
        page_title='Airwork採用管理集計ツール',
        page_icon='./assets/photo/rogo.jpg',
        )

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
st.write("有料版をご検討の方は「uu045081@gmail.com」へメール下さい。")