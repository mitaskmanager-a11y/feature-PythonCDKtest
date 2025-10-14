import sys, json, platform, pathlib

def main():
    info = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "cwd": str(pathlib.Path('.').resolve())
    }
    print("Smoke test OK")
    print(json.dumps(info, indent=2))

if __name__ == "__main__":
    main()
