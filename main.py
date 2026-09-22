import pandas as pd
import plotly.express as px
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide",
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.markdown(
    "KOBIS 박스오피스 데이터를 바탕으로 한국 극장가에 걸린 영화들의 분포와 변수 간의 관계를 시각적으로 탐색하는 도감입니다."
)


# 데이터 로드 함수
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)

    # 장르 전처리: 세로막대 기호(|)로 여러 개인 경우 첫 번째 장르만 추출
    if "genre" in df.columns:
        df["genre"] = df["genre"].astype(str).apply(lambda x: x.split("|")[0].strip())

    return df


try:
    df = load_data()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# 사이드바 설정 (필터링 옵션)
st.sidebar.header("🔍 데이터 필터")
selected_nations = st.sidebar.multiselect(
    "제작 국가 선택",
    options=df["nation"].unique().tolist(),
    default=df["nation"].unique().tolist(),
)

# 필터 적용
filtered_df = df[df["nation"].isin(selected_nations)]

st.sidebar.markdown(f"**선택된 영화 편수:** {len(filtered_df)}편")
st.sidebar.markdown("---")

# ---------------------------------------------------------
# 첫 번째 그래프: 장르별 영화 편수 (Plotly 도넛 그래프)
# ---------------------------------------------------------
st.header("1. 장르별 영화 편수 분포")
st.markdown("선택된 영화들의 장르별 구성 비율과 편수를 도넛 그래프로 확인합니다.")

if not filtered_df.empty:
    genre_counts = filtered_df["genre"].value_counts().reset_index()
    genre_counts.columns = ["genre", "count"]

    fig_donut = px.pie(
        genre_counts,
        names="genre",
        values="count",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    fig_donut.update_traces(
        textposition="inside", textinfo="percent+label", hoverinfo="label+value+percent"
    )
    fig_donut.update_layout(
        margin=dict(t=30, b=30, l=30, r=30),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
    )

    st.plotly_chart(fig_donut, use_container_width=True)
else:
    st.warning("조건에 해당하는 데이터가 없습니다.")

# 그래프 아래 '이 그래프로 알 수 있는 것' 구역 나누기 (구분선 및 컨테이너)
st.markdown("---")
with st.container():
    st.markdown("💡 **이 그래프로 알 수 있는 것**")
    st.info(
        "박스오피스 10위권에 진입한 영화 중 특정 장르(예: 드라마, 액션 등)가 전체 시장에서 차지하는 비중과 편수의 편중 현상을 한눈에 파악할 수 있습니다."
    )

st.markdown("---")

# ---------------------------------------------------------
# 추가적인 그래프 공간 예시 (분포와 관계 탐색)
# ---------------------------------------------------------
st.header("2. 개봉 첫 주 관객수와 총 관객수의 관계")
st.markdown("개봉 첫 주의 성적이 최종 흥행(총 관객수)에 미치는 영향을 살펴봅니다.")

if not filtered_df.empty and "first_week_audi" in filtered_df.columns and "total_audi" in filtered_df.columns:
    fig_scatter = px.scatter(
        filtered_df,
        x="first_week_audi",
        y="total_audi",
        hover_name="movieNm",
        color="genre",
        labels={
            "first_week_audi": "개봉 첫 주 관객수",
            "total_audi": "총 관객수",
            "genre": "장르",
        },
        opacity=0.7,
    )
    fig_scatter.update_layout(margin=dict(t=30, b=30, l=30, r=30))
    st.plotly_chart(fig_scatter, use_container_width=True)
else:
    st.warning("데이터 열을 찾을 수 없습니다.")

st.markdown("---")
with st.container():
    st.markdown("💡 **이 그래프로 알 수 있는 것**")
    st.info(
        "개봉 첫 주 관객수와 총 관객수 사이에는 강한 양의 상관관계가 존재하며, 첫 주 성적이 흥행 성패를 가늠하는 주요 지표임을 확인할 수 있습니다."
    )
