import os
import sys

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_banner():
    banner = f"""
{Colors.BOLD}
{Colors.FAIL}    ██████╗ ███████╗██╗   ██╗██╗██╗     ███████╗███████╗██████╗  ██████╗{Colors.RESET}
{Colors.FAIL}    ██╔══██╗██╔════╝██║   ██║██║██║     ██╔════╝╚══███╔╝██╔══██╗██╔═══██╗{Colors.RESET}
{Colors.FAIL}    ██║  ██║█████╗  ██║   ██║██║██║     █████╗    ███╔╝ ██████╔╝██║   ██║{Colors.RESET}
{Colors.FAIL}    ██║  ██║██╔══╝  ╚██╗ ██╔╝██║██║     ██╔══╝   ███╔╝  ██╔══██╗██║   ██║{Colors.RESET}
{Colors.FAIL}    ██████╔╝███████╗ ╚████╔╝ ██║███████╗███████╗███████╗██║  ██║╚██████╔╝{Colors.RESET}
{Colors.WARNING}    ╚═════╝ ╚══════╝  ╚═══╝  ╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝{Colors.RESET}
{Colors.WARNING}                         DDoS Testing Toolkit                         {Colors.RESET}
{Colors.OKBLUE}                     Author: krypthane                             {Colors.RESET}
{Colors.OKBLUE}                     GitHub: github.com/wavegxz-design               {Colors.RESET}
{Colors.HEADER}               Only for authorized security testing!                {Colors.RESET}
    """
    print(banner)

def confirm_action(prompt):
    answer = input(f"{Colors.WARNING}{prompt} (Y/n): {Colors.RESET}").strip().lower()
    return answer in ('y', 'yes', '')

def safe_input(prompt, default=None, type_func=str, valid_range=None):
    """Safely get user input with type conversion, default, and range validation."""
    while True:
        try:
            value = input(f"{Colors.OKCYAN}{prompt}{Colors.RESET}").strip()
            if not value and default is not None:
                return default
            converted = type_func(value)
            if valid_range and converted not in valid_range:
                print(f"{Colors.FAIL}Invalid choice. Allowed: {valid_range}{Colors.RESET}")
                continue
            return converted
        except ValueError:
            print(f"{Colors.FAIL}Invalid input. Try again.{Colors.RESET}")

def print_error(msg):
    print(f"{Colors.FAIL}[!] {msg}{Colors.RESET}")

def print_success(msg):
    print(f"{Colors.OKGREEN}[✓] {msg}{Colors.RESET}")

def print_info(msg):
    print(f"{Colors.OKBLUE}[i] {msg}{Colors.RESET}")

def print_warning(msg):
    print(f"{Colors.WARNING}[!] {msg}{Colors.RESET}")

def is_root():
    return os.geteuid() == 0

def restart_as_root():
    """Re-run the current script with sudo using the same Python interpreter."""
    script_path = os.path.abspath(sys.argv[0])
    python_exec = sys.executable
    print_warning("Root privileges required. Restarting with sudo...")
    os.execvp('sudo', ['sudo', python_exec, script_path] + sys.argv[1:])
