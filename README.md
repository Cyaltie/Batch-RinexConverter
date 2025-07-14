# Batch Rinex Converter

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1_EEAtk_WzpY_h_sYny5qQ-sm7VuxEjtE?usp=sharing)

This project aims:
- convert an original batch script converter into a python based converter that converts leica/trimble raw data into Rinex data.
- add an interactive user interface that adds qol aspects to the converter for easy user access.

This github repository serves as a way for members to collaborate on the creation of the program.
Modes of input include:

1. Downloading the repository into their local computer and pushing updates through Git.

2. Google Colab code that can be updated alongside the "master" file for the program<sup>1

1 *For those opting to use this input, I trust you can set up the installers (i have no clue how to implement the script in colab). Any changes to the script in this way can be pushed by pinging me in messenger.*

---

## 📖 Table of Contents
- [Batch Rinex Converter](#batch-rinex-converter)
  - [📖 Table of Contents](#-table-of-contents)
  - [✨ Planned Features (we can use this are as a sort of checklist to be edited when the program is finished.)](#-planned-features-we-can-use-this-are-as-a-sort-of-checklist-to-be-edited-when-the-program-is-finished)
  - [🛠 Prerequisites (**For code input**)](#-prerequisites-for-code-input)
  - [📦 Installation](#-installation)
  - [📖 Contributor Guide](#-contributor-guide)
  - [-](#-)

---

## ✨ Planned Features (we can use this are as a sort of checklist to be edited when the program is finished.)
[⬆️ Back to Top](#-collaborator-guide-how-to-work-on-this-repository)
- Takes in raw GNSS data (.m** and .T02) and converts it into Rinex files 🟢 **100% done**
    - For leica sites (.m**) 🟢
        - recognize file type from zip - 100% done 🟢
        - unzip it in a separate folder - 100% done 🟢
        - open cmd to access mdb2rinex for conversion - 100% done 🟢
        - use gfzrnx to clean header, logging interval, version change, hatanaka - 100% done 🟢
        - zip all files from same station to 1 file with correct extension in an output folder - 100% done 🟢
        - handles multiple stations and start and end dates - 100% done 🟢

    - For trimble sites (.T02)<sup>2 🟢 **100% done**
        - recognize file type from zip - 100% done 🟢
        - unzip it in a separate folder - 100% done 🟢
        - open cmd to access convertToRinex for conversion - 100% done 🟢
        - use gfzrnx to clean header, logging interval, version change, hatanaka - 100% done 🟢
        - zip all files from same station to 1 file with correct extension in an output folder - 100% done 🟢
        - handles multiple stations - 100% done 🟢

- Supports Hatanaka compression 🟢
- Works with multiple Leica `.m00` and Trimble `.t02` files simultaneously 🔴<sup>2
- Integrate a UI (preferably based on ver4\.3c ) to make the program user friendly 🟢|🔴 <sup>3

2 not debugged or tested  
3 we have a preliminary UI (ver4\.3C) w/o conversion logic integrated; since logic hasn't been integrated it is still incomplete

---

## 🛠 Prerequisites (**For code input**)
[⬆️ Back to Top](#-collaborator-guide-how-to-work-on-this-repository)
- Python 3.x installed
- Interpreter installed (VSCode, notepad++, etc.)
- Required utilities (`mdb2rinex`, `gfzrnx`, etc.) (have at least 15 mb free space for all required dependecies) refer to Installation for setup [prerequisites folder](prerequisites/)
- Google Colab (optional)
- Git (if opt to use github and edit files locally) See git push guide for details.

---

## 📦 Installation 
[⬆️ Back to Top](#-collaborator-guide-how-to-work-on-this-repository)
## 📖 Contributor Guide

If you're a collaborator and want to propose changes, follow the detailed step-by-step guide here:  

➡️ [**View the Collaborator Guide**](Collaborator_Guide.md)

➡️ [**View the Prerequisites Guide**](Prerequisite_Guide.md)


## -


