#!/usr/bin/env python3
"""
download chromedriver: https://chromedriver.chromium.org/downloads
- schdule: run weekday only
- clean up monthly

"""
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from time import time
import time as time_sleep
import requests

def str2billion(raw_str):
    return round(int(raw_str.replace(',',''))/100000000, 2)

def numb_frmt(number_float, to_float=0): 
    if to_float==0:
        return "{:,}".format(number_float)
    elif to_float==1:
        return "{:,.1f}".format(number_float)
    elif to_float==2:
        return "{:,.2f}".format(number_float)

timer = False

def timeit(method):
    """
    timer for a function:
      1. assign global variable "timer" = True before this function
      2. assign decorater  "@timeit" before the function to time
    """
    if not timer:
        return method

    def timed(*args, **kw):
        ts = time()
        result = method(*args, **kw)
        te = time()
        if "log_time" in kw:
            name = kw.get("log_name", method.__name__.upper())
            kw["log_time"][name] = int((te - ts) * 1000)
        else:
            print("%r  %2.2f ms" % (method.__name__, (te - ts) * 1000))
        return result

    return timed

last_month = str(datetime.now().month - 1)
today_month = str(datetime.now().month)
today_day = str(datetime.now().day)
todate =  datetime.now().strftime('%Y/%m/%d')

@timeit
def drive_setup(headless=True):
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-dev-shm-usage")
    if headless:
        chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path="chromedriver", options=chrome_options)
    return driver

# 1. P/E
@timeit
def get_web1(driver)->str:
    web1 = "https://www.twse.com.tw/zh/trading/statistics/list02-199.html"
    driver.get(web1)
    drop1 = Select(driver.find_element(By.NAME,'mm'))
    drop1.select_by_value(last_month)
    driver.find_element(By.XPATH, '//*[@id="form"]/div/div/div[2]/button').click()
    time_sleep.sleep(8)
    driver.find_element(By.XPATH, '//*[@id="reports"]/div[1]/div[2]/table/tbody/tr/td[2]/a').click()
    time_sleep.sleep(8)
    web1_add = "https://www.twse.com.tw/zh/trading/historical/fmtqik.html"
    driver.get(web1_add)
    time_sleep.sleep(8)
    tableTSE_data = driver.find_element(By.CLASS_NAME, 'rwd-table.dragscroll.sortable.F1.R2_').get_attribute('innerHTML')
    parseTSE_row = BeautifulSoup(tableTSE_data, "html.parser")
    lastest_d = parseTSE_row.find('tbody').find_all('tr')[-1]
    item1_amt = str(numb_frmt(str2billion(lastest_d.find_all('td')[2].text), 2))
    item1_ind = lastest_d.find_all('td')[-2].text
    if lastest_d.find_all('td')[0].text[-5:] != todate[-5:]:
        return item1_amt+"*", item1_ind+'*'
    return item1_amt, item1_ind



@timeit
def parse_web1_file()->str:
    # parse file
    import re
    import os
    import glob
    import xlrd
    from zipfile import ZipFile
    chechZipf = glob.glob("C:\\Users\\USER\\Downloads\\*.zip")
    item1 = None
    if len(chechZipf) > 0:
        with ZipFile(chechZipf[0], 'r') as zObj:
            zObj.extractall(path='C:\\Users\\USER\\Downloads')
        os.remove(chechZipf[0])
        chechExf = glob.glob("C:\\Users\\USER\\Downloads\\*.xls")
        if len(chechExf) > 0:
            book = xlrd.open_workbook(chechExf[0])
            sh = book.sheet_by_index(3)
            item1 = float(re.findall('(?<=:).*', str(sh.row(4)[-1]))[0])
            os.remove(chechExf[0])
    return item1

