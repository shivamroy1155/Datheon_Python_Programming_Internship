"""Console Hangman game. Run with: python hangman.py"""
import random

WORDS = ["PYTHON", "AUTOMATION", "GITHUB", "VARIABLE", "FUNCTION", "PROGRAMMING", "COMPUTER"]
MAX_MISTAKES = 6

STAGES = [
r"""
 +---+
 |   |
     |
     |
     |
     |
=========""",
r"""
 +---+
 |   |
 O   |
     |
     |
     |
=========""",
r"""
 +---+
 |   |
 O   |
 |   |
     |
     |
=========""",
r"""
 +---+
 |   |
 O   |
/|   |
     |
     |
=========""",
r"""
 +---+
 |   |
 O   |
/|\  |
     |
     |
=========""",
r"""
 +---+
 |   |
 O   |
/|\  |
/    |
     |
=========""",
r"""
 +---+
 |   |
 O   |
/|\  |
/ \  |
     |
=========""",
]


def display_word(secret, guessed):
    return " ".join(letter if letter in guessed else "_" for letter in secret)


def play():
    secret = random.choice(WORDS)
    guessed = set()
    wrong = set()

    print("\n=== HANGMAN ===")
    print(f"You have {MAX_MISTAKES} incorrect guesses. Enter one letter at a time.")

    while len(wrong) < MAX_MISTAKES:
        print(STAGES[len(wrong)])
        print("\nWord:", display_word(secret, guessed))
        print("Guessed:", " ".join(sorted(guessed | wrong)) or "(none)")
        guess = input("Your guess (or 'quit'): ").strip().upper()

        if guess == "QUIT":
            print(f"Game ended. The word was {secret}.")
            return
        if len(guess) != 1 or not guess.isalpha() or not guess.isascii():
            print("Please enter one English letter.")
            continue
        if guess in guessed or guess in wrong:
            print("You already guessed that letter; no penalty.")
            continue

        if guess in secret:
            guessed.add(guess)
            print("Correct!")
            if all(letter in guessed for letter in secret):
                print(f"\n🎉 You won! The word was {secret}.")
                return
        else:
            wrong.add(guess)
            print("Incorrect!")

    print(STAGES[MAX_MISTAKES])
    print(f"\nGame over. The word was {secret}.")


if __name__ == "__main__":
    play()
