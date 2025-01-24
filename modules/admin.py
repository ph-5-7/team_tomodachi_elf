import streamlit as st
import os

# 管理者ページのパスワード
ADMIN_PASSWORD = "bbb"  # パスワードを適宜変更してください

def show_admin_page(DATA_DIR):
    # 現在の保存先パスを表示
    st.write(f"現在のデータ保存先パス: {os.path.abspath(DATA_DIR)}")

    # パスワード入力
    password = st.text_input("🔑 パスワードを入力", type="password")

    if password == ADMIN_PASSWORD:
        st.success("ログイン成功！")
        st.subheader("⚙️ 管理者ページ")
        st.write("ここに管理者専用の機能を追加します。")

        # CSVファイルアップロード機能
        uploaded_file = st.file_uploader("📁 CSVファイルをアップロード", type=["csv"])
        if uploaded_file is not None:
            st.write(f"アップロードされたファイル: {uploaded_file.name}")

            # ディレクトリが存在しない場合は作成
            if not os.path.exists(DATA_DIR):
                os.makedirs(DATA_DIR)

            # 保存処理
            file_path = os.path.join(DATA_DIR, uploaded_file.name)
            try:
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"ファイルが正常に保存されました！ ({file_path})")
            except Exception as e:
                st.error(f"ファイルの保存中にエラーが発生しました: {e}")

        # 保存されたファイルを表示
        if st.button("📂 保存されたファイルを表示"):
            saved_files = os.listdir(DATA_DIR) if os.path.exists(DATA_DIR) else []
            if saved_files:
                st.write("保存されているファイル:")
                for file in saved_files:
                    st.write(f"- {file}")
            else:
                st.write("保存されているファイルはありません。")
    elif password:  # 入力がある場合、エラーを表示
        st.error("パスワードが間違っています！")

