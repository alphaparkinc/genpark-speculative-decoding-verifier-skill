import random
from typing import List, Dict, Any

class SpeculativeDecodingVerifier:
    @staticmethod
    def verify(draft_tokens: List[int], draft_probs: List[float], target_probs: List[float]) -> Dict[str, Any]:
        if len(draft_tokens) != len(draft_probs) or len(draft_tokens) != len(target_probs):
            return {"error": "Lengths of tokens, draft_probs, and target_probs must match"}
        accepted = []
        rej_idx = None
        for idx, (token, q, p) in enumerate(zip(draft_tokens, draft_probs, target_probs)):
            ratio = min(1.0, p / max(1e-9, q))
            if random.random() <= ratio:
                accepted.append(token)
            else:
                rej_idx = idx
                break
        total = len(draft_tokens)
        acc_count = len(accepted)
        alpha = acc_count / total if total > 0 else 0.0
        speedup = 1.0 + alpha * 1.65
        return {
            "total_drafted": total,
            "accepted_count": acc_count,
            "acceptance_rate": round(alpha, 4),
            "accepted_tokens": accepted,
            "rejected_at_index": rej_idx,
            "estimated_speedup_factor": round(speedup, 2)
        }

    @staticmethod
    def benchmark_verification() -> Dict[str, Any]:
        toks = [1045, 2023, 2003, 1037, 3042]
        qp = [0.88, 0.92, 0.79, 0.85, 0.65]
        tp = [0.94, 0.89, 0.81, 0.87, 0.72]
        return SpeculativeDecodingVerifier.verify(toks, qp, tp)
