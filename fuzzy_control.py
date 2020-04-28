import math
import numpy as np
import matplotlib.pyplot as plt


import skfuzzy as fuzz
from skfuzzy import control as ctrl

e = ctrl.Antecedent(np.arange(-50, 51, 1), 'err')
de = ctrl.Antecedent(np.arange(-20, 21, 1), 'derr')
u = ctrl.Consequent(np.arange(0, 11, 1), 'acc')

e['Neg'] = fuzz.trimf(e.universe, [-50, -50, 0])
e['Zer'] = fuzz.trimf(e.universe, [-50, 0, 50])
e['Pos'] = fuzz.trimf(e.universe, [0, 50, 50]) 

de['Neg'] = fuzz.trimf(de.universe, [-20, -20, 0])
de['Zer'] = fuzz.trimf(de.universe, [-20, 0, 20])
de['Pos'] = fuzz.trimf(de.universe, [0, 20, 20]) 

u['Low'] = fuzz.trapmf(u.universe, [0, 0, 3, 7])
u['Hig'] = fuzz.trapmf(u.universe, [3, 7, 10, 10])

"""
# görselleştirme
e.view()
de.view()
u.view()
"""

rule1 = ctrl.Rule(e['Pos'] & de['Neg'], u['Hig'])
rule2 = ctrl.Rule(e['Pos'] & de['Zer'], u['Hig'])
rule3 = ctrl.Rule(e['Pos'] & de['Pos'], u['Hig'])
rule4 = ctrl.Rule(e['Zer'], u['Low'])
rule5 = ctrl.Rule(e['Neg'], u['Low'])

altitude_ctrl = ctrl.ControlSystem([
    rule1, rule2, rule3, rule4, rule5
])


altitude_sim = ctrl.ControlSystemSimulation(altitude_ctrl)
ref = 50
h0 = 0
step = 30
last_error = 0

sys_model = lambda x: 0.1*math.pow(x, 2)

output = [h0]
for i in range(step):
    last_fb = output[i]
    error = ref - last_fb
    derror = error - last_error
    altitude_sim.input['err'] = error
    altitude_sim.input['derr'] = derror 
    altitude_sim.compute()
    x = altitude_sim.output['acc']
    output.append(sys_model(x) + last_fb)
    last_error = error

print(output)

plt.axhline(ref, color = 'r', label = 'referans-degeri')
plt.plot(range(step+1), output, 'b', marker='o', label = 'irtifa')
plt.xlabel('zaman')
plt.ylabel('cikis')
plt.legend()
plt.show()