@timeit
# 2. Juridical Person
def get_web2(driver):
    web2 = "https://www.twse.com.tw/zh/trading/foreign/bfi82u.html"
    driver.get(web2)
    time_sleep.sleep(6)
    drop1 = Select(driver.find_element(By.XPATH,'//*[@id="form"]/div/div[1]/div[1]/span/select[2]'))
    drop1.select_by_value(today_month)
    drop2 = Select(driver.find_element(By.XPATH,'//*[@id="form"]/div/div[1]/div[1]/span/select[3]'))
    drop2.select_by_value(today_day)
    driver.find_element(By.XPATH, '//*[@id="form"]/div/div[2]/button').click()
    time_sleep.sleep(6)
    table_data = driver.find_element(By.CLASS_NAME, 'is-last-page').get_attribute('innerHTML')
    parse_row = BeautifulSoup(table_data, "html.parser")
    item2_self = round(str2billion(parse_row.find_all('tr')[0].find_all('td')[3].text) + str2billion(parse_row.find_all('tr')[1].find_all('td')[3].text), 1)
    item2_trust = round(str2billion(parse_row.find_all('tr')[2].find_all('td')[3].text),1)
    item2_foreign = round(str2billion(parse_row.find_all('tr')[3].find_all('td')[3].text) + str2billion(parse_row.find_all('tr')[4].find_all('td')[3].text),1)
    item2_tot = round(item2_self+item2_trust+item2_foreign,2)
    return str(item2_self), str(item2_trust), str(item2_foreign), str(item2_tot)

@timeit
# 6. Margin Trading and Short Selling
def get_web6(driver):
    web6 = "https://www.cmoney.tw/finance/f00012.aspx"
    driver.get(web6)
    time_sleep.sleep(8)
    tableList_data = driver.find_element(By.CLASS_NAME, 'tb.tb1').get_attribute('innerHTML')
    parseList_row = BeautifulSoup(tableList_data, "html.parser")
    item6_margin_change, item6_margin_amt = [float(i.text.replace(',', '')) for i in parseList_row.find_all('tr')[1].find_all('td')[1:3]]
    item6_maintein = float(parseList_row.find_all('tr')[1].find_all('td')[-1].text.replace(',',''))
    item6_short_change, item6_short_amt = [float(i.text.replace(',', '')) for i in parseList_row.find_all('tr')[2].find_all('td')[1:3]]
    updateTm = driver.find_element(By.XPATH, '//*[@id="HeaderContent"]/time/span[2]').get_attribute('innerHTML')
    if updateTm.replace('-','/') != todate:
        return numb_frmt(item6_margin_change,1)+"*", numb_frmt(item6_margin_amt,1), numb_frmt(item6_short_change,1), numb_frmt(item6_short_amt/10000,1), numb_frmt(item6_maintein,1)
    return numb_frmt(item6_margin_change,1), numb_frmt(item6_margin_amt,1), numb_frmt(item6_short_change,1), numb_frmt(item6_short_amt/10000,1), numb_frmt(item6_maintein,1)

@timeit
# 3. Future
def get_web3(driver):
    web3 = "https://www.taifex.com.tw/cht/3/futContractsDate"
    driver.get(web3)
    time_sleep.sleep(8)
    driver.find_element(By.ID, 'queryDate').clear()
    driver.find_element(By.ID, 'queryDate').send_keys(todate)
    driver.find_element(By.XPATH, '//*[@id="button"]').click()
    time_sleep.sleep(10)
    tableFutr_data = driver.find_element(By.CLASS_NAME, 'table_f').get_attribute('innerHTML')
    parseFutr_row = BeautifulSoup(tableFutr_data, "html.parser")
    item3_trade = numb_frmt(int(parseFutr_row.find_all('tr')[5].find_all('td')[4].text.strip().replace(',','')))
    item3_open = numb_frmt(int(parseFutr_row.find_all('tr')[5].find_all('td')[10].text.strip().replace(',','')))
    return str(item3_trade), str(item3_open)

