import sys, json
from client import SpeculativeDecodingVerifier

def handle_jsonrpc(line):
    try:
        req = json.loads(line)
        req_id = req.get("id")
        method = req.get("method")
        if method == "initialize":
            return {"jsonrpc": "2.0", "id": req_id, "result": {"protocolVersion": "2024-11-05", "serverInfo": {"name": "genpark-speculative-decoding-verifier-skill", "version": "1.0.0"}, "capabilities": {"tools": {}}}}
        elif method == "tools/list":
            return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": [
                {"name": "verify_draft_tokens", "description": "Verify draft tokens against target probs.", "inputSchema": {"type": "object", "properties": {"draft_tokens": {"type": "array"}, "draft_probs": {"type": "array"}, "target_probs": {"type": "array"}}, "required": ["draft_tokens", "draft_probs", "target_probs"]}},
                {"name": "benchmark_verification", "description": "Run speculative decoding benchmark.", "inputSchema": {"type": "object", "properties": {}}}
            ]}}
        elif method == "tools/call":
            params = req.get("params", {})
            tool = params.get("name")
            args = params.get("arguments", {})
            if tool == "verify_draft_tokens":
                res = SpeculativeDecodingVerifier.verify(args.get("draft_tokens", []), args.get("draft_probs", []), args.get("target_probs", []))
            elif tool == "benchmark_verification":
                res = SpeculativeDecodingVerifier.benchmark_verification()
            else:
                return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}
    except Exception as e:
        return {"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": str(e)}}

def main():
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_jsonrpc(line.strip())), flush=True)

if __name__ == "__main__":
    main()
