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
BASE_URL = 'https://ajento.ru/'     #адрес сайта для парсинга
massiv = []       #массив для хранения прокси
4444