import matplotlib

import SchemDraw as schem
import SchemDraw.elements as e
import SchemDraw.logic as l
#import matplotlib.pyplot as plt
#plt.xkcd()


matplotlib.use('Agg')

class Drawer():
    def __init__(self, text):
        self.d = schem.Drawing()
        self.text = text
        self.term = self.text.replace(' ', '')
        print(self.term)
        for char in self.text:
            if char in ('(', ')', '&', '+', '!'):
                self.text = self.text.replace(char, ' ')
        self.all_args = sorted(self.text.split())
        self.args = sorted(set(self.text.split()))
        for arg in self.args:
            if ((len(arg) == 1 and arg.isalpha()) or
               (len(arg) == 2 and arg[0].isalpha() and arg[1].isdigit())):
                pass
            else:
                raise Exception

        self.length = 3*len(self.all_args)+1
        self.x = 2
        self.y = self.length-1
        self.params = {}

    def drawLines(self):
        for arg in self.args:
            self.params[arg] = self.d.add(e.LINE, endpts=[[self.x, 2],
                                          [self.x, self.length]],
                                          rgtlabel=arg)
            self.x += 1
        self.last_x = self.x
        self.x += 5

    def start(self):
        self.drawLines()
        term = self.del_brackets(self.term)
        sign = self.check_sign(term)
        if sign == 0:
            sign = self.check_unsign(term)
        print(term, sign)

        if sign == '+':
            coords = self.sum(term)
        elif sign == '&':
            coords = self.mul(term)

        self.d.add(e.LINE, l=.5, d='right', xy=coords, rgtlabel='f')
        self.d.draw()
        self.d.save(self.term+'.jpg')

    def sum(self, text, flag=False):
        coords = {}
        elems = self.parse(text, '+')
        print('----------sum---------')
        print(elems, self.x, self.y)

        for i in range(len(elems)):
            print(elems[i])
            if elems[i][0] == '!' and len(elems[i]) > 3:
                sign = self.check_sign(elems[i][2:-1])
                if sign == '&':
                    coords[elems[i]] = self.mul(elems[i][2:-1], True)
                elif sign == '+':
                    coords[elems[i]] = self.sum(elems[i][2:-1], True)
            else:
                sign = self.check_sign(elems[i])
                if sign == '&':
                    coords[elems[i]] = self.mul(elems[i])
                else:
                    if elems[i][0] == '!' and len(elems[i][0]) <= 3:
                        coords[elems[i]] = [self.params[elems[i][1:]].start[0], self.y]
                    else:
                        coords[elems[i]] = [self.params[elems[i]].start[0], self.y]
                    self.y -= 3
        print(coords)

        xses = [x[0] for x in coords.values()]
        xses.append(self.last_x)
        self.x = max(xses)+2

        if len(coords) == 1:
            return list(coords.values())[0]

        t = self.drawOr(coords, flag)

        return t

    def drawOr(self, coords, flag):
        y_coord = self.get_y(coords)
        nots = self.get_nots(coords)
        print(nots)
        gate = self.d.add(l.orgate(inputs=len(coords), inputnots=nots, nor=flag),
                              xy=[self.x, y_coord],
                              d='right')

        count = 1
        dict = {}

        for elem in coords:
            dict[elem] = 'gate.in' + str(count)
            count += 1

        self.drawConnect(coords, dict, gate)

        return gate.out

    def mul(self, text, flag=False):
        coords = {}
        elems = self.parse(text, '&')
        print('----------mul---------')
        print(elems, self.x, self.y)

        for i in range(len(elems)):
            if elems[i][0] == '!' and len(elems[i]) > 3:
                sign = self.check_sign(elems[i][2:-1])
                if sign == '&':
                    coords[elems[i]] = self.mul(elems[i][2:-1], True)
                elif sign == '+':
                    coords[elems[i]] = self.sum(elems[i][2:-1], True)
            else:
                sign = self.check_sign(elems[i])
                if sign == '+':
                    coords[elems[i]] = self.sum(elems[i])
                else:
                    if elems[i][0] == '!':
                        coords[elems[i]] = [self.params[elems[i][1:]].start[0], self.y]
                    else:
                        coords[elems[i]] = [self.params[elems[i]].start[0], self.y]
                    self.y -= 3
        print(coords)

        xses = [x[0] for x in coords.values()]
        xses.append(self.last_x)
        self.x = max(xses)+2

        if len(coords) == 1:
            return list(coords.values())[0]

        t = self.drawAnd(coords, flag)

        return t

    def drawAnd(self, coords, flag):
        y_coord = self.get_y(coords)
        nots = self.get_nots(coords)
        gate = self.d.add(l.andgate(
                                inputs=len(coords), inputnots=nots, nand=flag),
                                xy=[self.x, y_coord],
                                d='right')

        count = 1
        dict = {}

        for elem in coords:
            dict[elem] = 'gate.in' + str(count)
            count += 1

        self.drawConnect(coords, dict, gate)

        return gate.out

    def drawConnect(self, coords, dict, gate):
        count = 1
        print(coords, 'fgfgw')
        all = len(coords)
        unit = 1/(all//2)
        print(self.length, unit, all, '--------', coords)
        for elem in coords:
            length = count*unit if count < (all+1)/2 else (all-count+1)*unit
            self.d.add(e.LINE, xy=eval(dict[elem]), l=length, d='left')
            if count < (all+1)/2:
                self.d.add(e.LINE, toy=coords[elem][1], d='up')
            elif count == (all+1)/2:
                pass
            else:
                self.d.add(e.LINE, toy=coords[elem][1], d='down')
            self.d.add(e.LINE, tox=coords[elem][0], d='left')

            if not bool({'+', '&'} & set(elem)):
                self.d.add(e.DOT)

            count+=1

    def get_y(self, coords):
        if len(coords) % 2 == 0:
            y = (list(coords.values())[0][1] +
                 list(coords.values())[-1][1])/2
        else:
            num = len(coords)//2
            y = list(coords.values())[num][1]

        return y

    def get_nots(self, coords):
        elems = list(coords.keys())
        print(elems)
        nots = []
        for i in range(len(elems)):
            if elems[i][0] == '!' and not bool({'+', '&'} & set(elems[i])):
                nots.append(i+1)

        return nots

    def parse(self, text, sign):
        c = 0
        a = []
        s = ''
        for i in text:
            if i == '(':
                c -= 1
            if i == ')':
                c += 1
            if i == sign and c == 0:
                a.append(s)
                s = ''
            else:
                s += i
        a.append(s)
        print(a)

        for i in range(len(a)):
            a[i] = self.del_brackets(a[i])

        for i in range(len(a)):
            next_sign = self.check_sign(a[i])
            if sign == next_sign:
                a[i] = self.parse(a[i], sign)

        a = self.norm(a)
        a = self.set_list(a)

        return a

    def del_brackets(self, text):
        while text[0] == '(' and text[-1] == ')' and self.check(text[1:-1]) is True:
            text = text[1:-1]
        if text[0] == '!' and ('+' in text or '&' in text):
            while text[1] == text[2] == '(' and text[-1] == text[-2] == ')':
                text = text[0] + text[2:-1]
        elif text[0] == '!' and not('+' in text or '&' in text):
            while len(text) > 3 and text[1] == '(' and text[-1]:
                text = text[0] + text[2:-1]
        return text

    def set_list(self, a):
        if len(list(set(a))) != len(a):
            return list(set(a))
        else:
            return a

    def norm(self, a):
        norm_list = []
        for i in a:
            if type(i) == list:
                for j in i:
                    norm_list.append(j)
            else:
                norm_list.append(i)
        return norm_list

    def check(self, string):
        stack = []
        for i in string:
            if i == '(':
                stack.append(i)
            if i == ')':
                if len(stack) == 0:
                    return False
                if stack[-1] == '(':
                    stack = stack[:-1]
                else:
                    return False
        return (not stack)

    def check_sign(self, text):
        c = 0
        for i in text:
            if i == '(':
                c -= 1
            if i == ')':
                c += 1
            if i == '+' and c == 0:
                return '+'
        c = 0
        for i in text:
            if i == '(':
                c -= 1
            if i == ')':
                c += 1
            if i == '&' and c == 0:
                return '&'
        return 0

    def check_unsign(self, text):
        if text[0] is '!' and len(text)>4:
            sign = self.check_sign(text[2:-1])
            return sign
        else:
            return 0

#d= Drawer('!(a+bb)')
#d.start()
