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

# ---------------------------------------------------------
# 3. 총 관객수 분포 (히스토그램)
# ---------------------------------------------------------
st.subheader("3. 총 관객수 분포")

fig_hist = px.histogram(
    df,
    x="total_audi",
    nbins=30,
    title="영화별 총 관객수 분포 히스토그램",
    labels={"total_audi": "총 관객수"},
)

fig_hist.update_traces(
    hovertemplate="<b>관객수 구간</b>: %{x}<br><b>영화 수</b>: %{y}편"
)

st.plotly_chart(fig_hist, use_container_width=True)

# 가장 관객수가 많은 영화 계산
max_movie = df.loc[df["total_audi"].idxmax()]
max_title = max_movie["movieNm"]
max_audi = max_movie["total_audi"]

# 3번 그래프 해석 구역
st.divider()
st.markdown("##### 💡 이 그래프로 알 수 있는 것")
st.caption(
    f"대부분의 영화가 관객수 하위 구간(약 100만 명 이하)에 집중되어 있는 우편향 분포를 보입니다. "
    f"이 중 가장 관객 수가 많은 영화는 **{max_title}**({max_audi:,}명)입니다."
)
st.divider()

# ---------------------------------------------------------
# 4. 개봉일 스크린수와 총 관객수의 관계 (산점도)
# ---------------------------------------------------------
st.subheader("4. 개봉일 스크린수와 총 관객수의 관계")

fig_scatter = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre_first",
    hover_name="movieNm",
    title="개봉일 스크린수 vs 총 관객수",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객수",
        "genre_first": "장르",
    },
)

# 마우스오버 시 표시 형태 지정
fig_scatter.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,}개<br>총 관객수: %{y:,}명"
)

st.plotly_chart(fig_scatter, use_container_width=True)

# 4번 그래프 해석 구역
st.divider()
st.markdown("##### 💡 이 그래프로 알 수 있는 것")
st.caption(
    "개봉일 스크린수가 많을수록 대체로 총 관객수도 증가하는 양의 상관관계를 보여주며, "
    "초기 스크린 확보가 최종 흥행 스코어에 큰 영향을 미침을 알 수 있습니다."
)
st.divider()

# ---------------------------------------------------------
# 5. 주요 장르별 총 관객수 분포 (박스플롯)
# ---------------------------------------------------------
st.subheader("5. 주요 장르별 총 관객수 분포 (영화 10편 이상)")

# 영화가 10편 이상인 장르만 필터링
genre_counts_series = df["genre_first"].value_counts()
top_genres = genre_counts_series[genre_counts_series >= 10].index
df_top_genres = df[df["genre_first"].isin(top_genres)]

fig_box = px.box(
    df_top_genres,
    x="genre_first",
    y="total_audi",
    color="genre_first",
    hover_name="movieNm",
    points="outliers",  # 이상치 점 표시
    title="영화 10편 이상 장르별 총 관객수 상자 그림",
    labels={"genre_first": "장르", "total_audi": "총 관객수"},
)

# 마우스오버 설정
fig_box.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>총 관객수: %{y:,}명"
)

st.plotly_chart(fig_box, use_container_width=True)

# 5번 그래프 해석 구역
st.divider()
st.markdown("##### 💡 이 그래프로 알 수 있는 것")
st.caption(
    "주요 장르별 관객수 중앙값과 변동 범위를 한눈에 비교할 수 있으며, "
    "상자 밖의 이상치 점들을 통해 해당 장르 내에서 기록적인 대흥행을 거둔 작품을 직관적으로 식별할 수 있습니다."
)
st.divider()

# ---------------------------------------------------------
# 6. 스크린수, 총 관객수, 첫 주 관객수의 관계 (버블 그래프)
# ---------------------------------------------------------
st.subheader("6. 개봉일 스크린수, 총 관객수, 첫 주 관객수의 관계")

fig_bubble = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",  # 버블 크기 설정
    color="genre_first",
    hover_name="movieNm",
    size_max=60,  # 버블 최대 크기 조정
    title="개봉일 스크린수 vs 총 관객수 (버블 크기: 개봉 첫 주 관객수)",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객수",
        "genre_first": "장르",
        "first_week_audi": "개봉 첫 주 관객수",
    },
)

# 마우스오버 시 표시 형태 지정 및 첫 주 관객수 추가
fig_bubble.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>"
    "개봉일 스크린수: %{x:,}개<br>"
    "총 관객수: %{y:,}명<br>"
    "개봉 첫 주 관객수: %{marker.size:,}명"
)

st.plotly_chart(fig_bubble, use_container_width=True)

# 6번 그래프 해석 구역
st.divider()
st.markdown("##### 💡 이 그래프로 알 수 있는 것")
st.caption(
    "4번 산점도에 개봉 첫 주 관객수를 버블 크기로 추가한 것입니다. "
    "스크린수와 총 관객수가 많은 우상단에 위치할수록 대체로 버블 크기도 커서, 초기 흥행(첫 주 관객)이 "
    "최종 흥행(총 관객)과 스크린 확보 모두에 밀접하게 연결되어 있음을 시각적으로 파악할 수 있습니다."
)
st.divider()

# ---------------------------------------------------------
# 7. 제작 국가 및 장르별 영화 편수 (선버스트)
# ---------------------------------------------------------
st.subheader("7. 제작 국가 및 장르별 영화 편수 분포")

# 국가 및 장르별 영화 편수 집계
df_nation_genre = (
    df.groupby(["nation", "genre_first"]).size().reset_index(name="count")
)

fig_sunburst = px.sunburst(
    df_nation_genre,
    path=["nation", "genre_first"],
    values="count",
    title="제작 국가 및 장르 계층 구조 (칸 크기: 영화 편수)",
)

# 마우스오버 설정
fig_sunburst.update_traces(
    hovertemplate="<b>%{label}</b><br>영화 편수: %{value}편"
)

st.plotly_chart(fig_sunburst, use_container_width=True)

# 7번 그래프 해석 구역
st.divider()
st.markdown("##### 💡 이 그래프로 알 수 있는 것")
st.caption(
    "제작 국가별로 주를 이루는 영화 장르의 세부 비중을 계층적으로 파악할 수 있으며, 국가에 따라 선호되거나 주력 생산되는 장르 구성의 차이를 확인할 수 있습니다."
)
st.divider()
