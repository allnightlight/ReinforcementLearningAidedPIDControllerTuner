'''
Created on 2020/05/25

@author: ukai
'''
from scipy.integrate import ode
import numpy as np
from framework import Environment
from google_auth_oauthlib import flow
from ConcObservation import ConcObservation
from AsmAction import AsmAction

class AsmSimulator(Environment):
    '''
    classdocs
    '''
    
    nMv = 1
    nPv = -1

    asmVarNames = "S_A, S_ALK, S_F, S_I, S_N2, S_NH4, S_NO3, S_O2, S_PO4, "\
        "X_AUT, X_H, X_I, X_PAO, X_PHA, X_PP, X_S, X_TSS".replace(" ", \
        "").split(",")

    def __init__(self, h = 15/60/24, volume = 12, flow = 24, rho = 1/24, pgain = 10000., amplitudePeriodicDv = 1.0):
        '''
        Constructor
        the unit of h is [day]
        '''
        
        self.odeHandler = ode(self.f)        
        self.t = None # (,)
        self.x = None # (*,)
        self.h = h
        self.flow = flow
        self.volume = volume
        self.rho = rho
        self.pgain = pgain
        self.amplitudePeriodicDv = amplitudePeriodicDv
        self.idxSO2 = AsmSimulator.asmVarNames.index("S_O2")
        self.idxNH4 = AsmSimulator.asmVarNames.index("S_NH4")

        self.isSoluble = np.array([elm[0] == 'S' for elm in AsmSimulator.asmVarNames]) # (nS + nX,)
        self.nAsm = len(self.asmVarNames)
    
    def init(self):
        self.t = 0
        self.x = self.getSteadyState()
        
    def getSteadyState(self):        
        # steady state with DO = 3, rho = 1/24, volume = 12, flow = 24
        return np.array([9.71554810e-02, 4.97924362e+02, 4.20472160e-01, 3.00000000e+01,
           1.74268503e+01, 3.98470015e-01, 1.71534735e+01, 2.95591312e+00,
           4.57085240e+00, 3.86973112e+01, 1.08088987e+03, 9.62959386e+02,
           4.42990298e-05, 1.94593829e-08, 3.94257857e-05, 2.75683299e+01,
           2.61009185e+03])
            
    def observe(self):
        y = self.x[self.idxNH4].reshape(1,1).astype(np.float32)
        return ConcObservation(y)        
    
    def update(self, action):
        assert isinstance(action, AsmAction)
        
        Do = action.getActionOnEnvironment()
        Mv = Do
        
        Dv = self.generateDv() # (nAsm,)
        
        self.odeHandler.set_initial_value(self.x, self.t)
        self.odeHandler.set_f_params(Dv, Mv)
        self.odeHandler.integrate(self.t + self.h)
        self.t = self.t + self.h
        self.x = self.odeHandler.y
    
    def f(self, t, x, Dv, Mv):
        # x: (nAsm,)
        # Dv: (*, ), Mv: (*, )
        
        xInflow = Dv # (nAsm,)
        Do = Mv # (,)
        
        dxdt = np.zeros(self.nAsm) # (nAsm,)
        retentionTime = self.volume/self.flow
        
        # Volume * dX/dt = 
        #    Xinflow * flow
        #    - X * flow
        #    + (1-rho) * flow
        #    + ASM(S, X) * Volume

        # Volume * dS/dt = 
        #    Sinflow * flow
        #    - S * flow
        #    + ASM(S, X) * Volume
        #
        # dSO2/dt += Gain * max(DO - SO2, 0)
        
        dxdt += xInflow/retentionTime # (nAsm,)
        dxdt[self.isSoluble] -= self.x[self.isSoluble]/retentionTime # (nS,)
        dxdt[~self.isSoluble] -= self.rho * self.x[~self.isSoluble]/retentionTime # (nX,)
        
        dxdtAsm= np.array(AsmSimulator.getBiologicalProcess(*x)) # (nAsm,)         
        dxdt += dxdtAsm # (nAsm,)
        
        dxdt[self.idxSO2] += self.pgain * max(Do - x[self.idxSO2], 0) # (,)
        
        return dxdt # (nAsm,)
    
    def generateDv(self):
        
        xInflow = np.array(AsmSimulator.getDefaultInflow()) # (nAsm,)
        Dv = xInflow * np.exp(np.log(self.amplitudePeriodicDv) * np.sin(np.pi * 2 * (self.t % 1.0))) # (nAsm,)
        
        return Dv
    
    @classmethod
    def getBiologicalProcess(cls, S_A, S_ALK, S_F, S_I, S_N2, S_NH4, S_NO3, S_O2, 
        S_PO4, X_AUT, X_H, X_I, X_PAO, X_PHA, X_PP, X_S, X_TSS):

        b_AUT = 0.15
        b_H = 0.4
        b_PAO = 0.2
        b_PHA = 0.2
        b_PP = 0.2
