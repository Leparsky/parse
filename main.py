#https://habr.com/post/322608/
#https://habr.com/post/250921/
from selenium import webdriver
import selenium.common.exceptions
from selenium.webdriver.common.keys import Keys
import requests  # осуществляет работу с HTTP-запросами
import urllib.request  # библиотека HTTP
from lxml import html  # библиотека для обработки разметки xml и html, импортируем только для работы с html
import re  # осуществляет работу с регулярными выражениями
from bs4 import BeautifulSoup  # осуществляет синтаксический разбор документов HTML
import csv  # осуществляет запись файла в формате CSV
import tkinter  # создание интерфейса
from tkinter.filedialog import *  # диалоговые окна
global proxy1     #объвляем глобальную переменную для запоминания прокси на следующий проход цикла
proxy1 = ''       #и приравниваем к пустому тексту
#BASE_URL = 'https://ajento.ru/'     #адрес сайта для парсинга
BASE_URL = 'https://ajento.ru'     #адрес сайта для парсинга
numproxy  =-1    #текущий номер прокси изсписка
pagesproxycount =0 #количество страниц , полученных через текущий прокси
proxy = None

root = Tk()                                    #главное окно
root.geometry('850x500')                       #ширина и высота главного окна в пикселях
txt1 = Text(root, width = 18, heigh = 2)       #текстовое поле для ввода поисковых слов
txt2 = Text(root, width = 60, heigh = 22)      #текстовое поле для вывода данных
lbl4 = Label(root, text = '')                  #надпись для вывода прокси
btn1 = Button(root, text = 'Отпарсить сайт')   #кнопка для парсинга
btn2 = Button(root, text = 'Найти по слову')    #кнопка для поиска
btn3 = Button(root, text = 'Очистить поля')     #кнопка для очистки полей
lbl1 = Label(root, text = 'Впишите ключевые слова для поиска')      #надпись для поиска
lbl2 = Label(root, text = '')                   #надпись для вывода процента парсинга
lbl3 = Label(root, text = '')

def get_bsoup_proxy(url) :
    global proxy1
    global pagesproxycount
    pagesproxycount+=1
    if pagesproxycount>=15 : proxy1 = proxy.get_proxy()# получить proxy-адрес
    lbl4.update()
# обновляем виджет
    lbl4.config(text='Прокси: ' + proxy1)
# и приравниваем к полученному прокси
    recieved = False
    #страница не получена
    while not recieved :
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
        }
        try:  # обработчик исключительных ситуаций
            r = requests.get(url , proxies={'https': proxy1},headers = headers )
            parsing = BeautifulSoup(r.content, "lxml")
            # получаем данные со страницы сайта
            # вызываем функцию сохранения данных в csv, передаем туда массив projects
            recieved=True
        except requests.exceptions.ProxyError as e:
            # неудача при подключеннии с прокси
            print(e)
            proxy1 = proxy.get_proxy()
            # сменим прокси
            pagesproxycount = 0
            #и обнулим счетчик
            recieved = False
        except requests.exceptions.ConnectionError as e:
            # не удалось сформировать запрос
            print(e)
        except requests.exceptions.ChunkedEncodingError as e:
            # сделана попытка доступа к сокету методом, запрещенным правами доступа
            print(e)
        except requests.exceptions.HTTPError as e:
            # HTTPError
            print(e)
    return parsing
#https://gist.github.com/tushortz/cba8b25f9d80f584f807b65890f37be5
def get_proxies(co=co):
    driver = webdriver.Chrome(chrome_options=co)
    driver.get("https://free-proxy-list.net/")

    PROXIES = []
    proxies = driver.find_elements_by_css_selector("tr[role='row']")
    for p in proxies:
        result = p.text.split(" ")

        if result[-1] == "yes":
            PROXIES.append(result[0]+":"+result[1])

    driver.close()
    return PROXIES


ALL_PROXIES = get_proxies()


def proxy_driver(PROXIES, co=co):
    prox = Proxy()

    if PROXIES:
        pxy = PROXIES[-1]
    else:
        print("--- Proxies used up (%s)" % len(PROXIES))
        PROXIES = get_proxies()

    prox.proxy_type = ProxyType.MANUAL
    prox.http_proxy = pxy
    prox.socks_proxy = pxy
    prox.ssl_proxy = pxy

    capabilities = webdriver.DesiredCapabilities.CHROME
    prox.add_to_capabilities(capabilities)

    driver = webdriver.Chrome(chrome_options=co, desired_capabilities=capabilities)

    return driver

