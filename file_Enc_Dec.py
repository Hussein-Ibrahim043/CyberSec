import os
import sys
import getpass
import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.status import Status
from rich.progress import (
    Progress,
    BarColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
    TaskProgressColumn,
    TransferSpeedColumn,
    FileSizeColumn,
)
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidTag

console = Console()
MAGIC = b"FENC1"            # 5 bytes
SALT_LENGTH = 16            # PBKDF2 salt
NONCE_LEN = 12              # GCM standard nonce length
TAG_LEN = 16                # GCM tag length
KDF_ITERS = 200_000
KEY_LEN = 32                # AES-256
CHUNCK_SIZE = 1024 * 1024   # 1 MB


def banner():
    console.print(Panel.fit(
        "[bold green]FILE CONTENT ENCRYPTION TOOL[/bold green]\n"
        "[dim]AES-256-GCM • PBKDF2-HMAC-SHA256 • Streaming I/O[/dim]",
        border_style="green"))
    

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm= hashes.SHA256(),
        length= KEY_LEN,
        salt=salt,
        iterations=KDF_ITERS,
        backend=default_backend()
    )
    return kdf.derive(password.encode("utf-8"))


def encrypt_file(inp: str, outp: str, password: str):
    salt = os.urandom(SALT_LENGTH)    
    key = derive_key(password, salt)
    nonce = os.urandom(NONCE_LEN)   # IV


    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()

    total = os.path.getsize(inp)

    with open(inp, "rb") as fin, open(outp, "wb") as fout, Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        TaskProgressColumn(),
        FileSizeColumn(),
        TransferSpeedColumn(),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        fout.write(MAGIC)
        fout.write(salt)
        fout.write(nonce)

        task = progress.add_task("[cyan]Encrypting...", total=total)
        while True:
            chunck = fin.read(CHUNCK_SIZE)
            if not chunck:
                break
            ct = encryptor.update(chunck)
            if ct:
                fout.write(ct)
                progress.update(task, advance=len(chunck))
        
        encryptor.finalize()
        fout.write(encryptor.tag)
        
    del key
    console.print("[bold green][+] Encryption complete.[/bold green]")


def decrypt_file(inp: str, outp: str, password: str):
    header_len = len(MAGIC) + SALT_LENGTH + NONCE_LEN
    total = os.path.getsize(inp)
    if total < header_len + TAG_LEN:
        raise ValueError("Input too small to be a valid encrypted file.")
    
    with open(inp, "rb") as fin:
        magic = fin.read(len(MAGIC))
        if magic != MAGIC:
            raise ValueError("[-] Invalid file format (magic mismatch)")
        salt = fin.read(SALT_LENGTH)
        nonce = fin.read(NONCE_LEN)
        ciphertext_length = total - header_len - TAG_LEN

        key = derive_key(password, salt)
        cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
        decryptor = cipher.decryptor()
        decryptor.authenticate_additional_data(b"")

        try:
            with open(outp, "wb") as fout, Progress(
                "[progress.description]{task.description}",
                BarColumn(),
                TaskProgressColumn(),
                FileSizeColumn(),
                TransferSpeedColumn(),
                TimeElapsedColumn(),
                TimeRemainingColumn(),
                console=console,
            ) as progress:
                task  = progress.add_task("[cyan]Decrypting...", total=ciphertext_length)

                remaining = ciphertext_length
                while remaining > 0:
                    to_read = min(CHUNCK_SIZE, remaining)
                    chunck = fin.read(to_read)
                    if not chunck:
                        break
                    pt = decryptor.update(chunck)
                    if pt:
                        fout.write(pt)
                    remaining -= len(chunck)
                    progress.update(task, advance=len(chunck))

                tag = fin.read(TAG_LEN)
                try:
                    decryptor.finalize_with_tag(tag)
                except InvalidTag:
                    fout.close()
                    os.remove(outp)
                    raise ValueError("[-] Authentication failed. Wrong password or corrupted file.")
        finally:
            del key

        console.print("[bold green][+] Decryption complete.[/bold green]")

def default_output_path(mode: str, input_path: str) -> str:
    if mode == "enc":        # file.txt -> file.enc/ file.txt.enc
        return input_path + ".enc"
    else:
        if input_path.endswith(".enc"):
            return input_path[:-4]
        base, ext = os.path.splittext(input_path)       #D:\Projects\fiel.txt
        return base + ".dec" + ext
    

def main():
    print("\033c", end="")
    while True:
        try:

            banner()
            console.print("[bold cyan]Choose an option:[/bold cyan]")
            console.print(Panel.fit("Choose an option:", style="bold"))
            console.print("[bold] 1) Encrypt a file\n 2) Decrypt a file\n 3) Exit[/bold]")
            choice = IntPrompt.ask("[bold cyan]Enter choice[/bold cyan]")

            if choice == 1:
                mode = "enc"
            elif choice == 2:
                mode = "dec"
            elif choice == 3:
                console.print("\n[yellow]Exiting File Encryptor / Decryptor CLI 👋[/yellow]")
                print("\033c", end="")
                sys.exit()            
            
            inp = input("Enter input file path: ").strip()
            if not os.path.isfile(inp):
                console.print(f"[red][-] File Not Found: {inp}[/red]")
                sys.exit(1)
            
            default_out = default_output_path(mode, inp)
            outp =  input(f"Enter output file path (default: {default_out}) :").strip() or default_out 

            if os.path.abspath(inp) == os.path.abspath(outp):
                console.print("[red]Input and Output paths must differ.[/red]")     #file.txt != file.txt
                sys.exit(1)


            password = getpass.getpass("Enter password: ")
            if not password:
                console.print("[red]Empty password now allowed.[/red]")
                sys.exit(1)
            
            try:
                if mode == "enc":
                    encrypt_file(inp, outp, password)
                else:
                    decrypt_file(inp, outp, password)

                console.print(Panel.fit(f"[bold green]Output: [/bold green]{outp}",border_style="green"))
            except Exception as e:
                console.print(f"[red]ERROR: [/red]{e}")
                sys.exit(1)
        except KeyboardInterrupt:
            console.print("[bold red]\n[-] Key Interrupt : [ CTRL + C ] Pressed[/bold red]")
            sys.exit()

if __name__ == "__main__":
    main()
