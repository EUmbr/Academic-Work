import SchemDraw as schem
import SchemDraw.elements as e
import SchemDraw.logic as l


class Drawer():
    def __init__(self, text):
        self.d = schem.Drawing()
        self.text = text
        self.term = self.text.replace(' ', '')
        print(self.term)
        for char in self.text:
            if char in ('(', ')', '*', '+', '!'):
                self.text = self.text.replace(char, ' ')
        self.all_args = sorted(self.text.split())
        self.args = sorted(set(self.text.split()))
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
        self.x += 5

    def start(self):
        self.drawLines()
        sign = self.check_sign(self.term)

        if sign == '+':
            coords = self.sum(self.term)
        elif sign == '*':
            coords = self.mul(self.term)

        self.d.draw()
        return coords

    def sum(self, text):
        coords = {}
        elems = self.parse(text, '+')
        print('----------sum---------')
        print(elems, self.x, self.y)

        for i in range(len(elems)):
            sign = self.check_sign(elems[i])
            if sign == '*':
                coords[elems[i]] = self.mul(elems[i])
            else:
                coords[elems[i]] = [self.params[elems[i]].start[0], self.y]
                self.y -= 3
        print(coords)

        xses = [x[0] for x in coords.values()]
        self.x = max(xses)+2

        t = self.drawOr(coords)

        return t

    def drawOr(self, coords):
        gate = self.d.add(l.orgate(inputs=len(coords)),
                              xy=[self.x, (list(coords.values())[0][1] +
                              list(coords.values())[-1][1])/2],
                              d='right')

        count = 1
        dict = {}

        for elem in coords:
            dict[elem] = 'gate.in' + str(count)
            count += 1

        count = 1
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

            if len(elem) < 3:
                self.d.add(e.DOT)

            count+=1

        return gate.out

    def mul(self, text):
        coords = {}
        elems = self.parse(text, '*')
        print('----------mul---------')
        print(elems, self.x, self.y)

        for i in range(len(elems)):
            sign = self.check_sign(elems[i])
            if sign == '+':
                coords[elems[i]] = self.sum(elems[i])
            else:
                coords[elems[i]] = [self.params[elems[i]].start[0], self.y]
                self.y -= 3
        print(coords)

        xses = [x[0] for x in coords.values()]
        self.x = max(xses)+2

        t = self.drawAnd(coords)

        return t

    def drawAnd(self, coords):
        gate = self.d.add(l.andgate(
                                inputs=len(coords)),
                                xy=[self.x, (list(coords.values())[0][1]+list(coords.values())[-1][1])/2],
                                d='right')

        count = 1
        dict = {}

        for elem in coords:
            dict[elem] = 'gate.in' + str(count)
            count += 1

        for elem in coords:
            self.d.add(e.LINE, xy=eval(dict[elem]), tox=coords[elem][0], d='left')
            self.d.add(e.DOT)

        return gate.out

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

        for i in range(len(a)):
            while a[i][0] == '(' and a[i][-1] == ')' and self.check(a[i][1:-1]) is True:
                a[i] = a[i][1:-1]

        for i in range(len(a)):
            next_sign = self.check_sign(a[i])
            if sign == next_sign:
                a[i] = self.parse(a[i], sign)

        a = self.norm(a)
        a = self.set_list(a)

        return a

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
            if i == '*' and c == 0:
                return '*'
        return 0


draw = Drawer('a+b*c')
draw.start()
