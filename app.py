from flask import Flask, render_template, request, redirect, url_for, flash
import subprocess
import os
import glob

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        print("request.form: ", request.form)
        ssid = request.form["ssid"]
        password = request.form["password"]
        action = request.form["submit"]   
        print("action: ", action)  
        if (len(ssid) > 0 and len(password) > 0 and action == "Update Wi-Fi Configuration") or action == "Remove Wi-Fi Configuration":
            try:
                update_netplan_config(ssid, password, action)
                flash("Wi-Fi configuration updated successfully.", "success")
            except Exception as e:
                flash(
                    f"Error updating Wi-Fi configuration: {str(e)}", "danger")
        else:
            flash(
                "Please provide a valid SSID and password (minimum 8 characters).", "danger")

    return render_template("index.html")


def get_wifi_interface():
    interfaces = glob.glob("/sys/class/net/*/wireless")
    if not interfaces:
        raise Exception("No Wi-Fi interface found.")
    return os.path.basename(os.path.dirname(interfaces[0]))


def update_netplan_config(ssid, password, action):
    wifi_interface = get_wifi_interface()
    if action == "Remove Wi-Fi Configuration" or len(ssid) == 0 or len(password) == 0:
        config = f"""network:
  version: 2
  renderer: networkd
""" 
    else: 
        config = f"""
network:
  version: 2
  renderer: networkd
  wifis:
    {wifi_interface}:
      dhcp4: yes
      dhcp6: yes
      access-points:
        "{ssid}":
          password: "{password}"
"""

    with open("/etc/netplan/01-netcfg.yaml", "w") as f:
        f.write(config)

    subprocess.run(["sudo", "netplan", "apply"], check=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5551, debug=True)
