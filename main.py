import requests
import json
import subprocess
from pathlib import Path

# لینک‌های رسمی Cloudflare برای IPv4 و IPv6
URLS = {
    "IPv4": "https://www.cloudflare.com/ips-v4",
    "IPv6": "https://www.cloudflare.com/ips-v6"
}

OUTPUT_FILE = Path("cloudflare_ip_ranges.json")

def fetch_cloudflare_ips():
    all_ips = {}
    for ip_type, url in URLS.items():
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            ips = response.text.strip().splitlines()
            all_ips[ip_type] = ips
            print(f"[+] {ip_type} fetched: {len(ips)} IPs")
        except Exception as e:
            print(f"[!] Failed to fetch {ip_type}: {e}")
            all_ips[ip_type] = []
    return all_ips

def save_ips_to_file(ip_data):
    with open(OUTPUT_FILE, "w") as f:
        json.dump(ip_data, f, indent=4)
    print(f"[+] Saved IP ranges to {OUTPUT_FILE}")

def git_commit_push():
    try:
        subprocess.run(["git", "add", str(OUTPUT_FILE)], check=True)
        subprocess.run(["git", "commit", "-m", "Update Cloudflare IP ranges"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("[+] Changes pushed to GitHub")
    except subprocess.CalledProcessError as e:
        print(f"[!] Git operation failed: {e}")

if __name__ == "__main__":
    ip_data = fetch_cloudflare_ips()
    save_ips_to_file(ip_data)
    
    # اگر میخوای GitHub آپدیت شود، uncomment کن
    # git_commit_push()
