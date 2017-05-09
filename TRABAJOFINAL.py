# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal
"""

import numpy as np
import xlrd

doc = xlrd.open_workbook("DATOSDEENTRADA.xlsx")#IMPORTAMOS EL ARCHIVO DE EXCEL
worksheet = doc.sheet_by_name("Hoja1")#INDICAMOS LA HOJA
worksheet2 = doc.sheet_by_name("Hoja2")#INDICAMOS LA HOJA
                     
r = worksheet.cell_value (2,0)#RESISTENCIA
a = worksheet.cell_value (2,1)#ASENTAMIENTO
tnm = worksheet.cell_value (2,2)#TAMAÑO NOMINAL MAXIMO
mf = worksheet.cell_value (2,3)#MODULO DE FINURA
ma = worksheet.cell_value (2,4)#MASA UNITARIA COMPACTADA
hg = worksheet.cell_value (2,5)#% HUMEDAD GRAVA
hf = worksheet.cell_value (2,6)#%HUMEDAD FINO
absg = worksheet.cell_value (2,7)#ABSORCION GRUESO
absf = worksheet.cell_value (2,8)#ABSORCION FINO 
gg = worksheet.cell_value (2,9)#DENSIDAD SECA GRUESO
gf = worksheet.cell_value (2,10)#DENSIDAD SECA FINO
                          
if r<215: #RESISTENCIAS CORREGIDAS
    rc = r + 70

if 215<=r<=350:
    rc = r + 85
    
if r>350:
    rc = 11*r + 50

print ()
print (("SU RESISTENCIA CORREGIDA ES") , (rc))
print ()

V35 = np.zeros (7) #VECTORES DE AGUA EN KILOGRAMOS 
V58 = np.zeros (7)
V810 = np.zeros (7) 
V1015= np.zeros (7)
V1518 = np.zeros (7)
VTM = np.zeros (7)

for i in range (0,7): # GUARDAR LOS VALORES DE AGUA
    V35[i] = worksheet2.cell_value (12,i+1)
    V58[i] = worksheet2.cell_value (13,i+1)
    V810[i] = worksheet2.cell_value (14,i+1)
    V1015[i] = worksheet2.cell_value (15,i+1)
    V1518[i] = worksheet2.cell_value (16,i+1)
    VTM[i] = worksheet2.cell_value (11,i+1)

for i in range (0,6): #APROXIMACION AL VALOR DEL TNM
    if VTM[i]<=tnm<=VTM[i+1]:
        mit = (VTM[i] + VTM[i+1])/2
        if tnm<=mit :
            tnm = VTM[i]
        else:
            tnm = VTM[i+1]

if 3<=a<=5:
    V = V35
if 5<=a<=8:
    V = V58
if 8<=a<=10:
    V = V810
if 10<=a<=15:
    V = V1015
if 15<=a<=18:
    V = V1518

for i in range (0,7): #AGUA EN BASE A POSICION
    if tnm == VTM[i]:
        agua = V[i]

print (("VALOR DE LA CANTIDAD DE AGUA"), (agua))
print ()

VCA = np.zeros (7) #VECTOR PORCENTAJE CONTENIDO DE AIRE
for i in range (0,7):
    VCA[i] = worksheet2.cell_value (17,i+1)
    if tnm == VTM[i]:
       aire = VCA[i]
       print (("VALOR DEL PORCENTAJE DE AIRE"), (aire))
       print ()
    

rac = np.zeros (6) #GUARDAR EN UN VECTOR LAS RELACIONES AGUA/CEMENTO

for i in range (0,6):
    rac [i] = worksheet2.cell_value ((i+1),1)

    
if rc<=175: #VALOR DE LA RELACION AGUA/CEMENTO
    RAC = rac[0]
    
if 175<rc<=210:
    RAC = rac[1]

if 210<rc<=245:
    RAC = rac[2]

if 245<rc<=280:
    RAC = rac[3]
    
if 280<rc<=315:
    RAC = rac[4]
    
if 315<rc<=350:
    RAC = rac[5]    
    
print (("VALOR DE LA RELACION AGUA/CEMENTO"), (RAC))
print()

C = round((agua)/(RAC),2)

print (("CONTENIDO DE CEMENTO"), (C))
print()

VMF = np.zeros(4)  #VECTOR MODULO DE FINURA
VTM2 = np.zeros(7) #VECTOR TAMAÑO AGREGADO
MVA = np.zeros([7,4]) #MATRIZ VOLUMEN DE AGREGADO GRUESO

for i in range (0,4):
    VMF[i] = worksheet2.cell_value (22,i+1) 
for i in range(7):
    VTM2[i] = worksheet2.cell_value ((i+23),0)                 

for i in range (0,4):
    for j in range (0,7):
        MVA[j,i] = worksheet2.cell_value (j+23,i+1)

for i in range (0,4):
    if mf == VMF[i]:
        c=i
        
for i in range (0,7):
    if tnm == VTM2[i]:
        f=i
        
VAG = MVA[f,c]
print (("VOLUMEN DE AGREGADO GRUESO"), (VAG))
print ()

B = (VAG*(ma/gg))

CK = 1000 -(0.318*C) - VAG
P = round(((CK -1000*B)/CK)*100,2) #PORCENTAJE DE AGREGADO FINO
print (("PORCENTAJE DE AGREGADO FINO"), (P))
print ()

#PROPORCIONES
K = (1000/C)-0.318-RAC #CONSTANTE PARA F Y G
F = round(((K*P)/100)*gf,2) #AGREGADO FINO
G = round(((K*(100-P))/100)*gg,2) #AGREGADO GRUESO

#CORRECCION HUMEDAD
HGC = VAG*(1+(hg/100)) #HUMEDAD GRUESO
HFC = P*(1+(hf/100)) #HUMEDAD FINO
AC = agua-P*((hf/100)-(absf/100))-VAG*((hg/100)-(absg/100)) #CORRECCION AGUA




    

