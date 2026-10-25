"""Direct client for the Meta XR Unity MCP bridge (use when the MCP server drops out of a Claude session).

Usage (from the project root):
    python -I Tools/unity_bridge.py list
    python -I Tools/unity_bridge.py CompilationTools '{"method":"GetCompilationErrors"}'
    python -I Tools/unity_bridge.py UIVerificationTools '{"method":"ExecuteMenuItem","menuPath":"CSER/Build All Scenes (story mode)"}'

The bridge URL and bearer token are read from ~/.claude.json (mcpServers -> meta-xr-unity-runtime),
so no secret is stored in this repository.
"""
import json
import os
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")


def bridge_config():
    cfg = json.load(open(os.path.expanduser("~/.claude.json"), encoding="utf-8"))
    for proj in cfg.get("projects", {}).values():
        srv = proj.get("mcpServers", {}).get("meta-xr-unity-runtime")
        if srv:
            return srv["url"], srv.get("headers", {}).get("Authorization", "")
    raise SystemExit("meta-xr-unity-runtime not found in ~/.claude.json")


URL, TOKEN = bridge_config()


def post(body, sid=None):
    headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream", "Authorization": TOKEN}
    if sid:
        headers["Mcp-Session-Id"] = sid
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers=headers)
    with urllib.request.urlopen(req, timeout=600) as r:
        raw = r.read().decode("utf-8", "replace")
        new_sid = r.headers.get("Mcp-Session-Id")
    if "data:" in raw:
        datas = [l[5:].strip() for l in raw.splitlines() if l.startswith("data:")]
        raw = datas[-1] if datas else ""
    return (json.loads(raw) if raw.strip() else None), new_sid


def session():
    _, sid = post({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                   "params": {"protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "cser", "version": "1"}}})
    try:
        post({"jsonrpc": "2.0", "method": "notifications/initialized"}, sid)
    except Exception:
        pass
    return sid


if __name__ == "__main__":
    tool = sys.argv[1]
    args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    sid = session()
    if tool == "list":
        res, _ = post({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, sid)
        print([t["name"] for t in res["result"]["tools"]])
    else:
        res, _ = post({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": tool, "arguments": args}}, sid)
        out = res.get("result", res)
        for c in out.get("content", []) if isinstance(out, dict) else []:
            print(c.get("text", ""))
