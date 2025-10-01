import pyfiglet
import sys
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.panel import Panel

console = Console()

#Display Banner
banner = pyfiglet.figlet_format("Caesar Cipher")
def banner():
	console.print(Panel.fit(r"""[bold green] ██████╗ █████╗ ███████╗███████╗ █████╗ ██████╗      ██████╗██╗██████╗ ██╗  ██╗███████╗██████╗ 
██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗    ██╔════╝██║██╔══██╗██║  ██║██╔════╝██╔══██╗
██║     ███████║█████╗  ███████╗███████║██████╔╝    ██║     ██║██████╔╝███████║█████╗  ██████╔╝
██║     ██╔══██║██╔══╝  ╚════██║██╔══██║██╔══██╗    ██║     ██║██╔═══╝ ██╔══██║██╔══╝  ██╔══██╗
╚██████╗██║  ██║███████╗███████║██║  ██║██║  ██║    ╚██████╗██║██║     ██║  ██║███████╗██║  ██║
 ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝     ╚═════╝╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝[/bold green]"""), style="bold")

# Encryption
def caesarEncryption(plainText, key):
	cipherText = []
	try:
		for ch in plainText: # ch = Hello world
			if 'A' <= ch <= 'Z':
				cipherText.append(chr((ord(ch) - 65 + key) % 26 + 65))
			elif 'a' <= ch <= 'z':
				cipherText.append(chr((ord(ch) - 97 + key) % 26 + 97))
			else:
				cipherText.append(ch)
		return ''.join(cipherText)
		
	except Exception as e:
		print(e)

# Decryption
def caesarDecryption(plainText, key):
	cipherText = []
	try:
		for ch in plainText: # ch = Hello world
			if 'A' <= ch <= 'Z':
				cipherText.append(chr((ord(ch) - 65 - key) % 26 + 65))
			elif 'a' <= ch <= 'z':
				cipherText.append(chr((ord(ch) - 97 - key) % 26 + 97))
			else:
				cipherText.append(ch)
		return ''.join(cipherText)
		
	except Exception as e:
		print(e)
		
#main body	
if __name__ == "__main__":
	print("\033c", end="")
	banner()
	while True:
		try:
			console.print(Panel.fit("Choose an option:", style="bold blue"))
			console.print("[bold] 1) Encryption\n 2) Decryption\n 3) Exit")
			choice = IntPrompt.ask("Select Option: ", choices=['1','2','3'])
			
			if choice == 1:
				plainText = input("Enter text to encrypt: ")
				key = int(input("Enter Key (number) : "))
				print(f"Encrypted text is: {caesarEncryption(plainText, key)}\n")
			elif choice == 2:
				plainText = input("Enter text to decrypt: ")
				key = int(input("Enter Key (number) : "))
				print(f"Decrypted text is: {caesarDecryption(plainText, key)}\n")
			elif choice == 3:				
				console.print("\n[yellow]Exiting Caesar Cipher CLI 👋[/yellow]")
				print("\033c", end="")
				sys.exit()			
		except KeyboardInterrupt:
			console.print("[bold red]\n[-] Key Interrupt : [ CTRL + C ] Pressed ![/bold red]")
			sys.exit()
	
