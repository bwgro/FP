

import matplotlib.pyplot as plt
import numpy as np
import scipy.constants as const
from scipy.optimize import curve_fit
from uncertainties import ufloat
import uncertainties.unumpy as unp
from scipy import integrate

import os

if os.path.exists("build") == False:
   os.mkdir("build")

#konstante definieren
k = const.k
k_ev = const.k/const.e

#Werte auslesen
t_1, T_1, I_1, dI_1 = np.genfromtxt('../data/step20.csv', unpack=True)

T_1 += 273.15 # in kelvin
I_1 *= 10**(-11) #pico ampere
dI_1 *= 10**(-11)

t_2, T_2, I_2, dI_2 = np.genfromtxt('../data/step15.csv', unpack=True)

T_2 += 273.15 # in kelvin
I_2 *= 10**(-11) #pico ampere
dI_2 *= 10**(-11)

#Temperatur-Strom Diagramm

plt.figure()
plt.errorbar(T_1, I_1, yerr=dI_1, fmt='+k', label=r'Heizrate 1')
plt.errorbar(T_2, I_2, yerr=dI_2, fmt='+r', label=r'Heizrate 2')

plt.grid()

plt.xlabel(r'$T/\si{\kelvin}')
plt.ylabel(r'$I/\si{\pico\ampere}$')

plt.tight_layout()
plt.legend()
plt.savefig('build/plot.pdf')
plt.clf()


#_____________________________________________________________________________________________________________________________________________________
# Untergrund rausnehmen mit e-Fkt mit Messwerten vom Anstieg des zweiten Maximums
# Werte ab t = 45 bis 66 fürs Fitten nehmen

#Untergrund Fit für Messung 1

unter_I_1 = np.concatenate((I_1[0:11], I_1[23:28], I_1[56:]), axis=None )
unter_T_1 = np.concatenate((T_1[0:11], T_1[23:28], T_1[56:]), axis=None )

#print(unter_I_1) 
#print(unter_T_1)


def untergrund(T, a, b):
    return a*np.exp(-b/T)

popt, pcov = curve_fit(untergrund, unter_T_1, unter_I_1)
errors = np.sqrt(np.diag(pcov))

print('Untergrund Fit für Messung 1:')
print("a =", popt[0])
print("a fehler =",errors[0])
print("b =", popt[1])
print("b fehler =",errors[1])
print('\n')

plt.xlabel(r'$T/\si{\kelvin}$')
plt.ylabel(r'$I/\si{\ampere}$')

x = np.linspace(220, 340 ,1000)
plt.plot(x, untergrund(x, popt[0], popt[1]),label = 'Untergrund-Fit')
#print( untergrund(unter_T_1, popt[0], popt[1])) 
#plt.plot(unter_T_1, unter_I_1,'+k', label = 'verwendete Messpunkte')

plt.errorbar(T_1, I_1,yerr=dI_1, fmt='+k', label='Heizrate 1')

plt.legend()
plt.grid()

plt.savefig('build/untergrund_1.pdf')
plt.clf()


unter_a_1 = popt[0]
unter_b_1 = popt[1]

# irgendwie sieht der plot richtig komisch aus, aber ok, lets just pretend that it works
# also die folgende Rechnung muss ja mit korrigierten Werten laufe, und joah die werte sind jetzt erstmal nicht korrigiert
# oder doch erst bei Methode 2? ka 

# Untergrund Fit für Messung 2

unter_I_2 = np.concatenate((I_2[0:10],I_2[43:48],I_2[-1:]), axis=None)
unter_T_2 = np.concatenate((T_2[0:10],T_2[43:48],T_2[-1:]), axis=None)

popt, pcov = curve_fit(untergrund, unter_T_2, unter_I_2)
errors = np.sqrt(np.diag(pcov))

print('Untergrund Fit für Messung 2:')
print("a =", popt[0])
print("a fehler =",errors[0])
print("b =", popt[1])
print("b fehler =",errors[1])
print('\n')

plt.xlabel(r'$T/\si{\kelvin}$')
plt.ylabel(r'$I/\si{\ampere}$')

x = np.linspace(220, 340 ,1000)
plt.plot(x, untergrund(x, popt[0], popt[1]),label = 'Untergrund')
plt.plot(T_2, I_2, '+r', label=r'Messwerte')

