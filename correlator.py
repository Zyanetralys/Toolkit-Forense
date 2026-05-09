import json, argparse, sys, requests, socket, ipaddress

def resolve_dns(domain):
    try: return socket.gethostbyname(domain)
    except: return None

def reverse_dns(ip):
    try: return socket.gethostbyaddr(ip)[0]
    except: return None

def enrich(target):
    res = {"target": target, "type": "domain" if "." in target else "ip", "dns": None, "rdns": None}
    if res["type"] == "domain":
        res["dns"] = resolve_dns(target)
        if res["dns"]: res["rdns"] = reverse_dns(res["dns"])
    else:
        res["rdns"] = reverse_dns(target)
    return res

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("target")
    args = p.parse_args()
    print(json.dumps(enrich(args.target), indent=2))
