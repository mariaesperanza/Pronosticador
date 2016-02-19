#Esperanza Ramirez
import numpy as np
import xlrd
from numpy.linalg import pinv
localizacion = "C:\Users\18-4004\Documents\muestra_data_pronosticador.xlsx"
workbook = xlrd.open_workbook(localizacion)
sh = workbook.sheet_by_index(0)
i = 0
y = np.zeros(shape=(12,1))
for i in range(12):
    y[i] = sh.cell_value(1+i,0)
x = np.zeros(shape=(12,2))
j=0
k=0
for j in range(12):
    for k in range(2):
        x[j][k] = sh.cell_value(j+1,k+1)
xSeudoinv = pinv(x)
o = np.dot(xSeudoinv,y)
def h(x1,x2,x3):
    prueba = x1*o[0] + x2*o[1] + x3*o[2]
    resultado = 0
    for i in range(prueba.size):
        resultado += prueba[i]
    return resultado

z=0
j=13
yReal = np.zeros(shape=(13,1))
for z in range(13):
    yReal[z] = sh.cell_value(j,0)
    j += 1
xPrueba = np.zeros(shape=(12,2))
j=0
l=12
k=0
for j in range(12):
    l += 1
    for k in range(2):
        xPrueba[j][k] = sh.cell_value(l,k+1)
yPredecido = np.zeros(shape=(12,1))
j=0
k=0
for j in range(12):
    yPredecido[j] = h(xPrueba[j][0],xPrueba[j][1],xPrueba[j][2]
j=0
mapeo = np.zeros(shape=(12,1))
acumMapeo = 0
for j in range(12):
    mapeo [j]= ((abs(yReal[j] - yPredecido[j])/yReal[j])/12)*100
    acumMapeo += ((abs(yReal[j] - yPredecido[j])/yReal[j])/12)*100
print('Resultados de la prediccion del modelo \n')
print yPredecido
print('\n')
print('MAPEO \n')
print mapeo
print ('acumulado Mapeo ',acumMapeo)