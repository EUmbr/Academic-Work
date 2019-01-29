import SchemDraw as schem
import SchemDraw.elements as e
import SchemDraw.logic as l


def drawLines(x, name, dict, pl, d):
    dict[name] = d.add(e.LINE, endpts=[[x, 2], [x, 2+3*(pl+2)]], rgtlabel=name)


def drawAnd(term, x, y, coords, d):
    mults = sorted(list(set(term.split('&'))))

    n = []
    for i in range(len(mults)):
        if mults[i][0] == '!':
            n.append(i+1)

    gate = d.add(l.andgate(inputs=len(mults), inputnots=n), d='right', xy=[x,y])

    st = 1
    dict = {}
    print(mults)

    for elem in mults:
        dict[elem] = 'gate.in' + str(st)
        st += 1

    for elem in mults:
        if elem[0] == '!':
            g_x = coords[elem[1:]].start[0]
        else:
            g_x = coords[elem].start[0]
        d.add(e.LINE, xy=eval(dict[elem]), tox=g_x, d='left')
        d.add(e.DOT)


def drawer(text, d):
    term = text.replace(' ', '')
    print(term)
    for char in text:
        if char in ('(', ')', '&', '+', '!'):
            text = text.replace(char, ' ')
    args = sorted(set(text.split()))
    x = 2
    coords = {}
    pl = term.count('+')
    for arg in args:
        drawLines(x, arg, coords, pl, d)
        x += 1
    x += 2

    if '+' not in term:
        drawAnd(term, x, 5, coords, d)
    else:
        equat = list(set(term.split('+')))
        y = 5
        for eq in equat:
            drawAnd(eq, x, y, coords, d)
            y += 3
        x += 5
        d.add(l.orgate(inputs=len(equat)), xy=[x, 2+(3*(pl+2))/2])


d = schem.Drawing()
drawer('a&b+!c&!g&w', d)
d.draw()
