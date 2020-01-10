# -*- coding: utf-8 -*-
"""
Created on Fri May 24 14:53:51 2019

@author: Igor
"""

# In[]
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from   bs4 import BeautifulSoup
from unicodedata import normalize
import time
import pandas as pd
from selenium.webdriver import ActionChains
#import urllib2 

# In[]
browser =webdriver.Chrome(executable_path=r'C:\Users\Igor\Documents\MEGA\MEGAsync\UFJF\Qualificacao\Dados\Tarifas_por_companhia\chromedriver_win32\chromedriver.exe')
browser.get('https://www.neosolar.com.br/simulador-solar-calculadora-fotovoltaica')
time.sleep(10)

# In[]

browser.find_element_by_xpath("//select[@name='region-estado-e-cidade-49']/option[text()='MG']").click()
time.sleep(2.5)
browser.find_element_by_xpath("//select[@name='city-estado-e-cidade-49']/option[text()='juiz de fora']").click()
time.sleep(2.5)
browser.find_element_by_xpath("//label[@for='chk-alterar-tarifa-60-alterar-tarifa']").click()
browser.find_element_by_xpath("//input[@name='ajuste-de-tarifa-99']").clear()
browser.find_element_by_xpath("//input[@name='ajuste-de-tarifa-99']").send_keys(100)

action = ActionChains(browser)
bar = browser.find_element_by_xpath("//span[@class='ui-slider-handle ui-state-default ui-corner-all']")
action.click_and_hold(bar).move_by_offset(-500,0).release().perform()
time.sleep(2.5)

data=[]

for i in range(490):
    if i == 1:
        target = browser.find_element_by_xpath("//input[@name='alterar-tarifa-60[]']")
        action.move_to_element(target).release().perform()
        browser.find_element_by_xpath("//div[@class='spinner']/div[3]").click()
    if i >=2:
        browser.find_element_by_xpath("//div[@class='spinner']/div[3]").click()
    browser.find_element_by_xpath("//input[@value='Resultado']").click()
    time.sleep(5)

# In[]
    
    preco = browser.find_element_by_xpath("//div[@class='result-block result-investment text-left']/div[@class='result-highlight bg-black']").text
    preco = preco.split(' ')
    consumo = browser.find_element_by_xpath("//div[@class ='consumo-estimado']/input[1]").get_attribute('value')
    
    indic = browser.find_element_by_xpath("//div[@class='result-block result-indication text-left']").text
    indic = indic.split('\n')
    data.append({'Fonte':'NeoSolar',
                 'preco_min':float(preco[2].replace('.','').replace(',','.')),
                 'preco_max':float(preco[5].replace('.','').replace(',','.')),
                 'Potência_Instalada':indic[1].replace(',','.'),
                 'Consumo_estimado': consumo,
                 'Potência_painel':(float(indic[1].replace(',','.').split(' ')[0])*1000)/float(indic[5].split(' ')[0]),
                 'n_modulos':float(indic[5].split(' ')[0]),
                 'area_modulos':float(indic[9].replace(',','.').split(' ')[0]),
                 'peso_sistema':float(indic[11].replace('.','').replace(',','.').split(' ')[0])})

# In[]
browser.close()
# In[]
browser =webdriver.Chrome(executable_path=r'C:\Users\Igor\Documents\MEGA\MEGAsync\UFJF\Qualificacao\Dados\Tarifas_por_companhia\chromedriver_win32\chromedriver.exe')
browser.get('https://www.portalsolar.com.br/calculo-solar')
time.sleep(10)

# In[]

browser.find_element_by_xpath("//input[@id='lead_name']").send_keys('Igor Leite')
browser.find_element_by_xpath("//input[@id='lead_postalcode']").send_keys('36025275')
browser.find_element_by_xpath("//input[@id=ex]").click()
time.sleep(5)
browser.find_element_by_xpath("//input[@id='lead_email']").send_keys('igormsleite@hotmail.com')
browser.find_element_by_xpath("//select[@id='lead_city']/option[@value='Juíz de Fora']").click()

for i in range(4010,5010,10):
    if i != 4010:
        browser.find_element_by_xpath("//input[@id='lead_monthly_usage']").clear()    
    browser.find_element_by_xpath("//input[@id='lead_monthly_usage']").send_keys(i)
    browser.find_element_by_xpath("//button[@type='submit']").click()
    time.sleep(15)
    data.append({'Fonte':'Portal Solar',
                 'preco_min':float(browser.find_element_by_xpath("//div[@class='info-border-wrapper']").text.split('\n')[-1][2:].replace('.','').replace(',','.')),
                 'preco_max':float(browser.find_element_by_xpath("//div[@class='info-border-wrapper']").text.split('\n')[-1][2:].replace('.','').replace(',','.')),
                 'Potência_Instalada':browser.find_element_by_xpath("//div[@class='energy-data-wrapper content-wrapper info-border-wrapper']/div[1]").text.split('\n')[-1].replace(',','.'),
                 'Consumo_estimado': i,
                 'Potência_painel':(browser.find_element_by_xpath("//div[@class='energy-data-wrapper content-wrapper info-border-wrapper']/div[4]").text.split('\n')[-1].split(' ')[2]),
                 'n_modulos':float(browser.find_element_by_xpath("//div[@class='energy-data-wrapper content-wrapper info-border-wrapper']/div[4]").text.split('\n')[-1].split(' ')[0]),
                 'area_modulos':float(browser.find_element_by_xpath("//div[@class='energy-data-wrapper content-wrapper info-border-wrapper']/div[2]").text.split('\n')[-1].split(' ')[0].replace(',','.')),
                 'peso_sistema':(float(browser.find_element_by_xpath("//div[@class='energy-data-wrapper content-wrapper info-border-wrapper']/div[2]").text.split('\n')[-1].split(' ')[0].replace(',','.'))*
                                 float(browser.find_element_by_xpath("//div[@class='energy-data-wrapper content-wrapper info-border-wrapper']/div[3]").text.split('\n')[-1].split(' ')[0].replace(',','.')))})

# In[]
browser.close()
# In[]
# browser =webdriver.Chrome(executable_path=r'C:\Users\Igor\Documents\MEGA\MEGAsync\UFJF\Qualificacao\Dados\Tarifas_por_companhia\chromedriver_win32\chromedriver.exe')
# browser.get('https://www.aldo.com.br/calculadora-solar/')
# time.sleep(10)