#Korrektur
I_2 -= untergrund(T_2, popt[0], popt[1])
plt.plot(plt.plot(T_2, I_2, '+r', label=r'korrigierte Messwerte'))

plt.legend()
plt.grid()

plt.savefig('build/untergrund_2.pdf')
plt.clf()

unter_a_2 = popt[0]
unter_b_2 = popt[1]

#_________________________________________________________________________________________________________________________________________________________

# Bestimmung der Aktivierungsenergie erste Methode (mit Maximum)

def line(t,b,y):
    return b*t + y
# t Zeit, b Heizrate, y y-Achsenabschnitt

# nur die Messungen
plt.figure()
plt.plot(t_1, T_1, '.k', label='Messung 1')
plt.plot(t_2, T_2, '.r', label='Messung 2')
plt.legend()
plt.xlabel('t / min')
plt.ylabel('T / K')

plt.savefig('build/zeit_temp.pdf')
plt.clf()

# Ausgleichsrechnung Messung 1
popt, pcov = curve_fit(line, t_1, T_1)
errors = np.sqrt(np.diag(pcov))

print('Zeit-Temperatur-Fit_1 mit der Form: b*t + y')
print("b =", popt[0])
print("b fehler =",errors[0])
print("y =", popt[1])
print("y fehler =",errors[1])
print('\n')

b1 = ufloat(popt[0], errors[0])

plt.plot(t_1, T_1, '.k', label='Messung 1')
plt.plot(t_1, line( t_1, popt[0], popt[1] ), label = 'Ausgleichsgerade')
plt.legend()
plt.xlabel('t / min')
plt.ylabel('T / K')

plt.savefig('build/zeit_temp_fit_1.pdf')
plt.clf()

# Ausgleichsrechnung Messung 2
popt, pcov = curve_fit(line, t_2, T_2)
errors = np.sqrt(np.diag(pcov))

print('Zeit-Temperatur-Fit_2 mit der Form: b*t + y')
print("b =", popt[0])
print("b fehler =",errors[0])
print("y =", popt[1])
print("y fehler =",errors[1])
print("\n")

b2 = ufloat(popt[0], errors[0])

plt.plot(t_2, T_2, '.k', label='Messung 2')
plt.plot(t_2, line( t_2, popt[0], popt[1] ), label = 'Ausgleichsgerade')
plt.legend()
plt.xlabel('t / min')
plt.ylabel('T / K')

plt.savefig('build/zeit_temp_fit_2.pdf')
plt.clf()

#_____________________________________________________________________________________________________________________________________________
# Logarithmus von I und Kehrwert von T plotten
# Messung 1

log_I_1 = I_1[5:]
log_T_1 = T_1[5:]

log_I_1 -= untergrund(log_T_1, unter_a_1, unter_b_1)


T_1_korr = log_T_1 #hier kann man bestimmt noch was abschneiden an werten, die man betrachtet
I_1_korr = log_I_1

plt.plot(T_1_korr, I_1_korr, '+k', label = 'korrigierte Messung 2')
#plt.plot(1/log_T_1, np.log(log_I_1), '+k')
plt.xlabel('T / K')
plt.ylabel('I / pA')
plt.grid()
plt.legend()
plt.savefig('build/korrigierte_werte_1.pdf')
plt.clf()

# print('werte für log: ', np.log(log_I_1) )

#hier müssen die Werte noch einmal korrigiert werden, also Untergrund noch abziehen
#log_I_1 -= untergrund(log_T_1, unter_a, unter_b)
#print(log_I_1)

#plt.plot((1/T_1_korr), np.log(I_1_korr), '.k', label='Messung 1')
plt.xlabel('1/T / (1/K)')
# plt.xlabel(r'$\frac{1}{T} \, / \, \frac{1}{k}$') #\text{K}}$')
plt.ylabel(r'$\ln(I) \, / \, \ln(pA)$') #\text{pA})$')
plt.grid()

# print(1/log_T_1)
# fit_1_durch_T_1 = 1/log_T_1[:26]
# fit_log_I_1 = log_I_1[:26]

fit_1_durch_T_1 = 1/T_1_korr[9:26]      
fit_log_I_1 = np.log(I_1_korr[9:26])

