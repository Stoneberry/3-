#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
import urllib.request
import urllib.parse
import csv
import lxml.html
   
from bs4 import BeautifulSoup
import pandas as pd



def open_rules():
    d = {}
    with open('rules_of_streets.txt', 'r', encoding='utf-8') as rules:
        array = rules.readlines()
        for i in array:
            string = i.split('\t')
            d[string[1][:-1]] = string[0]
    return d


class AddressInfo:

    def __init__(self, *args):
        self.address = ''
        for index, item in enumerate(args):
            if index == len(args) - 1:
                self.address += '{}'.format(item)
            else:
                self.address += '{}+'.format(item)


class Table:

    def __init__(self, html):
        self.dataFrame = self.table(html)
    
    def table(self, html):

        soup = BeautifulSoup(html, "lxml")  
 #            pasport = soup.find("div", "numbered").findAll('span')  # массив всех данных из паспорта
        a2 = soup.find("div", "numbered")
        a3 = a2.findAll("tr", "left")

        questions = []
        answers = []

        for i in a3:
            question = i.findAll('span')[0].string
            questions.append(question)

            answer = i.findNextSiblings('tr')[0]
            answers.append(answer.findAll('span')[0].string)

        df = pd.DataFrame({'Наименования': questions,
                           'Параметры': answers
                           })
        return df


    

class HouseInfo(AddressInfo, Table):

    def download(self):

        def search(main_link):  # - поиск по
            
            link = main_link + '/search/houses?query=' + urllib.parse.quote_plus(self.address)

            with urllib.request.urlopen(link) as response:
               html = response.read().decode('utf-8')
            return html

        def pasport(html1, main_link):
            reg = '<td><a href="(/myhouse/profile/view/.*?)">.*?</a> </td>'
            links = re.findall(reg, html1)
            
            if links == []:
                raise ValueError('There is no info about this house')

            for link in links:  # - если несколько результатов поиска
                page = urllib.request.urlopen(main_link + link)
                html1 = page.read().decode('utf-8')              

            return html1
        

        main_link = 'https://www.reformagkh.ru'

        a1 = search(main_link)
        pasport_html = pasport(a1, main_link)  # html странца паспорта дома
        
        return self.table(pasport_html)



def newfile(html):
    f = open('new.txt', 'a', encoding='utf-8')
    f.write(html)
    f.close
    return


def main():

    if len(sys.argv) <= 4:
        raise ValueError('Enter correct arguments:')
    else:
        a1 = HouseInfo(*sys.argv)
        a2 = a1.download()
    return a2


a1 = HouseInfo('Чертановская', '18')
a2 = a1.download()
print(a2)
