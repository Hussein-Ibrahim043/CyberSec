import re
import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.align import Align
import pyfiglet

console = Console()

def banner():
    console.print(Panel.fit(r'''[bold cyan]
██████╗  █████╗ ███████╗███████╗██╗    ██╗ ██████╗ ██████╗ ██████╗      ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗ 
██╔══██╗██╔══██╗██╔════╝██╔════╝██║    ██║██╔═══██╗██╔══██╗██╔══██╗    ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗
██████╔╝███████║███████╗███████╗██║ █╗ ██║██║   ██║██████╔╝██║  ██║    ██║     ███████║█████╗  ██║     █████╔╝ █████╗  ██████╔╝
██╔═══╝ ██╔══██║╚════██║╚════██║██║███╗██║██║   ██║██╔══██╗██║  ██║    ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██╔══╝  ██╔══██╗
██║     ██║  ██║███████║███████║╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝    ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗███████╗██║  ██║
╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝      ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
[/bold cyan]'''), style="bold")


def check_password_strength(password: str) -> None:
    # Criteria checks
    length_error = len(password) < 8
    lowercase_error = re.search(r"[a-z]", password) is None
    uppercase_error = re.search(r"[A-Z]", password) is None
    digit_error = re.search(r"\d", password) is None
    special_error = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password) is None

    # Collect feedback
    comments = []
    if length_error:
        comments.append("[red]⚠ Too short (use at least 8 characters).[/red]")
    if lowercase_error:
        comments.append("[red]⚠ Missing lowercase letter.[/red]")
    if uppercase_error:
        comments.append("[red]⚠ Missing uppercase letter.[/red]")
    if digit_error:
        comments.append("[red]⚠ Missing a number.[/red]")
    if special_error:
        comments.append("[red]⚠ Missing a special character (e.g., ! @ # $ % ).[/red]")

    # Strength levels
    if not any([length_error, lowercase_error, uppercase_error, digit_error, special_error]):
        strength = "[bold green]🔐 Strong password![/bold green]"
    elif len(comments) <= 2:
        strength = "[yellow] Medium strength password.[/yellow]"
    else:
        strength = "[bold red]❌ Weak password.[/bold red]"

    # Build final panel text
    analysis = f"[bold cyan]Password Entered:[/bold cyan] [white]{password}[/white]\n\n"
    analysis += f"[bold magenta]Analysis Result:[/bold magenta]\n{strength}\n"
    
    if comments:
        analysis += "\n" + "\n".join(comments)

    # Show in one Panel
    console.print(Panel.fit(analysis, title="[ Password Strength Checker ]", style="bold blue"))


# Run until user exits
if __name__ == "__main__":
    try:

        print("\033c", end="")
        banner()
        while True:
            try:

                pwd = Prompt.ask("[bold green]Enter a password to check[/bold green]")
                check_password_strength(pwd)

                choice = Prompt.ask("\n[cyan]Do you want to check another password?[/cyan] (y/n)", choices=["y","n"], default="y")
                if choice.lower() == "n":
                    console.print("\n[bold yellow]Exiting Password Checker CLI 👋 Goodbye![/bold yellow]")
                    print("\033c", end="")
                    break
            except Exception as e:
                console.print(f"[red]ERROR: [/red]{e}")
                sys.exit(1)
            except KeyboardInterrupt:
                console.print("[bold red]\n[-] Key Interrupt : [ CTRL + C ] Pressed[/bold red]")
                sys.exit()
    except KeyboardInterrupt:
        console.print("[bold red]\n[-] Key Interrupt : [ CTRL + C ] Pressed[/bold red]")
        sys.exit()
    except Exception as e:
        console.print(f"[red]ERROR: [/red]{e}")
        sys.exit(1)
