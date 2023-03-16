from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By

# --크롬창을 숨기고 실행-- driver에 options를 추가해주면된다
# options = webdriver.ChromeOptions()
# options.add_argument('headless')

def get_reviews(dong, name): 

    # 옵션 생성
    options = webdriver.ChromeOptions()
    # 창 숨기는 옵션 추가
    options.add_argument("headless")

    url = 'https://map.naver.com/v5/search'
    driver = webdriver.Chrome('restaurant/register_functions/chromedriver', options=options)
    query = dong + " " + name
    driver.get(f"https://map.naver.com/v5/search/{query}?c=14203933.7141038,4562681.4505997,10,0,0,0,dh")

    link = f"https://map.naver.com/v5/search/{query}?c=14203933.7141038,4562681.4505997,10,0,0,0,dh"
    
    sleep(5)

    driver.switch_to.default_content()
    driver.switch_to.frame("entryIframe")

    sleep(3)

    try:
        visitor_reviews = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/ul/li/div[1]/div[2]/span[3]/text()[2]').text
        blog_reviews = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/ul/li/div[1]/div[2]/span[4]/text()[2]').text
        sleep(3)
    
    except:
        visitor_reviews = driver.find_element(By.CSS_SELECTOR, "#app-root > div > div > div > div.place_section.GCwOh > div._3uUKd._2z4r0 > div._20Ivz > span:nth-child(2) > a > em").text
        blog_reviews = driver.find_element(By.CSS_SELECTOR, "#app-root > div > div > div > div.place_section.GCwOh > div._3uUKd._2z4r0 > div._20Ivz > span:nth-child(3) > a > em").text

    print(visitor_reviews, blog_reviews)

    return visitor_reviews, blog_reviews, link

