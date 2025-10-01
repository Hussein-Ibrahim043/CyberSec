import os, sys
import time
import requests
from rich.prompt import Prompt, IntPrompt
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

# === CONFIG ===
API_KEY = "509c9faa95dc43c7dc957229e6f4e079888451af0d3c98b0c1a67776e4dc0cff"  # <-- Replace with your VirusTotal API key
VT_FILE_SCAN_URL = "https://www.virustotal.com/api/v3/files"
VT_REPORT_URL = "https://www.virustotal.com/api/v3/analyses/{}"
VT_URL_SCAN = "https://www.virustotal.com/api/v3/urls"
VT_URL_REPORT = "https://www.virustotal.com/api/v3/analyses/{}"

console = Console()

def banner():
    console.print(Panel.fit(r'''[bold blue]
██╗   ██╗████████╗     █████╗ ███╗   ██╗████████╗██╗      ██╗   ██╗██╗██████╗ ██╗   ██╗███████╗
██║   ██║╚══██╔══╝    ██╔══██╗████╗  ██║╚══██╔══╝██║      ██║   ██║██║██╔══██╗██║   ██║██╔════╝
██║   ██║   ██║       ███████║██╔██╗ ██║   ██║   ██║█████╗██║   ██║██║██████╔╝██║   ██║███████╗
╚██╗ ██╔╝   ██║       ██╔══██║██║╚██╗██║   ██║   ██║╚════╝╚██╗ ██╔╝██║██╔══██╗██║   ██║╚════██║
 ╚████╔╝    ██║       ██║  ██║██║ ╚████║   ██║   ██║       ╚████╔╝ ██║██║  ██║╚██████╔╝███████║
  ╚═══╝     ╚═╝       ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝        ╚═══╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
                                                                                               
[/bold blue]'''), style="bold")


# ===================== FILE SCAN =====================
def upload_file(file_path: str) -> str:
    headers = {"x-apikey": API_KEY}
    files = {"file": (os.path.basename(file_path), open(file_path, "rb"))}

    console.print(f"[cyan]📤 Uploading file: [white]{file_path}[/white][/cyan]")
    response = requests.post(VT_FILE_SCAN_URL, headers=headers, files=files)
    if response.status_code != 200:
        console.print(f"[red]❌ Error uploading file: {response.text}[/red]")
        return None
    
    analysis_id = response.json()["data"]["id"]
    console.print(f"[green]✅ File uploaded.\n🆔 Analysis ID: {analysis_id}[/green]")
    return analysis_id


# ===================== URL SCAN =====================
def scan_url(target_url: str) -> str:
    headers = {"x-apikey": API_KEY}
    data = {"url": target_url}

    console.print(f"[cyan]🌐 Submitting URL: [white]{target_url}[/white][/cyan]")
    response = requests.post(VT_URL_SCAN, headers=headers, data=data)
    if response.status_code != 200:
        console.print(f"[red]❌ Error submitting URL: {response.text}[/red]")
        return None
    
    analysis_id = response.json()["data"]["id"]
    console.print(f"[green]✅ URL submitted.\n🆔 Analysis ID: {analysis_id}[/green]")
    return analysis_id


# ===================== REPORT FETCH =====================
def get_report(analysis_id: str):
    headers = {"x-apikey": API_KEY}
    url = VT_REPORT_URL.format(analysis_id)

    with Progress(
        SpinnerColumn(),
        TextColumn("[yellow]{task.description}"),
        transient=False,
        console=console,
    ) as progress:
        task = progress.add_task("⏳ Waiting for VirusTotal analysis...", total=None)
        while True:
            response = requests.get(url, headers=headers)
            result = response.json()
            status = result["data"]["attributes"]["status"]

            if status == "completed":
                progress.update(task, description="[green]✅ Analysis completed!\n")
                break
            time.sleep(3)

    return result


# ===================== REPORT DISPLAY =====================
def display_report(report: dict):
    stats = report["data"]["attributes"]["stats"]
    malicious = stats.get("malicious", 0)
    suspicious = stats.get("suspicious", 0)
    undetected = stats.get("undetected", 0)
    harmless = stats.get("harmless", 0)

    verdict = (
        "[bold red]⚠️ Malicious content detected![/bold red]"
        if malicious > 0 else
        "[bold green]✅ No malicious content detected.[/bold green]"
    )

    table = Table(title="🛡️ VirusTotal Scan Report", header_style="bold cyan", style="bold white")
    table.add_column("Category", style="bold white", justify="left")
    table.add_column("Count", style="bold yellow", justify="center")

    table.add_row("🔴 Malicious", str(malicious))
    table.add_row("🟠 Suspicious", str(suspicious))
    table.add_row("🟢 Harmless", str(harmless))
    table.add_row("🚫 Undetected", str(undetected))

    console.print(Panel.fit(table, title="[bold red]🔍 Scan Results[/bold red]", border_style="blue"))
    console.print(f"\n{verdict}")


# ===================== MAIN MENU =====================
if __name__ == "__main__":
    try:
        print("\033c", end="")
        banner()
        while True:
            try:
                console.print(Panel.fit("Choose an option:", style="bold blue"))
                console.print("[bold] 1) Scan File\n 2) Scan URL\n 3) Exit\n[/bold]")
                choice = IntPrompt.ask("[bold]Select option[/bold]",choices=['1','2','3'])

                if choice == 1:
                    file_path = input("Enter the file path to scan: ").strip()
                    if not os.path.isfile(file_path):
                        console.print("[red][-] File not found![/red]")
                    else:
                        analysis_id = upload_file(file_path)
                        if analysis_id:
                            report = get_report(analysis_id)
                            display_report(report)

                elif choice == 2:
                    target_url = input("Enter the URL to scan: ").strip()
                    analysis_id = scan_url(target_url)
                    if analysis_id:
                        report = get_report(analysis_id)
                        display_report(report)
                elif choice == 3:
                    console.print("\n[yellow]Exiting VT Anti Virus CLI 👋[/yellow]")
                    print("\033c", end="")
                    sys.exit()
                    
            except KeyboardInterrupt:
                console.print("[bold red]\n[-] Key Interrupt : [ CTRL + C ] Pressed ![/bold red]")
                sys.exit()
    except Exception as e:
        print("[bold red]Execution corrupt occur[/bold red]")
    except KeyboardInterrupt:
        console.print("[bold red]\n[-] Key Interrupt : [ CTRL + C ] Pressed[/bold red]")
        sys.exit()

    	#print("\033c", end="")
