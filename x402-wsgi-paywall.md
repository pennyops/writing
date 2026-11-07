---
title: "Sell your API for USDC: an x402 v2 paywall for plain Python WSGI (no SDK, ~50 lines)"
published: false
tags: api, python, web3, webdev
---

x402 sounds like it needs a framework. It doesn't. A server-side x402 paywall comes down to three steps:

1. With no payment attached, answer **402** and describe your price in a `PAYMENT-REQUIRED` header.
2. When the client retries with a `PAYMENT-SIGNATURE` header, ask a **facilitator** whether that signature is valid (`/verify`).
3. Ask the facilitator to **settle** it on-chain (`/settle`), then serve the response with a `PAYMENT-RESPONSE` header.

The facilitator submits the transaction, so your server never holds a private key or pays gas. Below is the whole thing for any WSGI app (Flask, Django, bare `wsgiref`), using only the standard library. It's the same logic my own paid endpoints run, cut down.

## The price object

```python
USDC_BASE = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
PAY_TO = "0xYourWalletAddressHere"

def requirements(url, amount_atomic, desc):
    return {"x402Version": 2, "error": "PAYMENT-SIGNATURE header is required",
            "resource": {"url": url, "description": desc, "mimeType": "application/json"},
            "accepts": [{"scheme": "exact", "network": "eip155:8453", "amount": str(amount_atomic),
                         "asset": USDC_BASE, "payTo": PAY_TO, "maxTimeoutSeconds": 120,
                         "extra": {"name": "USD Coin", "version": "2"}}]}
```

- `amount` is in atomic units. USDC has 6 decimals, so `1000` = $0.001.
- `network` uses the CAIP-2 format in v2 (`eip155:8453` = Base). v1 said `"base"`.
- `extra.name`/`extra.version` is the EIP-712 domain of USDC on Base. Get it wrong and every client signature fails verification.

## The paywall

```python
def paywall(environ, start_response, pr):
    def deny(msg):
        p = dict(pr, error=msg)
        start_response("402 Payment Required", [("Content-Type", "application/json"),
                                                ("PAYMENT-REQUIRED", b64(p))])
        return False, [json.dumps(p).encode()]
    sig = environ.get("HTTP_PAYMENT_SIGNATURE")
    if not sig: return deny(pr["error"])
    try:
        payload = json.loads(base64.b64decode(sig)); assert isinstance(payload, dict)
    except Exception:
        return deny("malformed PAYMENT-SIGNATURE")
    reqs = pr["accepts"][0]          # the server's own terms, never the client's copy
    acc = payload.get("accepted") or {}
    if any(acc.get(k) != reqs[k] for k in ("scheme", "network", "asset", "payTo", "amount")):
        return deny("payment does not match requirements")
    body = {"x402Version": 2, "paymentPayload": payload, "paymentRequirements": reqs}
    v = post("/verify", body)
    if not v.get("isValid"): return deny(v.get("invalidReason", "invalid"))
    s = post("/settle", body)
    if not s.get("success"): return deny(s.get("errorReason", "settle failed"))
    return True, b64(s)
```

The one line that matters most is `reqs = pr["accepts"][0]`. The client's payload echoes back the terms it says it accepted. Always send **your own** requirements to the facilitator. If you forward the client's copy, a client can "accept" an amount of 1 or a different `payTo`, and the facilitator will happily confirm that as valid.

The helpers and a route:

```python
FAC = "https://facilitator.payai.network"   # any facilitator exposing /verify and /settle

def b64(o): return base64.b64encode(json.dumps(o).encode()).decode()

def post(path, body):
    r = urllib.request.Request(FAC + path, json.dumps(body).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(r, timeout=30) as f: return json.load(f)

def app(environ, start_response):
    pr = requirements("https://example.com/paid/hello", 1000, "Hello for $0.001")
    ok, out = paywall(environ, start_response, pr)
    if not ok: return out
    start_response("200 OK", [("Content-Type", "application/json"), ("PAYMENT-RESPONSE", out)])
    return [json.dumps({"hello": "paid world"}).encode()]
```

## Test it without spending anything

Mock `post` and drive the WSGI app directly:

```python
calls = []
paywall_mod.post = lambda path, body: calls.append(path) or (
    {"isValid": True} if path == "/verify" else {"success": True, "transaction": "0xabc"})
```

My test covers four paths: no header (402 with a decodable `PAYMENT-REQUIRED`), garbage header, mismatched amount, and the happy path (`/verify` then `/settle`, then 200). Then do one real $0.001 payment against your deployed endpoint with a client. The [plain-Python client post](https://dev.to/pennyops/pay-an-x402-endpoint-from-plain-python-no-sdk-30-lines-5bem) does it in about 30 lines.

## v1 clients

Some clients still send v1 (`X-PAYMENT` header, `"network": "base"`, `maxAmountRequired`). If you want both, check `HTTP_X_PAYMENT` first and branch. Every renamed field is in my [v1 to v2 cheat sheet](https://dev.to/pennyops/x402-v1-to-v2-every-header-and-field-that-changed-migration-cheat-sheet-599b).

## The honest part

The code is the easy part. I run a dozen endpoints like this and they get plenty of handshakes and unpaid tool calls, but almost no payments ([numbers here](https://dev.to/pennyops/my-paid-x402-mcp-server-533-handshakes-in-a-day-0-tool-calls-4hn9)). If you build one, spend most of your effort on what the endpoint sells (data people can't easily get elsewhere) and on getting listed where agents look (the bazaar extension, 402index), not on the paywall.

---
*Written with AI assistance; code tested by the author.*
