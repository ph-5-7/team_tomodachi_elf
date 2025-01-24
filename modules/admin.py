import streamlit as st
import os
import pandas as pd

# データフォルダのパス
DATA_FOLDER = "data"

# データフォルダが存在しない場合は作成
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

def show_page():
    st.subheader("🔒 管理者ページ - CSVファイル管理")

    # パスワード認証
    password = st.text_input("🔑 パスワードを入力", type="password")
    correct_password = "your_password"  # 任意の管理者用パスワード
    if password != correct_password:
        st.warning("正しいパスワードを入力してください。")
        return

    st.success("✅ 認証成功！CSVファイルをアップロードできます。")

    # CSVファイルアップロード機能
    uploaded_file = st.file_uploader("📁 CSVファイルをアップロード", type=["csv"])
    if uploaded_file is not None:
        # ファイルを保存
        file_path = os.path.join(DATA_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"✅ ファイルが保存されました: {file_path}")

        # アップロードしたCSVをデータフレームで表示
        df = pd.read_csv(file_path)
        st.write("アップロードされたファイルのプレビュー:")
        st.dataframe(df)

    # 保存されているCSVファイル一覧を表示
    st.subheader("📂 保存済みファイル一覧")
    files = os.listdir(DATA_FOLDER)
    if files:
        for file in files:
            st.write(f"📄 {file}")
    else:
        st.write("保存されているファイルはありません。")

    # ファイル削除機能（オプション）
    st.subheader("🗑️ ファイル削除")
    delete_file = st.selectbox("削除するファイルを選択", ["選択してください"] + files)
    if delete_file != "選択してください":
        if st.button("削除する"):
            os.remove(os.path.join(DATA_FOLDER, delete_file))
            st.success(f"✅ ファイルを削除しました: {delete_file}")
