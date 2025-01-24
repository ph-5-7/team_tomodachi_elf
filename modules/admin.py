import streamlit as st

# 管理者ページのパスワード
ADMIN_PASSWORD = "admin123"  # 適宜パスワードを変更してください

def show_admin_page():
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
            # 保存処理
            with open(f"data/{uploaded_file.name}", "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success("ファイルが正常に保存されました！")
    elif password:  # 入力がある場合、エラーを表示
        st.error("パスワードが間違っています！")
