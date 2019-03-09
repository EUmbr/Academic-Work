import sys
from PyQt5.QtWidgets import QWidget, QApplication, QInputDialog, QLineEdit, QStyleFactory
from PyQt5.QtGui import QPainter, QColor, QFont, QPen
from PyQt5.QtCore import Qt


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(10, 40, 800, 1000)
        self.setWindowTitle('Draw text')
        self.getText()

        self.show()

    def getText(self):
        text, okPressed = QInputDialog.getText(self, "Get text", "Enter the equation:", QLineEdit.Normal, "")
        if okPressed and text != '':
            self.text = text

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        qp.end()

    def drawLines(self, qp, x):
        pen = QPen(Qt.black, 2, Qt.SolidLine)

        qp.setPen(pen)
        qp.drawLine(x, 40, x, 90 + 180*(len(self.eq)-1))
        self.mid = 45 + (50 + 180*(len(self.eq)-1))//2

    def drawAnd(self, qp, y, terms, term_num):
        qp.drawRect(200, y-100, 50, 80)
        qp.drawText(210, y-80, '&')
        self.drawConnect(qp, y, terms, term_num)

    def drawConnect(self, qp, y, terms, term_num):
        if terms == 1:
            qp.drawLine(250, y-60, 650, y-60)
        if terms%2 == 0:
            if term_num == 1 or term_num == terms:
                qp.drawLine(250, y-60, 550, y-60)
                if term_num <= terms//2:
                    qp.drawLine(550, y-60, 550, self.mid - 20)
                    qp.drawLine(550, self.mid - 20, 650, self.mid - 20)
                else:
                    qp.drawLine(550, y-60, 550, self.mid + 20)
                    qp.drawLine(550, self.mid + 20, 650, self.mid + 20)
            else:
                qp.drawLine(250, y-60, 450, y-60)
                if term_num <= terms//2:
                    qp.drawLine(450, y-60, 450, self.mid - 10)
                    qp.drawLine(450, self.mid - 10, 650, self.mid - 10)
                else:
                    qp.drawLine(450, y-60, 450, self.mid + 10)
                    qp.drawLine(450, self.mid + 10, 650, self.mid + 10)
        else:
            if term_num != terms//2+1:
                self.drawConnect(qp, y, terms-1, term_num-1 if term_num>terms//2+1 else term_num)
            else:
                qp.drawLine(250, y-60, 650, y-60)

    def drawOr(self, qp, y):
        qp.drawRect(650, y-100, 50, 80)
        qp.drawText(660, y-80, '1')
        qp.drawLine(700, y-60, 740, y-60)
        qp.drawText(750, y-55, 'f')

    def drawNot(self, qp, y):
        qp.drawRect(90, y-18, 20, 36)
        qp.drawEllipse(110, y-4, 8, 8)
        qp.drawLine(118, y, 200, y)
        qp.drawText(91, y-4, '1')

    def drawText(self, event, qp):
        qp.setFont(QFont('Decorative', 10))
        self.term = self.text.replace(' ', '')
        print(self.term)
        for char in self.text:
            if char in ('(', ')', '&', '+', '!'):
                self.text = self.text.replace(char, ' ')
        self.args = sorted(set(self.text.split()))
        print(self.args)
        self.eq = set(self.term.split('+')) #1 - 50 2 - 190 3 - 330 4 - 470 5 - 610
        print(self.eq)
        x = 25
        self.coords = {}
        for arg in self.args:
            qp.drawText(x-5, 20, arg)
            self.drawLines(qp, x)
            self.coords[arg] = x
            x += 20
        print(self.coords)
        y = 50
        term_num = 0
        for eq in self.eq:
            terms = eq.split('&')
            print(terms)
            for term in sorted(terms):
                print(term)
                if term[0] == '!':
                    term = term[1:]
                    qp.setPen(QPen(Qt.black, 10, Qt.SolidLine))
                    qp.drawPoint(self.coords[term], y)
                    qp.setPen(QPen(Qt.black, 2, Qt.SolidLine))
                    qp.drawLine(self.coords[term], y, 90, y)
                    self.drawNot(qp, y)
                    y += 40
                else:
                    qp.setPen(QPen(Qt.black, 10, Qt.SolidLine))
                    qp.drawPoint(self.coords[term], y)
                    qp.setPen(QPen(Qt.black, 2, Qt.SolidLine))
                    qp.drawLine(self.coords[term], y, 200, y)
                    y += 40
            term_num += 1
            self.drawAnd(qp, y, len(self.eq), term_num)
            y += 100
        self.drawOr(qp, self.mid+60)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    ex = Example()
    sys.exit(app.exec_())
