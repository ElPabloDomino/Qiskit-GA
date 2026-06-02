#počet qubitů
import time
import clifford as cl
import numpy as np
n=2
layout, blades = cl.Cl(2*n, 0)
# g-basis
g = [blades[f'e{i+1}'] for i in range(2*n)]

# witt basis
f = []
f_dag = []
for i in range(n):
    f.append((1/2)*(g[i]-1j*g[i+n]))
    f_dag.append((1/2)*(g[i]+1j*g[i+n]))

I=1
I_dag=1
#idempotent 
for i in range(n):
    I*=f[i]*f_dag[i]
    I_dag*=f[n-i-1]*f_dag[n-i-1]
#states
qubit=[]
qubit_dags=[]

for i in range (2**n):
    l=1
    #qubit states
    bin_i=bin(i)[2:].zfill(n)
    for idx, bit in enumerate(bin_i):
        if bit=='1':
            l*=f_dag[idx]
    q=l*I
    qubit.append(q)
    l=1
    #dag qubit states
    for idx, bit in enumerate(bin_i):
        if bit=='1':
            l*=f[idx]
    q_dag=I_dag*l
    qubit_dags.append(q_dag)


# Pauli matrices
def X(m):
    return f_dag[m] + f[m]
def Y(m):
    return 1j*f_dag[m] - 1j*f[m]
def Z(m):
    return f[m]*f_dag[m] - f_dag[m]*f[m]

# Identity
def id(m):
    return 1

# C_not gate
def C_not():
    return (f[0]*f_dag[0]-f_dag[0]*f[0]*(f_dag[1]+f[1]))

# Hadamard gate
def H(m):
    return (1/np.sqrt(2)) * (X(m) + Z(m))

def measure(state):
    if state==1:
        return f[0]*f_dag[0]*id(1)*state
    if state==2:
        return id(0)*f[1]*f_dag[1]*state

#Uf matrix for constant function
U_f_constant=X(0)*id(1)
#Uf matrix for balanced function
U_f_balanced=C_not()

def deutsch_algorithm_GA():
    quantum_state=qubit[0]
    
    quantum_state=id(0)*X(1)*quantum_state
    if quantum_state==qubit[1]:
        print("|0>|1>")
        
    quantum_state=H(0)*H(1)*quantum_state
    if quantum_state==(1/2)*(qubit[0]-qubit[1]+qubit[2]-qubit[3]):
        print("H|0>H|1>")
    
    # For balanced function use U_f_balanced
    quantum_state=U_f_constant*quantum_state
    
    quantum_state=H(0)*id(1)*quantum_state
    
    quantum_state_after_measurement=measure(1)*quantum_state
    if quantum_state==quantum_state_after_measurement:
        print("funkce je konstantní")
    if (quantum_state_after_measurement==0):
        print("funkce je vyvážená")
    print(quantum_state)
# pravděpodobnosti měření
    p_00 = abs(2**n * (qubit_dags[0] * quantum_state).value[0])**2
    p_01 = abs(2**n * (qubit_dags[1] * quantum_state).value[0])**2
    p_10 = abs(2**n * (qubit_dags[2] * quantum_state).value[0])**2
    p_11 = abs(2**n * (qubit_dags[3] * quantum_state).value[0])**2
    print(f"pravděpodobnost stavu |00> je {p_00}, |01> je {p_01}, |10> je {p_10}, |11> je {p_11}")
    
start = time.perf_counter()
deutsch_algorithm_GA()
end = time.perf_counter()

print(f"⏱️ Doba běhu algoritmu: {end - start:.6f} sekund")
