import os
import sys

def clear_screen():
    """Clear terminal screen (cross-platform)."""
    # Cara paling kompatibel:
    if os.name == 'nt':          # Windows
        os.system('cls')
    else:                        # macOS / Linux / lainnya
        os.system('clear')