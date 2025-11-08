import random
import datetime

def get_questions():
    # Traits are mostly based on Big 5, but modified for simplicity
    traits = {
        "Empathy": [
            "I notice when someone is upset even if they don’t say it.",
            "I feel bad if I hurt someone's feelings.",
            "I can easily sense others’ moods.",
            "I get emotional seeing others cry.",
            "I try to understand other people's problems." #5 questions
        ],
        "Logic": [
            "I stay calm even in emotional situations.",
            "I rely on facts more than feelings.",
            "I analyze before deciding.",
            "I solve problems step by step." #4 questions
        ],
        "Morality": [
            "I believe lying is wrong even for good reasons.",
            "I follow rules even when no one is watching.",
            "I feel guilty if I do something unfair.",
            "I care about honesty more than gain.",
            "I admit mistakes even when it’s hard." #5 questions
        ],
        "Impulsiveness": [
            "I speak before thinking sometimes.",
            "I act on feelings instead of plans.",
            "I make quick decisions without thinking much." #3 questions
        ],
        "Anxiety": [
            "I overthink small mistakes.",
            "I get nervous easily.",
            "I worry about what others think of me.",
            "I find it hard to relax.",
            "I panic under stress." #5 questions
        ],
        "Confidence": [
            "I feel comfortable speaking in groups.",
            "I lead when no one else does.",
            "I can make decisions easily.",
            "I stand up for my opinions.",
            "I believe I can handle challenges." #5 questions
        ],
        "Openness": [
            "I enjoy learning new things.",
            "I like meeting different people.",
            "I am curious about how things work.",
            "I like trying new activities.",
            "I am open to different opinions.",
            "I like abstract art." #6 questions
        ],
        "Trust": [
            "I believe most people are honest.",
            "I trust people easily.",
            "I forgive people who wrong me.",
            "I rarely suspect others’ motives.", #4 questions
        ],
        "SelfControl": [
            "I finish tasks I start.",
            "I control my anger even when provoked.",
            "I avoid doing things that harm my goals.",
            "I plan ahead for my work.",
            "I resist temptations easily." #5 questions
        ],
        "RiskTaking": [
            "I like doing things that scare me a bit.",
            "I take risks if I believe in the outcome.",
            "I enjoy challenges others avoid.",
            "I try new experiences without much fear.",
            "I take bold steps even if uncertain." #5 questions
        ]
    }

    #build the full list and shuffle it so questions aren't grouped by trait
    qs = []
    for trait, arr in traits.items():
        for q in arr:
            qs.append((q, trait))
    random.shuffle(qs)
    return qs


def ask(q):
    #loop ensures the user provides valid input, or skips.
    while True:
        print(q)
        print("  1=Strongly disagree  2=Disagree  3=Neutral  4=Agree  5=Strongly agree")
        ans = input("Your answer (1-5, or just press Enter to skip): ").strip()

        #check for skip/empty input
        if not ans:
            sim = random.randint(2, 4) #non-extreme guess
            print(f"-> Skipped. Guessing a neutral answer: {sim}")
            return sim
            
        #check for valid numeric input
        if ans.isdigit():
            n = int(ans)
            if 1 <= n <= 5:
                return n
            else:
                #simple error message
                print("--- Not 1-5. Try again. ---")
        else:
            #simple error message
            print("--- Input must be a number (1-5). Try again. ---")


def analyze(scores):
    results = {}
    #calculate the raw trait percentage
    for trait, values in scores.items():
        avg = sum(values) / len(values)
        #convert the 1-5 scale to a 0-100 percentage.
        results[trait] = round((avg / 5) * 100, 1)

    #derived analysis (simple, readable logic)
    emotional_stability = 100 - results["Anxiety"]
    self_control = (results["SelfControl"] + (100 - results["Impulsiveness"])) / 2
    curiosity = results["Openness"]
    social_conf = (results["Confidence"] + results["Trust"]) / 2
    morality = results["Morality"]

    #summary based on hardcoded thresholds
    summary = []
    if results["Empathy"] > 75 and morality > 70:
        summary.append("You are deeply empathetic and value fairness.")
    if self_control < 45:
        summary.append("You might act on impulses or struggle with self-control.")
    if emotional_stability < 50:
        summary.append("You tend to overthink or get anxious easily.")
    if results["RiskTaking"] > 70:
        summary.append("You are adventurous and comfortable with uncertainty.")
    
    # If no major flags, give a simple general statement.
    if len(summary) == 0:
        summary.append("You seem emotionally balanced and practical overall.")

    profile = {
        "results": results,
        "emotional_stability": round(emotional_stability, 1),
        "self_control": round(self_control, 1),
        "curiosity": round(curiosity, 1),
        "social_conf": round(social_conf, 1),
        "summary": summary
    }
    return profile


def main():
    #the actual number is 43 questions due to the uneven lists, but we leave the old title for flavor.
    print("Welcome to the Personality Analyzer (Simple 50-ish questions)")
    print("This is just for learning purposes, not a clinical test. Enjoy!\n")

    consent = input("\nReady to begin? (y/n): ").strip().lower()
    if consent not in ["y", "yes", "yep"]:
        print("No worries! Come back whenever you're ready.")
        return

    questions = get_questions()
    scores = {}
    total_questions = len(questions)

    #main loop for asking questions
    for i, (q, trait) in enumerate(questions, start=1):
        print(f"\nQuestion {i}/{total_questions} - Trait: {trait}")
        ans = ask(q)
        scores.setdefault(trait, []).append(ans)

    result = analyze(scores)

    # --- REPORT OUTPUT ---
    print("\n\n#####################################")
    print("####### FINAL PSYCHE REPORT #########")
    print("#####################################")
    
    print("\nRaw Trait Percentages (Higher is stronger):")
    for t, v in result["results"].items():
        print(f"  > {t:<15}: {v}%") # Use f-string formatting for neatness

    print("\nDerived Traits:")
    print(f"  > Emotional Stability: {result['emotional_stability']}%")
    print(f"  > Self Control: {result['self_control']}%")
    print(f"  > Curiosity (Openness): {result['curiosity']}%")
    print(f"  > Social Confidence: {result['social_conf']}%")

    print("\nSummary & Notes:")
    for line in result["summary"]:
        print(" -", line)

    #optional save (Simple file write without heavy error handling)
    save = input("\nSave this profile to a text file? (y/n): ").strip().lower()
    if save in ["y", "yes"]:
        filename = f"profile_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        # We'll use simple file writing here, skipping the try/except for a "quick code" feel
        with open(filename, "w", encoding="utf-8") as f:
            f.write("PERSONALITY REPORT\n\n")
            f.write("RAW TRAITS:\n")
            for t, v in result["results"].items():
                f.write(f"{t}: {v}%\n")
            f.write("\nSUMMARY:\n")
            for line in result["summary"]:
                f.write(" - " + line + "\n")
        print("--- Saved successfully as", filename, "---")

    print("\nDone! Don't overthink the results;\n")


if __name__ == "__main__":
    main()
