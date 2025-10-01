#!/usr/bin/env python3
import socket
import ssl
import re
import sys
import time
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

import pyfiglet
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.progress import track

console = Console()

# Banner
def banner():
    title = pyfiglet.figlet_format("Port Scanner", font="slant")
    console.print(f"[bold green]{title}[/bold green]")
    console.print("[yellow]>> Port Scanning Tool (Multi-threaded + Banner Grab)[/yellow]\n")


def detect_service_version(ip, port, timeout=1.0):
    """
    Try to detect a service banner/version on a TCP port.
    Returns a short string (e.g. "HTTP Server: nginx/1.18") or None.
    """
    probe_map = {
        80: b"HEAD / HTTP/1.0\r\nHost: localhost\r\n\r\n",
        443: b"HEAD / HTTP/1.0\r\nHost: localhost\r\n\r\n",
        21: b"\r\n",
        22: b"\r\n",
        25: b"EHLO example.com\r\n",
        110: b"USER test\r\n",
        143: b"\r\n",
        3306: b"\x00",
    }

    # quick banner grab (plain TCP)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip, port))

            probe = probe_map.get(port)
            if probe:
                try:
                    s.sendall(probe)
                except Exception:
                    pass

            try:
                data = s.recv(4096)
            except socket.timeout:
                data = b""

            banner = data.decode(errors="ignore").strip()
            if banner:
                banner = re.sub(r"\s+", " ", banner)[:300]
                # HTTP Server header
                m = re.search(r"Server:\s*([^\r\n]+)", banner, re.I)
                if m:
                    return f"HTTP Server: {m.group(1).strip()}"
                # SSH banner
                if banner.startswith("SSH-"):
                    return banner.split("\n")[0]
                # Generic useful banner
                return banner[:200]
    except Exception:
        pass

    # Try SSL/TLS handshake and cert subject / Server header via HTTPS
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        with socket.create_connection((ip, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=ip) as ssock:
                cert = ssock.getpeercert()
                # Try to extract commonName from cert subject
                subj = None
                if cert and "subject" in cert:
                    for item in cert["subject"]:
                        for key, value in item:
                            if key.lower() in ("commonName", "cn"):
                                subj = value
                                break
                        if subj:
                            break
                if subj:
                    return f"Certificate CN={subj}"

                # If TLS, try a HTTP HEAD to fetch Server header
                try:
                    ssock.sendall(b"HEAD / HTTP/1.0\r\nHost: localhost\r\n\r\n")
                    data = ssock.recv(4096).decode(errors="ignore")
                    m = re.search(r"Server:\s*([^\r\n]+)", data, re.I)
                    if m:
                        return f"HTTPS Server: {m.group(1).strip()}"
                except Exception:
                    pass
    except Exception:
        pass

    return None


# single-port scan (returns tuple on open or None)
def scan_port(ip, port, timeout=0.5):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((ip, port))
            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except OSError:
                    service = "Unknown"

                # try to get version/banner (slightly larger timeout)
                try:
                    version = detect_service_version(ip, port, timeout=max(0.8, timeout))
                except Exception:
                    version = None

                if version:
                    service_display = f"{service} ({version})"
                else:
                    service_display = service

                return (port, "Open", service_display)
    except Exception:
        return None
    return None


# start scan using threads and safe collection of results
def start_scan(target, port_start, port_end, timeout=0.5, workers=100):
    # resolve
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        console.print(f"[bold red]❌ ERROR: Unable to resolve {target}[/bold red]")
        return []

    console.print(f"\n[cyan]🔍 Port Scanner Report for [bold]{target}[/bold] ({target_ip})[/cyan]\n")
    console.print(
        Panel.fit(
            f"Scanning Ports: {port_start} - {port_end}   timeout={timeout}s   threads={workers}",
            border_style="blue",
        )
    )

    ports = range(port_start, port_end + 1)
    open_ports = []

    # Use ThreadPoolExecutor for concurrency
    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_port = {executor.submit(scan_port, target_ip, p, timeout): p for p in ports}

        # Use a simple track progress bar while futures complete
        for future in track(
            as_completed(future_to_port), total=(port_end - port_start + 1), description="[green]Scanning..."
        ):
            try:
                res = future.result()
                if res:
                    open_ports.append(res)
            except Exception:
                # ignore single task exceptions, continue scanning others
                continue

    # sort results by port number
    open_ports.sort(key=lambda x: x[0])

    # print table
    table = Table(show_header=True, header_style="bold green")
    table.add_column("Port", justify="center", style="cyan", no_wrap=True)
    table.add_column("Status", style="yellow", justify="center")
    table.add_column("Service", style="magenta")

    if open_ports:
        for port, status, service in open_ports:
            table.add_row(str(port), status, service)
    else:
        console.print("[bold yellow]No open ports found in the given range.[/bold yellow]\n")

    console.print("\n[bold green]✅ Scan Complete![/bold green]\n")
    console.print(table)

    return open_ports


def export_csv(open_ports, filename):
    try:
        with open(filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["port", "status", "service"])
            for row in open_ports:
                writer.writerow(row)
        console.print(f"[bold green]Saved results to {filename}[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Failed to save CSV: {e}[/bold red]")


def main():
    print("\033c", end="")  # clear terminal
    banner()

    # common top 1000 ports sample (you can replace with actual list if you prefer)
    top_1000_sample = "1-1024"

    while True:
        console.print(Panel.fit("Choose an option:", style="bold", border_style="blue"))
        console.print(" [1] [bold]Scan top common ports (1-1024)[/bold]")
        console.print(" [2] [bold]Scan custom port range[/bold]")
        console.print(" [3] [bold]Exit[/bold]\n")

        choice = IntPrompt.ask("[bold cyan]Enter choice[/bold cyan]", choices=["1", "2", "3"])
        if choice == 3:
            console.print("\n[yellow]👋 Exiting Port Scanner... Goodbye![/yellow]\n")
            print("\033c", end="")
            sys.exit()

        target = Prompt.ask("[bold green]> Enter Target IP/Domain[/bold green]")

        # default parameters
        timeout = Prompt.ask("[bold green]> Enter timeout in seconds (default 0.5)[/bold green]", default="0.5")
        try:
            timeout = float(timeout)
        except ValueError:
            console.print("[red]Invalid timeout, using 0.5s[/red]")
            timeout = 0.5

        workers = Prompt.ask("[bold green]> Enter number of threads/workers (default 100)[/bold green]", default="100")
        try:
            workers = int(workers)
            if workers < 1:
                raise ValueError
        except ValueError:
            console.print("[red]Invalid workers, using 100[/red]")
            workers = 100

        if choice == 1:
            start, end = map(int, top_1000_sample.split("-"))
        else:
            # custom range
            pr = Prompt.ask("[bold green]> Enter Port Range (e.g. 1-1000)[/bold green]", default="1-1024")
            try:
                start, end = map(int, pr.split("-"))
                if start < 1:
                    start = 1
                if end < start:
                    raise ValueError
            except Exception:
                console.print("[red]⚠ Invalid range. Using default (1-1024)[/red]")
                start, end = 1, 1024

        # run scan
        open_ports = start_scan(target, start, end, timeout=timeout, workers=workers)

        # offer export
        if open_ports:
            save = Prompt.ask("[bold cyan]> Save results to CSV? (y/n)[/bold cyan]", choices=["y", "n"], default="n")
            if save == "y":
                default_name = f"{target.replace('.', '_')}_ports_{start}-{end}.csv"
                filename = Prompt.ask("[bold green]> Enter filename[/bold green]", default=default_name)
                export_csv(open_ports, filename)

        # small pause before returning to menu
        time.sleep(0.5)


if __name__ == "__main__":
    main()
