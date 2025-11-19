# rollup-latency-soundness-evaluator

A lightweight evaluator that compares different Web3 rollup architectures through two dimensions:

1. **Cryptographic soundness** (inspired by formal verification approaches)  
2. **Observed RPC latency** (real-world performance)  

The tool blends characteristics of rollups inspired by **Aztec (zk privacy)**, **Zama (FHE compute)**, and **soundness-first L2 engineering**.


## Files in this repository

There are exactly two files:

- `app.py` — the script
- `README.md` — this documentation


## What the script does

Given an Ethereum RPC endpoint, the script:

1. Measures live RPC latency  
2. Selects a rollup model (aztec, zama, or soundness)  
3. Computes a combined *final score* using:  
   - privacy level  
   - soundness strength  
   - throughput capability  
   - overhead cost  
   - latency penalty  

The score is purely conceptual and meant to illustrate architecture trade-offs.


## Installation

Requirements:

- Python 3.8+
- `pip install web3`


## Usage

Run with a real RPC endpoint:

## Notes

- This evaluator is conceptual only.
- It does not interact with transactions or state.
- It is intended for researchers, rollup designers, and L2 comparison experiments.
- Extend the models or scoring weights as needed.
