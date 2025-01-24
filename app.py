# Show Code ボタンを無効化
import streamlit as st

st.set_page_config(page_title="チームともだち♡管理ツール", layout="wide", initial_sidebar_state="collapsed")

import modules.warehouse as warehouse
import modules.alliance_war as alliance_war
import modules.admin as admin
from utils import load_all_data

# データフォルダを指定
data_dir = "data"

# データをロード
df = load_all_data(data_dir)

# タイトル
st.title("チームともだち♡管理ツール🫶")

# サイドバーでページ選択
page = st.sidebar.radio("ページを選択", ["倉庫履歴", "同盟戦データ", "管理者ページ"])

# 各ページを表示
if page == "倉庫履歴":
    warehouse.show_page(df)
elif page == "同盟戦データ":
    alliance_war.show_page(df)
elif page == "管理者ページ":
    admin.show_admin_page()
