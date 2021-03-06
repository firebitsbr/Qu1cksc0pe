#!/usr/bin/python3

import os
import sys

# Checking for puremagic
try:
    import puremagic as pr
except:
    print("Error: >puremagic< module not found.")
    sys.exit(1)

# Checking for colorama
try:
    from colorama import Fore, Style
except:
    print("Error: >colorama< not found.")
    sys.exit(1)

# Checking for prettytable
try:
    from prettytable import PrettyTable
except:
    print("Error: >prettytable< module not found.")
    sys.exit(1)

# Checking for oletools
try:
    from oletools.olevba import VBA_Parser
except:
    print("Error: >oletools< module not found.")
    print("Try 'sudo -H pip3 install -U oletools' command.")
    sys.exit(1)

# Colors
red = Fore.LIGHTRED_EX
cyan = Fore.LIGHTCYAN_EX
white = Style.RESET_ALL
green = Fore.LIGHTGREEN_EX
yellow = Fore.LIGHTYELLOW_EX
magenta = Fore.LIGHTMAGENTA_EX

# Legends
infoS = f"{cyan}[{red}*{cyan}]{white}"
errorS = f"{cyan}[{red}!{cyan}]{white}"

# Target file
targetFile = str(sys.argv[1])

# A function that finds VBA Macros
def MacroHunter(targetFile):
    answerTable = PrettyTable()
    answerTable.field_names = [f"{green}Threat Levels{white}", f"{green}Macros{white}", f"{green}Descriptions{white}"]

    print(f"\n{infoS} Looking for VBA Macros...")
    fileData = open(targetFile, "rb").read()
    vbaparser = VBA_Parser(targetFile, data=fileData)
    if vbaparser.contains_macros == True:
        macroList = list(vbaparser.analyze_macros())
        for fi in range(0, len(macroList)):
            if macroList[fi][0] == 'Suspicious':
                answerTable.add_row([f"{yellow}{macroList[fi][0]}{white}", f"{macroList[fi][1]}", f"{macroList[fi][2]}"])
            elif macroList[fi][0] == 'IOC':
                answerTable.add_row([f"{magenta}{macroList[fi][0]}{white}", f"{macroList[fi][1]}", f"{macroList[fi][2]}"])
            elif macroList[fi][0] == 'AutoExec':
                answerTable.add_row([f"{red}{macroList[fi][0]}{white}", f"{macroList[fi][1]}", f"{macroList[fi][2]}"])
            else:
                answerTable.add_row([f"{macroList[fi][0]}", f"{macroList[fi][1]}", f"{macroList[fi][2]}"])
        print(f"{answerTable}\n")
    else:
        print(f"{errorS} Not any macros found.")

# A function that handles file types, extensions etc.
def MagicParser(targetFile):
    # Defining table
    resTable = PrettyTable()

    # Magic byte parsing
    resCounter = 0
    resTable.field_names = [f"Extracted File Extensions", "Names", "Byte Matches", "Confidence"]
    resourceList = list(pr.magic_file(targetFile))
    for res in range(0, len(resourceList)):
        extrExt = str(resourceList[res].extension)
        extrNam = str(resourceList[res].name)
        extrByt = str(resourceList[res].byte_match)
        if resourceList[res].confidence >= 0.8:
            resCounter += 1
            if extrExt == '':
                resTable.add_row([f"{red}No Extension{white}", f"{red}{extrNam}{white}", f"{red}{extrByt}{white}", f"{red}{resourceList[res].confidence}{white}"])
            else:
                resTable.add_row([f"{red}{extrExt}{white}", f"{red}{extrNam}{white}", f"{red}{extrByt}{white}", f"{red}{resourceList[res].confidence}{white}"])
    if len(resourceList) != 0:
        print(resTable)

# Execution area
if __name__ == '__main__':
    MagicParser(targetFile)
    try:
        MacroHunter(targetFile)
    except:
        print(f"{errorS} File format not supported for macro scanning.")