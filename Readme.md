# Netplan Wi-Fi Configuration Web Interface

This application provides a simple web interface for modifying Wi-Fi configurations on netplan. Users can change the SSID and password, and the application will update the netplan configuration file and apply the changes.

## Requirements

- Python 3.6 or higher
- Flask

## Installation

1. Clone this repository or download the source files.

2. Install Flask using pip:

```bash
pip install Flask
````

## Setup the systemd service

1. Create a new file called `netplan-wifi-config.service` with the following content:

`````
[Unit]
Description=Netplan Wi-Fi Configuration Web Interface
After=network.target

[Service]
User=root
WorkingDirectory=/path/to/your/app
ExecStart=/usr/bin/python3 /path/to/your/app/app.py
Restart=always

[Install]
WantedBy=multi-user.target
`````

Make sure to replace `/path/to/your/app` with the actual path to your Flask application directory.

2. Copy the `netplan-wifi-config.service` file to the `/etc/systemd/system` directory:

````
sudo cp netplan-wifi-config.service /etc/systemd/system/
`````

3. Reload the systemd configuration:

`````
sudo systemctl daemon-reload
`````

4. Enable the service to start on boot:

````
sudo systemctl enable netplan-wifi-config.service
````

5. Start the service:

````
sudo systemctl start netplan-wifi-config.service
````

Now your Flask server will start automatically on system boot. You can check the status of the service using:

````
sudo systemctl status netplan-wifi-config.service
`````

## Application Structure

- `app.py`: The main Flask application file that handles the web interface and updates the netplan configuration.
- `templates/index.html`: The HTML template for the web interface.
- `README.md`: This documentation file.

## Notes

This application has been designed to work on systems using netplan for network configuration. Please ensure your system is using netplan before attempting to use this application.

Running the Flask app requires root privileges as it needs to modify the netplan configuration file and apply the changes. Make sure to take necessary security precautions when running any application with root privileges.

