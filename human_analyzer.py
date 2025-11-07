import random

def get_score(ans):
    # order: logic, empathy, morality, darkness
    if ans == 1:
        return (10, 3, 10, 1)
    elif ans == 2:
        return (4, 10, 7, 2)
    elif ans == 3:
        return (6, 4, 5, 6)
    elif ans == 4:
        return (9, 0, 1, 12)
    else:
        return (0, 0, 0, 0)  # should never hit but just in case


def get_questions():
    q = [
        "If you saw someone commit a small crime, what would you do?",
        "Would you kill a friend to save five others?",
        "Do you lie easily when needed?",
        "When you argue, you usually...",
        "You believe people are mostly..."
    ]

    a = [
        ["Report them immediately", "Confront them", "Ignore it", "Use it to your advantage"],
        ["Yes, logically it's better", "No, it's wrong", "Depends on who they are", "I would rather not choose"],
        ["Never", "Sometimes", "Often", "Only when it benefits me"],
        ["Use facts and logic", "Appeal emotionally", "Stay silent", "Twist the other person’s logic"],
        ["Good", "Neutral", "Driven by self-interest", "Evil in disguise"]
    ]

    pairs = []
    for i in range(len(q)):
        pairs.append((q[i], a[i]))
    return pairs


def ask_choice():
    try:
        c = input("Choose (1-4): ").strip()
        if c.isdigit():
            val = int(c)
            if 1 <= val <= 4:
                return val
    except:
        # not gonna crash over invalid input
        pass
    return random.choice([1, 2, 3, 4]) 


def main():
    print("Be honest in answering. If you skip, I'll guess for you.\n")

    qs = get_questions()
    logic = empathy = morality = dark = 0

    for i, (question, options) in enumerate(qs):
        print(f"{i+1}. {question}")
        for j, opt in enumerate(options):
            print(f"  {j+1}. {opt}")
        ans = ask_choice()
        print("-> You picked:", ans, "\n")

        l, e, m, d = get_score(ans)
        logic += l
        empathy += e
        morality += m
        dark += d

    n = len(qs)
    # quick math to get % values
    logic_pct = (logic / (n * 10)) * 100
    empathy_pct = (empathy / (n * 10)) * 100
    morality_pct = (morality / (n * 10)) * 100
    dark_pct = (dark / (n * 12)) * 100

    # random-ish weights I decided on
    idx = (dark_pct * 0.5) + (logic_pct * 0.25) - (empathy_pct * 0.15) - (morality_pct * 0.1)
    idx = int(max(0, min(100, round(idx))))

    # classification — not perfect but fine
    if idx > 70:
        type_ = "Strategist"
    elif idx > 50:
        type_ = "Realist"
    elif idx > 25:
        type_ = "Empath"
    else:
        type_ = random.choice(["Idealist", "Dreamer"])

    print("\n--- PSYCHE REPORT ---")
    print(f"Logic: {logic} | Empathy: {empathy} | Morality: {morality} | Darkness: {dark}")
    print(f"Darkness Index: {idx}")
    print(f"Archetype: {type_}")
 
if __name__ == "__main__":
    main()
