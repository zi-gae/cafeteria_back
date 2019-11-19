from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException
import time
from datetime import datetime
from selenium.webdriver.common.alert import Alert

today = datetime.today().day
year = datetime.today().year


def dormitory(uid, upasswd, first, second, apply_text):
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('headless')
    # chrome_options.add_argument("disable-gpu")
    driver = webdriver.Chrome('/Users/user/Library/Caches/Homebrew/downloads/chromedriver')  # 웹브라우저 chrome
    driver.get("http://dormitory.tu.ac.kr/default/main/main.jsp")
    login_bt = driver.find_element_by_xpath('/html/body/div[2]/div[1]/ul[2]/li[2]/a/img')
    login_bt.click()
    print("로그인페이지버튼 클릭")
    try:
        # 학번 입력
        tu_id = driver.find_element_by_name('_58_login')
        tu_id.send_keys(uid)
        # 비번 입력에렁
        tu_pw = driver.find_element_by_name('_58_password')
        tu_pw.send_keys(upasswd)
        # 로그인 버튼클릭
        tu_submit = driver.find_element_by_id('loginImg')
        tu_submit.click()
        print("로그인 완료 버튼 클릭")
        # 외박신청 페이지클릭
        dormitory_out_apply_bt = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/ul/li[3]')
        dormitory_out_apply_bt.click()
        driver.implicitly_wait(1)
        print("외박신청페이지 버튼클릭")
        # ifram으로 전환
        driver.switch_to_frame('iFrameModule')
        print("외박신청 일자 선택")
        first_apply = driver.find_element_by_xpath('//*[@id="txtSTAYOUT_REQ_FR_DT"]')
        driver.execute_script('arguments[0].removeAttribute("readonly")', first_apply)
        first_day = first_apply.send_keys(first)
        sec_apply = driver.find_element_by_xpath('//*[@id="txtSTAYOUT_REQ_TO_DT"]')
        driver.execute_script('arguments[0].removeAttribute("readonly")', sec_apply)
        sec_day = sec_apply.send_keys(second)
        # 외박사유 입력
        text = driver.find_element_by_name('txtBIGO')
        text.send_keys(apply_text)
        # 외박신청 버튼 클릭
        out_apply_submit = driver.find_element_by_name('btnSave')
        out_apply_submit.click()
        print("외박신청 버튼 클릭")
        time.sleep(1)
        alert = Alert(driver).text

        return alert

    except UnexpectedAlertPresentException as e:
        return e.alert_text
    except NoAlertPresentException as e:
        return e.msg

    finally:
        driver.quit()
        print("드라이브 종료")
