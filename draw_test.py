import SchemDraw as schem
import SchemDraw.elements as e
import SchemDraw.logic as l


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


def drawLines(x, name, dict, length, d):
    dict[name] = d.add(e.LINE, endpts=[[x, 2], [x, length]], rgtlabel=name)


def drawAnd(params, elems, coords, x, y, d):
    gate = d.add(l.andgate(
                            inputs=len(elems)),
                            xy=[x, (coords[0][1]+coords[-1][1])/2],
                            d='right')

    count = 1
    dict = {}

    for elem in elems:
        dict[elem] = 'gate.in' + str(count)
        count += 1

    for i in range(len(elems)):
        d.add(e.LINE, xy=eval(dict[elems[i]]), tox=coords[i][0], d='left')
        d.add(e.DOT)

    return gate.out


def drawOr(params, elems, coords, x, y, d):
    gate = d.add(l.orgate(
                            inputs=len(elems)),
                            xy=[x, (coords[0][1]+coords[-1][1])/2],
                            d='right')

    count = 1
    dict = {}

    for elem in elems:
        dict[elem] = 'gate.in' + str(count)
        count += 1

    for i in range(len(elems)):
        d.add(e.LINE, xy=eval(dict[elems[i]]), tox=coords[i][0], d='left')
        d.add(e.DOT)

    return gate.out


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
    length = 3*len(all_args)
    for arg in args:
        drawLines(x, arg, params, length, d)
        x += 1
    x += 5
    y = length

    print(start(term, params, x, y, d))


def start(text, params, x, y, d):
    sign = check_sign(text)

    if sign == '+':
        coords = sum(text, params, x, y, d)
    elif sign == '*':
        coords = mul(text, params, x, y, d)

    return coords


def sum(text, params, x, y, d):
    coords = []
    elems = parse(text, '+')
    print('----------sum---------')
    print(elems, x, y)

    for i in range(len(elems)):
        sign = check_sign(elems[i])
        if sign == '*':
            coords.append(mul(elems[i], params, x, y, d))
        else:
            coords.append((params[elems[i]].start[0], y))
            y -= 3
    print(coords)

    xses = [x[0] for x in coords]
    x = max(xses)+2

    t = drawOr(params, elems, coords, x, y, d)

    return t


def mul(text, params, x, y, d):
    coords = []
    elems = parse(text, '*')
    print('----------mul---------')
    print(elems, x, y)

    for i in range(len(elems)):
        sign = check_sign(elems[i])
        if sign == '+':
            coords.append(sum(elems[i], params, x, y, d))
        else:
            coords.append((params[elems[i]].start[0], y))
            y -= 3
    print(coords)

    xses = [x[0] for x in coords]
    x = max(xses)+2

    t = drawAnd(params, elems, coords, x, y, d)

    return t


d = schem.Drawing()
drawer('c+a', d)
d.draw()
