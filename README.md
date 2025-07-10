# Batch Rinex Converter

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1_EEAtk_WzpY_h_sYny5qQ-sm7VuxEjtE?usp=sharing)

This project aims:
- convert an original batch script converter into a python based converter that converts leica/trimble raw data into Rinex data.
- add an interactive user interface that adds qol aspects to the converter for easy user access.

This github repository serves as a way for members to collaborate on the creation of the program.
Modes of input include:

1. Downloading the repository into their local computer and pushing updates through Git.

2. Google Colab code that can be updated alongside the "master" file for the program\*

*\* For those opting to use this input, I trust you can set up the installers (i have no clue how to implement the script in colab). Any changes to the script in this way can be pushed by pinging me in messenger.

---

## 📖 Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Google Colab](#google-colab)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features
- Converts raw GNSS data to RINEX v2/v3
- Supports Hatanaka compression
- Includes daily/hourly file concatenation
- Works with Leica `.m00` and Trimble `.t02` files

---

## 🛠 Prerequisites
- Python 3.x
- Required utilities (`mdb2rinex`, `gfzrnx`, etc.)
- See [prerequisites folder](prerequisites/) for setup.

---

## 📦 Installation
```bash
git clone https://github.com/Cyaltie/Batch-RinexConverter.git
cd Batch-RinexConverter
pip install -r requirements.txt
```


