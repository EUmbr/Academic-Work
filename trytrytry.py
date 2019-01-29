import SchemDraw as schem
import SchemDraw.elements as e
import SchemDraw.logic as l



def drawLines(x, eq, d):
    d.add(e.LINE, endpts=[[x,40],[x,90+180*(len(eq)-1)]])
    #qp.drawLine(x, 40, x, 90 + 180*(len(self.eq)-1))


def drawConnect(y, terms, term_num, d):
    if terms == 1:
        d.add(e.LINE, endpts=[[250, y-60], [550, y-60]])
        #qp.drawLine(250, y-60, 650, y-60)
    if terms%2 == 0:
        if term_num == 1 or term_num == terms:
            d.add(e.LINE, endpts=[[250, y-60], [550, y-60]])
            #qp.drawLine(250, y-60, 550, y-60)
            if term_num <= terms//2:
                d.add(e.LINE, endpts=[[550, y-60], [550, y-20]])
                #qp.drawLine(550, y-60, 550, self.mid - 20)
                d.add(e.LINE, endpts=[[550, y-20], [650, y-20]])
                #qp.drawLine(550, self.mid - 20, 650, self.mid - 20)
            else:
                d.add(e.LINE, endpts=[[550, y-60], [550, y + 20]])
                #qp.drawLine(550, y-60, 550, self.mid + 20)
                d.add(e.LINE, endpts=[[550, y + 20], [650, y + 20]])#
                #qp.drawLine(550, self.mid + 20, 650, self.mid + 20)
        else:
            d.add(e.LINE, endpts=[[250, y-60], [450, y-60]])
            #qp.drawLine(250, y-60, 450, y-60)
            if term_num <= terms//2:
                d.add(e.LINE, endpts=[[450, y-60], [450, y - 10]])
                #qp.drawLine(450, y-60, 450, self.mid - 10)
                d.add(e.LINE, endpts=[[450, y - 10], [650, y - 10]])
                #qp.drawLine(450, self.mid - 10, 650, self.mid - 10)
            else:
                d.add(e.LINE, endpts=[[450, y-60], [450, y + 10]])
                #qp.drawLine(450, y-60, 450, self.mid + 10)
                d.add(e.LINE, endpts=[[450, y + 10], [650, y + 10]])
                #qp.drawLine(450, self.mid + 10, 650, self.mid + 10)
    else:
        if term_num != terms//2+1:
            drawConnect(y, terms-1, term_num-1 if term_num>terms//2+1 else term_num, d)
        else:
            d.add(e.LINE, endpts=[[250, y-60], [650, y-60]])
            #qp.drawLine(250, y-60, 650, y-60)

def drawOr(y, terms, d):
    d.add(l.orgate(inputs=terms), xy=[650,y])

def drawText(text, d):
    term = text.replace(' ', '')
    print(term)
    for char in text:
        if char in ('(', ')', '&', '+', '!'):
            text = text.replace(char, ' ')
    args = sorted(set(text.split()))
    print(args)
    equat = set(term.split('+')) #1 - 50 2 - 190 3 - 330 4 - 470 5 - 610
    mid = 45 + (50 + 180*(len(equat)-1))//2
    x = 25
    coords = {}
    for arg in args:
        drawLines(x, equat, d)
        coords[arg] = x
        x += 20

    print(coords)
    y = 50
    term_num = 0

    for eq in equat:

        terms = sorted(eq.split('&'))
        print(terms)
        n=[]
        for i in range(len(terms)):
            if terms[i][0] == '!':
                n.append(i+1)

        D = d.add(l.andgate(inputs=2, nand=False, inputnots=n), xy=[200, y], d='right')

        d.add(e.DOT, xy=[coords[terms[0]], D.in1[1]])
        d.add(e.LINE, endpts=[[coords[terms[0]], D.in1[1]],[200, D.in1[1]]])

        d.add(e.DOT, xy=[coords[terms[1]], D.in2[1]])
        d.add(e.LINE, endpts=[[coords[terms[1]], D.in2[1]],[200, D.in2[1]]])

        #for term in terms:
        #    print(term)
        #    if term[0] == '!':
        #        term = term[1:]
        #        #qp.setPen(QPen(Qt.black, 10, Qt.SolidLine))
        #        d.add(e.DOT, xy=[self.coords[term], ])
        #        #qp.drawPoint(self.coords[term], y)
        #        #qp.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        #        d.add(e.LINE, endpts=[[self.coords[term], y],[200, y]])
        #        #qp.drawLine(self.coords[term], y, 90, y)
        #        self.drawNot(qp, y)
        #        y += 40
        #    else:
        #        qp.setPen(QPen(Qt.black, 10, Qt.SolidLine))
        #        qp.drawPoint(self.coords[term], y)
        #        qp.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        #        qp.drawLine(self.coords[term], y, 200, y)
        #        y += 40
        term_num += 1
        #self.drawAnd(y, len(self.eq), term_num)
        drawConnect(y, len(equat), term_num, d)
        y += 100
    print('---------------\n', type(equat))
    drawOr(mid, len(equat), d)


text=input()

d = schem.Drawing()
drawText(text, d)





d.draw()
