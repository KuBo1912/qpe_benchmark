import numpy as np
from core.qpe import build_qpe
from qiskit.circuit import Gate
from qiskit.circuit.library import TGate, PhaseGate
import qiskit.quantum_info as qi
from qiskit_aer import AerSimulator
from qiskit import ClassicalRegister

import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram

def get_probs(t_qubits : int, unitary_gate : Gate) -> dict:
    qc  = build_qpe(t_qubits, unitary_gate, None)

    psi = qi.Statevector(qc)
    probs = psi.probabilities_dict(qargs=range(t_qubits))
    
    return probs


def estimate_phase(t_qubits : int, unitary_gate : Gate) -> float :
    qc  = build_qpe(t_qubits, unitary_gate, None)
    cr = ClassicalRegister(t_qubits)

    aer_simulation = AerSimulator()

    qc_measure = qc.copy()
    qc_measure.add_register(cr)
    qc_measure.measure(qc_measure.qubits[:t_qubits], cr) # chỉ đo target qubits 

    result = aer_simulation.run(qc_measure.decompose(), shots=1024).result()
    counts = result.get_counts() #dict
    
    best_res_str = max(counts, key=counts.get)
    best_res_Oct = int(best_res_str, 2)
    phase_estimate = best_res_Oct / 2**t_qubits
    
    return phase_estimate


if __name__ == "__main__":
    test_cases = [
        (PhaseGate(np.pi * 2 * 1 /3),   1 / 3, 1, "Phase 1/3"),
        (PhaseGate(np.pi / 2),           0.25,  2, "S Gate"),
        (TGate(),                       0.125, 3, "T Gate"),
    ]
    
    fig, axes = plt.subplots(1, 3)
    
    for i, (gate, true_phase, t, name) in enumerate(test_cases):
        probs = get_probs(t, gate)
        est = estimate_phase(t, gate)
        
        plot_histogram(probs, ax=axes[i])
        
        status = "PASS" if np.isclose(est, true_phase) else "FAIL"
        axes[i].set_title(f"[{status}] {name}\ntrue_phase = {true_phase} | est_phase = {est}")

    plt.show()