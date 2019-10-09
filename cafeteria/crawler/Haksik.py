from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from datetime import date

today = date.today()


def restaurant():
    req = Request("http://tusso.tu.ac.kr/jsp/manage/restaurant/restaurant_menu.jsp")
    res = urlopen(req)
    html = res.read().decode("UTF-8")
    bs = BeautifulSoup(html, 'html.parser')
    student_tr_tag = bs.select('body > div.center > div:nth-child(4) > table > tbody > tr')
    faculty_tr_tag = bs.select('body > div.center > div:nth-child(6) > table > tbody > tr')

    ddoock = []
    il = []
    rice = []
    noodle = []
    yang = []
    faculty_menu = []

    if student_tr_tag == [] and faculty_tr_tag == []:
        message = "식단 메뉴가 없습니다."
        return message
    else:
        for students in student_tr_tag:
            menu = students.text.split()
            menu = ",".join(menu) \
                .replace('크림스프/야채샐러드/피클', '') \
                .replace('김치/단무지', '') \
                .replace('크리스프/야채샐러드/피클', '')
            if '뚝배기' in menu:
                menu = menu.replace('뚝배기,', '')
                ddoock.append(menu)
            elif '일품' in menu:
                menu = menu.replace('일품,', '')
                il.append(menu)
            elif '덮밥' in menu:
                menu = menu.replace('덮밥,', '')
                rice.append(menu)
            elif '면류' in menu:
                menu = menu.replace('면류,', '')
                noodle.append(menu)
            elif '양식' in menu:
                menu = menu.replace('양식', '')
                menu = menu.split(',')
                while '' in menu:
                    menu.remove('')
                for menus in menu:
                    yang.append(menus)
        for faculties in faculty_tr_tag:
            menu = faculties.text.split()
            menu = ",".join(menu)
            menu = menu.replace('특정식', '')
            menu = menu.split(',')
            menu.remove('')
            for menus in menu:
                faculty_menu.append(menus)

        return ddoock, il, rice, yang, noodle, faculty_menu


restaurant()
# schedule.every().day.at("00:00").do(restaurant)
#
# while True:
#     schedule.run_pending()