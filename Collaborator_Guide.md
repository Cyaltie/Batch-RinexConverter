# 🤝 Collaborator Guide: How to Work on This Repository

This guide is for contributors who want to propose changes to this repository, especially if you're starting from a ZIP download. It includes setup instructions, update syncing, and how to resume work after rebooting your system.

---

## 📑 Table of Contents

- [📂 Local Installation](#-local-installation)
- [🔱 Creating a Fork Branch in GitHub](#-creating-a-fork-branch-in-github)
- [🔧 First-Time Git Setup](#-first-time-git-setup)
- [🌿 Creating a Branch and Making Changes](#-creating-a-branch-and-making-changes)
- [🔁 Submitting a Pull Request](#-submitting-a-pull-request)
- [🔄 Syncing Your Fork With Latest Changes](#-syncing-your-fork-with-latest-changes)
- [💻 Resuming Work After Reboot](#-resuming-work-after-reboot)

## 📂 Local Installation  

[⬆️ Back to Top](#-collaborator-guide-how-to-work-on-this-repository)

### 1. Make sure Git is installed  
- Install Git following this YouTube guide (from 2:11 to 3:13):  
  [![Watch on YouTube](https://img.shields.io/badge/Watch_on-YouTube-red?logo=youtube)](https://youtu.be/tRZGeaHPoaw?si=NV-0TO8qYmWDUhnu&t=131)

### 2. Download the repository  
- Click **Code > Download ZIP** in the GitHub repo.  
  ![Download ZIP](Resources/githubstep2.png)
  ![Download ZIP](Resources/githubstep2a.png)    
- Unzip it to:  
  `C:/Users/<YourName>/Batch-RinexConverter`  
  ![Unzip Folder](Resources/githubstep2b.png)

---
## 🔱 Creating a fork branch in GitHub  

[⬆️ Back to Top](#-collaborator-guide-how-to-work-on-this-repository)
- To avoid having conflicts with the main branch (where owner is working), each collaborator is recommended to create their own fok of the github repo.
### 1. Go to the main repo page.
-  click on the **Fork** on the top-right corner.
    ![Alt text](Resources/gitfork.png)<br>

This creates a copy of the repository under your own github account.

## 🔧 First-Time Git Setup  

[⬆️ Back to Top](#-collaborator-guide-how-to-work-on-this-repository)

### 1. Open Git Bash and configure Git [only once] (do it line-by-line)  
```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

### 2. Navigate to the repo folder and initialize Git (do it line-by-line)

```bash
cd C:/Users/<YourName>/Batch-RinexConverter
git init
```

### 3. Add remote connections (do it line-by-line)
Replace with your GitHub username and repo name.
```bash
git remote add origin https://github.com/<your-username>/<repo-name>.git
git remote add upstream https://github.com/<owner-username>/Batch-RinexConverter.git
```
### 4. Verify that the remotes are set
```bash
git remote -v
```
Expected output should be something like this:
```bash
origin   https://github.com/<your-username>/<repo-name>.git (fetch)
origin   https://github.com/<your-username>/<repo-name>.git (push)
upstream https://github.com/Cyaltie/Batch-RinexConverter.git (fetch)
upstream https://github.com/Cyaltie/Batch-RinexConverter.git (push)
```

## 🌿 Creating a Branch and Making Changes  

[⬆️ Back to Top](#-collaborator-guide-how-to-work-on-this-repository)

### 1. Create a new feature branch
```bash
git checkout -b my-feature-branch
```
### 2. Make edits in the folder

### 3. Stage and commit your changes
- if you want all the files to be updated in your github fork: (**do this line by line**)
```bash
git add .
git commit -m "Describe your changes"
```
- if you want to update a single file (say the python code) (**do this line by line**)
```bash
git add /path of file or folder
git commit -m "Describe your changes"
```

sample (edited python code)
```bash
git add /C:/Users/User/Batch-RinexConverter/UsersUserBatch-RinexConverter/RNXConv_1.4.5r.py
git commit -m "added logging interval functionality"
```

### 4. Push to your fork
```bash
git push -u origin my-feature-branch
```

## 🔁 Submitting a Pull Request  

[⬆️ Back to Top](#-collaborator-guide-how-to-work-on-this-repository)
### 1. Go to your fork on GitHub

### 2. Click “Compare & pull request”

### 3. Confirm:

Base repo = Cyaltie/Batch-RinexConverter

Compare branch = your feature branch

### 4. Add a description and click “Create pull request”

## 🔄 Syncing Your Fork With Latest Changes  

[⬆️ Back to Top](#-collaborator-guide-how-to-work-on-this-repository)
To update your fork with changes from the original main branch: (line-by-line)
```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

## 💻 Resuming Work After Reboot  

[⬆️ Back to Top](#-collaborator-guide-how-to-work-on-this-repository)
After restarting your PC:

### 1.Open Git Bash

### 2.Navigate to your local repo:
```bash
cd C:/Users/<YourName>/Batch-RinexConverter
```

### 3.Fetch remote changes and continue your branch:
```bash
git fetch --all
git checkout my-feature-branch
You can now continue editing and pushing changes as usual.
```

