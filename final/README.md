# Автоматическая выгрузка паспорта указанного пользователем дома с сайта https://www.reformagkh.ru/
 
<b>Используемые модули:</b>
1) sys, re, os
2) urllib
3) bs4 (BeautifulSoup)
4) pandas
5) lxml


<b>Структура</b>
1) Класс AddressInfo - В нем хранится адрес, который передал пользователь.
2) Класс TableHouse - Разбирает html паспорта дома и вреобразует полученную информацию в таблицу и записывает в файл.
3) Класс HouseInfo - наследует от двух предыдущих. Проверяет есть ли в базе дом с указанным адресом, скачивает паспорт дома и с помощью класса TableHouse преобразует все в таблицы.

Работа с программой осуществляется через консоль.

<b>Рассмотрим каждый класс:</b>
<pre><b>AddressInfo</b></pre>


<p><pre>class AddressInfo:<br>
    def __init__(self, *args):<br>
        self.adress = ''<br>
        for index, item in enumerate(args):<br>
            if index == len(args) - 1:<br>
                self.adress += '{}'.format(item)<br>
            else:
                self.adress += '{}+'.format(item)<br></pre></p>

Переданный адрес формируется в единую строку через разделитель +.


<pre><b>HouseInfo(AddressInfo, TableHouse)</b></pre>

В данном классе есть основной метод download, которые реализует следующие:
1) С помощью функции search осуществляется поиск дома в базе данных сайта. 
   На вход функция принимает ссылку на гланую страницу сайта.
   Возращает html результата поиска
2) Рasport_html принимает на вход html, полученный в результате работы предыдущей функции, и ссылку на гланую страницу сайта.
   Смотрит, если среди ссылок есть ссылка на дом, находящийся в Москве или Москвоской области, и выдает html анкеты дома. 
   Если нашлось несколько домов с похожим адрессом, информация найдется по каждому из них.
3) Далее с помощью функции table в файлы записываются вся информация из паспорта дома. 


<pre><b>TableHouse</b></pre>

1) Метод <b>clean</b> очищает строки от лишних пробелов и переносов строки

Html этого сайта построен таким образом, что информация в паспорте содержится в одном из двух видом таблиц.
Чтобы получить информацию из обоих типов есть два метода: numbered_table и grid_table.
Так как таблицы могут быть вложены друг в друга, предусмотрено обход всех таблиц при помощи рекурсии.

2) Метод <b>numbered_table</b> работает с таблицей, состоящей из двух колонок, где наименования выделены с помощью класса left.
    Входные данные:
        а) self
        б) child - ветвь, на которой сейчас находится программа
        в) questions - массив наименований для всех таблиц такого типа
        г) answers - массив парметров (ответов на наименования) для всех таблиц такого типа
        д) tables - для случая, когда внутри есть grid_table. По умолчанию None

3) Метод <b>grid_table</b> работает с таблицей, состоящей из нескольких колонок с заранее определенными названиями столбцов. 
   Программа ходит по деревьям страницы и достает все неободимую информацию, далее ращбивает все на колонки и записывает в словарь.
   Если параметров меньше, чем заявленных названий столбцов, то последний множится и заполняет пустые клетки 
   (так как в некоторых таблица отсутсвуют значения сразу по некольким категориям). <br>
   <b>Входные данные:</b><br>
        а) self<br>
        б) child - ветвь, на которой сейчас находится программа<br>
        д) tables - массив всех таблиц вида grid_table

4) <b>table</b> ищет в html паспорт, далее с помоцию grid_table и numbered_table дастает всю информацию и записвает в файлы.
   Все таблицы вида numbered_table будут в одном файле, все таблицы вида grid_table в разных.
  
   <b>Входные данные:</b><br>
        а) self<br>
        б) html_pas - html паспорта дома <br>
        д) adress - адрес дома
        
<pre><b>main()</b></pre>
<p><pre>def main():<br>
    if len(sys.argv) < 3:
        raise ValueError('Enter correct arguments:')
    else:
        a1 = HouseInfo(*sys.argv[1:])
        a2 = a1.download()
        return a2</pre></p>

Программа проверяет, чтобы пользователь ввел как минимум 3 аргумента: название программы, улица и дом. 
Если все введено правильно, то программа начинает свою работу. 