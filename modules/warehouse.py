import streamlit as st
import pandas as pd
from utils import get_end_of_day

def show_page(df):
    st.subheader("📦 倉庫履歴")

    with st.expander("🔍 **検索画面を開く❣**"):
        # 📅 期間選択
        start_date = st.date_input("📅 開始日", value=pd.Timestamp.today() - pd.Timedelta(days=7))
        end_date = st.date_input("📅 終了日", value=pd.Timestamp.today())

        # 🎒 加工品選択
        all_items = sorted(df["加工品"].dropna().unique())
        selected_items = st.multiselect("🎒 確認する加工品", all_items, default=all_items[:3])

        # 🔄 操作の種類選択
        operation_type = st.selectbox("🔄 操作の種類を選択", ["すべて", "預ける", "取り出す"])

        # 👤 操作者選択
        unique_users = sorted(df["操作者"].dropna().unique())
        selected_user = st.selectbox("👤 操作者を選択", ["全員"] + unique_users)

    # ✅ フィルタリング
    df["日時"] = pd.to_datetime(df["日時"])
    filtered_df = df[(df["日時"] >= pd.Timestamp(start_date)) & (df["日時"] <= get_end_of_day(end_date))]

    if operation_type == "預ける":
        filtered_df = filtered_df[filtered_df["操作"] == "預ける"]
    elif operation_type == "取り出す":
        filtered_df = filtered_df[filtered_df["操作"] == "取り出す"]

    if selected_user != "全員":
        filtered_df = filtered_df[filtered_df["操作者"] == selected_user]

    if selected_items:
        filtered_df = filtered_df[filtered_df["加工品"].isin(selected_items)]

    # ✅ 「取り出す」の場合は数量をマイナス表示
    filtered_df["数量"] = filtered_df.apply(
        lambda row: -row["数量"] if row["操作"] == "取り出す" else row["数量"], axis=1
    )

    # ✅ 列順を変更
    filtered_df = filtered_df[["日時", "操作", "加工品", "操作者", "数量", "同盟ポイント"]]

    # ✅ 合計計算
    total_points = filtered_df["同盟ポイント"].sum()
    total_quantity = filtered_df["数量"].sum()

    # ✅ 表を表示
    st.dataframe(filtered_df, use_container_width=True, height=500)

    # ✅ 合計値を表示
    st.write(f"🪙 **同盟ポイント合計:** {total_points}")
    st.write(f"📦 **数量合計:** {total_quantity}")
