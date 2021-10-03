
import math
pi = 3.141592653

class fluid:
    
    def __init__(self, Tin = 0, Tout = 0, w = 0, Cp = 0, ro = 0, mu = 0, K = 0 , Pr = 0, Rf = 0):
        self.Tin = Tin
        self.Tout = Tout
        self.CaloricT = (Tout+Tin)/2
        self.w = w
        self.Cp = Cp
        self.ro = ro
        self.K = K
        self.mu = mu
        self.Pr = 0
        self.Rf = Rf 
        
        self.di = 0
        self.do = 0
        self.Re = 0
        self.vel = 0
        self.jH = 0
        self.h = 0
        self.de = 0
        self.pt = 0
        self.Nu = 0
        self.delP = 0

        
    
    def calcCaloricT(self, Fc):
        return min(self.Tin, self.Tout) + Fc*(abs(self.Tout-self.Tin))
    
    def calcQ(self):
        return self.Cp*self.w*abs(self.Tout-self.Tin)    
    
    def calcW(self):
        return self.Q/(abs(self.Tout-self.Tin)*self.Cp)
    
    def calcRe(self):
        return (self.ro*self.vel*self.De)/(self.mu)
    
        
        
class shell(fluid):
    def __init__(self):
        super().__init__()
        self.As = 0
        self.De = 0
        self.B = self.di/2
        self.Clearance = 0
        self.Vs = 0

    
    def calcClearance(self, x):
        return self.pt - x
    
    def calcAs(self):
        return ((self.Clearance*self.B*self.di)/(self.pt))
    
    def calcVs(self):
        return self.w/(self.As*self.ro)
    
    def calcDe(self, x):
        return (4*(self.pt**2 - (pi/4)*x**2))/(pi*x)
    
    def calcRe(self):
        return (self.ro*self.De*self.Vs)/(self.mu)
    
    def calcNu(self):
        return self.jH*((self.Cp*self.mu)/(self.K))**(1/3)*0.95
    
    def calch(self):
        return (self.Nu*(self.K))/self.De
    

class tube(fluid):
    def __init__(self):
        super().__init__()
        self.np = 2
        self.nt = 0
        self.overdesign = 100
        self.tolerance = 100
        self.Uoverall = 0
        self.Aoverall = 0
        self.Ft = 0.93
        
    def calcVel(self):
        return (4*self.w*self.np)/(self.ro*3.14159*self.di*self.di*self.nt)
    
    def calcRe(self):
        return (self.ro*self.vel*self.di)/self.mu
    
    def calcNu(self):
        return 0.023*(self.Re**0.8)*(self.Pr**0.4)*(1.05)
    
    def calch(self):
        return (self.Nu*(self.K))/self.di

class process:

    def __intit__(self):
        self.tolerance = 100
        self.overdes = 100
        self.LMTD = 0
        self.tubeLength = 0



def inchToMeter(inch):
    return inch*0.0254

def meterToInch(meter):
    return meter/0.0254

def fahrenheitToKelvin(temperature):
    return (temperature-32)/1.8 + 273.15

def kelvinToFahrenheit(temperature):
    return (temperature-273.15)*1.8 + 32

def celsiusToKelvin(temperature):
    return temperature + 273.15

def toK_SI(K):
    return K*1.7295772056

def toCp_SI(Cp):
    return Cp*4186.8

def toU_SI(U):
    return U*5.678263341

    
    
def calcLMTD(Thin, Thout, Tcin, Tcout):
    
    delT1 = Thin- Tcout
    delT2 = Thout - Tcin
    
    return (delT1 - delT2)/(math.log((delT1/delT2)))

def calcAfromUassumed(Q, Uassumed, Ft, LMTD):
    return Q/(Uassumed*Ft*LMTD)

def calcNoOfTubes(A, do):
    return A/(pi*do*6.096)

def calcU(ho, hi, Ro, Ri, do, di, Kw):
    temp = (1/ho) + Ro + ((di*di)/(do*do))*(((do-di)/(2*Kw)) + Ri + (1/hi))
    return (1/temp)

def calcTolerance(U, Uassumed):
    return (abs(U- Uassumed)/(Uassumed))*100

pitchFromTubeOD = {}
pitchFromTubeOD[0.75] = 1.00
pitchFromTubeOD[1.00] = 1.25
pitchFromTubeOD[1.25] = 1.5625
pitchFromTubeOD[1.5] = 1.875


