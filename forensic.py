import os, hashlib, json, argparse, glob, datetime

def hash_file(f):
    h = hashlib.sha256()
    with open(f, "rb") as fp:
        for chunk in iter(lambda: fp.read(8192), b""): h.update(chunk)
    return h.hexdigest()

def scan_dir(root, ext="*"):
    out = []
    for f in glob.glob(f"{root}/**/*.{ext}", recursive=True):
        stat = os.stat(f)
        out.append({
            "path": f, "size": stat.st_size,
            "created": datetime.datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "sha256": hash_file(f)
        })
    return out

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("path")
    p.add_argument("-e", "--ext", default="*")
    args = p.parse_args()
    print(json.dumps(scan_dir(args.path, args.ext), indent=2))
