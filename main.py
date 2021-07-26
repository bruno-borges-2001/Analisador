from Operations import *
from Grammar import *
from AF import *
from ER import *

er1 = ER("(0-3)*|a(4-5)b*")
er2 = ER("b|a*c(a|b)*")
er3 = ER("(0-9)*")

afd1 = er1.get_afd()
afd2 = er2.get_afd()
afd3 = er3.get_afd()

nafd = union(afd1, afd2)
nafd = union(nafd, afd3)

afd = nafd.determinize("S")
afd.print_transition_table()