tubeIDfromTubeOD = {}
tubeIDfromTubeOD[0.75] = 0.652
tubeIDfromTubeOD[1.00] = 0.902
tubeIDfromTubeOD[1.25] = 1.15
tubeIDfromTubeOD[1.5] = 1.40

practicalTubes = {}
practicalTubes[1.00] = [[8,16], [10,32], [12,45], [13.25, 56], [15.25, 76], [17.25,112], [19.25,132], [21.25, 166], [23.25, 208], [25, 252], [27,288], [29,326], [31,398]]
practicalTubes[0.75] = [[8,26], [10,52], [12,76], [13.25, 90], [15.25, 124], [17.25,166], [19.25,220], [21.25, 270], [23.25, 324], [25, 394], [27,460], [29,526], [31,640]]
practicalTubes[1.25] = [[10,12], [12,24], [13.25,30], [15.25, 40], [17.25, 53], [19.25,73], [21.25,90], [23.25, 112], [25, 135], [27, 166], [29,188], [31,220]]
practicalTubes[1.50] = [[12,16], [13.25,22], [15.25, 29], [17.25, 39], [19.25,48], [21.25,60], [23.25, 74], [25, 90], [27, 108], [29,127], [31,146]]


def calcPracticalTubes(ntheoretical, tubedo):
    for curr in practicalTubes[tubedo]:
        if(curr[1] > ntheoretical):
            return curr[0],curr[1]


def design(shellFluid, tubeFluid):

    
    tubeODlist = [0.75, 1.00, 1.25, 1.50]

    Ft = tubeFluid.Ft

    shellFluid.Q = shellFluid.calcQ()
    tubeFluid.Q = shellFluid.Q
    tubeFluid.w = tubeFluid.calcW()

    LMTD  = calcLMTD(max(tubeFluid.Tin, shellFluid.Tin), max(tubeFluid.Tout, shellFluid.Tout), min(tubeFluid.Tin, shellFluid.Tin), min(tubeFluid.Tout, shellFluid.Tout))
    tubeFluid.LMTD = LMTD

    for tubeod in tubeODlist :
        
        Uassumed = 500
        overdes = 100
        tolerance = 100

        tubeFluid.do = inchToMeter(tubeod)
        tubeFluid.di = inchToMeter(tubeIDfromTubeOD[tubeod])
        tubeFluid.pt = inchToMeter(pitchFromTubeOD[tubeod])
        shellFluid.pt = tubeFluid.pt
        tubeFluid.np = 2
        
        while tolerance > 5:
            
            A = calcAfromUassumed(tubeFluid.Q, Uassumed, Ft, LMTD)
            tubeFluid.Aoverall = A
            theoretical_nt = calcNoOfTubes(A, tubeFluid.do)   

            shellFluid.di, tubeFluid.nt = calcPracticalTubes(theoretical_nt, tubeod)
            shellFluid.di = inchToMeter(shellFluid.di)

            tubeFluid.vel = tubeFluid.calcVel()
            tubeFluid.Re = tubeFluid.calcRe()

            tubeFluid.Nu = tubeFluid.calcNu()
            tubeFluid.h = tubeFluid.calch()

            shellFluid.Clearance = shellFluid.calcClearance(tubeFluid.do)
            shellFluid.B = (shellFluid.di/2)
            shellFluid.As = shellFluid.calcAs()
            shellFluid.Vs = shellFluid.calcVs()
            shellFluid.De = shellFluid.calcDe(tubeFluid.do)
            shellFluid.Re = shellFluid.calcRe()

            shellFluid.jH = 0.5168*(shellFluid.Re**0.508)
            shellFluid.Nu = shellFluid.calcNu()
            shellFluid.h = shellFluid.calch()

            U = calcU(shellFluid.h, tubeFluid.h, shellFluid.Rf, tubeFluid.Rf, tubeFluid.do, tubeFluid.di, 25)

            tolerance = calcTolerance(Uassumed, U)
            Uassumed = U
            overdes = ((tubeFluid.nt - theoretical_nt)/(tubeFluid.nt))*100
            tubeFluid.Uoverall = U
        
        if(overdes<10):
            fric = 0.4*shellFluid.Re**(-0.24825)
            delPf = (0.5*fric*tubeFluid.ro*tubeFluid.vel*tubeFluid.vel*(6.095))*(1/tubeFluid.di)

            delPr = (8*tubeFluid.vel*tubeFluid.vel)/(2*tubeFluid.ro*9.8)

            tubeFluid.delP = delPf + delPr

            if(tubeFluid.delP < 100000):

                tubeFluid.tolerance = tolerance
                tubeFluid.overdesign = overdes
                return
    
    return
