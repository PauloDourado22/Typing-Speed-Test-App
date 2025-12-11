import tkinter as tk
import time
import random
from dictionary import TEST_DICT
import json
import os

SCORE_FILE = "score.json"
HISTORY_LIMIT = 5  # Number of most recent scores
test_running = False
start_time = None
words_list = []

# --------------------------
# SCORE MANAGEMENT
# --------------------------
def load_scores():
    if not os.path.exists(SCORE_FILE):
        return {"highscore": 0.0, "history": []}
    with open(SCORE_FILE, "r") as file:
        data = json.load(file)
    data["highscore"] = float(data.get("highscore", 0))
    data["history"] = [float(score) for score in data.get("history", [])]
    return data

def save_score(scores_dict):
    with open(SCORE_FILE, "w") as file:
        json.dump(scores_dict, file, indent=4)

def update_scores(wpm):
    wpm = float(wpm)
    # Update highscore if needed
    if wpm > float(scores.get("highscore", 0)):
        scores["highscore"] = wpm
    # Add to history
    scores.setdefault("history", []).append(wpm)
    if len(scores["history"]) > HISTORY_LIMIT:
        scores["history"] = scores["history"][-HISTORY_LIMIT:]
    # Save to JSON
    save_score(scores)

def update_scores_labels():
    highscore = scores.get("highscore", 0.0)
    highscore_label.config(text=f"Highscore: {highscore:.2f} WPM")

    history = scores.get("history", [])
    if not history:
        history_label.config(text="")
        score_frame.grid_configure(pady=5)
        return

    history_text = "Last Scores:\n" + "\n".join(f"{val:.2f} WPM" for val in history)
    history_label.config(text=history_text)
    score_frame.grid_configure(pady=20)

# --------------------------
# TYPING TEST FUNCTIONS
# --------------------------
def random_word(n=10):
    return " ".join(random.choice(TEST_DICT) for _ in range(n))

def display_words():
    label.config(state="normal")
    label.delete("1.0", tk.END)
    for i, word in enumerate(words_list):
        label.insert(tk.END, word)
        if i != len(words_list) - 1:
            label.insert(tk.END, " ")
    label.tag_config("completed", foreground="green")
    label.config(state="disabled")

def refresh_words():
    global start_time, words_list, test_running
    start_time = None
    test_running = False
    words_list = random_word(n=10).split()
    display_words()
    input_box.delete("1.0", tk.END)
    input_box.config(state="disabled")
    start_btn.config(state="normal")
    finish_btn.config(state="disabled")
    result_label.config(text="")
    update_scores_labels()
    root.focus_set()

def start_test():
    global start_time, test_running
    input_box.config(state="normal")
    input_box.focus_set()
    start_time = time.time()
    test_running = True
    start_btn.config(state="disabled")
    finish_btn.config(state="normal")

def finish_test():
    global start_time, test_running
    if start_time is None:
        return

    typed_text = input_box.get("1.0", tk.END).strip()
    if not typed_text:
        wpm = 0.0
    else:
        elapsed_time = max(time.time() - start_time, 0.01)  # avoid division by zero
        word_count = len(typed_text.split())
        wpm = word_count / (elapsed_time / 60)

    # Load latest scores from JSON to avoid stale data
    latest_scores = load_scores()

    # Update highscore if current WPM exceeds previous
    if wpm > latest_scores.get("highscore", 0):
        latest_scores["highscore"] = wpm

    # Update history (keep last N)
    latest_scores.setdefault("history", []).append(wpm)
    if len(latest_scores["history"]) > HISTORY_LIMIT:
        latest_scores["history"] = latest_scores["history"][-HISTORY_LIMIT:]

    # Save back to JSON
    save_score(latest_scores)

    # Update in-memory scores dict and labels
    global scores
    scores = latest_scores
    update_scores_labels()

    # Show result
    result_label.config(text=f"Your typing speed is: {wpm:.2f} WPM")

    # Reset state
    test_running = False
    start_time = None
    finish_btn.config(state="disabled")
    start_btn.config(state="normal")



def on_typing(event):
    typed_text = input_box.get("1.0", tk.END).strip()
    typed_words = typed_text.split()
    label.config(state="normal")
    label.tag_remove("completed", "1.0", tk.END)

    for i, word in enumerate(typed_words):
        if i < len(words_list) and word == words_list[i]:
            start_index = f"1.0 + {sum(len(w)+1 for w in words_list[:i])} chars"
            end_index = f"1.0 + {sum(len(w)+1 for w in words_list[:i+1])-1} chars"
            label.tag_add("completed", start_index, end_index)

    label.config(state="disabled")

def handle_enter(event):
    global test_running
    if not test_running and input_box["state"] == "disabled":
        start_test()
    else:
        finish_test()

# --------------------------
# INITIALIZE SCORES
# --------------------------
scores = load_scores()

# --------------------------
# GUI SETUP
# --------------------------
root = tk.Tk()
root.title("Typing Speed Test")
root.geometry("600x500")
root.bind("<Return>", handle_enter)

# Root layout
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

main = tk.Frame(root)
main.grid(row=0, column=0, sticky="nsew")
main.grid_rowconfigure(0, weight=0)
main.grid_rowconfigure(1, weight=1)
main.grid_rowconfigure(2, weight=0)
main.grid_columnconfigure(0, weight=1)

# TOP AREA
top_frame = tk.Frame(main)
top_frame.grid(row=0, column=0, pady=10)
new_words_btn = tk.Button(top_frame, text="New Words", command=refresh_words)
new_words_btn.pack()

# CENTER AREA
center_frame = tk.Frame(main)
center_frame.grid(row=1, column=0, sticky="n", pady=10)
center_frame.grid_columnconfigure(0, weight=1)

label = tk.Text(center_frame, height=2, width=60, font=("Arial", 20), wrap="word", bd=0, bg=root.cget("bg"))
label.grid(row=0, column=0, pady=10)
label.config(state="disabled")

input_box = tk.Text(center_frame, height=5, width=60, font=("Arial", 12), state="disabled")
input_box.grid(row=1, column=0, pady=10)
input_box.bind("<KeyRelease>", on_typing)

# Buttons
btn_frame = tk.Frame(center_frame)
btn_frame.grid(row=2, column=0, pady=10)

start_btn = tk.Button(btn_frame, text="Start", command=start_test)
start_btn.grid(row=0, column=0, padx=5)

finish_btn = tk.Button(btn_frame, text="Finish", command=finish_test, state="disabled")
finish_btn.grid(row=0, column=1, padx=5)

result_label = tk.Label(center_frame, text="", font=("Arial", 12, "bold"))
result_label.grid(row=3, column=0)

# SCORE AREA
score_frame = tk.Frame(center_frame)
score_frame.grid(row=4, column=0, pady=5)

highscore_label = tk.Label(score_frame, text="", font=("Arial", 14, "bold"))
highscore_label.grid(row=0, column=0)

history_label = tk.Label(score_frame, text="", font=("Arial", 12))
history_label.grid(row=1, column=0)

# BOTTOM AREA
bottom_frame = tk.Frame(main)
bottom_frame.grid(row=2, column=0, pady=10)
bottom_frame.grid_columnconfigure(0, weight=1)

# --------------------------
# INITIALIZE WORDS AND LABELS
# --------------------------
refresh_words()
update_scores_labels()

root.mainloop()

