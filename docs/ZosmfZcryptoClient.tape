# VHS Tape for zosmfrestapi demo
# Render command: docker run --rm -v ${PWD}:/vhs ghcr.io/charmbracelet/vhs docs/demo.tape

Output ZosmfZcryptoClient.gif

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
Type 'echo "Python 3.14.4.1 (heads/pyz_dev-3.14:3f3ddf59ff3, Jul 15 2026, 10:31:31) [Clang 18.1.8 (build 2ac8998)] on zos"'
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
Type "        sleep 0.2"
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


# --- Part 2: zcrypto SAF key ring client ---
Sleep 300ms
Type "python3"
Enter
Sleep 700ms

Type "from zosmfrestapi import ZosmfZcryptoClient"
Enter
Sleep 400ms

Type "with ZosmfZcryptoClient('https://zosmf.example', keyring='demo/Ring', label='client cert') as client:"
Enter
Sleep 200ms
Type "    for swi in client.list_swis():"
Enter
Sleep 200ms
Type "        print(f'{swi.name} ({swi.system})')"
Enter
Sleep 200ms
Enter
Sleep 6s

Type "exit()"
Enter
Sleep 200ms
