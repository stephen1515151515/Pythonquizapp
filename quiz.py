"""
╔══════════════════════════════════════════════════════════╗
║          AI QUIZ GENERATOR — THINK CHAMP PV LTD          ║
║                  Internship Mini Project                  ║
╚══════════════════════════════════════════════════════════╝

Features:
  ✅ Colorful terminal UI using colorama
  ✅ 15 questions across 5 categories
  ✅ Multiple choice (A/B/C/D)
  ✅ Per-question countdown timer
  ✅ Difficulty levels (Easy / Medium / Hard)
  ✅ Streak tracking (🔥)
  ✅ Score saved to scores.txt
  ✅ Detailed result summary
  ✅ Play again without restarting
"""

import os
import sys
import time
import random
import threading
from datetime import datetime

# ── Try to import colorama ──────────────────────────────────
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORS = True
except ImportError:
    COLORS = False
    # Create dummy color objects if colorama not installed
    class _Dummy:
        def __getattr__(self, _): return ""
    Fore = Back = Style = _Dummy()

# ═══════════════════════════════════════════════════════════
#  COLOR HELPERS
# ═══════════════════════════════════════════════════════════
def c(text, color=Fore.WHITE, bold=False):
    b = Style.BRIGHT if bold else ""
    return f"{b}{color}{text}{Style.RESET_ALL}"

def success(t): return c(t, Fore.GREEN, bold=True)
def error(t):   return c(t, Fore.RED,   bold=True)
def warn(t):    return c(t, Fore.YELLOW, bold=True)
def info(t):    return c(t, Fore.CYAN,  bold=True)
def accent(t):  return c(t, Fore.MAGENTA, bold=True)
def dim(t):     return c(t, Fore.WHITE)

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

# ═══════════════════════════════════════════════════════════
#  QUESTIONS DATABASE
# ═══════════════════════════════════════════════════════════
QUESTIONS = [
    {
        "q": "What does CPU stand for?",
        "opts": ["Central Process Unit", "Central Processing Unit",
                 "Computer Personal Unit", "Core Processing Utility"],
        "a": "B", "diff": "easy", "cat": "Computer Basics"
    },
    {
        "q": "Which language is known as the 'mother of all programming languages'?",
        "opts": ["Python", "Java", "C", "Assembly"],
        "a": "C", "diff": "easy", "cat": "Programming"
    },
    {
        "q": "What does HTML stand for?",
        "opts": ["HyperText Markup Language", "High Tech Modern Language",
                 "HyperTransfer Markup Language", "HyperText Module Language"],
        "a": "A", "diff": "easy", "cat": "Web"
    },
    {
        "q": "What is the output of:  print(2 ** 3)  in Python?",
        "opts": ["6", "8", "9", "16"],
        "a": "B", "diff": "easy", "cat": "Python"
    },
    {
        "q": "Which data structure works on LIFO (Last In First Out) principle?",
        "opts": ["Queue", "Stack", "Array", "Linked List"],
        "a": "B", "diff": "medium", "cat": "Data Structures"
    },
    {
        "q": "What does AI stand for?",
        "opts": ["Automated Input", "Artificial Intelligence",
                 "Automated Intelligence", "Advanced Interface"],
        "a": "B", "diff": "easy", "cat": "AI/ML"
    },
    {
        "q": "Which keyword is used to define a function in Python?",
        "opts": ["function", "define", "def", "fun"],
        "a": "C", "diff": "easy", "cat": "Python"
    },
    {
        "q": "What is the full form of RAM?",
        "opts": ["Read Access Memory", "Random Access Memory",
                 "Run Access Memory", "Read And Memory"],
        "a": "B", "diff": "easy", "cat": "Computer Basics"
    },
    {
        "q": "Which symbol is used for single-line comments in Python?",
        "opts": ["//", "<!-- -->", "#", "--"],
        "a": "C", "diff": "easy", "cat": "Python"
    },
    {
        "q": "What is Machine Learning?",
        "opts": ["A type of hardware", "A subset of AI that learns from data",
                 "A programming language", "A database system"],
        "a": "B", "diff": "medium", "cat": "AI/ML"
    },
    {
        "q": "What does SQL stand for?",
        "opts": ["Structured Query Language", "Simple Query Language",
                 "System Query Language", "Structured Question Language"],
        "a": "A", "diff": "medium", "cat": "Database"
    },
    {
        "q": "Which of the following is NOT a Python built-in data type?",
        "opts": ["list", "tuple", "char", "dict"],
        "a": "C", "diff": "medium", "cat": "Python"
    },
    {
        "q": "What is a neural network inspired by?",
        "opts": ["The human brain", "Computer circuits",
                 "Mathematical equations", "DNA structure"],
        "a": "A", "diff": "medium", "cat": "AI/ML"
    },
    {
        "q": "What is the time complexity of binary search?",
        "opts": ["O(n)", "O(n²)", "O(log n)", "O(1)"],
        "a": "C", "diff": "hard", "cat": "Algorithms"
    },
    {
        "q": "In Python, which method adds an element to the end of a list?",
        "opts": ["add()", "push()", "append()", "insert()"],
        "a": "C", "diff": "easy", "cat": "Python"
    },
]

