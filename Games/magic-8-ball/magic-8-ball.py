#!/data/data/com.termux/files/usr/bin/python

import random

def magic_8_ball():
    responses = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes - definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful.",
        "Definitely not.",
        "The answer is hiding inside you.",
        "It's better not to know.",
        "Focus and ask again.",
        "Don't ask now.",
        "Cannot foretell now.",
        "Possibly.",
        "There is a small chance.",
        "Yes, but not now.",
        "You can count on it.",
        "In your dreams.",
        "The future is uncertain.",
        "Forget about it.",
        "You will regret it.",
        "It's improbable.",
        "Don't bet on it.",
        "Absolutely not.",
        "There's a high probability.",
        "No way.",
        "Not a chance.",
        "I don't think so.",
        "Highly unlikely.",
        "Chances are low.",
        "It's not looking good.",
        "It's beyond your control.",
        "It's up to fate.",
        "Wait and see.",
        "The outlook is unclear.",
        "Unlikely.",
        "Ask someone else.",
        "The stars say no.",
        "It's a mystery.",
        "Time will tell.",
        "Probably not.",
        "It's doubtful.",
        "Very unlikely.",
        "Don't hold your breath.",
        "Unpredictable.",
        "It's complicated.",
        "Ask again tomorrow.",
        "The signs point to no.",
        "Not likely.",
        "Unsure right now.",
        "Future uncertain.",
        "Cannot say for sure.",
        "Doubtful.",
        "It's a toss-up.",
        "Try again next week.",
        "The answer eludes me.",
        "Consult the spirits.",
        "Seek professional advice.",
        "Don't rely on it.",
        "Not now.",
        "Too soon to tell.",
        "Need more information.",
        "Ambiguous.",
        "Indications unclear.",
        "Ask again in due time.",
        "Cloudy future.",
        "Destiny uncertain.",
        "Outcome unknown.",
        "Divine intervention needed."
    ]
    
    # Prompt user for a question
    question = input("Ask the magic 8 ball a question: ")
    
    # Generate a random response
    response = random.choice(responses)
    
    # Print the response
    print(response)

if __name__ == "__main__":
    magic_8_ball()
