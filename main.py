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


# 5. 세 번째 그래프: 총 관객 수 분포 (히스토그램)
st.subheader('3. 총 관객 수 분포 (히스토그램)')

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
counts, bins = np.histogram(df['total_audi'].dropna(), bins=30)
max_bin_idx = counts.argmax()
bin_start = bins[max_bin_idx]
bin_end = bins[max_bin_idx + 1]

max_movie_row = df.loc[df['total_audi'].idxmax()]
max_movie_name = max_movie_row['movieNm']
max_movie_audi = max_movie_row['total_audi']

st.markdown(f"""
**📊 데이터 요약**
* 대부분의 영화가 **{bin_start:,.0f}명 ~ {bin_end:,.0f}명** 구간에 몰려 있습니다. (총 {counts[max_bin_idx]}편)
* 가장 관객이 많은 영화는 **'{max_movie_name}'** (총 {max_movie_audi:,.0f}명)입니다.
""")

st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 이 그래프를 통해 발견한 사실을 한 문장으로 적어주세요.)")
st.divider()


# 6. 네 번째 그래프: 개봉일 스크린 수와 총 관객 수 관계 (산점도)
st.subheader('4. 개봉일 스크린 수와 총 관객 수의 관계 (산점도)')

fig4 = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    color='genre',
    hover_name='movieNm',
    labels={
        'first_scrn': '개봉일 스크린 수 (개)', 
        'total_audi': '총 관객 수 (명)', 
        'genre': '장르'
    }
)
fig4.update_traces(
    hovertemplate='<b>%{hovertext}</b><br>개봉일 스크린 수: %{x:,.0f}개<br>총 관객 수: %{y:,.0f}명<extra></extra>'
)

st.plotly_chart(fig4, use_container_width=True)
st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 이 그래프를 통해 발견한 사실을 한 문장으로 적어주세요.)")
st.divider()


# 7. 다섯 번째 그래프: 주요 장르별 총 관객 수 분포 (상자 그림)
st.subheader('5. 주요 장르별 총 관객 수 분포 (상자 그림)')

# 영화가 10편 이상인 장르만 필터링
genre_counts_all = df['genre'].value_counts()
major_genres = genre_counts_all[genre_counts_all >= 10].index
df_major_genres = df[df['genre'].isin(major_genres)]

fig5 = px.box(
    df_major_genres,
    x='genre',
    y='total_audi',
    hover_name='movieNm',  # 튀는 점(이상치)에 마우스를 올렸을 때 영화명이 보이도록 설정
    labels={
        'genre': '장르 (10편 이상)', 
        'total_audi': '총 관객 수 (명)'
    }
)

st.plotly_chart(fig5, use_container_width=True)
st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 이 그래프를 통해 발견한 사실을 한 문장으로 적어주세요.)")
st.divider()


# 8. 여섯 번째 그래프: 개봉일 스크린 수, 총 관객 수, 첫 주 관객 수 관계 (버블 그래프)
st.subheader('6. 스크린 수, 첫 주 관객, 총 관객 수의 관계 (버블 그래프)')

# 플롯리 산점도에 size 속성을 추가하여 버블 그래프로 변환
fig6 = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    size='first_week_audi',  # 버블 크기를 개봉 첫 주 관객 수로 지정
    color='genre',           # 장르별 색상 구분
    hover_name='movieNm',
    custom_data=['first_week_audi'], # 툴팁에 활용할 추가 데이터
    size_max=50,             # 최대 버블 크기 지정
    labels={
        'first_scrn': '개봉일 스크린 수 (개)', 
        'total_audi': '총 관객 수 (명)', 
        'genre': '장르'
    }
)

# 툴팁에 첫 주 관객 수 정보가 추가로 보이도록 수정
fig6.update_traces(
    hovertemplate='<b>%{hovertext}</b><br>개봉일 스크린 수: %{x:,.0f}개<br>총 관객 수: %{y:,.0f}명<br>첫 주 관객 수: %{customdata[0]:,.0f}명<extra></extra>'
)

st.plotly_chart(fig6, use_container_width=True)
st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 이 그래프를 통해 발견한 사실을 한 문장으로 적어주세요.)")
st.divider()
