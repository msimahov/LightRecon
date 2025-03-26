import requests
import socket
import threading
import queue
import time
import json
import csv
from datetime import datetime


class SubScanner:
    def __init__(self, target_domain, wordlist_path="subdomains.txt"):
        self.target_domain = target_domain.rstrip('.')
        self.wordlist_path = wordlist_path
        self.subdomains = set()
        self.results = {}
        self.port_queue = queue.Queue()
        self.common_ports = [21, 22, 23, 25, 80, 443, 3389, 8080]

    def load_wordlist(self):
        """Load subdomain wordlist from file"""
        try:
            with open(self.wordlist_path, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print("Wordlist not found. Using default small list.")
            return ['www', 'mail', 'ftp', 'test', 'dev', 'staging']

    def check_subdomain(self, subdomain):
        """Check if subdomain exists via DNS resolution"""
        full_domain = f"{subdomain}.{self.target_domain}"
        try:
            socket.gethostbyname(full_domain)
            self.subdomains.add(full_domain)
            return True
        except socket.gaierror:
            return False

    def enumerate_subdomains(self):
        """Enumerate subdomains using wordlist"""
        print(f"Starting subdomain enumeration for {self.target_domain}")
        wordlist = self.load_wordlist()
        threads = []

        for word in wordlist:
            t = threading.Thread(target=self.check_subdomain, args=(word,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        print(f"Found {len(self.subdomains)} subdomains")

    def scan_port(self, subdomain, port):
        """Scan a specific port on a subdomain"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((subdomain, port))
        sock.close()
        return port if result == 0 else None

    def scan_ports(self, subdomain):
        """Scan common ports for a subdomain"""
        open_ports = []
        for port in self.common_ports:
            result = self.scan_port(subdomain, port)
            if result:
                open_ports.append(result)
        return open_ports

    def run_full_scan(self):
        """Execute complete scan process"""
        # Step 1: Enumerate subdomains
        self.enumerate_subdomains()

        # Step 2: Scan ports for each subdomain
        print("Starting port scanning...")
        for subdomain in self.subdomains:
            open_ports = self.scan_ports(subdomain)
            self.results[subdomain] = {
                'open_ports': open_ports,
                'scanned_at': datetime.now().isoformat()
            }

    def save_report(self, format='json', output_file=None):
        """Save results in specified format"""
        if not output_file:
            output_file = f"scan_results_{self.target_domain}_{int(time.time())}"

        if format.lower() == 'json':
            with open(f"{output_file}.json", 'w') as f:
                json.dump(self.results, f, indent=4)

        elif format.lower() == 'csv':
            with open(f"{output_file}.csv", 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Subdomain', 'Open Ports', 'Timestamp'])
                for subdomain, data in self.results.items():
                    writer.writerow([subdomain, ','.join(map(str, data['open_ports'])), data['scanned_at']])

        elif format.lower() == 'markdown':
            with open(f"{output_file}.md", 'w') as f:
                f.write(f"# Scan Results for {self.target_domain}\n\n")
                for subdomain, data in self.results.items():
                    f.write(f"## {subdomain}\n")
                    f.write(f"- Open Ports: {', '.join(map(str, data['open_ports']))}\n")
                    f.write(f"- Scanned At: {data['scanned_at']}\n\n")

        print(f"Report saved as {output_file}.{format.lower()}")


def main():
    target = input("Enter target domain example.com: ")
    scanner = SubScanner(target)

    # Run the scan
    scanner.run_full_scan()

    # Save results in all formats
    scanner.save_report('json')
    scanner.save_report('csv')
    scanner.save_report('markdown')


if __name__ == "__main__":
    main()