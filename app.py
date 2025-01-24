# Show Code ボタンを無効化
import streamlit as st

st.set_page_config(page_title="チームともだち♡管理ツール", layout="wide", initial_sidebar_state="collapsed")

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
page = st.sidebar.radio("ページを選択", ["倉庫履歴", "同盟戦データ", "管理者用ページ"])

# 各ページを表示
if page == "倉庫履歴":
    warehouse.show_page(df)
elif page == "同盟戦データ":
    alliance_war.show_page(df)
elif page == "管理者用ページ":
    st.subheader("🔒 管理者用ページ")

    # パスワード設定
    admin_password = "your_secure_password"  # 管理者用パスワードを設定
    entered_password = st.text_input("パスワードを入力してください", type="password")

    # パスワード認証
    if entered_password == admin_password:
        st.success("✅ 管理者としてログインしました！")

        # ファイルアップロード機能
        uploaded_file = st.file_uploader("CSVファイルをアップロード", type=["csv"])
        if uploaded_file is not None:
            save_path = f"{data_dir}/{uploaded_file.name}"
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"{uploaded_file.name} を {save_path} に保存しました！")
            st.info("ページを再読み込みしてください。")
    else:
        st.warning("❌ 正しいパスワードを入力してください。")
