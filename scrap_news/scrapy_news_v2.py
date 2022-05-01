import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os

## scrap news
def scrap_news(news_title,dates,contents,urls,driver,start_page,pages):
    current_page = int(start_page)
    for i in range(pages):
        news = []
        if i != 0:
            next_button = driver.find_element(By.CLASS_NAME, 'p_next')
            next_button.send_keys(Keys.RETURN)
        print('正在爬取第'+str(current_page)+'頁')
        time.sleep(2)
        titles = driver.find_elements_by_class_name('tit')
        for title in titles:
            news.append(title.text)
        count = 1
        for new in news:
            print('第'+str(current_page)+'頁的第'+str(count)+'則新聞')
            news_title.append(new)
            time.sleep(2)
            a = driver.find_element(By.LINK_TEXT, new)
            a.send_keys(Keys.RETURN)
            time.sleep(2)
            urls.append(driver.current_url)
            time.sleep(6)
            date = driver.find_element(By.CLASS_NAME, 'time')
            dates.append(date.text)
            time.sleep(2)
            content = driver.find_element(By.CLASS_NAME, 'text')
            contents.append(content.text)
            time.sleep(2)
            driver.back()
            time.sleep(2)
            count+=1
    
        current_page+=1
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
    start_page = input('輸入起始頁數: ')
    print('起始頁數: ' + start_page)
    pages = int(input('輸入爬取頁數: '))
    print('爬取頁數: '+ str(pages))
    end_time = input('輸入最新日期(default:今天日期 ex. 20220501): ')
    if end_time == '':
        end_time = time.strftime('%Y%m%d', time.localtime())
        
    print('最新日期: ' + end_time)
    
    # ## set keyword
    # keyword = '核四'
    # ## set start page
    # start_page = '2'
    # ## set how many pages you want
    # pages = 1
    # ## set time
    start_time = '20041201'
    # end_time = '20220501'
    
    ## chrome driver
    driver_path = 'driver/chromedriver.exe'
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("prefs", {"profile.password_manager_enabled": False, "credentials_enable_service": False})
    options.use_chromium = True
    
    driver = webdriver.Chrome(driver_path, options=options)
    
    ## search
    url_format = 'https://search.ltn.com.tw/list?keyword='+keyword+'&start_time='+start_time+'&end_time='+end_time+'&sort=date&type=all&page='
    # print(url_format)
    target_url = url_format + start_page
    print("目標初始網址: ", target_url)
    driver.get(target_url)
    print('網頁名稱: '+ driver.title)
    
    ## data
    ## 新聞標題
    news_title = []
    ## 新聞時間
    dates = []
    ## 新聞內容
    contents = []
    ## 新聞連結
    urls = []
    
    ## Create Folder
    if not os.path.isdir('result/'):
        os.mkdir('result/')
    
    news_title,dates,contents,urls = scrap_news(news_title,dates,contents,urls,driver,start_page,pages)
    save_csv(news_title,dates,contents,urls)
    
    print('執行完畢')