import string, random, time, sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.status import Status

console = Console()

def banner():
    console.print(Panel.fit(r'''[bold green]██████╗  █████╗ ███████╗███████╗     ██████╗ ███████╗███╗   ██╗███████╗██████╗  █████╗ ████████╗ ██████╗ ██████╗ 
██╔══██╗██╔══██╗██╔════╝██╔════╝    ██╔════╝ ██╔════╝████╗  ██║██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
██████╔╝███████║███████╗███████╗    ██║  ███╗█████╗  ██╔██╗ ██║█████╗  ██████╔╝███████║   ██║   ██║   ██║██████╔╝
██╔═══╝ ██╔══██║╚════██║╚════██║    ██║   ██║██╔══╝  ██║╚██╗██║██╔══╝  ██╔══██╗██╔══██║   ██║   ██║   ██║██╔══██╗
██║     ██║  ██║███████║███████║    ╚██████╔╝███████╗██║ ╚████║███████╗██║  ██║██║  ██║   ██║   ╚██████╔╝██║  ██║
╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝     ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝[/bold green]'''), style="bold")

def password_generator():    
    # Ask user what to include
    include_alpha = Prompt.ask("[bold green]Include alphabets? (Y/N)[/bold green]").upper() == "Y"
    include_numbers = Prompt.ask("[bold green]Include numbers? (Y/N)[/bold green]").upper() == "Y"
    include_specials = Prompt.ask("[bold green]Include special characters? (Y/N)[/bold green]").upper() == "Y"


    #Ask for Length
    while  True:
        try:
            length = IntPrompt.ask("[bold green]Enter password length[/bold green]")
            if length <= 0:
                console.print("[red]❌ Length must be greater than 0.[/red]")
                continue
            break
        except ValueError:
            console.print("[yellow]Please enter a valid number.[/yellow]")

    # Build character pool
    char_pool = ""
    if include_alpha:
        char_pool += string.ascii_letters
    if include_numbers:
        char_pool += string.digits
    if include_specials:
        char_pool += string.punctuation

    # If not pool selected
    if not char_pool:
        console.print("[bold red]❌ No character type selected.\nExiting....[/bold red]")
        return
    
    # Generate password
    password = ''.join(random.choice(char_pool) for _ in range(length))

    # Display result
    with Status("[bold yellow]Generating password...[/bold yellow]", spinner="dots") as status:
        time.sleep(1.5)

    console.print("[bold cyan]\nGenerated Password: [/bold cyan]")
    console.print(Panel.fit(f"Your secure password is: [bold yellow]{password}[/bold yellow]", border_style="cyan"))


if __name__ == "__main__":
    try:
        print("\033c", end="")
        banner()
        while True:
            try:
                
                choice = Prompt.ask("[bold]Generate new password ?[/bold] [Y/N]").upper()
                if choice == "Y":
                    password_generator()                    
                elif choice == "N":        
                    console.print("\n[yellow]Exiting Password Generator CLI 👋[/yellow]")
                    print("\033c", end="")
                    sys.exit()
            except KeyboardInterrupt:
                console.print("[bold red]\n[-] Key Interrupt : [ CTRL + C ] Pressed ![/bold red]")                
                sys.exit()
    except KeyboardInterrupt:
                console.print("[bold red]\n[-] Key Interrupt : [ CTRL + C ] Pressed ![/bold red]")                
                sys.exit()
