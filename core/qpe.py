import numpy as np
from core.qft import build_inverse_qft
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import Gate

def build_qpe(t_qubits : int, unitary_gate : Gate, state_prep_circ : QuantumCircuit | None = None) -> QuantumCircuit:
    qr = QuantumRegister(t_qubits, name="counting") # q_0 -> q_t-1
    
    num_target = unitary_gate.num_qubits
    qtarget = QuantumRegister(num_target, name="target") #bit target ở vị trí đầu bên trái q_t
    
    qc = QuantumCircuit(qr, qtarget, name="QPE")
    
    if state_prep_circ is not None:
        qc.compose(state_prep_circ, qubits=qtarget, front=False, inplace=True)
    else:
        qc.x(qtarget)
        
    qc.h(qr)
    
    curr_unitary_gate = unitary_gate
    for i in range(t_qubits):
        ctrl_gate = curr_unitary_gate.control()
        qc.append(ctrl_gate, [qr[i], qtarget[0]])
        
        curr_unitary_gate = curr_unitary_gate.power(2)
    
    inv_qft = build_inverse_qft(t_qubits)
    qc.compose(inv_qft, qubits=qr, inplace=True, front=False)
    return qc
