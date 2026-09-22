import streamlit as st
import pandas as pd
import numpy as np
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

genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['장르', '편수']

fig1 = px.pie(
    genre_counts, 
    names='장르', 
    values='편수', 
    hole=0.4,
)
fig1.update_traces(
    textposition='inside', 
    textinfo='percent+label',
    hovertemplate='<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}<extra></extra>'
)

st.plotly_chart(fig1, use_container_width=True)
st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 이 그래프를 통해 발견한 사실을 한 문장으로 적어주세요.)")
st.divider()


# 4. 두 번째 그래프: 장르 내 영화 관객 수 (트리맵)
st.subheader('2. 장르별 총 관객 수 및 영화 분포 (트리맵)')

fig2 = px.treemap(
    df,
    path=['genre', 'movieNm'],
    values='total_audi'
)
fig2.update_traces(
    hovertemplate='<b>%{label}</b><br>총 관객: %{value:,.0f}명<extra></extra>'
)

st.plotly_chart(fig2, use_container_width=True)
st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 이 그래프를 통해 발견한 사실을 한 문장으로 적어주세요.)")
st.divider()


# 5. 세 번째 그래프: 총 관객 수 히스토그램
st.subheader('3. 총 관객 수 분포 (히스토그램)')

# 플롯리 히스토그램 생성 (구간 30개로 분할)
fig3 = px.histogram(
    df, 
    x='total_audi',
    nbins=30,
    labels={'total_audi': '총 관객 수 (명)'}
)
fig3.update_traces(
    hovertemplate='관객 수 구간: %{x}<br>영화 편수: %{y}편<extra></extra>'
)

st.plotly_chart(fig3, use_container_width=True)

# 데이터 요약 계산 (구간 및 최고 흥행작)
# 1) 가장 많이 몰려있는 관객 수 구간 계산
counts, bins = np.histogram(df['total_audi'].dropna(), bins=30)
max_bin_idx = counts.argmax()
bin_start = bins[max_bin_idx]
bin_end = bins[max_bin_idx + 1]

# 2) 가장 관객이 많은 영화 찾기
max_movie_row = df.loc[df['total_audi'].idxmax()]
max_movie_name = max_movie_row['movieNm']
max_movie_audi = max_movie_row['total_audi']

# 결과 텍스트 출력
st.markdown(f"""
**📊 데이터 요약**
* 대부분의 영화가 **{bin_start:,.0f}명 ~ {bin_end:,.0f}명** 구간에 몰려 있습니다. (총 {counts[max_bin_idx]}편)
* 가장 관객이 많은 영화는 **'{max_movie_name}'** (총 {max_movie_audi:,.0f}명)입니다.
""")

st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 이 그래프를 통해 발견한 사실을 한 문장으로 적어주세요.)")
st.divider()
