import streamlit as st
from utils import load_all_data
import modules.warehouse as warehouse
import modules.alliance_war as alliance_war

# データフォルダを指定
data_dir = "data"

# データをロード
df = load_all_data(data_dir)

# タイトル
st.title("チームともだち♡管理ツール🫶")

# サイドバーでページ選択
page = st.sidebar.radio("ページを選択", ["倉庫履歴", "同盟戦データ"])

# 各ページを表示
if page == "倉庫履歴":
    warehouse.show_page(df)
elif page == "同盟戦データ":
    alliance_war.show_page(df)