def main(event):
    global proxy
    lstCatPages=[]
    #страницы каталога

    # присваиваем классу
    proxy = Proxy()
    proxy1 = proxy.get_proxy()  # получить proxy-адрес
    ''' 
    bsObj=get_bsoup_proxy(BASE_URL)
    #получаем главную страницу сайта
    for kat in bsObj.findAll("a",{"class":"cs-menu__link"}) :
        lstCatPages.append(kat.attrs["href"])  if kat.attrs["href"] not in lstCatPages else None
    #добавляем в список верхние меню, проверяем задвоение
    for kat in bsObj.findAll("a",{"class":"cs-sub-menu__link"}) :
        lstCatPages.append(kat.attrs["href"]) if kat.attrs["href"] not in lstCatPages else None
    #добавляем в список вложеные подменю проверяем задвоение
    '''

    lstCatPages.append("/g20508555-ajento-kurtki-optom")
    #lstCatPages.append("/g21160870-ajento-rubashki")
    #для тэста
    lstGoodPages = []
    # страницы каталога товаров
    '''
    for page in lstCatPages:
        bsObj = get_bsoup_proxy(BASE_URL+page)
        for kat in bsObj.findAll("a", {"class": "cs-goods-title"}):
            lstGoodPages.append(kat.attrs["href"]) if kat.attrs["href"] not in lstGoodPages else None
            #добавляем в список товаров ссылку,если такой ссылки нет
            lbl3.config(text='Всего найдено страниц: ' + str(len(lstGoodPages)))
        for kat in bsObj.findAll("a", {"class": "b-pager__link"}):
            lstCatPages.append(kat.attrs["href"]) if kat.attrs["href"] not in lstCatPages else None
    '''
    lstGoodPages.append("https://ajento.ru/p336841792-ajento-muzhskoj-bomber.html")
    url   = ""#url
    cost  = ""# Цена
    size  = ""# Размер
    art   = ""# Артикул
    color = ""# Цвет
    edizm = ""# Единица    измерения
    descr = ""# // Описание
    album = ""# // Альбом
    position = ""# Позиция
    picture = ""# // Ссылка на картинку
    name = ""# Название

    pagesproxycount = 30
    for page in lstGoodPages:
        #driver = webdriver.Firefox()
        pagesproxycount+=1
        if pagesproxycount>30:
            pagesproxycount=0
            get_bsoup_proxy(page)
            #вызов для проверки прокси
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--proxy-server=%s' % proxy1)
            driver = webdriver.Chrome(chrome_options=chrome_options)


        driver.maximize_window()
        driver.get(page)
        url = page
        #cost = bsObj.find("span", {"data-qaid": "product_price"}).get_text()
        #for sz in bsObj.find("div", {"class": "b-custom-drop-down"}):
        #    size+=sz.get_text()+','
        #art=bsObj.find("span", {"data-qaid": "product_code"}).get_text()
        #name=bsObj.findAll("span", {"data-qaid": "product_code"})
        element = driver.find_element_by_xpath("//p[@class='b-product-cost__price']")
        cost=(element.text)

        for element in driver.find_elements_by_xpath("//li[ @class='b-custom-drop-down__list-item']"):
            size+=element.get_attribute("innerHTML")+','

        element = driver.find_element_by_xpath("//h1[@class='cs-title cs-title_type_product cs-online-edit']/span")
        name = (element.text)

        element = driver.find_element_by_xpath("//li[@class='b-product-data__item b-product-data__item_type_sku']/span")
        art = (element.text)
        try:
            element = driver.find_element_by_xpath("//li[@class='b-product-data__item b-product-data__item_type_available']")
            descr = (element.text)+' , '
        except selenium.common.exceptions.NoSuchElementException:
            None
        try:
                element = driver.find_element_by_xpath("//li[@class='b-product-data__item b-product-data__item_type_selling']")
                descr += (element.text)
        except selenium.common.exceptions.NoSuchElementException:
                None
        try:
            element = driver.find_element_by_xpath("//p[@class='b-product-cost__min-order']")
            descr += (element.text)
        except selenium.common.exceptions.NoSuchElementException:
            None





        #/ ul[@ class ='b-custom-drop-down__list']

def main2(event):
#запуск функции с передачей переменной event (для работы виджетов)
    page_count = get_page_count(get_html(BASE_URL))
#переменную присваиваем функции пересчета страниц, где сначала выполняется другая функция, получающая http-адрес от переменной BASE_URL
    lbl3.config(text='Всего найдено страниц: '+str(page_count))
#меняем текстовую часть переменной lbl3 на количество найденных страниц
    page = 1
