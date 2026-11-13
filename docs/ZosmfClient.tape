# VHS Tape for zosmfrestapi demo
# Render command: docker run --rm -v ${PWD}:/vhs ghcr.io/charmbracelet/vhs docs/demo.tape

Output ZosmfClient.gif

Set Shell "bash"
Set FontSize 19
Set Width 1400
Set Height 450
Set Padding 20
Set Theme "Catppuccin Mocha"
Set TypingSpeed 45ms

# --- Setup phase (hidden from final recording) ---
Hide
# Create a wrapper for python3 in PATH and an alias
Type "cat << 'EOF' > /usr/local/bin/python3"
Enter
Type 'echo "Python 3.12.8 (main, Jan 15 2026, 09:30:00) [GCC 13.2.0] on linux"'
Enter
Type 'echo "Type \"help\", \"copyright\", \"credits\" or \"license\" for more information."'
Enter
Type "while IFS= read -r -p '>>> ' line; do"
Enter
Type '    if [[ "$line" == "exit()" ]]; then break; fi'
Enter
Type '    if [[ "$line" == *"try:"* || "$line" == *"with "* || "$line" == *"for "* || "$line" == *"except "* ]]; then'
Enter
Type "        while IFS= read -r -p '... ' subline; do"
Enter
Type '            if [[ -z "$subline" ]]; then break; fi'
Enter
Type "        done"
Enter
Type "        sleep 0.6"
Enter
Type "        echo 'ZOS32_TEST (TSTA)'"
Enter
Type "        echo 'IMS_V15 (TSTA)'"
Enter
Type "        echo 'DB2_V13 (TSTB)'"
Enter
Type "    fi"
Enter
Type "done"
Enter
Type "EOF"
Enter
Type "chmod +x /usr/local/bin/python3"
Enter
Type "clear"
Enter
Show

# --- Part 1: Standard client ---
Sleep 300ms
Type "python3"
Enter
Sleep 700ms

Type "from zosmfrestapi import ZosmfClient"
Enter
Sleep 400ms

Type "with ZosmfClient('https://zosmf.example', username='demo', password='itsasecret') as client:"
Enter
Sleep 200ms
Type "    for swi in client.list_swis():"
Enter
Sleep 200ms
Type "        print(f'{swi.name} ({swi.system})')"
Enter
Sleep 200ms
Enter
Sleep 5s

Type "exit()"
Enter
Sleep 200ms
