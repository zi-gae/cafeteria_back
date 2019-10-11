from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.alert import Alert
import time


def dormitory(uid, upasswd, first, second, apply_text):
    # display = Display(visible=0, size=(800, 800))
    # display.start()
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
        # 조회버튼 클릭
        print("조회버튼 클릭")
        lookup_bt = driver.find_element_by_xpath('//*[@id="btnRetrieveStd"]')
        lookup_bt.click()
        time.sleep(1)
        # 외박신청 일자 선택
        print("외박신청 일자 선택")
        apply = driver.find_element_by_name('txtSTAYOUT_REQ_FR_DT')
        apply.click()
        time.sleep(1)
        if first < second:
            print("첫번째 외박일 선택")
            first_day = driver.find_element_by_xpath('//*[text() = ' + first + ']')  # text 추출
            time.sleep(1)
            first_day.click()
            apply = driver.find_element_by_xpath('//*[@id="txtSTAYOUT_REQ_TO_DT"]')
            apply.click()
            print("두번째 외박인 선택")
            second_day = driver.find_element_by_xpath('//*[text() = ' + second + ']')  # text 추출
            time.sleep(1)
            second_day.click()
        else:
            first_day = driver.find_element_by_xpath('//*[text() = ' + first + ']')  # text 추출
            first_day.click()
            print("첫번째 외박일 선택")
            apply = driver.find_element_by_xpath('//*[@id="txtSTAYOUT_REQ_TO_DT"]')
            apply.click()
            next_month = driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div/a[2]/span')
            next_month.click()
            second_day = driver.find_element_by_xpath('//*[text() = ' + second + ']')  # text 추출
            second_day.click()
        # 외박사유 입력
        text = driver.find_element_by_name('txtBIGO')
        time.sleep(1)
        text.send_keys(apply_text)
        print("dormitory out reason")
        # 외박신청 버튼 클릭
        out_apply_submit = driver.find_element_by_name('btnSave')
        out_apply_submit.click()
        print("외박신청 버튼 클릭")
        time.sleep(1)
        alert = Alert(driver).text

        return alert

    except UnexpectedAlertPresentException as e:
        return e.alert_text

    finally:
        driver.quit()
        print("드라이브 종료")
        # display.stop()
        # print("디스플레이 종료")
