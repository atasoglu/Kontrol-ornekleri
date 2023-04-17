import math
import matplotlib.pyplot as plt
from pid import PID

# parametreler
ref = 50
Kpid = [0.25, 0.001, 0.0001]
dt = 1
h0 = 0
step = 30

# sistem modeli
sys_model = lambda x: 0.1 * math.pow(x, 2)

"""
# sistem modeli şu şekilde de tanımlanabilirdi:
def f(x):
    return 0.1*math.pow(x, 2)
sys_model = f
"""

ctrl = PID(ref, dt, sys_model, Kpid)

output = [h0]
for i in range(step):
    last_fb = output[-1]
    x = ctrl.step(last_fb)
    output.append(x + last_fb)
# print(output)


# görselleştirme
plt.axhline(ref, color="r", label="referans-degeri")
plt.plot(range(step + 1), output, "b", marker="o", label="irtifa")
plt.xlabel("zaman")
plt.ylabel("cikis")
plt.legend()
plt.show()
