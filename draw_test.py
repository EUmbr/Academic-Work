import SchemDraw as schem
import SchemDraw.elements as e
import SchemDraw.logic as l


def drawLines(x, name, dict, length, d):
    dict[name] = d.add(e.LINE, endpts=[[x, 2], [x, length]], rgtlabel=name)


def parse(text, sign):
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
        while a[i][0] == '(' and a[i][-1] == ')' and check(a[i][1:-1]) is True:
            a[i] = a[i][1:-1]

    for i in range(len(a)):
        next_sign = check_sign(a[i])
        if sign == next_sign:
            a[i] = parse(a[i], sign)

    a = norm(a)
    a = set_list(a)

    return a


def set_list(a):
    if len(list(set(a))) != len(a):
        return list(set(a))
    else:
        return a


def norm(a):
    norm_list = []
    for i in a:
        if type(i) == list:
            for j in i:
                norm_list.append(j)
        else:
            norm_list.append(i)
    return norm_list


def check_parse(text, sign):
    c = 0
    for i in text:
        if i == '(':
            c -= 1
        if i == ')':
            c += 1
        if i == sign and c == 0:
            return True
    return False


def check(string):
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


def check_sign(text):
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


def start(text, params, d):
    sign = check_sign(text)

    if sign == '+':
        coords = sum(text, params, d)
    elif sign == '*':
        coords = mul(text, params, d)

    return coords


def drawer(text, d):
    term = text.replace(' ', '')
    print(term)
    for char in text:
        if char in ('(', ')', '*', '+', '!'):
            text = text.replace(char, ' ')
    all_args = sorted(text.split())
    args = sorted(set(text.split()))
    x = 2
    params = {}
    length = 5*len(all_args)
    for arg in args:
        drawLines(x, arg, params, length, d)
        x += 1
    x += 2

    start(term, params, d)


def sum(text, params, d):
    coords = []
    a = parse(text, '+')

    for i in range(len(a)):
        sign = check_sign(a[i])
        if sign == '*':
            coords.append(mul(a[i]))
        else:
            coords.append(params[a[i]])
    res = res[:-1] + ']'

    return res


def mul(text):
    res = '{'
    a = parse(text, '*')
    for i in range(len(a)):
        sign = check_sign(a[i])
        if sign == '+':
            res = res + sum(a[i]) + ','
        else:
            res = res + a[i] + ','
    res = res[:-1] + '}'

    return res


d = schem.Drawing()
drawer('a+b', d)
d.draw()