# ═══════════════════════════════════════════════════════════
#  UI COMPONENTS
# ═══════════════════════════════════════════════════════════
WIDTH = 60

def divider(char="─", color=Fore.MAGENTA):
    print(c(char * WIDTH, color))

def box_top(color=Fore.MAGENTA):
    print(c("╔" + "═" * (WIDTH - 2) + "╗", color))

def box_bot(color=Fore.MAGENTA):
    print(c("╚" + "═" * (WIDTH - 2) + "╝", color))

def box_line(text, color=Fore.MAGENTA, text_color=Fore.WHITE):
    pad = WIDTH - 4 - len(text)
    print(c("║ ", color) + c(text, text_color, bold=True) + " " * pad + c(" ║", color))

def print_banner():
    clear()
    print()
    box_top()
    box_line("  🧠  AI QUIZ GENERATOR", text_color=Fore.CYAN)
    box_line("  Think Champ PV Ltd — Internship Project", text_color=Fore.WHITE)
    box_bot()
    print()

def progress_bar(current, total, width=40):
    filled = int((current / total) * width)
    bar = "█" * filled + "░" * (width - filled)
    pct = int((current / total) * 100)
    print(f"  {c(bar, Fore.MAGENTA)}  {c(str(pct) + '%', Fore.CYAN, bold=True)}")

def diff_badge(diff):
    colors = {"easy": Fore.GREEN, "medium": Fore.YELLOW, "hard": Fore.RED}
    icons  = {"easy": "🟢", "medium": "🟡", "hard": "🔴"}
    return f"{icons.get(diff,'')} {c(diff.upper(), colors.get(diff, Fore.WHITE), bold=True)}"

# ═══════════════════════════════════════════════════════════
#  TIMER (threaded)
# ═══════════════════════════════════════════════════════════
class QuizTimer:
    def __init__(self, seconds):
        self.total = seconds
        self.remaining = seconds
        self.expired = False
        self._stop = threading.Event()

    def start(self):
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        while self.remaining > 0 and not self._stop.is_set():
            time.sleep(1)
            self.remaining -= 1
        if not self._stop.is_set():
            self.expired = True

    def stop(self):
        self._stop.set()

    def status(self):
        r = self.remaining
        if r > 10:   return c(f"⏱  {r}s", Fore.GREEN, bold=True)
        elif r > 5:  return c(f"⏱  {r}s", Fore.YELLOW, bold=True)
        else:        return c(f"⏱  {r}s !!!", Fore.RED, bold=True)


# ═══════════════════════════════════════════════════════════
#  SCORE SAVING
# ═══════════════════════════════════════════════════════════
SCORES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scores.txt")

def save_score(score, total, time_taken):
    pct  = round((score / total) * 100)
    line = (f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]  "
            f"Score: {score}/{total}  ({pct}%)  Time: {time_taken}s\n")
    with open(SCORES_FILE, "a", encoding="utf-8") as f:
        f.write(line)
    return line.strip()

