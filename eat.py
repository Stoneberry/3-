
import os
import sys

class Game(object):
    def __init__(self, filename):
        self.filename = filename
        self.text = self.opening()  # - двумерный массив
        self.food = 0

    def opening(self):
        if not os.path.isfile(self.filename):
            raise FileNotFoundError('No such file')
        f = open(self.filename, 'r', encoding='utf-8') 
        s = f.readlines() 
        f.close()

        s2 = [] 
        for line in s[1:]: 
            line = list(line.strip('\n')) 
            s2.append(line)
        return s2


    def left_right(self, d, index):
        if d[index-1] == '*':
            d[index-1] = '@'
            self.food += 1
        if d[index-1] == '.':
            d[index-1] = '@'
         
        if d[index+1] == '*':
            d[index+1] = '@'
            self.food += 1
        if d[index+1] == '.':
            d[index+1] = '@'
        return d


    def up_down(self, idx, index):
        if self.text[idx-1][index] == '.':  # - верхний
            self.text[idx-1][index] = '@'
        if self.text[idx-1][index] == '*':  # - верхний
            self.text[idx-1][index] = '@'
            self.food  += 1
                    
        if self.text[idx+1][index] == '.':  # - верхний
            self.text[idx+1][index] = '@'
        if self.text[idx+1][index] == '*':  # - верхний
            self.text[idx+1][index] = '@'
            self.food  += 1
        return self.text
    
    
    def move(self, d, idx):
        for index, item in enumerate(d):
            if item == '@':
                a1 = self.left_right(d, index)
                a2 = self.up_down(idx, index)
        return d

    def count(self):
        for idx, line in enumerate(self.text):
            k = 1
            while k <= len(line):
                c = self.move(line, idx)
                k+=1
        return 

def path1():
    if len(sys.argv) != 2:
        raise ValueError('Enter a correct path')
    line = sys.argv[1]
    return line


def answer():
    path = path1()
    game = Game(path)
    a1 = game.count()
    print(game.food)

if __name__ == "__main__":
    answer()

 
