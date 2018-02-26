import numpy as np
import IOPart as io
import Classes as cl
from tqdm import tqdm


def SaveInfected(infec):
    res = []
    for inf in infec.values():
        res.append( ','.join([str(np.round(inf.Position[0],4)),str(np.round(inf.Position[1],4)),str(inf.IsDiagnosed)]))

    io.SaveJustLines([';'.join(res)], io.dir + "aids2.dat", clear = False)


