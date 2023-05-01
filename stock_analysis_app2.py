import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime


def calculate_std(row, recent_years):
    eps_values = row[recent_years]
    return np.std(eps_values)


def analyze_data(file, current_year):
    data = pd.read_excel(file, engine='openpyxl')

    years = [f"{year}年度每股盈餘(元)" for year in range(current_year - 1, current_year - 6, -1)]
    dividend_years = [f"{year}合計股利" for year in range(current_year - 1, current_year - 6, -1)]

    data["盈餘標準差"] = data.apply(lambda row: calculate_std(row, years), axis=1)
    data["近5年平均EPS(元)"] = data[years].mean(axis=1)
    data["近5年平均合計股利(元)"] = data[dividend_years].mean(axis=1)
    data["股利發放率"] = data["近5年平均合計股利(元)"] / data["近5年平均EPS(元)"]

    return data


st.title("股票分析工具")

uploaded_file = st.file_uploader("選擇一個 .xlsx 文件", type="xlsx")
current_year = st.number_input("請輸入當前年份：", min_value=1900, max_value=9999, value=2023, step=1)

filtered_data = pd.DataFrame()
if uploaded_file is not None:
    data = analyze_data(uploaded_file, current_year)

    # 增加股票代號搜尋功能
    stock_id = st.text_input("輸入股票代號：")
    if stock_id:
        display_data = data[data["代號"].apply(lambda x: str(x).startswith(stock_id))]
        if not display_data.empty:
            st.write(display_data[["代號", "名稱", "盈餘標準差", "近5年平均EPS(元)", "近5年平均合計股利(元)", "股利發放率"]])
        else:
            st.warning("找不到該股票代號。")

    # 增加篩選功能
    st.header("篩選功能")
    eps_filter = st.slider("近5年平均EPS(元)：", min_value=float(data["近5年平均EPS(元)"].min()), max_value=float(data["近5年平均EPS(元)"].max()), value=(float(data["近5年平均EPS(元)"].min()), float(data["近5年平均EPS(元)"].max())))
    div_filter = st.slider("近5年平均合計股利(元)：", min_value=float(data["近5年平均合計股利(元)"].min()), max_value=float(data["近5年平均合計股利(元)"].max()), value=(float(data["近5年平均合計股利(元)"].min()), float(data["近5年平均合計股利(元)"].max())))
    std_filter = st.slider("盈餘標準差：", min_value=float(data["盈餘標準差"].min()), max_value=float(data["盈餘標準差"].max()), value=(float(data["盈餘標準差"].min()), float(data["盈餘標準差"].max())))
    payout_filter = st.slider("股利發放率：", min_value=float(data["股利發放率"].min()), max_value=float(data["股利發放率"].max()), value=(float(data["股利發放率"].min()), float(data["股利發放率"].max())))
    filtered_data = data[(data["近5年平均EPS(元)"] >= eps_filter[0]) & (data["近5年平均EPS(元)"] <= eps_filter[1]) &
                     (data["近5年平均合計股利(元)"] >= div_filter[0]) & (data["近5年平均合計股利(元)"] <= div_filter[1]) &
                     (data["盈餘標準差"] >= std_filter[0]) & (data["盈餘標準差"]<= std_filter[1]) &
                     (data["股利發放率"] >= payout_filter[0]) & (data["股利發放率"] <= payout_filter[1])]
if st.button("篩選"):
    if not filtered_data.empty:
        st.write(filtered_data[["代號", "名稱", "盈餘標準差", "近5年平均EPS(元)", "近5年平均合計股利(元)", "股利發放率"]])
    else:
        st.warning("沒有符合篩選條件的股票。")
else:
    st.warning("請選擇一個文件進行分析。")
