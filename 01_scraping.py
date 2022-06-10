import datetime
from bs4 import BeautifulSoup
import requests
import pandas as pd
import streamlit as st
from datetime import date

def check_yahoo_news(serch_word,dt_now):

    url_target = 'https://news.yahoo.co.jp/topics/'
    soup_target = BeautifulSoup(requests.get(url_target,timeout=3).text,'html.parser')

    href_list = soup_target.find_all('a',{'class':'sc-hEsumM fnXbh'})

    detail_list = []
    contents_list = []

    for href in range(len(href_list)):
        detail = {}
        detail['no'] = href
        url_detail = 'https://news.yahoo.co.jp'+href_list[href].attrs['href']+'?date='+str(dt_now)
        cate = url_detail.split('/')[4].split('?')[0]
        detail['category']=cate
        detail['urls']=url_detail
        detail['title']=href_list[href].contents[0]
        detail_list.append(detail)

        soup_detail = BeautifulSoup(requests.get(url_detail).text,'html.parser')
        ul_new_feeds = soup_detail.find_all('li',{'class':'newsFeed_item'})

        for content in ul_new_feeds:
            href_detail = content.find('div',{'class':'newsFeed_item_title'})
            href_detail_rul = content.find('a')['href']
            contents = {}
            contents['category'] =cate
            contents['title'] =href_detail.text
            contents['url'] =href_detail_rul

            soup_article = BeautifulSoup(requests.get(href_detail_rul).text,'html.parser')
            article_word = soup_article.find('article')

            contents['flg'] ='検索ワードあり' if serch_word in article_word.text else ''
            contents_list.append(contents)

        contents_df = pd.DataFrame(contents_list)
        contents_df = contents_df.sort_values(['flg'],ascending=False)
    return contents_df

st.title('Yahoo News Check')

st.sidebar.markdown('### 検索キーワード')
serch_word = st.sidebar.text_area('キーワードを入力してください')

st.sidebar.markdown('### 検索対象日')
dt_now = st.sidebar.date_input('入力してください'
                     ,min_value = date(2022,1,1)
                     ,max_value = date.today()
                     ,value = date.today())
dt_now = dt_now.strftime('%Y%m%d')

st.button('更新')

contents_df = check_yahoo_news(serch_word,dt_now)
st.markdown('### 検索された記事')
st.dataframe(contents_df)
