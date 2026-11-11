import numpy as np
from qiskit import QuantumCircuit

def build_qft(n_qubits : int) -> QuantumCircuit:
    qc = QuantumCircuit(n_qubits, name="QFT")
    
    for i in range(n_qubits):
        qc.h(i)
        for j in range(i + 1 , n_qubits):
            qc.cp((2 * np.pi) / (2 ** (j - i + 1)), j, i)
    
    for i in range(n_qubits // 2):
        qc.swap(i, n_qubits - 1 - i)
    
    return qc

def build_inverse_qft(n_qubits : int ) -> QuantumCircuit:
    qc = QuantumCircuit(n_qubits, name="Inverse_QFT")
    
    for i in range(n_qubits // 2):
        qc.swap(i, n_qubits - 1 - i)
    
    for i in range(n_qubits - 1, -1, - 1):
        for j in range(n_qubits - 1, i, - 1):
            qc.cp(-(2 * np.pi) / (2 ** (j - i + 1)), j, i)
            
        qc.h(i)
    return qc