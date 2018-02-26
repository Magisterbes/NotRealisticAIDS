import numpy as np
import IOPart as io
import Classes as cl
from tqdm import tqdm
import Output as ou






if __name__ == '__main__':
   
    s = cl.Soc(100000)

    io.SaveJustLines([], io.dir + "aids.dat", clear = True)
    for week in tqdm(range(52*10)):
        s.IterSoc();

        ou.SaveInfected(s.Infected)


    a=1
