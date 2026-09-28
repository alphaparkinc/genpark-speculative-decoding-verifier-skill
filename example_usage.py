from client import SpeculativeDecodingVerifier

def run_example():
    print("=== GenPark Speculative Decoding Verifier Example ===")
    tokens = [502, 1024, 789, 999]
    q = [0.85, 0.70, 0.60, 0.90]
    p = [0.95, 0.75, 0.50, 0.92]
    res = SpeculativeDecodingVerifier.verify(tokens, q, p)
    print("Accepted Tokens:", res["accepted_tokens"])
    print("Acceptance Rate:", res["acceptance_rate"])
    print("Speedup Factor:", res["estimated_speedup_factor"])

if __name__ == "__main__":
    run_example()
