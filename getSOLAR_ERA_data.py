# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 11:28:53 2019

@author: Igor
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from   bs4 import BeautifulSoup
from unicodedata import normalize
import time
import pandas as pd
from selenium.webdriver import ActionChains
#import urllib2 

# In[]
browser = webdriver.Chrome(executable_path=r'C:\Users\Igor\Documents\MEGA\MEGAsync\UFJF\Qualificacao\Dados\Tarifas_por_companhia\chromedriver_win32\chromedriver.exe')
browser.get('http://www.eraenergie.com.br/simulador/')
time.sleep(5)

browser.find_element_by_xpath("//input[@id='campoCEP']").send_keys('36025275')
browser.find_element_by_xpath("//select[@name='campoTipoLigacao']/option[text()='Monofásico']").click()
data = []
for w in range(200,230,10):
    browser.find_element_by_xpath("//input[@id='campoConsumoMedio']").send_keys(str(w))
    browser.find_element_by_xpath("//a[@id='btEnviar']").click()
    time.sleep(3)
    info = browser.find_element_by_xpath("//section[@class='resultado']").text
    info = info.split('\n')
    price = float(info[5].split(' ')[2].replace('.','').replace(',','.'))
    p_int = float(info[1].split(' ')[3].replace(',','.'))
    n_int = float(info[2].split(' ')[3])
    data.append({'Fonte':'ERA_Energie',
                 'preco_min':price,
                 'preco_max':price,
                 'Potência_Instalada':p_int,
                 'Consumo_estimado': w,
                 'Potência_painel':(p_int/n_int)*1000,
                 'n_modulos':n_int,
                 'area_modulos':'N/A',
                 'peso_sistema':'N/A'})
    browser.find_element_by_xpath("//a[@href='javascript:history.go(-1);']").click()
    time.sleep(2)
    browser.find_element_by_xpath("//input[@id='campoConsumoMedio']").clear()   

d = pd.DataFrame(data)
d.to_csv('ERA_solar.csv')