#переменная для счетчика
    projects = []
#массив для хранения всей искомой информации
    while page_count != page:
#цикл выполняется, пока переменная page не равна количеству найденных страниц
        proxy = Proxy()
#присваиваем классу, где зададим нужные параметры
        proxy = proxy.get_proxy()
#получать proxy-адрес
        lbl4.update()
#обновляем виджет
        lbl4.config(text='Прокси: '+proxy)
#и приравниваем к полученному прокси
        global proxy1
#глобальная переменная
        proxy1 = proxy
#приравниваем переменные для дальнейшей проверки их совпадения
        try:      #обработчик исключительных ситуаций
            for i in range(1,10):
#этот цикл будет прогонять полученный прокси определенное количество раз (range - определяет, сколько раз будем его использовать для входа на сайт). Можно и каждый раз брать новый прокси, но это существенно замедлит скорость работы программы
                page += 1
#счетчик необходим для подсчета выполненной работы
                lbl2.update()
#обновляем виджет
                lbl2.config(text='Парсинг %d%%'%(page / page_count * 100))
#меняет процент сделанной работы от 100%
                r = requests.get(BASE_URL + '?page=%d' % page, proxies={'https': proxy1})
#получаем данные со страницы сайта
                parsing = BeautifulSoup(r.content, "lxml")
#получаем html-код по средству BeautifulSoup (чтобы позже использовать поисковые возможности этого модуля) для дальнейшей передачи переменной в функцию
                projects.extend(parse(BASE_URL + '?page=%d' % page, parsing))
#получаем данные из функции parse (передавая адрес страницы и html-код) и добавляем их в массив
                save(projects, 'proj.csv')
#вызываем функцию сохранения данных в csv, передаем туда массив projects
        except requests.exceptions.ProxyError as e:
#неудача при подключеннии с прокси
            print(e)
            continue
        except requests.exceptions.ConnectionErroras as e:
# не удалось сформировать запрос
            print(e)
            continue
        except requests.exceptions.ChunkedEncodingError as e:
#сделана попытка доступа к сокету методом, запрещенным правами доступа
            print(e)
            continue

def get_html(url):
#объявление функции и передача в нее переменной url, которая является page_count[count]
    response = urllib.request.urlopen(url)
#это надстройка над «низкоуровневой» библиотекой httplib, то есть, функция обрабатывает переменную для дальнейшего взаимодействия с самим железом
    return response.read()
#возвращаем полученную переменную с заданным параметром read для корректного отображения

def get_page_count(html):
#функция с переданной переменной html
   soup = BeautifulSoup(html, 'html.parser')
#получаем html-код от url сайта, который парсим
   paggination = soup('ul')[3:4]
#берем только данные, связанные с количеством страниц
   lis = [li for ul in paggination for li in ul.findAll('li')][-1]
#перебираем все страницы и заносим в массив lis, писать так циклы куда лучше для работоспособности программы
   for link in lis.find_all('a'):
#циклом ищем все данные связанные с порядковым номером страницы
       var1 = (link.get('href'))
#и присваиваем переменной
   var2 = var1[-3:]
#создаем срез, чтобы получить лишь число
   return int(var2)
#возвращаем переменную как числовой тип данных

class Proxy:
    # создаем класс
    proxy_url = 'http://www.ip-adress.com/proxy_list/'
    # переменной присваиваем ссылку сайта, выставляющего прокси-сервера
    proxy_list = []

    # пустой массив для заполнения

    def __init__(self):
        # функция конструктора класса с передачей параметра self
        r = requests.get(self.proxy_url)
        # http-запрос методом get, запрос нужно осуществлять только с полным url
        str = html.fromstring(r.content)
        # преобразование документа к типу lxml.html.HtmlElement
        result1 = str.xpath(".//tr/td[1]")
        result=[]
        for member in result1:
           r1=member.xpath(".//text()")
           result.append(r1[0]+r1[1]);
           # суммируем адрес прокси и порт
        self.list = result
    # конструктору класса приравниваем прокси

    def get_proxy(self):
        # функция с передачей параметра self
        global numproxy;
        numproxy+=1
        if numproxy>=len(self.list) :
            numproxy=0
        url = 'https://' +self.list[numproxy]
        #Берем следующий по порядку прокси.
        return url


# возвращаем данные

def parse(html,parsing):
 #запуск функции с получением переменных html и parsing
   projects = []
#создаем пустой массив, где будем хранить все полученные данные
   table = parsing.find('div' , {'class' : 'container-fluid cols_table show_visited'})
