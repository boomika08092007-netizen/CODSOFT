"""
╔══════════════════════════════════════════════════════════╗
║           NUMBER GUESSING GAME  🎯                       ║
║   Guess the secret number and rack up points!            ║
╚══════════════════════════════════════════════════════════╝
"""

import random
import time

# ─────────────────────────────────────────────
#  Configuration
# ─────────────────────────────────────────────
RANGE_MIN       = 1
RANGE_MAX       = 100
MAX_ATTEMPTS    = 5          # Change this to adjust difficulty


# ─────────────────────────────────────────────
#  Helper: pretty banner
# ─────────────────────────────────────────────
def print_banner() -> None:
    """Print the game welcome banner."""
    print("\n" + "═" * 58)
    print("  🎯  NUMBER GUESSING GAME  🎯")
    print(f"  Guess a number between {RANGE_MIN} and {RANGE_MAX}.")
    print(f"  You have {MAX_ATTEMPTS} attempts per round.")
    print("═" * 58 + "\n")


# ─────────────────────────────────────────────
#  Helper: score calculator
#  Fewer attempts used → higher score
#  Score = MAX_ATTEMPTS - (attempts_used - 1)
#  Bonus: first-try gets a big bonus!
# ─────────────────────────────────────────────
def calculate_score(attempts_used: int) -> int:
    """Return score based on how quickly the player guessed."""
    if attempts_used == 1:
        return MAX_ATTEMPTS * 2          # Lucky first-guess bonus 🎉
    return max(0, MAX_ATTEMPTS - (attempts_used - 1))


# ─────────────────────────────────────────────
#  Helper: safe integer input
# ─────────────────────────────────────────────
def get_integer_input(prompt: str, lo: int, hi: int) -> int:
    """Prompt the user until a valid integer in [lo, hi] is entered."""
    while True:
        raw = input(prompt).strip()
        if raw.lstrip("-").isdigit():
            value = int(raw)
            if lo <= value <= hi:
                return value
            print(f"  ⚠️  Please enter a number between {lo} and {hi}.\n")
        else:
            print("  ⚠️  That doesn't look like a number. Try again.\n")


# ─────────────────────────────────────────────
#  Core: play a single round
#  Returns score earned (0 if round is lost)
# ─────────────────────────────────────────────
def play_round(round_num: int) -> int:
    """
    Run one complete round of the game.

    Returns:
        Score earned this round (0 if the player didn't guess correctly).
    """
    secret = random.randint(RANGE_MIN, RANGE_MAX)
    print(f"\n  ── Round {round_num} ──")
    print("  A secret number has been chosen. Good luck!\n")

    for attempt in range(1, MAX_ATTEMPTS + 1):
        remaining = MAX_ATTEMPTS - attempt + 1
        label = "attempt" if remaining == 1 else "attempts"
        print(f"  [{remaining} {label} remaining]")

        guess = get_integer_input(f"  Your guess: ", RANGE_MIN, RANGE_MAX)

        if guess == secret:
            score = calculate_score(attempt)
            print(f"\n  ✅  Correct! The number was {secret}.")
            if attempt == 1:
                print("  🎉 First-try bonus!")
            print(f"  You got it in {attempt} attempt{'s' if attempt > 1 else ''}.")
            print(f"  Points earned this round: +{score}\n")
            return score

        elif guess > secret:
            print("  🔻 Too High!\n")
        else:
            print("  🔺 Too Low!\n")

    # Player ran out of attempts
    print(f"\n  ❌ Out of attempts! The number was {secret}.")
    print("  Better luck next round!\n")
    return 0


# ─────────────────────────────────────────────
#  Helper: display scoreboard
# ─────────────────────────────────────────────
def show_scoreboard(rounds_played: int, rounds_won: int, total_score: int) -> None:
    """Print a summary scoreboard."""
    win_rate = (rounds_won / rounds_played * 100) if rounds_played else 0

    print("\n" + "─" * 40)
    print("       📊  SCOREBOARD")
    print("─" * 40)
    print(f"  Rounds played : {rounds_played}")
    print(f"  Rounds won    : {rounds_won}")
    print(f"  Win rate      : {win_rate:.1f}%")
    print(f"  Total score   : {total_score}")
    print("─" * 40 + "\n")


# ─────────────────────────────────────────────
#  Main game loop
# ─────────────────────────────────────────────
def main() -> None:
    """Entry point – manages the multi-round session."""
    print_banner()
    time.sleep(0.5)

    rounds_played = 0
    rounds_won    = 0
    total_score   = 0

    while True:
        rounds_played += 1
        score = play_round(rounds_played)

        total_score += score
        if score > 0:
            rounds_won += 1

        show_scoreboard(rounds_played, rounds_won, total_score)

        # Ask to play again
        again = input("  🔄  Do you want to play again? (yes / no): ").strip().lower()
        if again not in ("yes", "y"):
            break

    # Final farewell
    print("\n" + "═" * 58)
    print("  Thanks for playing!  Here's your final summary:\n")
    show_scoreboard(rounds_played, rounds_won, total_score)

    if rounds_won == rounds_played:
        print("  🏆 Perfect game – you won every round!")
    elif rounds_won > rounds_played // 2:
        print("  🥈 Great job – you won more than half your rounds!")
    elif rounds_won > 0:
        print("  🥉 Keep practising – you'll get better!")
    else:
        print("  💪 Don't give up – try again!")

    print("\n  Goodbye! 👋")
    print("═" * 58 + "\n")


# ─────────────────────────────────────────────
#  Entry point guard
# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()
