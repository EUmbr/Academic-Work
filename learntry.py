import SchemDraw as schem
import SchemDraw.elements as e
import SchemDraw.logic as l

d=schem.Drawing(unit=4)
D=d.add(l.andgate(inputs=3, nand=False, inputnots=[2]), xy=[100,100])
print(eval('D.in1'))
d.draw()
