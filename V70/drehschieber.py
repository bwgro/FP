import numpy as np
import matplotlib.pyplot as plt
import uncertainties.unumpy as unp
from uncertainties.unumpy import (nominal_values as noms, std_devs as stds)
from uncertainties import ufloat

# Kompilieren mit Konsole: $TEXINPUTS=$(pwd): python drehschieber.py
#
# (Nicht nötig mit Makefile aus dem Toolbox-Workshop)

# Evakuierungskurve
t, dt, p1, dp1, p2, dp2, p3, dp3 = np.genfromtxt('data/dreh_evac.csv', unpack=True)
T = unp.uarray(t,dt)
p_1 = unp.uarray(p1,dp1)
p_2 = unp.uarray(p2,dp2)
p_3 = unp.uarray(p3,dp3)
P= np.mean([p_1,p_2,p_3], axis=0)
mP = P

# Messdaten zu LateX-Tabelle
with open('content/dreh_evac.tex', 'w') as f:
    for i in range(t.size):
        f.write(f'{T[i]:.1uS} & {p_1[i]:.2uS} & {p_2[i]:.2uS} & {p_3[i]:.2uS}\\\\ \n')

# Enddruck
pE = ufloat(6.7e-3, (6.7e-3)/10)
print(f'{pE:S}')

# Rezipientenvolumen
V = ufloat(34, 3.4)

# Anpassen an Enddruck
p_1 = p_1 - pE
p_2 = p_2 - pE
p_3 = p_3 - pE
P = P - pE


# Lograthmischer Ausdruck nach Enddruckanpassung
p_1 = unp.log(p_1/p_1[0])
p_2 = unp.log(p_2/p_2[0])
p_3 = unp.log(p_3/p_3[0])
P = unp.log(P/P[0])

with open('content/dreh_evac_mean.tex', 'w') as f:
    for i in range(t.size):
        f.write(f'{T[i]:.1uS} & {mP[i]:.2uS} & {P[i]:S} \\\\ \n')

# Ausgleichsgeraden in Abschnitten
print('Parameter der Ausgleichsgeraden zur Evakuierungskurve der Drehschieberpumpe:')
params1,cov_matrix1 = np.polyfit(t[0:17], noms(P[0:17]), deg=1, cov=True)
uParams1 = unp.uarray(params1, np.sqrt(np.diag(cov_matrix1)))
print(f'Abschnitt 1: m = {uParams1[0]:S}, b = {uParams1[1]:S}')
params2,cov_matrix2 = np.polyfit(t[22:33], noms(P[22:33]), deg=1, cov=True)
uParams2 = unp.uarray(params2, np.sqrt(np.diag(cov_matrix2)))
print(f'Abschnitt 2: m = {uParams2[0]:S}, b = {uParams2[1]:S}')
params3,cov_matrix3 = np.polyfit(t[39:60], noms(P[39:60]), deg=1, cov=True)
uParams3 = unp.uarray(params3, np.sqrt(np.diag(cov_matrix3)))
print(f'Abschnitt 3: m = {uParams3[0]:S}, b = {uParams3[1]:S}\n')

# Saugvermögen 
print('Ausgerechnete Saugvermögen:')
S_1 = - params1[0] * V
print(f'Abschnitt 1: S = {S_1:S}, Druck von {mP[0]:S} bis {mP[20]:S}')
S_2 = - params2[0] * V
print(f'Abschnitt 2: S = {S_2:S}, Druck von {mP[20]:S} bis {mP[34]:S}')
S_3 = - params3[0] * V
print(f'Abschnitt 3: S = {S_3:S}, Druck von {mP[34]:S} bis {mP[60]:S} \n')

