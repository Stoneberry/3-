#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
import urllib.request
import urllib.parse
import csv
from bs4 import BeautifulSoup, SoupStrainer
from bs4 import BeautifulSoup
import pandas as pd
from lxml import etree
from lxml import html
import os


class AddressInfo:

    def __init__(self, *args):
        self.adress = ''
        for index, item in enumerate(args):
            if index == len(args) - 1:
                self.adress += '{}'.format(item)
            else:
                self.adress += '{}+'.format(item)


class TableHouse:

    def __init__(self, html):
        self.dataFrame = self.table(html)

    def clean(self, x):
        cleaned = re.sub('\n|                |            ', '', x)
        return cleaned

    def numbered_table(self, child, questions, answers, tables=None):
        left_class = child.find_class("left")

        for line in left_class:

            for i in line.getchildren():
                if i.text_content() != '':
                    if i.text_content() not in questions:
                        questions.append(self.clean(i.text_content()))

            for k in line.getnext():
                if k.text_content() != '':
                    answers.append(self.clean(k.text_content()))

        grid_class = child.find_class("grid")
        if grid_class != []:
            for grid in grid_class:
                self.grid_table(grid, tables)

    def grid_table(self, child, tables):

        for line in child.getchildren():

            d = {}

            ques = []
            ans = []

            q = []
            a = []

            for simbling in line.getchildren():

                if simbling.tag == 'thead':
                    for tr in simbling.getchildren():
                        for th in tr:
                            if th.tag == 'th':
                                ques.append(self.clean(th.text_content()))

                elif simbling.tag == 'tbody':

                    for tr in simbling.getchildren():

                        tr.classes

                        if tr.get('class') == "collapsible":
                            self.numbered_table(tr, q, a)

                        else:
                            for td in tr:
                                if td.tag == 'td':
                                    ans.append(self.clean(td.text_content()))
                            if len(tr) < len(ques):
                                ans += [ans[-1]]*(len(ques) - len(tr))

                elif simbling.tag == 'tr':
                    for td in simbling.getchildren():
                        if td.tag == 'td':
                            ans.append(self.clean(td.text_content()))

            ques_len = len(ques)

            if a != 0:
                i = 0
                while i < len(a):
                    ans.insert(ques_len, a[i])
                    ans.insert(ques_len + 1, a[i + 1])
                    i += 2
                    ques_len += len(ques) + 2
            ques += q

            if len(ques) != 0:
                if len(ques) > len(ans):
                    ans += [ans[-1]]*(len(ques) - len(ans))

                for index, item in enumerate(ques):
                    d[item] = []
                    i = index
                    while i < len(ans):
                        d[item].append(ans[i])
                        i += len(ques)

                tables.append(d)

    def table(self, html_pas, adress):

        tree = html.fromstring(html_pas)
        tab = tree.get_element_by_id("tab1")

        num = 0

        for chld in tab.getchildren():
            chld.classes

            questions = []
            answers = []
            tables = []

            if chld.get('class') == "subtab":

                for child in chld.getchildren():
                    child.classes

                    if child.get('class') == "numbered":
                        self.numbered_table(child, questions, answers, tables)

                    for i in child.getchildren():
                        i.classes
                        if i.get('class') == "numbered":
                            self.numbered_table(i, questions, answers, tables)

                    if child.get('class') == "grid":
                        self.grid_table(child, tables)

                if questions != []:
                    df = pd.DataFrame({'Наименования': questions,
                                       'Параметры': answers})
                    df.to_csv(adress + '.csv', mode='a', encoding='utf-8')

                if tables != []:
                    for i in tables:
                        num += 1
                        df2 = pd.DataFrame(i)
                        df2.to_csv(adress + '_' + str(num) + '.csv',
                                   mode='a', encoding='utf-8')


class HouseInfo(AddressInfo, TableHouse):

    def download(self):

        def search(main_link):  # - поиск по
            link = main_link + '/search/houses?query=' \
                   + urllib.parse.quote_plus(self.adress)
            with urllib.request.urlopen(link) as response:
                html = response.read().decode('utf-8')
            return html

        def pasport_html(html, main_link):

            soup = BeautifulSoup(html, "lxml")
            for link in soup.find_all('a'):

                if 'г. Москва,' in link.get_text() or 'обл. Московская,' \
                        in link.get_text():
                    self.adress = link.get_text()
                    page = urllib.request.urlopen(main_link + link.get('href'))
                    html_pas = page.read().decode('utf-8')
                    yield html_pas

        main_link = 'https://www.reformagkh.ru'
        a1 = search(main_link)
        for html_pas in pasport_html(a1, main_link):
            self.table(html_pas, self.adress)
        return


def main():
    if len(sys.argv) < 3:
        raise ValueError('Enter correct arguments:')
    else:
        a1 = HouseInfo(*sys.argv[1:])
        a2 = a1.download()
        return a2


if __name__ == "__main__":
    main()