#DO = 3
        f_SI = 0
        f_XI = 0.1
        Inflow_S_A = 20
        Inflow_S_ALK = 500
        Inflow_S_F = 30
        Inflow_S_I = 30
        Inflow_S_N2 = 15
        Inflow_S_NH4 = 16
        Inflow_S_NO3 = 0
        Inflow_S_O2 = 0
        Inflow_S_PO4 = 3.6
        Inflow_X_AUT = 0
        Inflow_X_H = 30
        Inflow_X_I = 25
        Inflow_X_PAO = 0
        Inflow_X_PHA = 0
        Inflow_X_PP = 0
        Inflow_X_S = 125
        Inflow_X_TSS = 180
        i_NBM = 0.07
        i_NSF = 0.03
        i_NSI = 0.01
        i_NXI = 0.03
        i_NXS = 0.04
        i_PBM = 0.02
        i_PSF = 0.01
        i_PSI = 0
        i_PXI = 0.01
        i_PXS = 0.01
        i_TSSBM = 0.9
        i_TSSXI = 0.75
        i_TSSXS = 0.75
        K_A = 4
        K_ALK = 0.1
        K_ALK_aut = 0.5
        K_F = 4
        K_fe = 4
        K_h = 3
        K_IPP = 0.02
        K_MAX = 0.34
        K_NH4 = 0.05
        K_NH4_aut = 1
        K_NO3 = 0.5
        K_O2 = 0.2
        K_O2_aut = 0.5
        K_P = 0.01
        K_PHA = 0.01
        K_PP = 0.01
        K_PS = 0.2
        K_X = 0.1
        n_fe = 0.4
        n_NO3_het = 0.8
        n_NO3_hyd = 0.6
        n_NO3_pao = 0.6
        Qin = 24
        Qinter = 1*Qin
        Qsludge = 0.2*Qin
        q_fe = 3
        q_PHA = 3
        q_PP = 1.5
        SRT = 12
        u_AUT = 1
        u_H = 6
        u_PAO = 1
        v15_PO4 = -(f_XI*i_PXI+(1-f_XI)*i_PXS-i_PBM)
        v19_NH4 = -(f_XI*i_NXI+(1-f_XI)*i_NXS-i_NBM)
        v19_PO4 = -(f_XI*i_PXI+(1-f_XI)*i_PXS-i_PBM)
        v1_NH4 = -((1-f_SI)*i_NSF+f_SI*i_NSI-i_NXS)
        v1_PO4 = -((1-f_SI)*i_PSF+f_SI*i_PSI-i_PXS)
        v1_TSS = -i_TSSXS
        v2_NH4 = -((1-f_SI)*i_NSF+f_SI*i_NSI-i_NXS)
        v2_PO4 = -((1-f_SI)*i_PSF+f_SI*i_PSI-i_PXS)
        v2_TSS = -i_TSSXS
        v3_NH4 = -((1-f_SI)*i_NSF+f_SI*i_NSI-i_NXS)
        v3_PO4 = -((1-f_SI)*i_PSF+f_SI*i_PSI-i_PXS)
        v3_TSS = -i_TSSXS
        Y_AUT = 0.24
        Y_H = 0.625
        Y_PAO = 0.625
        Y_PHA = 0.2
        Y_PO4 = 0.4
        R01 = K_h*(S_O2/(K_O2+S_O2))*((X_S/X_H)/(K_X+X_S/X_H))*X_H
        R02 = K_h*n_NO3_hyd*(K_O2/(K_O2+S_O2))*(S_NO3/(K_NO3+S_NO3))*((X_S/X_H)/(K_X+X_S/X_H))*X_H
        R03 = K_h*n_fe*(K_O2/(K_O2+S_O2))*(K_NO3/(K_NO3+S_NO3))*((X_S/X_H)/(K_X+X_S/X_H))*X_H
        R04 = u_H*(S_O2/(K_O2+S_O2))*(S_F/(K_F+S_F))*(S_F/(S_F+S_A))*(S_NH4/(K_NH4+S_NH4))*(S_PO4/(K_P+S_PO4))*(S_ALK/(K_ALK+S_ALK))*X_H
        R05 = u_H*(S_O2/(K_O2+S_O2))*(S_A/(K_A+S_A))*(S_A/(S_F+S_A))*(S_NH4/(K_NH4+S_NH4))*(S_PO4/(K_P+S_PO4))*(S_ALK/(K_ALK+S_ALK))*X_H
        R06 = u_H*n_NO3_het*(K_O2/(K_O2+S_O2))*(S_F/(K_F+S_F))*(S_F/(S_F+S_A))*(S_NH4/(K_NH4+S_NH4))*(S_NO3/(K_NO3+S_NO3))*(S_ALK/(K_ALK+S_ALK))*(S_PO4/(K_P+S_PO4))*X_H
        R07 = u_H*n_NO3_het*(K_O2/(K_O2+S_O2))*(S_A/(K_A+S_A))*(S_A/(S_F+S_A))*(S_NH4/(K_NH4+S_NH4))*(S_NO3/(K_NO3+S_NO3))*(S_ALK/(K_ALK+S_ALK))*(S_PO4/(K_P+S_PO4))*X_H
        R08 = q_fe*(K_O2/(K_O2+S_O2))*(K_NO3/(K_NO3+S_NO3))*(S_F/(K_fe+S_F))*(S_ALK/(K_ALK+S_ALK))*X_H
        R09 = b_H*X_H
        R10 = q_PHA*(S_A/(K_A+S_A))*(S_ALK/(K_ALK+S_ALK))*((X_PP/X_PAO)/(K_PP+X_PP/X_PAO))*X_PAO
        R11 = q_PP*(S_O2/(K_O2+S_O2))*(S_PO4/(K_PS+S_PO4))*(S_ALK/(K_ALK+S_ALK))*((X_PHA/X_PAO)/(K_PHA+X_PHA/X_PAO))*((K_MAX-X_PP/X_PAO)/(K_IPP+K_MAX-X_PP/X_PAO))*X_PAO
        R12 = R11*n_NO3_pao*(K_O2/S_O2)*(S_NO3/(K_NO3+S_NO3))
        R13 = u_PAO*(S_O2/(K_O2+S_O2))*(S_NH4/(K_NH4+S_NH4))*(S_ALK/(K_ALK+S_ALK))*(S_PO4/(K_P+S_PO4))*((X_PHA/X_PAO)/(K_PHA+X_PHA/X_PAO))*X_PAO
        R14 = R13*n_NO3_pao*(K_O2/S_O2)*(S_NO3/(K_NO3+S_NO3))
        R15 = b_PAO*X_PAO*S_ALK/(K_ALK+S_ALK)
        R16 = b_PP*X_PP*S_ALK/(K_ALK+S_ALK)
        R17 = b_PHA*X_PHA*S_ALK/(K_ALK+S_ALK)
        R18 = u_AUT*(S_O2/(K_O2_aut+S_O2))*(S_NH4/(K_NH4_aut+S_NH4))*(S_PO4/(K_P+S_PO4))*(S_ALK/(K_ALK_aut+S_ALK))*X_AUT
        R19 = b_AUT*X_AUT
        v12_NO3 = -(7/20)*Y_PHA
        v13_O2 = 1-1/Y_H
        v14_NO3 = (7/20)*(1-1/Y_H)
        v18_NH4 = -i_NBM-1/Y_AUT
        v1_ALK = (1/14)*v1_NH4-(1.5/31)*v1_PO4
        v2_ALK = (1/14)*v2_NH4-(1.5/31)*v2_PO4
        v3_ALK = (1/14)*v3_NH4-(1.5/31)*v3_PO4
        d_S_A = 0
        d_S_ALK = 0
        d_S_F = 0
        d_S_I = 0
        d_S_N2 = 0
        d_S_NH4 = 0
        d_S_NO3 = 0
        d_S_O2 = 0
        d_S_PO4 = 0
        d_X_AUT = 0
        d_X_H = 0
        d_X_I = 0
        d_X_PAO = 0
        d_X_PHA = 0
        d_X_PP = 0
        d_X_S = 0
        d_X_TSS = 0
