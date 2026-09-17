import pandas as pd
import plotly.express as px
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")


# 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)

    # 장르 전처리: 첫 번째 장르만 추출 (예: '액션|드라마' -> '액션')
    df["genre_first"] = df["genre"].fillna("").apply(lambda x: x.split("|")[0])

    return df


df = load_data()

# 1. 장르별 영화 편수 (도넛 그래프)
st.subheader("1. 장르별 영화 편수")

genre_counts = df["genre_first"].value_counts().reset_index()
genre_counts.columns = ["장르", "영화 편수"]

fig = px.pie(
    genre_counts,
    values="영화 편수",
    names="장르",
    hole=0.4,
    title="장르별 영화 편수 비율",
)

# 마우스오버 시 편수와 비율 표기
fig.update_traces(
    hovertemplate="<b>%{label}</b><br>영화 편수: %{value}편<br>비율: %{percent}"
)

st.plotly_chart(fig, use_container_width=True)

# 시각화 해석 구역
st.divider()
st.markdown("##### 💡 이 그래프로 알 수 있는 것")
st.caption(
    "박스오피스 상위권에 진입한 영화 중 어떤 장르가 가장 큰 비중을 차지하는지 분포 현황을 한눈에 비교할 수 있습니다."
)
st.divider()