@timeit
# 5. Option
def get_web5(driver):
    web5 = "https://histock.tw/stock/option.aspx?m=week"
    driver.get(web5)
    time_sleep.sleep(8)
    tableOpt_data = driver.find_element(By.CLASS_NAME, 'tb-stock.tb-option-tw').get_attribute('innerHTML')
    parseOpt_row = BeautifulSoup(tableOpt_data, "html.parser")
    vals_rw = list()
    for row in parseOpt_row.find_all('tr')[2:]:
        tds = row.find_all('td')
        vals_rw.append([int(tds[6].text.replace(',','')), int(row.find_all('th')[0].text.replace(',','')), int(tds[-1].text.replace(',',''))])

    tmpls1 = [x[0] for x in vals_rw]
    tmpls1.sort()
    l1_l_val, l2_l_val = tmpls1[-1], tmpls1[-2]

    tmpls2 = [x[-1] for x in vals_rw]
    tmpls2.sort()
    l1_s_val, l2_s_val = tmpls2[-1], tmpls2[-2]

    l1_short_ind = [x[-1] for x in vals_rw].index(l1_s_val)
    l2_short_ind = [x[-1] for x in vals_rw].index(l2_s_val)

    item5_largest_long = numb_frmt(vals_rw[[x[0] for x in vals_rw].index(l1_l_val)][1], 0)
    item5_sec_long = numb_frmt(vals_rw[[x[0] for x in vals_rw].index(l2_l_val)][1], 0)
    item5_largest_short = numb_frmt(vals_rw[l1_short_ind][1], 0)
    item5_sec_short = numb_frmt(vals_rw[l2_short_ind][1], 0)
    return str(item5_largest_long), str(item5_sec_long), str(item5_largest_short), str(item5_sec_short)

@timeit  
# 7. 2330
def get_web7(driver):
    web7 = "https://histock.tw/stock/chips.aspx?no=2330"
    driver.get(web7)
    time_sleep.sleep(8)
    table_src = driver.find_element(By.CLASS_NAME, 'tb-stock.tbChip.w50p.pr0').get_attribute('innerHTML')
    parse2330_row = BeautifulSoup(table_src, "html.parser")
    item7_2330 = ""
    for tr in parse2330_row.find_all('tr'):
        if len(tr.find_all('td')) > 0:
            if tr.find_all('td')[0].text == todate:
                item7_2330 = tr.find_all('td')[1].text
                pass
    return str(item7_2330)

if __name__=='__main__':
    driver_show = drive_setup(headless=False)
    itm1add_ls = get_web1(driver_show) #item1_add1, item1_add2
    driver_show.close()
    time_sleep.sleep(2)
    driver = drive_setup()
    itm2_ls = get_web2(driver) #item2-1, item2-2, item2-3, item_tot
    itm3_ls = get_web3(driver) #item3-1, item3-2
    itm5_ls = get_web5(driver) #item5-1, item5-2, item5-3, item5-4
    itm7_ls = get_web7(driver) #item7
    itm6_ls = get_web6(driver) #item6-1, item6-2, item6-3, item6-4, item6-5
    itm1_ls = parse_web1_file() #item1
    driver.close()
    
    # Line Notify
    num_list = [datetime.now().strftime('%Y/%m/%d')]+[itm1_ls]+list(itm1add_ls)+list(itm2_ls)+list(itm6_ls)+list(itm3_ls)+list(itm5_ls)+[itm7_ls]
    content = '''
    {}

    加權指數(TSE) 本益比: {}
    收盤價格： {}
    成交量：{} 億

    -------------------------
    [三大法人買賣超金額]

    外資：{} 億
    投信：{} 億
    自營：{} 億
    總和：{} 億

    -------------------------
    台積電外資買買超：{} 張
    -------------------------
    [資券進出場]

    融資：{} 億
    餘額：{} 億
    維持率：{}%

    融券：{} 張
    餘額：{} 萬張

    -------------------------
    [外資期貨多空單]

    交易多空淨額：{} 口
    未平倉多空淨額：{} 口

    -------------------------
    [選擇權最大未平倉]

    買權：最大{} 次大 {}
    賣權：最大{}   次大 {}

    -------------------------
    '''.format(num_list[0], num_list[1], num_list[3], num_list[2], num_list[6], num_list[5], num_list[4], num_list[7], num_list[19], num_list[8], num_list[9], num_list[12], num_list[10], num_list[11], num_list[13], num_list[14], num_list[15], num_list[16], num_list[17], num_list[18])
    

    # Line Notify
    token = '<填寫自己的Token>'

    headers = { "Authorization": "Bearer " + token }
    data = { 'message': content }

    requests.post("https://notify-api.line.me/api/notify",
        headers = headers, data = data)