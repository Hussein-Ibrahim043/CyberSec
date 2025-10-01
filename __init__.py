import pyfiglet, sys, time, subprocess, os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import track
from rich.prompt import Prompt, IntPrompt
from rich.status import Status

console = Console()

Blue = "\033[1;36;40m"
Red = "\033[1;31;40m"
Reset = "\033[0m"
WhiteRed = "\033[93m"
Green = "\033[92m"
Yellow= "\033[93m"
Magenta = "\033[95m"
Cyan  = "\033[96m"


def framed_line(content, width=63, left_tage='[---]', right_tag='[---]'):
    inner_width = width - len(left_tage) - len(right_tag)
    content = content[:inner_width].strip()
    return f"{Blue}{left_tage}{content.center(inner_width)}{right_tag}{Reset}"

def centered(text, width=63):
    return text.center(width)


def print_banner():
    W = 73
    print()
    print(rf"""{Cyan}
     ██████╗██╗   ██╗██████╗ ███████╗██████╗ ███████╗███████╗ ██████╗   
    ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝██╔════╝   
    ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝███████╗█████╗  ██║        
    ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗╚════██║██╔══╝  ██║        
    ╚██████╗   ██║   ██████╔╝███████╗██║  ██║███████║███████╗╚██████╗   
    ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝    {Reset}
    """)
    print(framed_line("A Modular Cybersecurity Toolkit for Scanning, Hashing, Encryption & Decryption", W))
    print(framed_line("Caesar Cipher, Password Generator & Strength Checker, VT Anti-Virus", W))
    print(framed_line("", W))
    print(centered("Version: 1.0", W))
    print(centered(f"Codename: 'CyberSec-ToolKit'", W))
    print(framed_line("Created by: Abdalla Azzam", W))
    print(framed_line("Supervised by: Hussein Rabio", W))
    print()
    print(centered(f"{Green}Welcome to the Modular Cybersecurity Toolkit", W))
    print(centered(f"A learning tool for scanning, crypto and security practice.{Reset}", W))
    print()
    

def main_menu():
    console.print(Panel.fit("Choose an option:", style="bold blue"))
    console.print("[bold] [1] VT Anti-Virus\n [2] Port Scanner\n [3] Caesar Cipher\n [4] Hashing Tool\n [5] File Encryptor / Decryptor\n [6] Password Generator\n [7] Password Strength Checker\n [0] Exit\n[/bold]")
    

def main():
	os.system('clear')	
	with Status("[bold green]Launching CyberSec...\n[/bold green]", spinner="dots") as status:
		time.sleep(2.5)
	while True:
		print_banner()
		try:			
			main_menu()
			choice = IntPrompt.ask("[bold cyan]Enter choice[/bold cyan]")
			# 1
			if choice == 1:				
				with Status("[bold green] Running  VT Anti-Virus[/bold green]", spinner="dots") as status:
					time.sleep(1.5)				
				
				try:
					subprocess.run(['python3', 'vt_antivirus.py'], check=True)
				except subprocess.CalledProcessError as e:
					print(f"\033[1;31;40mError: {e}\033[0m")
			# 2		
			elif choice == 2:				
				with Status("[bold green] Running  Port Scanner[/bold green]", spinner="dots") as status:
					time.sleep(1.5)
				
				
				try:
					subprocess.run(['python3', 'portScanner.py'], check=True)
				except subprocess.CalledProcessError as e:
					print(f"\033[1;31;40mError: {e}\033[0m")
			# 3
			elif choice == 3:
				
				with Status("[bold green] Running  Caesar Cipher[/bold green]", spinner="dots") as status:
					time.sleep(1.5)
				
				
				try:
					subprocess.run(['python3', 'CaesarCipher.py'], check=True)
				except subprocess.CalledProcessError as e:
					print(f"\033[1;31;40mError: {e}\033[0m")
			# 4
			elif choice == 4:
				
				with Status("[bold green] Running  Hash Generator[/bold green]", spinner="dots") as status:
					time.sleep(1.5)			
				
				try:
					subprocess.run(['python3', 'hashGenerator.py'], check=True)
				except subprocess.CalledProcessError as e:
					print(f"\033[1;31;40mError: {e}\033[0m")
            # 5
			elif choice == 5:
				
				with Status("[bold green] Running  File Encryptor / Decryptor[/bold green]", spinner="dots") as status:
					time.sleep(1.5)
				
				
				try:
					subprocess.run(['python3', 'file_Enc_Dec.py'], check=True)
				except subprocess.CalledProcessError as e:
					print(f"\033[1;31;40mError: {e}\033[0m")
			# 6
			elif choice == 6:
				
				with Status("[bold green] Running  Password Generator[/bold green]", spinner="dots") as status:
					time.sleep(1.5)
				
				
				try:
					subprocess.run(['python3', 'passwordGenerator.py'], check=True)
				except subprocess.CalledProcessError as e:
					print(f"\033[1;31;40mError: {e}\033[0m")
			# 7
			elif choice == 7:
				with Status("[bold green] Running  Password Strength Checker[/bold green]", spinner="dots") as status:
					time.sleep(1.5)				
				
				try:
					subprocess.run(['python3', 'passwordChecker.py'], check=True)
				except subprocess.CalledProcessError as e:
					print(f"\033[1;31;40mError: {e}\033[0m")
            # 0
			elif choice == 0:
				print(f"\n{WhiteRed}Goodbye 👋{Reset}")
				sys.exit()
			else:
				print(f"\n{WhiteRed}[!] Invalid choice, please try again.{Reset}")
		except ValueError as e:
			print("[bold red]Execution corrupt occur[/bold red]")
		except KeyboardInterrupt:
			console.print("[bold red]\n[-] Key Interrupt : [ CTRL + C ] Pressed ![/bold red]")
			sys.exit()
    
    
if __name__ == "__main__":
     main()
