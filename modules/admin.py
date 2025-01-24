import streamlit as st
import os

# データフォルダの指定
data_dir = "data"

def show_page():
    st.subheader("🔒 管理者用ページ")

    # CSVファイルのアップロード
    st.header("📤 CSVファイルアップロード")
    uploaded_file = st.file_uploader("アップロードするCSVファイルを選択してください", type=["csv"])
    
    if uploaded_file is not None:
        # 保存先パスを作成
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)  # フォルダが存在しない場合は作成

        save_path = os.path.join(data_dir, uploaded_file.name)

        # ファイルを保存
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"ファイルがアップロードされました: {uploaded_file.name}")

    # 保存済みファイルの一覧を表示
    st.header("📂 保存済みCSVファイル")
    if os.path.exists(data_dir):
        files = os.listdir(data_dir)

        if files:
            # ファイル名をリスト表示
            selected_file = st.selectbox("削除するファイルを選択", files)
            if st.button("🗑️ ファイルを削除"):
                file_path = os.path.join(data_dir, selected_file)
                os.remove(file_path)
                st.success(f"{selected_file} を削除しました。")
        else:
            st.info("保存されたファイルはありません。")
    else:
        st.info("データフォルダが存在しません。")
