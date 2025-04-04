from flask import Flask, request, jsonify, render_template
import subprocess
import re

app = Flask(__name__)

def get_mac(ip):
    try:
        # Run ARP command
        result = subprocess.run(["arp", "-a"], capture_output=True, text=True)
        lines = result.stdout.split("\n")
        for line in lines:
            if ip in line:
                mac_match = re.search(r"([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}", line)
                if mac_match:
                    return mac_match.group(0)
    except Exception as e:
        print(f"Error getting MAC: {e}")
    return "Unknown"

def get_fqdn(ip):
    try:
        # Run nslookup command
        result = subprocess.run(["nslookup", ip], capture_output=True, text=True)
        fqdn = re.search(r"Name:\s+(.+)", result.stdout)
        return fqdn.split('.keystone')[0]
    except Exception as e:
        print(f"Error getting Hostname: {e}")
    return "Unknown"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_info")
def get_device_info():
    visitor_ip = request.remote_addr  # Get visitor's IP from request
    mac_address = get_mac(visitor_ip)
    hostname = get_fqdn(visitor_ip)
    return jsonify({"ip": visitor_ip, "mac": mac_address, "hostname": hostname})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
