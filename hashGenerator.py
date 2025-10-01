from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import track
from rich.prompt import Prompt, IntPrompt
from rich.status import Status
import hashlib, time, sys, pyfiglet, os


console = Console()

#Banner 
def banner():
    console.print(Panel.fit(r"""[bold green]██╗  ██╗ █████╗ ███████╗██╗  ██╗    ████████╗ ██████╗  ██████╗ ██╗     
██║  ██║██╔══██╗██╔════╝██║  ██║    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
███████║███████║███████╗███████║       ██║   ██║   ██║██║   ██║██║     
██╔══██║██╔══██║╚════██║██╔══██║       ██║   ██║   ██║██║   ██║██║     
██║  ██║██║  ██║███████║██║  ██║       ██║   ╚██████╔╝╚██████╔╝███████╗
╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝[/bold green]"""), style="bold")

def generate_hashes(data: str):
    hashes = {
        "MD5": hashlib.md5(data.encode()).hexdigest(),
        "SHA1": hashlib.sha1(data.encode()).hexdigest(),
        "SHA224": hashlib.sha224(data.encode()).hexdigest(),
        "SHA256": hashlib.sha256(data.encode()).hexdigest(),
        "SHA384": hashlib.sha384(data.encode()).hexdigest(),
        "SHA512": hashlib.sha512(data.encode()).hexdigest()            
    }

    return hashes

def generate_file_hashes(file_path: str):
    """Generate hashes for file contents."""
    hashes = {
        "MD5": hashlib.md5(),
        "SHA1": hashlib.sha1(),
        "SHA224": hashlib.sha224(),
        "SHA384": hashlib.sha384(),
        "SHA512": hashlib.sha512(),            
    }

    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                for h in hashes.values():
                    h.update(chunk)
    except FileNotFoundError:
        return f"[*] File not found: {file_path}\n"

    return {name: h.hexdigest() for name, h in hashes.items()}    



def display_hashes(hashes):
    if isinstance(hashes, str):
        console.print(f"[bold red]{hashes}[/bold red]")
        return
    
    table = Table()
    table.add_column("Algorithm", justify="center", style="cyan", no_wrap=True)
    table.add_column("Hash Value", style="yellow")

    for algo, h in hashes.items():
        table.add_row(algo, h)

    console.print(table)


def main():
    print("\033c", end="")
    banner()
    while True:
        console.print(Panel.fit("Choose an option:", style="bold", border_style="blue"))
        console.print(" [1] [bold]Generate Hashes for Text[/bold]")
        console.print(" [2] [bold]Generate Hashes for File[/bold]")
        console.print(" [3] [bold]Exit[/bold]\n")

        choice = IntPrompt.ask("[bold cyan]Enter choice[/bold cyan]", choices=["1","2","3"])
        if choice == 1:
            text = Prompt.ask("[bold green]> Enter text to hash[/bold green]")
            with Status("[bold yellow]Preparing to hash text...[/bold yellow]", spinner = "dots"):
                time.sleep(1.5)

            console.print("\n[bold yellow]✨ Generating hashes...[/bold yellow]")

            hashes = generate_hashes(text)
            display_hashes(hashes)
        
        elif choice == 2:
            file_path = Prompt.ask("[bold green]> Enter file path[/bold green]")

            with Status("[bold yellow]Reading file...[/bold yellow]", spinner = "dots"):
                time.sleep(1.5)

            hashes = generate_file_hashes(file_path)
            console.print("\n[bold yellow]✨ Generating file hashes...[/bold yellow]")

            display_hashes(hashes)
        elif choice == 3:
            console.print("\n[yellow]Exiting Hash Generator CLI 👋\nGood Bye!\n[/yellow]")            
            print("\033c", end="")
            sys.exit()
            

if __name__ == "__main__":
    main()





	
