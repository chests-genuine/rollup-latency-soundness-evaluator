#!/usr/bin/env python3
import argparse
import time
import json
from dataclasses import dataclass, asdict
from typing import Dict
from web3 import Web3


@dataclass
class RollupProfile:
    key: str
    family: str
    privacy_level: float       # 0–1
    proof_soundness: float     # 0–1
    throughput_capacity: float # 0–1
    overhead_cost: float       # 0–1


PROFILES: Dict[str, RollupProfile] = {
    "aztec": RollupProfile(
        key="aztec",
        family="zk privacy rollup",
        privacy_level=0.92,
        proof_soundness=0.84,
        throughput_capacity=0.63,
        overhead_cost=0.41,
    ),
    "zama": RollupProfile(
        key="zama",
        family="FHE compute rollup",
        privacy_level=0.88,
        proof_soundness=0.91,
        throughput_capacity=0.47,
        overhead_cost=0.72,
    ),
    "soundness": RollupProfile(
        key="soundness",
        family="formal verification L2",
        privacy_level=0.55,
        proof_soundness=0.99,
        throughput_capacity=0.75,
        overhead_cost=0.28,
    ),
}


def score_rollup(profile: RollupProfile, latency_ms: float) -> Dict:
    privacy = profile.privacy_level * 0.35
    soundness = profile.proof_soundness * 0.40
    throughput = profile.throughput_capacity * 0.20
    overhead_penalty = profile.overhead_cost * 0.25

    latency_penalty = min(0.20, latency_ms / 2000)

    final = privacy + soundness + throughput - overhead_penalty - latency_penalty

    return {
        "rollup": profile.key,
        "family": profile.family,
        "latencyMs": round(latency_ms, 2),
        "finalScore": round(final, 4),
    }


def measure_rpc_latency(rpc: str) -> float:
    w3 = Web3(Web3.HTTPProvider(rpc, request_kwargs={"timeout": 10}))
    t0 = time.time()
    try:
        _ = w3.eth.block_number
    except Exception:
        return 9999.0
    return (time.time() - t0) * 1000


def main():
    p = argparse.ArgumentParser(description="Rollup soundness + latency evaluator.")
    p.add_argument("--rpc", required=True, help="Ethereum RPC endpoint URL.")
    p.add_argument("--model", choices=list(PROFILES.keys()), default="aztec")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    latency = measure_rpc_latency(args.rpc)
    profile = PROFILES[args.model]
    result = score_rollup(profile, latency)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Rollup Model: {result['rollup']} ({result['family']})")
        print(f"Observed RPC Latency: {result['latencyMs']} ms")
        print(f"Final Score: {result['finalScore']}")


if __name__ == "__main__":
    main()
