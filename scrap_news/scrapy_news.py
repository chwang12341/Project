import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

## scrap news
def scrap_news(news_title,dates,contents,urls,driver):
    for i in range(pages):
        news = []
        if i != 0:
            next_button = driver.find_element_by_class_name('p_next')
            next_button.send_keys(Keys.RETURN)
        print('正在爬取第'+str(i+1)+'頁')
        time.sleep(2)
        titles = driver.find_elements_by_class_name('tit')
        for title in titles:
            news.append(title.text)
        count = 1
        for new in news:
            print('第'+str(i+1)+'頁的第'+str(count)+'則新聞')
            news_title.append(new)
            time.sleep(2)
            a = driver.find_element_by_link_text(new)
            a.send_keys(Keys.RETURN)
            time.sleep(2)
            urls.append(driver.current_url)
            time.sleep(6)
            date = driver.find_element_by_class_name("time")
            dates.append(date.text)
            time.sleep(2)
            content = driver.find_element_by_class_name('text')
            contents.append(content.text)
            time.sleep(2)
            driver.back()
            time.sleep(2)
            count+=1
    return news_title,dates,contents,urls

## save
def save_csv(t,d,c,l):
    result = {
              '新聞標題': t,
              '日期時間': d,
              '新聞內容': c,
              '新聞連結': l,
              }
    result_df = pd.DataFrame(result)
    now = time.strftime('%Y%m%d%H%M', time.localtime())
    result_df.to_csv('result/'+now+'_result.csv', encoding = 'utf-8-sig', index = False)
    

if __name__ == '__main__':
    ## Config
    keyword = input('輸入搜尋關鍵字: ')
    print('搜尋: ' + keyword)
    pages = int(input('輸入頁數: '))
    print('爬取頁數: '+ str(pages))
    # keyword = '虛擬貨幣'
    # pages = 6
    
    ## chrome driver
    driver_path = 'driver/chromedriver.exe'
    driver = webdriver.Chrome(driver_path)
    
    ## search
    driver.get('https://search.ltn.com.tw/')
    print('網頁名稱: '+ driver.title)
    search = driver.find_element_by_xpath('//*[@id="keyword_search"]')
    search.send_keys(keyword)
    search.send_keys(Keys.RETURN)
    time.sleep(2)
    
    
    ## data
    ## 新聞標題
    news_title = []
    ## 新聞時間
    dates = []
    ## 新聞內容
    contents = []
    ## 新聞連結
    urls = []
    news_title,dates,contents,urls = scrap_news(news_title,dates,contents,urls,driver)
    save_csv(news_title,dates,contents,urls)
    
    

