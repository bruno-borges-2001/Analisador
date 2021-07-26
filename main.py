from Operations import *
from Grammar import *
from AF import *
from ER import *

er = ER("a-z(1(0-9)*0)*0-9")

afd = er.get_afd(True)
