# initialization
import matplotlib.pyplot as plt
import numpy as np

# importing Qiskit
from qiskit import IBMQ, BasicAer
from qiskit.providers.ibmq import least_busy
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute
import matplotlib.pyplot as plt

# import basic plot tools
from qiskit.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor

n = 3
s = "011"

# We need n qubits plus 1 ancilla, n classical bits to record the value of "s"
bv_circuit = QuantumCircuit(n+1, n)

# put ancilla into minus state 
# bv_circuit.x(n)
bv_circuit.h(n)

# or use a phase shift
bv_circuit.z(n)

# Apply hadamard on rest of input qubits
for i in range(n):
    bv_circuit.h(i)

# apply barrier 
bv_circuit.barrier()

# Oracle: inner product (CNOT operation from first and second qubit to the third qubit simulates inner product)
s = s[::-1] #reverse s to fit qiskit qubit ordering 
for q in range(n):
    if s[q] == '0':
        bv_circuit.i(q)
    else:
        bv_circuit.cx(q,n)

# apply barrier 
bv_circuit.barrier()

# apply hadamard gate to resulting qubit state from oracle 
for i in range(n):
    bv_circuit.h(i)

# measure 
for i in range(n):
    bv_circuit.measure(i,i)

# Run locally
# bv_circuit.draw(output="mpl")
# backend = BasicAer.get_backend('qasm_simulator')
# shots = 1024
# results = execute(bv_circuit, backend=backend, shots=shots).result()
# answer = results.get_counts()

# plot_histogram(answer)

# Run on IBM Q

IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q')
provider.backends()
backend = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits <= 5 and
                                   x.configuration().n_qubits >= 2 and
                                   not x.configuration().simulator and x.status().operational==True))
print("least busy backend: ", backend)

shots = 1024
job = execute(bv_circuit, backend=backend, shots=shots)

job_monitor(job, interval = 2)
results = job.result()
answer = results.get_counts()

plot_histogram(answer)
plt.show()