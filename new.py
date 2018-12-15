import random
import numpy as np
from scipy.optimize import minimize

#Parameters
T = 30  #time span (days)
d = []  #demand (random, units per day)
for j in range(T):
    d.append(random.randint(0, 3)) 
RT = 1  # review time (days) - time between 2 placed orders
LT = 1  # lead time (days) - time that goes from when an order is placed to the moment it arrives
h = 1   # on-hand inventory cost (unit cost)
b = 5   # backorder cost (unit cost)
I0 = 1  # initial stock (units)
s = []  # target stock (units)
for j in range(T):
    s.append((RT+LT)*d[j]) 

#Variable Initialization
Qt = [0] * T    # quantity to order each day (units)
It = [0] * T    # on-hand inventory at the end of each day (units)
NIt = [0] * T   # net inventory at the start of each day (units) = (on-hand + in transit) inventory
Ip = [0] * T    # on-hand inventory (units) (It > 0)
Im = [0] * T    # backorder (units) (It < 0)

#Initial Values
It[0] = I0 - d[0]
NIt[0] = I0 
Qt[0] = 0

if (It[0] >= 0):
    Ip[0] = It[0]
    Im[0] = 0

elif (It[0] < 0):
    Ip[0] = 0
    Im[0] = -It[0]

#Counter
i=1

def objective (x):
    global Ip, Im
    if (It[i-1] - d[i] + Qt[i-LT]) >= 0:
        Ip[i] = x[2]
        Im[i] = 0
    else:
        Ip[i] = 0
        Im[i] = -x[2]
    return h*Ip[i]+b*Im[i]

    
def constraint1 (x):
    return x[0]

def constraint2 (x):
    if (NIt[i-1] < s[i-1]):
        return x[1] - NIt[i-1] + d[i-1] - x[0]
    else:
        return x[1] - NIt[i-1] + d[i-1]

def constraint3 (x):
    return x[2] - x[1] + d[i] + x[0] - Qt[i-LT]

def test(T):
    global i
    while i < T:
        x0 = [1, NIt[0], It[0]]
        con1 = {'type': 'ineq', 'fun': constraint1}
        con2 = {'type': 'eq', 'fun': constraint2}
        con3 = {'type': 'eq', 'fun': constraint3}
        cons = [con1, con2, con3]
        sol = minimize(objective, x0, constraints=cons)
        Qt[i] = round(sol.x[0], 0)
        NIt[i] = round(sol.x[1], 0)
        It[i] = round(sol.x[2], 0)
        i += 1
    return Qt, NIt, It

[Qt, NIt, It] = test(T)
print ('It = [%s]' % ', '.join(map(str, It)))
print ('NIt = [%s]' % ', '.join(map(str, NIt)))
print ('Qt = [%s]' % ', '.join(map(str, Qt)))
print ('d = [%s]' % ', '.join(map(str, d)))
print ('s = [%s]' % ', '.join(map(str, s)))

sum = 0
a = 0
while a < T:
    sum = sum + h*Ip[a]+b*Im[a]
    a += 1

print(sum)