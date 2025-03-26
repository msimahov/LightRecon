# ⚡🔍 LightRecon - Subdomain and Port Scanner

## Overview
This project is a simple yet powerful subdomain enumeration and port scanning tool written in Python. It discovers subdomains using a wordlist and scans for common open ports, generating reports in JSON, CSV, and Markdown formats.

## Features
- 🔄 Fast multi-threaded subdomain enumeration
- 🔍 Scans common ports (21, 22, 23, 25, 80, 443, 3389, 8080)
- 📄 Saves results in JSON, CSV, and Markdown formats
- 📂 Works with a custom wordlist
- 🚀 Lightweight and easy to use

## Installation
### Prerequisites
- Python 3.x

### Clone the Repository
```sh
git clone https://github.com/msimahov/LightRecon.git
cd lightrecon
```

### Install Dependencies (if any)
No external dependencies are required.

## Usage
Run the script and enter a target domain:
```sh
python lightrecon.py
```

### Example Output
```
Enter target domain (e.g., example.com): example.com
Starting subdomain enumeration for example.com
Found 3 subdomains
Starting port scanning...
Report saved as scan_results_example_com_1711522231.json
Report saved as scan_results_example_com_1711522231.csv
Report saved as scan_results_example_com_1711522231.md
```

### Example Report (Markdown)
```md
# Scan Results for example.com

## www.example.com
- Open Ports: 80, 443
- Scanned At: 2025-03-26T12:34:56
```

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.


