import streamlit as st
import datetime  # 必要なモジュールをインポート
import pandas as pd  # pandasモジュールをインポート
from utils import get_end_of_day

def show_page(df):
    st.subheader("⚔️ 同盟戦データ")

    with st.expander("⚙️ **検索画面を開く❣**"):
        # 📅 同盟戦の開始日と終了日
        alliance_start = st.date_input("📅 同盟戦の開始日", value=datetime.date.today() - datetime.timedelta(days=4))
        alliance_end = st.date_input("📅 同盟戦の終了日", value=datetime.date.today())

        # 🎯 同盟戦対象の加工品
        all_items = sorted(df["加工品"].dropna().unique())
        alliance_items = st.multiselect("🎯 同盟戦対象の加工品", all_items, default=[])

        # 👤 操作者の選択
        unique_users = sorted(df["操作者"].dropna().unique())
        selected_user = st.selectbox("👤 操作者を選択", ["全員"] + unique_users)

        # 💰 報酬額の入力
        reward_amount = st.number_input("💰 総報酬額を入力", min_value=0.0, step=1000.0)

    # 📅 日付フィルタを適用
    df["日時"] = pd.to_datetime(df["日時"])
    df_alliance = df[(df["日時"] >= pd.Timestamp(alliance_start)) & (df["日時"] <= get_end_of_day(alliance_end))]

    # 🎯 加工品フィルタ
    if alliance_items:
        df_alliance = df_alliance[df_alliance["加工品"].isin(alliance_items)]

    # 👤 操作者フィルタ
    if selected_user != "全員":
        df_alliance = df_alliance[df_alliance["操作者"] == selected_user]

    # 同盟ポイントを集計
    alliance_summary = df_alliance.groupby("操作者").agg(同盟ポイント=("同盟ポイント", "sum")).reset_index()
    total_alliance_points = alliance_summary["同盟ポイント"].sum()

    # 順位を追加
    alliance_summary = alliance_summary.sort_values(by="同盟ポイント", ascending=False).reset_index(drop=True)
    alliance_summary.insert(0, "順位", alliance_summary.index + 1)

    # 均等報酬の計算
    eligible_users = alliance_summary[alliance_summary["同盟ポイント"] >= 20000]
    equal_share = round(reward_amount * 0.2 / max(1, len(eligible_users)), 1)
    alliance_summary["均等"] = alliance_summary["操作者"].apply(lambda x: equal_share if x in eligible_users["操作者"].values else 0)

    # 割合報酬の計算
    alliance_summary["割合%"] = ((alliance_summary["同盟ポイント"] / total_alliance_points) * 100).round(1)
    alliance_summary["割合"] = ((reward_amount * 0.8) * (alliance_summary["同盟ポイント"] / total_alliance_points)).round(1)

    # マイナスの割合を適用
    alliance_summary.loc[alliance_summary["同盟ポイント"] < 0, ["割合%", "割合"]] *= -1

    # 経理費の計算
    alliance_summary["経理費"] = (alliance_summary["均等"] * 0.2 * -1).round(1)

    # 最終報酬
    alliance_summary["最終集計"] = (alliance_summary["均等"] + alliance_summary["割合"] + alliance_summary["経理費"]).round(1)

    # 経理報酬の金額表示
    total_finance_fee = alliance_summary["経理費"].sum() * -1
    st.write(f"💰 **経理報酬:** {total_finance_fee}")
    st.write(f"🔢 **同盟ポイント合計:** {total_alliance_points}")

    # 表のカラム順を固定
    alliance_summary = alliance_summary[["順位", "操作者", "同盟ポイント", "均等", "割合%", "割合", "経理費", "最終集計"]]
    st.dataframe(alliance_summary, use_container_width=True, height=500)
