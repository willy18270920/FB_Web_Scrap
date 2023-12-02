# 這是一段使用selenium爬取FaceBook粉絲專業的爬蟲程式碼
# 其中可以爬取到拜訪網頁的名字、id/帳號、有無藍鉤驗證、相關簡介、追蹤數、向下滑動至12篇貼文的位置並獲取所有展開貼文的連結
# 未來將連同貼文的內文、圖片、按讚數、留言數、分享數、前50則留言的留言內容、該留言按讚數一同爬取下來

# This is a Python code using Selenium for web scraping Facebook fan pages. 
# It is designed to retrieve the names, IDs/accounts, blue check verification status, related introductions, follower counts, scroll down to the position of the 12th post, and obtain all expanded post links. 
# In the future, it aims to crawl the content, images, likes, comments, shares of each post, as well as the content, likes, and ranking of the first 50 comments.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
from time import sleep
import random


username = 'abc@gmail.com'  # type loggin username
pwd = '123'  # type loggin passwd


# 配置Chrome WebDriver
my_options = webdriver.ChromeOptions()
my_options.add_argument("--start-maximized")
my_options.add_argument("--incognito")
my_options.add_argument("--disable-popup-blocking")
my_options.add_argument("--disable-notifications")
my_options.add_argument("--lang=zh-TW")


# 初始化Chrome WebDriver
driver = webdriver.Chrome(options=my_options)

fb_ids = []
fb_names = []
fb_checks = []
fb_intros = []
fb_followers = []
fb_posts = []
fb_links_1 = []
fb_links_2 = []
fb_links_3 = []
fb_links_4 = []
fb_links_5 = []
fb_links_6 = []
fb_links_7 = []
fb_links_8 = []
fb_links_9 = []
fb_links_10 = []
fb_links_11 = []
fb_links_12 = []


def visit():
    url = "https://zh-tw.facebook.com/"
    driver.get(url)
    sleep(5)


def loggin():
    # 輸入帳密
    account = driver.find_element(By.CSS_SELECTOR, 'input[name="email"]')
    account.send_keys(username)
    sleep(6)
    password = driver.find_element(By.CSS_SELECTOR, 'input[name="pass"]')
    password.send_keys(pwd)
    sleep(5)
    # 登入
    button = driver.find_element(
        By.CSS_SELECTOR, "button._42ft._4jy0._6lth._4jy6._4jy1.selected._51sy")
    button.click()
    sleep(6)


def crawl():
    # 讀取URL列表
    urls = ["https://www.facebook.com/profile.php?id=100080421850593",
            "https://www.facebook.com/95mizuki",
            "https://www.facebook.com/cherry.pan.585/"]

    for url in urls:
        driver.get(url)
        # 生成介於30到60秒之間的隨機數
        delay = random.randint(15, 30)
        sleep(delay)
        soup = bs(driver.page_source, "lxml")
        name_scrap = soup.select(
            'div.x78zum5.xdt5ytf.x1wsgfga.x9otpla h1.x1heor9g.x1qlqyl8.x1pd3egz.x1a2a7pz')
        id_scrap = soup.select('div.xng8ra.x6ikm8r.x10wlt62.x1n2onr6.xh8yej3.x1ja2u2z.x1a2a7pz a.x1i10hfl.x6umtig.x1b1mbwd.xaqea5y.xav7gou.xe8uvvx.xggy1nq.x1o1ewxj.x3x9cwd.x1e5q0jg.x13rtm0m.x87ps6o.x1lku1pv.x1a2a7pz.xjyslct.xjbqb8w.x18o3ruo.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1heor9g.x1ypdohk.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6.x16tdsg8.x1hl2dhg.x1vjfegm.x3nfvp2.xrbpyxo.xng8ra.x16dsc37')
        check_scrap = soup.select(
            'svg.x1lliihq.x1k90msu.x2h7rmj.x1qfuztq.x1qq9wsj.xlup9mm.x1kky2od')
        intro_scrap = soup.select(
            'div.x2b8uid.x80vd3b.x1q0q8m5.xso031l.x1l90r2v span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x3x7a5m.x6prxxf.xvq8zen.xo1l8bm.xzsf02u')
        followers_scrap = soup.find_all(
            href=lambda href: href and 'followers' in href)

        # 獲取名字
        if name_scrap:
            fb_text = [name_element.text for name_element in name_scrap]
            fb_name = fb_text[0].split("\xa0")[0]
            fb_names.append(fb_name)

        # 獲取id/帳號
        ids = []
        for id_element in id_scrap:
            id_href = id_element.get('href')
            if "id" in id_href:
                fb_id = id_href.split('=')[-1]
                ids.append(fb_id)
            else:
                fb_id = id_href.split('/')[1]
                ids.append(fb_id)
        fb_ids.append(ids[0])

        # 有無認證，有認證=1，沒認證=0
        if check_scrap:
            fb_checks.append(1)
        else:
            fb_checks.append(0)

        # 獲取簡介
        if intro_scrap:
            fb_intro = [intro_element.text for intro_element in intro_scrap]
            fb_intros.append(', '.join(fb_intro))
        else:
            fb_intros.append("None")

        # 獲取追蹤數
        for follower_element in followers_scrap:
            f_text = follower_element.text
            if "萬" in f_text:
                followers_count = float(f_text.split('\xa0')[0]) * 10000
                fb_followers.append(int(followers_count))
            elif "人" in f_text:
                followers_count = int(f_text.split(' ')[0])
                fb_followers.append(int(followers_count))

        # 滾動到12篇貼文的數量，並讀取HTML
        post_count = 0  # 紀錄已經收集到的貼文數量
        max_post_count = 12
        while post_count < max_post_count:
            body_element = driver.find_element(By.TAG_NAME, 'body')
            body_element.send_keys(Keys.END)
            sleep(2)
            soup = bs(driver.page_source, 'html.parser')
            post_scrap = soup.select(
                'a.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1heor9g.xt0b8zv.xo1l8bm')
            new_post_count = len(post_scrap)
            if new_post_count > post_count:
                post_count = new_post_count
            else:
                break

        # 獲取貼文連結
        fb_links = []
        for post_element in post_scrap[:max_post_count + 1]:
            fb_post = post_element.get('href')
            fb_links.append(fb_post)
        fb_links_lists = [fb_links_1, fb_links_2, fb_links_3, fb_links_4, fb_links_5,
                          fb_links_6, fb_links_7, fb_links_8, fb_links_9, fb_links_10, fb_links_11, fb_links_12]
        for i in range(12):
            fb_links_lists[i].append(fb_links[i])

    print(f"帳號/ID：{fb_ids}")
    print(f"名字：{fb_names}")
    print(f"藍鉤認證：{fb_checks}")
    print(f"追蹤數：{fb_followers}")
    print(f"自我介紹：{fb_intros}")
    fb_links_list = [fb_links_1, fb_links_2, fb_links_3, fb_links_4, fb_links_5,
                     fb_links_6, fb_links_7, fb_links_8, fb_links_9, fb_links_10, fb_links_11, fb_links_12]
    for i in range(12):
        print(f"第{i+1}篇貼文：{', '.join(fb_links_list[i])}")


if __name__ == "__main__":
    visit()
    loggin()
    crawl()
