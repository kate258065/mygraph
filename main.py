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

# ---------------------------------------------------------
# 1. 장르별 영화 편수 (도넛 그래프)
# ---------------------------------------------------------
st.subheader("1. 장르별 영화 편수")

genre_counts = df["genre_first"].value_counts().reset_index()
genre_counts.columns = ["장르", "영화 편수"]

fig_donut = px.pie(
    genre_counts,
    values="영화 편수",
    names="장르",
    hole=0.4,
    title="장르별 영화 편수 비율",
)

# 마우스오버 시 편수와 비율 표기
fig_donut.update_traces(
    hovertemplate="<b>%{label}</b><br>영화 편수: %{value}편<br>비율: %{percent}"
)

st.plotly_chart(fig_donut, use_container_width=True)

# 1번 그래프 해석 구역
st.divider()
st.markdown("##### 💡 이 그래프로 알 수 있는 것")
st.caption(
    "박스오피스 상위권에 진입한 영화 중 어떤 장르가 가장 큰 비중을 차지하는지 분포 현황을 한눈에 비교할 수 있습니다."
)
st.divider()

# ---------------------------------------------------------
# 2. 장르 및 영화별 총 관객수 분포 (트리맵)
# ---------------------------------------------------------
st.subheader("2. 장르 및 영화별 총 관객수 분포")

fig_treemap = px.treemap(
    df,
    path=[px.Constant("전체"), "genre_first", "movieNm"],
    values="total_audi",
    title="장르 및 영화별 총 관객수 (칸 크기: 총 관객수)",
)

# 마우스오버 시 영화명과 총 관객수 표기
fig_treemap.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객수: %{value:,}명",
    root_color="lightgrey",
)

st.plotly_chart(fig_treemap, use_container_width=True)

# 2번 그래프 해석 구역
st.divider()
st.markdown("##### 💡 이 그래프로 알 수 있는 것")
st.caption(
    "장르 내에서 특정 흥행작이 차지하는 관객 동원력의 크기를 한눈에 비교하고, 어떤 영화가 장르 전체의 관객수를 견인했는지 파악할 수 있습니다."
)
st.divider()