# Plot logarithmisch
x = np.linspace(0,600,6000)
fig, ax = plt.subplots()
ax.errorbar(t, noms(P), xerr=0.2, yerr=stds(P), fmt='k+', ecolor='r', capsize=2, label=r'Messwerte mit Fehlerbalken')
ax.plot(x[0:3150], params1[0]*x[0:3150] + params1[1], label=r'Abschnitt 1')
ax.plot(x[0:5500], params2[0]*x[0:5500] + params2[1], label=r'Abschnitt 2')
ax.plot(x, params3[0]*x + params3[1], label=r'Abschnitt 3')
ax.set_ylabel(r'$\ln\left(\frac{p(t)-p_E}{p _0-p_E}\right)$')
ax.set_xlabel(r'$t/\si{\second}$')

ax.grid()
ax.legend(loc='best')
plt.tight_layout()
plt.savefig('abb/dreh_evac.pdf')

# Leckratenmessung
t05, dt05, p05_1, dp05_1, p05_2, dp05_2, p05_3, dp05_3 = np.genfromtxt('data/dreh_leck0.5.csv', unpack=True)
t10, dt10, p10_1, dp10_1, p10_2, dp10_2, p10_3, dp10_3 = np.genfromtxt('data/dreh_leck10.csv', unpack=True)
t50, dt50, p50_1, dp50_1, p50_2, dp50_2, p50_3, dp50_3 = np.genfromtxt('data/dreh_leck50.csv', unpack=True)
t100, dt100, p100_1, dp100_1, p100_2, dp100_2, p100_3, dp100_3 = np.genfromtxt('data/dreh_leck100.csv', unpack=True)

# Gleichgewichtsdruck

# Messdaten Dictionary
dict = {'t': unp.uarray(t05,dt05),
    '0.5': [unp.uarray(p05_1, dp05_1), unp.uarray(p05_2, dp05_2), unp.uarray(p05_3, dp05_3)],
    '10': [unp.uarray(p10_1, dp10_1), unp.uarray(p10_2, dp10_2), unp.uarray(p10_3, dp10_3)],
    '50': [unp.uarray(p50_1, dp50_1), unp.uarray(p50_2, dp50_2), unp.uarray(p50_3, dp50_3)],
    '100': [unp.uarray(p100_1, dp100_1), unp.uarray(p100_2, dp100_2), unp.uarray(p100_3, dp100_3)]}


# Messdaten zu LateX-Tabelle
for p in ('0.5', '10', '50', '100'):
    with open('content/dreh_leck_raw' + p + '.tex', 'w') as f:
        for i in range(dict['t'].size):
            f.write(f'{dict["t"][i]:.1uS} & {dict[p][0][i]:S} & {dict[p][1][i]:S} & {dict[p][2][i]:S} & {np.mean(dict[p], axis=0)[i]:S}\\\\ \n')

# Mittelwert Dictionary
dict = {'t': dict['t'], '0.5': np.mean(dict['0.5'], axis=0), '10': np.mean(dict['10'], axis=0),
'50': np.mean(dict['50'], axis=0), '100': np.mean(dict['100'], axis=0),}
print(f'{dict["0.5"][8]:.2uS}')

# Plot
print('Leckratenmessung:')
for p in ['0.5', '10', '50', '100']:
    params,cov_matrix = np.polyfit(noms(dict['t'][1:]), noms(dict[p][1:]), deg=True, cov=True)
    uParams = unp.uarray(params, np.sqrt(np.diag(cov_matrix)))
    S = V / dict[p][0] * uParams[0]
    print(f'{p}: {uParams[0]:S} & {uParams[1]:S} & {S:S}\\\\')

    x = np.linspace(0,200,2000)

    fig, ax = plt.subplots()
    ax.errorbar(noms(dict['t'][1:]), noms(dict[p][1:]), xerr=stds(dict['t'][1:]), yerr=stds(dict[p][1:]), fmt='k+', ecolor='r', capsize=2, label=r'Messwerte mit Fehlerbalken')
    ax.plot(x, params[0]*x + params[1], label=r'Ausgleichsgerade')
    
    ax.set_xlabel(r't/\si{\second}')
    ax.set_ylabel(r'p/\si{\milli\bar}')
    ax.grid()
    ax.legend(loc='best')
    fig.tight_layout()
    fig.savefig('abb/dreh_leck' + p + '.pdf')