import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정
st.set_page_config(page_title='영화 데이터 그래프 도감 2 - 분포와 관계', layout='wide')
st.title('영화 데이터 그래프 도감 2 - 분포와 관계')

# 2. 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # 장르 데이터 전처리: 여러 장르가 '|'로 묶여있을 경우 첫 번째 장르만 남김
    df['genre'] = df['genre'].apply(lambda x: str(x).split('|')[0] if pd.notnull(x) else x)
    
    return df

df = load_data()

# 3. 첫 번째 그래프: 장르별 영화 편수 (도넛 그래프)
st.subheader('1. 장르별 영화 분포')

# 장르별 영화 편수 집계
genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['장르', '편수']

# 플롯리 도넛 그래프 생성
fig1 = px.pie(
    genre_counts, 
    names='장르', 
    values='편수', 
    hole=0.4,
)

# 마우스를 올렸을 때(hover) 편수와 비율이 명확하게 보이도록 설정
fig1.update_traces(
    textposition='inside', 
    textinfo='percent+label',
    hovertemplate='<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}<extra></extra>'
)

st.plotly_chart(fig1, use_container_width=True)
st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 이 그래프를 통해 발견한 사실을 한 문장으로 적어주세요.)")
st.divider()


# 4. 두 번째 그래프: 장르 내 영화 관객 수 트리맵
st.subheader('2. 장르별 총 관객 수 및 영화 분포 (트리맵)')

# 플롯리 트리맵 생성 (장르 안에 영화가 포함되는 계층 구조)
fig2 = px.treemap(
    df,
    path=['genre', 'movieNm'],  # 장르 -> 영화명 순으로 계층 설정
    values='total_audi'         # 칸의 크기를 총 관객 수로 지정
)

# 마우스를 올렸을 때(hover) 영화명(label)과 총 관객(value)이 보이도록 설정 (천 단위 콤마 포함)
fig2.update_traces(
    hovertemplate='<b>%{label}</b><br>총 관객: %{value:,.0f}명<extra></extra>'
)

st.plotly_chart(fig2, use_container_width=True)
st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 이 그래프를 통해 발견한 사실을 한 문장으로 적어주세요.)")
st.divider()
