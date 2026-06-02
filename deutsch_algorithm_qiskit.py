from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import time  # ⏱️ přidáno

# -------------------
# Orákulum pro DJ
# -------------------
def dj_oracle(case, n):
    oracle = QuantumCircuit(n+1)
    if case == "constant0":
        pass
    elif case == "constant1":
        oracle.x(n)
    elif case == "balanced":
        oracle.cx(0, n)
        oracle.cx(1, n)
    elif case == "practice_for_n":
        oracle.cx(3, n)
    elif case == "practice_for_n_modulo":
        for i in range(n):
            oracle.cx(i, n)
    return oracle

# -------------------
# Deutsch–Jozsa algoritmus
# -------------------
def deutsch_jozsa(case, n):
    qc = QuantumCircuit(n+1, n)
    qc.x(n)
    for qubit in range(n+1):
        qc.h(qubit)
    qc.append(dj_oracle(case, n), range(n+1))
    for qubit in range(n):
        qc.h(qubit)
    for i in range(n):
        qc.measure(i, i)
    return qc

# -------------------
# Spuštění simulace
# -------------------
simulator = Aer.get_backend("qasm_simulator")  # podporuje více qubitů efektivněji


for case in ["balanced"]:
    qc = deutsch_jozsa(case, 2)

    # ⏱️ Začátek měření
    start = time.perf_counter()

    tqc = transpile(qc, simulator)
    job = simulator.run(tqc, shots=1024)
    result = job.result()
    counts = result.get_counts()

    # ⏱️ Konec měření
    end = time.perf_counter()

    print(f"{case}: {counts}")
    print(f"⏱️ Celková doba běhu: {end - start:.6f} sekund\n")