#fit_1_durch_T_1 = 1/durch_T_1


plt.plot(fit_1_durch_T_1, fit_log_I_1, '+k', label='Werte')

popt, pcov = curve_fit(line, fit_1_durch_T_1, fit_log_I_1)
errors = np.sqrt(np.diag(pcov))

print('Ausgleichgerade 1 für Logarithmus Diagramm mit Form: b*t + y')
print("b =", popt[0])
print("b fehler =",errors[0])
print("y =", popt[1])
print("y fehler =",errors[1])
print('\n')

plt.plot(fit_1_durch_T_1, line( fit_1_durch_T_1, popt[0], popt[1] ), label = 'Ausgleichsgerade')

# die drei/vier punkte die abstehen vielleicht noch raus nehmen
# ja hab ich ja. passt trotzdem nicht
# ok geht klar, idk soll die drei punkte wieder rein?

plt.legend()
plt.savefig('build/log(I)_1durchT_1.pdf')
plt.clf()

#aktivierungsenergie berechnen
b = ufloat(popt[0], errors[0])
W_11 = - k*b 
W_11_ev = - k_ev*b
print(f'W_11 = {W_11} Joule = {W_11_ev} eV')

#Relaxationszeit
T_max_1 = 38.3 + 273.15 #für I_max_1 = 2.35 * 10^-11 A
tau_max11 = (k*(T_max_1**2))/(b1*W_11)
tau_11 = tau_max11 * unp.exp(- W_11/(k*T_max_1))
print(f'Realaxationszeit tau_11 = {tau_11} min')

#Messung 2

log_T_2 = np.append(T_2[1:5], T_2[12:])
log_I_2 = np.append(I_2[1:5], I_2[12:])

log_I_2 -= untergrund(log_T_2, unter_a_2, unter_b_2)

T_2_korr = log_T_2[0:50]
I_2_korr = log_I_2[0:50]

plt.plot(T_2_korr, I_2_korr, '+k', label = 'korrigierte Messung 2')
#plt.plot(1/log_T_2, np.log(log_I_2), '+k')
plt.xlabel('T / K')
plt.ylabel('I / pA')
plt.grid()
plt.legend()
plt.savefig('build/korrigierte_werte_2.pdf')
plt.clf()

# plt.plot(log_T_2, log_I_2, '+k')
plt.plot(1/T_2_korr, np.log(I_2_korr), '+k')
plt.grid()
plt.savefig('build/werte_log_2.pdf')
plt.clf()


#plt.plot((1/T_2_korr), np.log(I_2_korr), '.k', label='Messung 2')
plt.xlabel('1/T / (1/K)')
# plt.xlabel(r'$\frac{1}{T} \, / \, \frac{1}{K}$')#\text{K}}$')
plt.ylabel(r'$\ln(I) \, / \, \ln(pA)$')#\text{pA})$')
plt.grid()


fit_1_durch_T_2 = 1/T_2_korr[5:23]
fit_log_I_2 = np.log(I_2_korr[5:23])


plt.plot(fit_1_durch_T_2, fit_log_I_2, '+k', label='Werte')

popt, pcov = curve_fit(line, fit_1_durch_T_2, fit_log_I_2)
errors = np.sqrt(np.diag(pcov))

print('Ausgleichgerade 2 für Logarithmus Diagramm mit Form: b*t + y')
print("b =", popt[0])
print("b fehler =",errors[0])
print("y =", popt[1])
print("y fehler =",errors[1])
print('\n')

plt.plot(fit_1_durch_T_2, line( fit_1_durch_T_2, popt[0], popt[1] ), label = 'Ausgleichsgerade')

plt.legend()
plt.savefig('build/log(I)_1durchT_2.pdf')
plt.clf()

#aktivierungsenergie berechnen
b = ufloat(popt[0], errors[0])
W_12 = - k*b 
W_12_ev = - k_ev*b
print(f'W_12 = {W_12} Joule = {W_11_ev} eV \n')

#Relaxationszeit
tau_12 = (k*(T_max_1**2))/(b*W_12)
print('Realaxationszeit tau_12 = ', tau_12)

##ok cooler fit, W muss noch errechnet werden

