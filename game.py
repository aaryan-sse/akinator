import json
import os

DB_FILE = "akinator_db.json"

# Create default database if missing
def load_db():
    if not os.path.exists(DB_FILE):
        return {
            "question": "Is your character real?",
            "yes": {"guess": "Albert Einstein"},
            "no": {"guess": "Batman"}
        }
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)

def ask(question):
    while True:
        ans = input(question + " (yes/no): ").strip().lower()
        if ans in ["yes", "no", "y", "n"]:
            return ans.startswith("y")
        print("Please answer yes or no.")

def play(node):
    # If this is a guess node
    if "guess" in node:
        if ask(f"Is your character {node['guess']}?"):
            print("🎉 I guessed it!")
            return
        else:
            print("😢 I couldn't guess.")

            # Learn new character
            new_char = input("Who was your character? ")
            new_q = input(
                f"Give me a question that is YES for {new_char} "
                f"and NO for {node['guess']}: "
            )

            # Build a new question node
            node.update({
                "question": new_q,
                "yes": {"guess": new_char},
                "no": {"guess": node["guess"]},
            })
            # Remove old guess key
            if "guess" in node:
                del node["guess"]
            print("👍 I learned a new character!")
            return

    # If this is a question node
    if ask(node["question"]):
        play(node["yes"])
    else:
        play(node["no"])

def main():
    print("=== Akinator Python Clone ===")
    db = load_db()
    play(db)
    save_db(db)
    print("📁 Knowledge saved!")

if __name__ == "__main__":
    main()