#находим часть html-кода, хранящую название, категорию, цену, количество заявок, краткое описание
   for row in table.find_all('div' , {'class' : 'row'}):
#отбираем каждую запись
      cols = row.find_all('div')
#получаем название записи
      price = row.find_all('div' , {'class' : 'col-sm-1 amount title'})
#получаем цену записи
      cols1 = row.find_all('div' , {'class' : 'col-xs-12' , 'style' : 'margin-top: -10px; margin-bottom: -10px'})
#получаем краткое описание записи
      if cols1==[]:
#если массив остался пуст,
          application_text = ''
#то присваиваем пустую строку
      else:      #если не пуст
          application_text = cols1[0].text
#приравниваем к тексту из html-кода
      cols2 = [category.text for category in row.find_all('a' , {'class' : 'text-muted'})]
#с помощью цикла получаем категорию и заявку записи
      projects.append({'title': cols[0].a.text, 'category' : cols2[0], 'applications' : cols[2].text.strip(), 'price' : price[0].text.strip() , 'description' : application_text})
#в массив projects помещаем поочередно все найденные данные
   return projects
#возвращаем проект для сохранения

def delete(event):             #запуск функции
    txt1.delete(1.0, END)      #удаляет текст с вводимыми данными
    txt2.delete(1.0, END)      #удаляет текст с выведенными данными


def poisk(event):
    # запуск функции с передачей переменной event для работоспособности интерфейса
    file = open("proj.csv", "r")
    # открытие файла, где мы сохранили все данные
    rdr = csv.DictReader(file, fieldnames=['name', 'categori', 'zajavki', 'case', 'opisanie'])
    # читаем данные из файла по столбцам
    poisk = txt1.get(1.0, END)
    # получаем данные из поля для поиска соответствий
    poisk = poisk[0:len(r) - 1]
    # конкотенация необходима для отбрасывания последнего символа, который программа добавляет самостоятельно ('\n')
    for rec in rdr:
        # запуск цикла, проход по каждой строке csv-файла
        data = rec['opisanie'].split(';')
        # к переменной приравниваем данные по описанию задания
        data1 = rec['case'].split(';')
        # к переменной приравниваем данные по цене задания
        data = ('').join(data)
        # преобразовываем в строку
        data1 = ('').join(data1)
        # преобразовываем в строку
        w = re.findall(poisk, data)
        # ищем в описании совпадение с поисковыми словами
        if w != []:
            # условие, если переменная w не равна пустому массиву, то продолжать
            if data1 == '':
                # условие проверяющее, если цена не была получена, то продолжать
                data1 = 'Договорная'  # заменяем пустое значение на текст
            txt2.insert(END, data + '--' + data1 + '\n' + '---------------' + '\n')
            # соединяем краткое описание заказа, его цену, переход на новую строку, символы, разделяющие заказы и снова переход на новую строку

def save(projects, path):
#функция с переданной переменной и названием файла как переменная path
   with open(path, 'w') as csvfile:
#открываем файл как path и w (Открывает файл только для записи. Указатель стоит в начале файла. Создает файл с именем имя_файла, если такового не существует)
      writer = csv.writer(csvfile)
#writer - осуществляет запись файла, csv - определяет формат файла
      writer.writerow(('Проект', 'Категории', 'Заявки' , 'Цена' , 'Описание'))
#writerow - создает заглавия каждого заполняемого столбца
      for project in projects:
#перебираем элементы в массиве
          try:
#обработчик исключительных ситуаций
              writer.writerow((project['title'], project['category'], project['applications'], project['price'], project['description']))
#каждому параметру присвоим данные
          except UnicodeEncodeError:
#в description иногда будут попадаться символы из других кодировок, придется брать как пустую строку
              writer.writerow((project['title'], project['category'], project['applications'], project['price'], ''))
#каждому параметру присваиваем данные

btn1.bind('<Button-1>', main)      #при нажатии клавиши вызывает основную функцию
btn2.bind('<Button-1>', poisk)     #вызывает функцию поиска нужных заказов
btn3.bind('<Button-1>', delete)    #вызывает функцию очистки полей

lbl2.grid(row = 4, column = 1)
lbl4.grid(row = 5, column = 1)
lbl3.grid(row = 3, column = 1)
btn1.grid(row = 1, column = 1)
btn3.grid(row = 2, column = 1)
btn2.grid(row = 1, column = 2)
lbl1.grid(row = 2, column = 2)
txt1.grid(row = 3, column = 2)
txt2.grid(row = 6, column = 3)
root.mainloop()                     #запуск приложения

