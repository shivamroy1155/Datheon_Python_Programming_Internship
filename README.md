# Datheon Python Internship — Project Deliverables

This repository contains three beginner-friendly Python projects:
1. `hangman.py` — console Hangman word game
2. `organizer.py` — file organizer with collision handling and dry-run mode
3. `chatbot.py` — rule-based FAQ chatbot

All projects use the Python standard library; no third-party packages are required.

## Requirements
- Python 3.10 or newer recommended
- VS Code, PyCharm, or another editor (optional)

Check Python:
```bash
python --version
```
On some systems, use `python3` instead of `python`.

## Task 1: Hangman
Run:
```bash
python hangman.py
```
Features: random secret word, six incorrect guesses, ASCII gallows, duplicate-guess protection, input validation, win/loss/quit screens.

## Task 3: File Organizer
First create a temporary test folder and put copies of a few sample files in it. Preview changes:
```bash
python organizer.py "./organizer_test" --dry-run
```
When the preview looks right, run without `--dry-run`:
```bash
python organizer.py "./organizer_test"
```
**Safety:** Test on a temporary folder first. Do not initially run this on your real Downloads folder. The program organizes files directly inside the chosen folder and does not recursively move files from subfolders.

## Task 4: FAQ Chatbot
Run:
```bash
python chatbot.py
```
Try: `hello`, `what are your hours?`, `how do I reset my password?`, `what is the refund policy?`, and `bye`.

The FAQ answers are examples. Replace them with accurate details from the intended organization before presenting this as a real customer-support bot.

## Before submitting
- Run every program yourself and fix any errors on your computer.
- Understand the code well enough to explain the main functions.
- Capture genuine screenshots of each program running.
- Create a public GitHub repository if required by the internship portal, upload these files, and paste the repository URL into the portal.
- Check the official task rubric and submit only through the official workspace.
- Keep your own work and do not claim features you have not tested.

These are project implementations, not proof that Datheon has accepted or evaluated the submissions. Certificate eligibility and issuance are determined by Datheon's actual process.