#d_S_O2 += (10000*(DO-S_O2)) * (1)
        d_S_F += (R01) * (1-f_SI)
        d_S_NH4 += (R01) * (v1_NH4)
        d_S_PO4 += (R01) * (v1_PO4)
        d_S_I += (R01) * (f_SI)
        d_S_ALK += (R01) * (v1_ALK)
        d_X_S += (R01) * (-1)
        d_X_TSS += (R01) * (v1_TSS)
        d_S_F += (R02) * (1-f_SI)
        d_S_NH4 += (R02) * (v2_NH4)
        d_S_PO4 += (R02) * (v2_PO4)
        d_S_I += (R02) * (f_SI)
        d_S_ALK += (R02) * (v2_ALK)
        d_X_S += (R02) * (-1)
        d_X_TSS += (R02) * (v2_TSS)
        d_S_F += (R03) * (1-f_SI)
        d_S_NH4 += (R03) * (v3_NH4)
        d_S_PO4 += (R03) * (v3_PO4)
        d_S_I += (R03) * (f_SI)
        d_S_ALK += (R03) * (v3_ALK)
        d_X_S += (R03) * (-1)
        d_X_TSS += (R03) * (v3_TSS)
        d_S_O2 += (R04) * (1-1/Y_H)
        d_S_F += (R04) * (-1/Y_H)
        d_X_H += (R04) * (1)
        d_S_NH4 += (R04) * (i_NSF/Y_H-i_NBM)
        d_S_PO4 += (R04) * (i_PSF/Y_H-i_PBM)
        d_S_ALK += (R04) * (1/14*(i_NSF/Y_H-i_NBM)-(1.5/31)*(i_PSF/Y_H-i_PBM))
        d_X_TSS += (R04) * (i_TSSBM)
        d_S_O2 += (R05) * (1-1/Y_H)
        d_S_A += (R05) * (-1/Y_H)
        d_X_H += (R05) * (1)
        d_S_NH4 += (R05) * (-i_NBM)
        d_S_PO4 += (R05) * (-i_PBM)
        d_S_ALK += (R05) * ((1/64)*(1/Y_H)-(i_NBM/14)+(1.5*i_PBM)/31)
        d_X_TSS += (R05) * (i_TSSBM)
        d_S_F += (R06) * (-1/Y_H)
        d_S_NO3 += (R06) * (-(1-Y_H)/(2.86*Y_H))
        d_S_N2 += (R06) * ((1-Y_H)/(2.86*Y_H))
        d_X_H += (R06) * (1)
        d_S_NH4 += (R06) * (i_NSF/Y_H-i_NBM)
        d_S_PO4 += (R06) * (i_PSF/Y_H-i_PBM)
        d_S_ALK += (R06) * ((1/14)*((1-Y_H)/(2.86*Y_H))+(1/14)*(i_NSF/Y_H-i_NBM)-(1.5/31)*(i_PSF/Y_H-i_PBM))
        d_X_TSS += (R06) * (i_TSSBM)
        d_S_A += (R07) * (-1/Y_H)
        d_S_NO3 += (R07) * (-(1-Y_H)/(2.86*Y_H))
        d_S_N2 += (R07) * ((1-Y_H)/(2.86*Y_H))
        d_X_H += (R07) * (1)
        d_S_NH4 += (R07) * (-i_NBM)
        d_S_PO4 += (R07) * (-i_PBM)
        d_S_ALK += (R07) * ((1/64)*(1/Y_H)+(1/14)*((1-Y_H)/(2.86*Y_H))-(i_NBM/14)+(1.5*i_PBM/31))
        d_X_TSS += (R07) * (i_TSSBM)
        d_S_NH4 += (R08) * (i_NSF)
        d_S_F += (R08) * (-1)
        d_S_A += (R08) * (1)
        d_S_ALK += (R08) * (-1/64+(1/14)*i_NSF-(1.5/31)*i_PSF)
        d_S_PO4 += (R08) * (i_PSF)
        d_X_TSS += (R08) * (0)
        d_X_I += (R09) * (f_XI)
        d_X_S += (R09) * (1-f_XI)
        d_X_H += (R09) * (-1)
        d_S_PO4 += (R09) * (-i_PXI*f_XI-i_PXS*(1-f_XI)+i_PBM)
        d_S_ALK += (R09) * ((1/14)*(-i_NXI*f_XI-i_NXS*(1-f_XI)+i_NBM)-(1.5/31)*(-i_PXI*f_XI-i_PXS*(1-f_XI)+i_PBM))
        d_S_NH4 += (R09) * (-i_NXI*f_XI-i_NXS*(1-f_XI)+i_NBM)
        d_X_TSS += (R09) * (i_TSSXI*f_XI+i_TSSXS*(1-f_XI)-i_TSSBM)
        d_S_A += (R10) * (-1)
        d_S_PO4 += (R10) * (Y_PO4)
        d_X_PP += (R10) * (-Y_PO4)
        d_X_PHA += (R10) * (1)
        d_S_NH4 += (R10) * (0)
        d_S_ALK += (R10) * ((1/64)-(0.5/31)*Y_PO4)
        d_X_TSS += (R10) * (0.6-3.23*Y_PO4)
        d_S_O2 += (R11) * (-Y_PHA)
        d_S_PO4 += (R11) * (-1)
        d_X_PP += (R11) * (1)
        d_X_PHA += (R11) * (-Y_PHA)
        d_S_NH4 += (R11) * (0)
        d_S_ALK += (R11) * (0.5/31)
        d_X_TSS += (R11) * (3.23-0.6*Y_PHA)
        d_S_PO4 += (R12) * (-1)
        d_X_PP += (R12) * (1)
        d_X_PHA += (R12) * (-Y_PHA)
        d_S_NH4 += (R12) * (0)
        d_S_ALK += (R12) * (0.5/31-(1/14)*(v12_NO3))
        d_S_N2 += (R12) * (-v12_NO3)
        d_S_NO3 += (R12) * (v12_NO3)
        d_X_TSS += (R12) * (3.23-0.6*Y_PHA)
        d_S_O2 += (R13) * (v13_O2)
        d_S_PO4 += (R13) * (-i_PBM)
        d_X_PAO += (R13) * (1)
        d_X_PHA += (R13) * (-1/Y_PAO)
        d_S_NH4 += (R13) * (-i_NBM)
        d_S_ALK += (R13) * ((1.5/31)*i_PBM-(1/14)*i_NBM)
        d_X_TSS += (R13) * (i_TSSBM-0.6*(1/Y_H))
        d_S_PO4 += (R14) * (-i_PBM)
        d_X_PAO += (R14) * (1)
        d_X_PHA += (R14) * (-1/Y_PAO)
        d_S_NH4 += (R14) * (-i_NBM)
        d_S_ALK += (R14) * ((1.5/31)*i_PBM-(1/14)*i_NBM-(1/14)*v14_NO3)
        d_X_TSS += (R14) * (i_TSSBM-0.6*(1/Y_H))
        d_S_N2 += (R14) * (-v14_NO3)
        d_S_NO3 += (R14) * (v14_NO3)
        d_S_PO4 += (R15) * (v15_PO4)
        d_X_I += (R15) * (f_XI)
        d_X_S += (R15) * (1-f_XI)
        d_X_PAO += (R15) * (-1)
        d_S_NH4 += (R15) * (-i_NXI*f_XI-i_NXS*(1-f_XI)+i_NBM)
        d_S_ALK += (R15) * (-(1.5/31)*v15_PO4+(1/14)*(-i_NXI*f_XI-i_NXS*(1-f_XI)+i_NBM))
        d_X_TSS += (R15) * (i_TSSXI*f_XI+i_TSSXS*(1-f_XI)-i_TSSBM)
        d_S_PO4 += (R16) * (1)
        d_X_PP += (R16) * (-1)
        d_S_NH4 += (R16) * (0)
        d_S_ALK += (R16) * (-0.5/31)
        d_X_TSS += (R16) * (-3.23)
        d_S_A += (R17) * (1)
        d_X_PHA += (R17) * (-1)
        d_S_NH4 += (R17) * (0)
        d_S_ALK += (R17) * (-1/64)
        d_X_TSS += (R17) * (-0.6)
        d_S_O2 += (R18) * (-(4.57-Y_AUT)/Y_AUT)
        d_S_NH4 += (R18) * (v18_NH4)
        d_S_NO3 += (R18) * (1/Y_AUT)
        d_S_PO4 += (R18) * (-i_PBM)
        d_X_AUT += (R18) * (1)
        d_S_ALK += (R18) * (-(1/14)*i_NBM-(2/(14*Y_AUT))+(1.5/31)*i_PBM)
        d_X_TSS += (R18) * (i_TSSBM)
        d_S_NH4 += (R19) * (v19_NH4)
        d_S_PO4 += (R19) * (v19_PO4)
        d_X_I += (R19) * (f_XI)
        d_X_S += (R19) * (1-f_XI)
        d_X_AUT += (R19) * (-1)
        d_S_ALK += (R19) * ((1/14)*v19_NH4-(1.5/31)*v19_PO4)
        d_X_TSS += (R19) * (i_TSSXI*f_XI+i_TSSXS*(1-f_XI)-i_TSSBM)

        return d_S_A, d_S_ALK, d_S_F, d_S_I, d_S_N2, d_S_NH4, d_S_NO3, d_S_O2, d_S_PO4, d_X_AUT, d_X_H, d_X_I, d_X_PAO, d_X_PHA, d_X_PP, d_X_S, d_X_TSS

    @classmethod
    def getDefaultInflow(cls):
        Inflow_S_A = 20
        Inflow_S_ALK = 500
        Inflow_S_F = 30
        Inflow_S_I = 30
        Inflow_S_N2 = 15
        Inflow_S_NH4 = 16
        Inflow_S_NO3 = 0
        Inflow_S_O2 = 0
        Inflow_S_PO4 = 3.6
        Inflow_X_AUT = 0
        Inflow_X_H = 30
        Inflow_X_I = 25
        Inflow_X_PAO = 0
        Inflow_X_PHA = 0
        Inflow_X_PP = 0
        Inflow_X_S = 125
        Inflow_X_TSS = 180
        return Inflow_S_A,Inflow_S_ALK,Inflow_S_F,Inflow_S_I,Inflow_S_N2, \
            Inflow_S_NH4,Inflow_S_NO3,Inflow_S_O2,Inflow_S_PO4,Inflow_X_AUT, \
            Inflow_X_H,Inflow_X_I,Inflow_X_PAO,Inflow_X_PHA,Inflow_X_PP, \
            Inflow_X_S,Inflow_X_TSS

        
        
        