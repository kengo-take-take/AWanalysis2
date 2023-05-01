import streamlit as st
import streamlit_authenticator as stauth
import yaml
import pandas as pd
from datetime import date,timedelta
import datetime as dt
import matplotlib.pyplot as plt
import japanize_matplotlib
import math


with open('./config.yaml') as file:
    config = yaml.safe_load(file)


st.set_page_config(
        page_title='Airwork採用管理集計ツール',
        page_icon='assets/photo/rogo.jpg',
        )

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.title('Airwork採用管理 応募解析')

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# ログインメソッドで入力フォームを配置
name, authentication_status, username = authenticator.login('Login', 'main')

# 返り値、authenticaton_statusの状態で処理を場合分け
if st.session_state["authentication_status"]:
    st.write(f'ようこそ *{st.session_state["name"]}*さん')
    df = st.file_uploader("ファイルアップロード", type='csv')
    authenticator.logout('Logout', 'main')

    if df:
        st.sidebar.write("""
        応募者分析したい日時を指定してください。
        """)
        from_day = st.sidebar.date_input('いつから?',
                                    min_value=date.today()-timedelta(days=730),
                                    max_value=date.today(),
                                    value=date.today()-timedelta(days=30),
                                    )

        to_day = st.sidebar.date_input('いつまで?',
                                    min_value=date.today()-timedelta(days=730),
                                    max_value=date.today(),
                                    value=date.today(),
                                    )

        df = pd.read_csv(df)
        df["年代"] = df["年齢"].apply(lambda x:math.floor(x/10)*10).astype(str) + '代'
        df['応募日時'] = pd.to_datetime(df['応募日時'])
        df['応募日時'] = df['応募日時'].dt.date
        df = df[(df['応募日時'] >= from_day) & (df['応募日時'] <= to_day)]
        c = df['応募日時'].value_counts()
        sex = df['性別'].value_counts()
        job = df['現在の職業'].value_counts()
        generation = df['年代'].value_counts()
        df = c.rename_axis('応募日時').reset_index(name='応募数')
        df["応募日時"] = pd.to_datetime(df["応募日時"])

        #入れ物用意してくっつける
        template = pd.DataFrame(
            pd.date_range(start=from_day, end=to_day, freq='d'),
            columns=["応募日時"]
        )
        df = pd.merge(template, df[['応募日時', '応募数']], how='left', on='応募日時')
        df = df.fillna(0)

        template2 = pd.DataFrame(
            data={'列1': ['女性', '男性', '不明']}
        )
        df1 = sex.rename_axis('性別').reset_index(name='応募数')

        template3 = pd.DataFrame(
            data={'列1': ['高校生','大学生','大学院生','短大生','専門学校生','アルバイト・パート','正社員','契約社員','派遣社員','主婦・主夫','無職','その他']}
        )
        df2 = job.rename_axis('現在の職業').reset_index(name='応募数')

        template4 = pd.DataFrame(
            data={'列1': ['10代','20代','30代','40代','50代','60代','70代','80代','90代']}
        )
        df3 = generation.rename_axis('年代').reset_index(name='応募数')
        df3 = df3.sort_values('年代')

        #グラフ作成
        fig, ax = plt.subplots()
        ax.plot(df["応募日時"], df["応募数"])
        plt.xticks(rotation=30)
        plt.title('応募推移', fontsize=25)
        col1_1, col1_2 = st.columns(2)
        number = df1.sum().iloc[-1]

        td = (abs(to_day - from_day) / timedelta(days=1))
        with col1_1:
            st.pyplot(fig)
        with col1_2:
            st.write(f'{from_day}〜{to_day}までの応募数は{number}件。')
            st.write(f'１日あたりの応募は約{round((number / td),1)}件。')

        fig1, ax1 = plt.subplots()
        labels = df1['性別']
        sizes = df1['応募数']

        ax1.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            counterclock=False,
            startangle=90,
        )
        plt.title('応募者の男女比率', fontsize=25)
        col2_1, col2_2 = st.columns(2)
        with col2_1:
            st.pyplot(fig1)
        df1.index = df1['性別']
        df1 = df1.drop('性別', axis=1)
        with col2_2:
            st.dataframe(df1)

        
        fig2, ax2 = plt.subplots()
        labels = df2['現在の職業']
        sizes = df2['応募数']

        ax2.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            counterclock=False,
            startangle=90,
        )
        plt.title('応募者の現在の職業比率', fontsize=25)
        col3_1, col3_2 = st.columns(2)
        with col3_1:
            st.pyplot(fig2)
        df2.index = df2['現在の職業']
        df2 = df2.drop('現在の職業', axis=1)
        with col3_2:
            st.dataframe(df2)


        fig3, ax3 = plt.subplots()
        labels = df3['年代']
        sizes = df3['応募数']
        
        ax3.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            counterclock=False,
            startangle=90,
        )
        plt.title('応募者の年代比率', fontsize=25)
        col4_1, col4_2 = st.columns(2)
        with col4_1:
            st.pyplot(fig3)
        df3.index = df3['年代']
        df3 = df3.drop('年代', axis=1)
        with col4_2:
            st.dataframe(df3)



        # df['応募日時'] = pd.to_datetime(df['応募日時'])
        # df['応募日時'] = df['応募日時'].dt.date
        # c = df['応募日時'].value_counts()
        # df = c.rename_axis('応募日時').reset_index(name='応募数')
        # df["応募日時"] = pd.to_datetime(df["応募日時"])

        # template = pd.DataFrame(
        #     pd.date_range(start=from_day, end=to_day, freq='d'),
        #     columns=["応募日時"]
        # )

        # df = pd.merge(template, df[['応募日時', '応募数']], how='left', on='応募日時')
        # df = df.fillna(0)
        # df.index = df['応募日時']
        # #df = df.drop('応募日時', axis=1)
        # fig, ax = plt.subplots()
        # ax.plot(df["応募日時"], df["応募数"])
        # plt.xticks(rotation=30)
        # st.pyplot(fig)
        #st.line_chart(data=df, width=0, height=0, use_container_width=True)