def load_high_score():
    if not os.path.exists(SCORES_FILE):
        return 0, 0
    best = 0
    best_pct = 0
    try:
        with open(SCORES_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if "Score:" in line:
                    part = line.split("Score:")[1].split()[0]  # e.g. "7/10"
                    num, den = part.split("/")
                    pct = round(int(num) / int(den) * 100)
                    if pct > best_pct:
                        best_pct = pct
                        best = int(num)
    except Exception:
        pass
    return best, best_pct


# ═══════════════════════════════════════════════════════════
#  MENU
# ═══════════════════════════════════════════════════════════
def choose_difficulty():
    print(info("\n  Select Difficulty:"))
    print(f"  {c('[1]', Fore.CYAN)} {diff_badge('easy')}")
    print(f"  {c('[2]', Fore.CYAN)} {diff_badge('medium')}")
    print(f"  {c('[3]', Fore.CYAN)} {diff_badge('hard')}")
    print(f"  {c('[4]', Fore.CYAN)} 🌐 All Levels")
    while True:
        choice = input(f"\n  {c('Your choice (1-4): ', Fore.CYAN)}").strip()
        if choice == "1": return "easy"
        if choice == "2": return "medium"
        if choice == "3": return "hard"
        if choice == "4": return "all"
        print(warn("  ⚠  Enter 1, 2, 3 or 4"))

def choose_num_questions(pool):
    max_q = len(pool)
    print(info(f"\n  How many questions? (max {max_q})"))
    while True:
        try:
            n = int(input(f"  {c('Number (5–' + str(max_q) + '): ', Fore.CYAN)}").strip())
            if 1 <= n <= max_q:
                return n
            print(warn(f"  ⚠  Enter a number between 1 and {max_q}"))
        except ValueError:
            print(warn("  ⚠  Please enter a valid number"))


# ═══════════════════════════════════════════════════════════
#  MAIN QUIZ LOOP
# ═══════════════════════════════════════════════════════════
def run_quiz():
    print_banner()

    hs, hs_pct = load_high_score()
    if hs > 0:
        print(f"  🏆  High Score: {success(str(hs_pct) + '%')}  ({hs} correct)\n")

    print(accent("  Welcome to the AI Quiz Generator! 🎉"))
    print(dim("  Answer A/B/C/D within the time limit.\n"))

    diff = choose_difficulty()
    pool = [q for q in QUESTIONS if diff == "all" or q["diff"] == diff]
    random.shuffle(pool)

    if len(pool) < 5:
        print(warn("\n  Not enough questions for this difficulty. Switching to All."))
        pool = QUESTIONS[:]
        random.shuffle(pool)

    num_q = choose_num_questions(pool)
    questions = pool[:num_q]

    # ── Countdown ─────────────────────────────────────────
    print()
    for i in range(3, 0, -1):
        sys.stdout.write(f"\r  {accent('Starting in...')} {c(str(i), Fore.YELLOW, bold=True)} ")
        sys.stdout.flush()
        time.sleep(1)
    print(f"\r  {success('GO! 🚀')}                      ")
    time.sleep(0.5)

    # ── Quiz variables ─────────────────────────────────────
    score    = 0
    streak   = 0
    max_streak = 0
    wrong_qs = []
    start_time = time.time()
    TIMER_SECS = 15

    for idx, qdata in enumerate(questions):
        clear()
        print_banner()

        # Progress
        print(f"  Question {c(str(idx+1), Fore.CYAN, bold=True)} of {c(str(num_q), Fore.CYAN, bold=True)}  │  "
              f"Score: {success(str(score))}  │  "
              f"Streak: {c('🔥 ' + str(streak) if streak >= 3 else str(streak), Fore.YELLOW if streak>=3 else Fore.WHITE)}")
        progress_bar(idx, num_q)
        print()

        # Category + Difficulty
        print(f"  📂 {c(qdata['cat'], Fore.CYAN)}  {diff_badge(qdata['diff'])}")
        divider()

        # Question
        print(f"\n  {c('Q' + str(idx+1) + '.', Fore.MAGENTA, bold=True)} {c(qdata['q'], Fore.WHITE, bold=True)}\n")

        # Options (shuffled display)
        labels = ["A", "B", "C", "D"]
        opts_indexed = list(enumerate(qdata["opts"]))  # [(0,text), ...]
        random.shuffle(opts_indexed)
        orig_to_label = {}  # original index → shuffled label
        for label_i, (orig_i, text) in enumerate(opts_indexed):
            orig_to_label[orig_i] = labels[label_i]
            print(f"    {c('[' + labels[label_i] + ']', Fore.CYAN, bold=True)}  {text}")

        # Correct label in shuffled context
        correct_orig_idx = labels.index(qdata["a"])  # original correct index 0–3
        correct_label = orig_to_label[correct_orig_idx]

        print()

        # Timer
        timer = QuizTimer(TIMER_SECS)
        timer.start()

        # Input (show timer status)
        answer = None
        while True:
            sys.stdout.write(f"\r  {timer.status()}    {c('Your answer (A/B/C/D): ', Fore.CYAN)}")
            sys.stdout.flush()
            if timer.expired:
                print()
                break

            # Non-blocking read attempt (Windows compatible)
            if os.name == 'nt':
                import msvcrt
                if msvcrt.kbhit():
                    ch = msvcrt.getwch().upper()
                    if ch in ["A","B","C","D"]:
                        print(ch)
                        answer = ch
                        timer.stop()
                        break
            else:
                import select
                r, _, _ = select.select([sys.stdin], [], [], 0.5)
                if r:
                    raw = sys.stdin.readline().strip().upper()
                    if raw in ["A","B","C","D"]:
                        answer = raw
                        timer.stop()
                        break
                    elif raw:
                        print(warn("  ⚠  Enter A, B, C or D"))

            time.sleep(0.5)

        timer.stop()

        # ── Evaluate ───────────────────────────────────────
        print()
        divider(char="─", color=Fore.WHITE)

        if timer.expired and answer is None:
            print(warn("  ⏰  Time's up! You ran out of time."))
            correct_text = qdata["opts"][labels.index(qdata["a"])]
            print(f"  ✅  Correct answer was: {success('[' + correct_label + '] ' + correct_text)}")
            streak = 0
            wrong_qs.append({"q": qdata["q"], "your": "(Time Out)", "correct": correct_text})
        elif answer == correct_label:
            score += 1
            streak += 1
            max_streak = max(max_streak, streak)
            print(success("  ✅  CORRECT! Well done! 🎉"))
            if streak >= 3:
                print(c(f"  🔥  {streak} in a row! You're on fire!", Fore.YELLOW, bold=True))
        else:
            correct_text = qdata["opts"][labels.index(qdata["a"])]
            print(error("  ❌  WRONG!"))
            print(f"  ✅  Correct answer: {success('[' + correct_label + '] ' + correct_text)}")
            streak = 0
            your_text = "(No answer)" if answer is None else qdata["opts"][labels.index(answer)] if answer in labels else answer
            wrong_qs.append({"q": qdata["q"], "your": your_text, "correct": correct_text})

        print()
        input(c("  Press ENTER to continue...", Fore.MAGENTA))

    # ═══════════════════════════════════════════════════════
    #  RESULTS
    # ═══════════════════════════════════════════════════════
    total_time = round(time.time() - start_time)
    pct = round((score / num_q) * 100)
    saved = save_score(score, num_q, total_time)

    clear()
    print_banner()
    print()
    box_top(Fore.YELLOW)
    box_line("  🏆  QUIZ COMPLETE — FINAL RESULTS", text_color=Fore.YELLOW)
    box_bot(Fore.YELLOW)
    print()

    # Grade
    if pct == 100:
        grade_txt = "S RANK — PERFECT! 🏆🌟"
        grade_col = Fore.YELLOW
    elif pct >= 80:
        grade_txt = "A RANK — EXCELLENT! 🌟"
        grade_col = Fore.GREEN
    elif pct >= 60:
        grade_txt = "B RANK — GOOD JOB! 👍"
        grade_col = Fore.CYAN
    elif pct >= 40:
        grade_txt = "C RANK — KEEP LEARNING 📚"
        grade_col = Fore.YELLOW
    else:
        grade_txt = "D RANK — DON'T GIVE UP! 💪"
        grade_col = Fore.RED

    print(f"  {c(grade_txt, grade_col, bold=True)}\n")
    print(f"  📊  Score      : {success(str(score) + ' / ' + str(num_q))}  ({c(str(pct) + '%', grade_col, bold=True)})")
    print(f"  ❌  Wrong      : {error(str(len(wrong_qs)))}")
    print(f"  ⏱   Time Taken : {info(str(total_time) + ' seconds')}")
    print(f"  🔥  Best Streak: {c(str(max_streak), Fore.YELLOW, bold=True)}")
    print()

    # Visual bar
    filled = int((score / num_q) * 30)
    bar = "█" * filled + "░" * (30 - filled)
    print(f"  {c(bar, grade_col)}  {c(str(pct) + '%', grade_col, bold=True)}")
    print()

    # Wrong answers review
    if wrong_qs:
        divider(char="─")
        print(warn("  📋  Review — Questions You Missed:\n"))
        for i, item in enumerate(wrong_qs, 1):
            print(f"  {c(str(i) + '.', Fore.CYAN)} {item['q']}")
            print(f"     Your answer : {error(item['your'])}")
            print(f"     Correct      : {success(item['correct'])}")
            print()

    divider(char="─")
    print(f"  💾  Score saved to: {c('scores.txt', Fore.CYAN)}")
    print(f"  {dim(saved)}")
    print()

    # Play again?
    again = input(c("  🔄  Play again? (y/n): ", Fore.MAGENTA)).strip().lower()
    if again in ("y", "yes"):
        return True
    return False


# ═══════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    if not COLORS:
        print("TIP: Install colorama for a colorful experience: pip install colorama\n")

    while True:
        try:
            play_again = run_quiz()
            if not play_again:
                clear()
                print()
                print(accent("  Thanks for playing! — Think Champ PV Ltd 🎓"))
                print(dim("  Keep learning and coding! 🚀"))
                print()
                break
        except KeyboardInterrupt:
            print(f"\n\n{warn('  Quiz interrupted. Goodbye! 👋')}\n")
            break
