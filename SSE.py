import extremum as ex

def line(S1, S2, E):
    SEline = ex.inclination(S2[0], S2[1], E[0], E[1])
    SSline = ex.inclination(S1[0], S1[1], S2[0], S2[1])
    print(SEline, SSline)