#_________________________________________________________________________________________________________________________________________________________
# Methode 2
# irgendwas mit Trapezregel, gar kein bock
# hab das aus dem Internet: https://numpy.org/doc/stable/reference/generated/numpy.trapz.html
# und das https://www.geeksforgeeks.org/python-scipy-integrate-cumtrapz-method/

#mit korrigierten Werten rechnen? i think yes
#np.trapz(I_1_korr, T_2_korr)
plt.figure()
integral_1 = integrate.cumtrapz(I_1_korr, T_1_korr)
plt.plot(T_1_korr[1:], integral_1,'+k', label = 'Integral 1')
plt.legend()
plt.grid()
plt.savefig('build/integral_1.pdf')
plt.clf()

print(integral_1)
print(integral_1[47])

ln_bumms_1 = np.log((integral_1[47]- integral_1[10:31]) / I_1_korr[10:31])
fit_2_durch_T_1 = 1/T_1_korr[10:31]

print(ln_bumms_1)
# plt.plot((1/T_1_korr), np.log(I_2_korr), '.k', label='Messung 2')
plt.figure()
plt.xlabel('1/T / (1/K)')
plt.ylabel('log(x)')
plt.grid()
plt.plot(fit_2_durch_T_1, ln_bumms_1, '+k', label='Integrierte Messwert')

popt, pcov = curve_fit(line, fit_2_durch_T_1, ln_bumms_1)
errors = np.sqrt(np.diag(pcov))

print('Ausgleichgerade 1 für Logarithmus Diagramm mit Form: b*t + y')
print("b =", popt[0])
print("b fehler =",errors[0])
print("y =", popt[1])
print("y fehler =",errors[1])
print('\n')

plt.plot(fit_2_durch_T_1, line( fit_2_durch_T_1, popt[0], popt[1] ), label = 'Ausgleichsgerade')

plt.legend()
plt.savefig('build/log(int)_2durchT_1.pdf')
plt.clf()

#aktivierungsenergie berechnen
b = ufloat(popt[0], errors[0])
W_21 = k*b
W_21_ev = k_ev*b 
print(f'W_21 = {W_21} Joule = {W_21_ev} eV')

#Relaxationszeit
T_max_2 = 42.5 + 273.15 #für I_max_2 = 3.5 * 10^-11 A
tau_21 = (k*(T_max_1**2))/(b*W_21)
print('Relaxationszeit tau_21 = ', tau_21)


#Messung 2

plt.figure()
integral_2 = integrate.cumtrapz(I_2_korr, T_2_korr)
plt.plot(T_2_korr[1:], integral_2,'+k', label = 'Integral 2')
plt.legend()
plt.grid()
plt.savefig('build/integral_2.pdf')
plt.clf()

print(integral_2)
print(integral_2[39])

ln_bumms_2 = np.log((integral_2[29]- integral_2[11:29]) / I_2_korr[11:29])
fit_2_durch_T_2 = 1/T_2_korr[11:29]

print(ln_bumms_2)
# plt.plot((1/T_1_korr), np.log(I_2_korr), '.k', label='Messung 2')
plt.figure()
plt.xlabel('1/T / K^-1')
plt.ylabel('log(x)')
plt.grid()
plt.plot(fit_2_durch_T_2, ln_bumms_2, '+k', label='integrierte Messwete')

popt, pcov = curve_fit(line, fit_2_durch_T_2, ln_bumms_2)
errors = np.sqrt(np.diag(pcov))

print('Ausgleichgerade 1 für Logarithmus Diagramm mit Form: b*t + y')
print("b =", popt[0])
print("b fehler =",errors[0])
print("y =", popt[1])
print("y fehler =",errors[1])
print('\n')

plt.plot(fit_2_durch_T_2, line( fit_2_durch_T_2, popt[0], popt[1] ), label = 'Ausgleichsgerade')

plt.legend()
plt.savefig('build/log(int)_2durchT_2.pdf')
plt.clf()

#aktivierungsenergie berechnen
b = ufloat(popt[0], errors[0])
W_22 = k*b
W_22_ev = k_ev*b 
print(f'W_22 = {W_22} Joule = {W_22_ev} eV')


#Relaxationszeit
tau_22 = (k*(T_max_1**2))/(b*W_22)
print('Relaxationszeit tau_22 = ', tau_22)