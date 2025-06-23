# DeepFile-Detector-
A forensic tool developed to identify and recover files that have undergone file signature manipulation, an anti-forensic technique used by threat actors to hide file types by altering header/footer signatures (magic numbers).

This tool analyses internal structures and markers unique to each supported file type, without relying on magic numbers for file identification 

# Features
Detects true file types based on internal structure, not file headers( magic numbers).

Supports detection of:
-PDF

-Microsoft Office Open XML files (DOCX, XLSX, PPTX)

-JPEG

-PNG

-GIF (animated only)

-Reconstructs obfuscated files by restoring valid headers and extensions.

-Includes hashing (MD5/SHA) for integrity verification for recovered obfuscated files 

# Technologies Used
Python

PyQt5 - GUI

PyInstaller - Packaging to .exe

Hashlib - Cryptographic hashing

# User Interface
The tool provides the following features:

Upload File – Select a file for analysis

Download Report – Generate and Save scan results

Recover File – Reconstruct obfuscated file

Hash File – Generate MD5/SHA hashes for the recovered obfuscated file. 


![image](https://github.com/user-attachments/assets/cd1a6d5d-9a4c-4098-b6e0-386c2d044973)






