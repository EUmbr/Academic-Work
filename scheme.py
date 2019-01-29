import SchemDraw as schem
import SchemDraw.elements as e
import SchemDraw.logic as l


def draw(button):
    d = schem.Drawing()
    # Two front gates (SR latch)
    G1 = d.add(l.NAND2, anchor='in1')
    d.add(e.LINE, l=d.unit/6)
    Q1 = d.add(e.DOT)
    d.add(e.LINE, l=d.unit/6)
    Q2 = d.add(e.DOT)
    d.add(e.LINE, l=d.unit/3, rgtlabel='$Q$')
    G2 = d.add(l.NAND2, anchor='in1', xy=[G1.in1[0],G1.in1[1]-2.5])
    d.add(e.LINE, l=d.unit/6)
    Qb = d.add(e.DOT)
    d.add(e.LINE, l=d.unit/3)
    Qb2 = d.add(e.DOT)
    d.add(e.LINE, l=d.unit/6, rgtlabel='$\overline{Q}$')
    S1 = d.add(e.LINE, xy=G2.in1, d='up', l=d.unit/6)
    d.add(e.LINE, d='down', xy=Q1.start, l=d.unit/6)
    d.add(e.LINE, to=S1.end)
    R1 = d.add(e.LINE, xy=G1.in2, d='down', l=d.unit/6)
    d.add(e.LINE, d='up', xy=Qb.start, l=d.unit/6)
    d.add(e.LINE, to=R1.end)

    # Two back gates
    d.add(e.LINE, xy=G1.in1, d='left', l=d.unit/6)
    J = d.add(l.NAND3, anchor='out', reverse=True)
    d.add(e.LINE, xy=J.in3, d='up', l=d.unit/6)
    d.add(e.LINE, d='right', tox=Qb2.start)
    d.add(e.LINE, d='down', toy=Qb2.start)
    d.add(e.LINE, d='left', xy=J.in2, l=d.unit/4, lftlabel='$J$')
    d.add(e.LINE, xy=G2.in2, d='left', l=d.unit/6)
    K = d.add(l.NAND3, anchor='out', reverse=True)
    d.add(e.LINE, xy=K.in1, d='down', l=d.unit/6)
    d.add(e.LINE, d='right', tox=Q2.start)
    d.add(e.LINE, d='up', toy=Q2.start)
    d.add(e.LINE, d='left', xy=K.in2, l=d.unit/4, lftlabel='$K$')
    C = d.add(e.LINE, d='down', xy=J.in1, toy=K.in3)
    d.add(e.DOT, xy=C.center)
    d.add(e.LINE, d='left', xy=C.center, l=d.unit/4, lftlabel='$CLK$')
    d.draw()
