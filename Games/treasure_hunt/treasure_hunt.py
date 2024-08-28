import os
import sys
import random
import subprocess

# Ensure necessary modules are installed
def install_dependencies():
    try:
        import requests
    except ImportError:
        print("Requests module not found. Installing...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])
        print("Requests module installed.")

install_dependencies()

# Author's signature
author_signature = "dedsec1121fk made this game."

# Character details
characters = {
    'Explorer': {
        'name': 'Explorer 🧭',
        'description': 'A seasoned adventurer with a sharp eye for details.',
        'background': 'Raised on tales of lost civilizations, driven by curiosity and discovery.',
        'goal': 'To uncover legendary treasures and secure a legacy.'
    },
    'Adventurer': {
        'name': 'Adventurer 🏔️',
        'description': 'Brave and bold, passionate about high-risk challenges.',
        'background': 'Seeks thrills and challenges, eager to prove courage.',
        'goal': 'To find the ultimate treasure and gain fame and glory.'
    },
    'Scout': {
        'name': 'Scout 🕵️‍♂️',
        'description': 'Swift and stealthy, adept at navigation and reconnaissance.',
        'background': 'A master of stealth and survival, avoiding direct conflict.',
        'goal': 'To retrieve artifacts while avoiding conflict, using intelligence and stealth.'
    },
    'Historian': {
        'name': 'Historian 📜',
        'description': 'An expert in ancient lore and legends.',
        'background': 'A scholar of ancient civilizations and forgotten myths.',
        'goal': 'To preserve and share the lost knowledge of bygone eras.'
    },
    'Warrior': {
        'name': 'Warrior ⚔️',
        'description': 'A fearless combatant skilled in battle and strategy.',
        'background': 'A veteran of countless battles, driven by honor and glory.',
        'goal': 'To seek legendary artifacts and prove prowess in combat.'
    }
}

# Expanded NPCs with dialogues
npcs = {
    'Mysterious Stranger': {
        'description': 'A cloaked figure who seems to know more than they let on.',
        'dialogues': {
            'intro': [
                "You encounter a cloaked figure. 'Ah, a fellow seeker of fortunes,' they say.",
                "The stranger’s voice is calm but urgent. 'Be careful, not all is as it seems.'"
            ],
            'help': [
                "'I can offer guidance,' the stranger says. 'But be warned, the truth may not be what you expect.'",
                "'Seek the hidden lever in the chamber. It may reveal more than just treasure.'"
            ],
            'deceive': [
                "The stranger smirks. 'Why would you believe anything I say? Everyone has their own agenda.'",
                "'Perhaps it's best if you figure things out on your own.'"
            ],
            'warn': [
                "'Danger lurks in every corner of these ruins. Trust no one and stay vigilant.'",
                "'Many have fallen for the illusions that these ruins create.'"
            ]
        }
    },
    'Local Historian': {
        'description': 'A knowledgeable local with insights into the history of the ruins.',
        'dialogues': {
            'intro': [
                "A wise old historian greets you. 'These ruins are steeped in history. Many have tried to uncover their secrets.'",
                "'If you’re looking for clues, the murals might be your best guide.'"
            ],
            'help': [
                "'The murals tell the story of a great civilization,' the historian explains. 'Follow their instructions carefully.'",
                "'But be cautious, as not all treasures are meant to be found.'"
            ],
            'warn': [
                "'The deeper you go, the more dangerous it becomes,' warns the historian. 'Many have never returned from these ruins.'",
                "'Consider turning back before it's too late.'"
            ],
            'history': [
                "'The ruins date back thousands of years, each layer revealing more about the civilization that built them.'",
                "'Study the inscriptions carefully; they hold the key to unlocking the next stage of your quest.'"
            ]
        }
    },
    'Ancient Guardian': {
        'description': 'A spectral figure who guards the ancient secrets.',
        'dialogues': {
            'intro': [
                "The Guardian materializes from the shadows. 'Only the worthy may proceed,' it intones.",
                "'Prove your worth, or face the consequences of your intrusion.'"
            ],
            'challenge': [
                "'To proceed, solve the riddle I present,' the Guardian challenges. 'Failure will seal your fate.'",
                "'The ancient knowledge comes at a price. Are you willing to pay it?'"
            ],
            'warn': [
                "'Tread carefully, for the path is fraught with peril,' the Guardian warns.",
                "'Many have fallen before you, blinded by their greed.'"
            ],
            'greet': [
                "'Welcome, seeker. The path ahead will test all your skills and resolve.'",
                "'Remember, not all is as it seems in these ancient ruins.'"
            ]
        }
    },
    'Rival Adventurer': {
        'description': 'A cunning competitor seeking to outsmart you.',
        'dialogues': {
            'intro': [
                "A rival adventurer approaches with a sly grin. 'Looks like we have some competition,' they say.",
                "'Care to join forces, or do you prefer to compete for the treasure?'"
            ],
            'compete': [
                "'May the best adventurer win,' the rival says with a smirk. 'I won't go easy on you.'",
                "'Good luck. You’ll need it to keep up with me.'"
            ],
            'team_up': [
                "'Forming an alliance could benefit us both,' the rival suggests. 'Together, we might achieve more.'",
                "'Trust is rare in these ruins, but it could be our greatest asset.'"
            ],
            'challenge': [
                "'Prepare for a showdown,' the rival challenges. 'Let’s see who really deserves the treasure.'",
                "'I’ve set traps along the way. Try not to fall for them.'"
            ]
        }
    },
    'Wise Sage': {
        'description': 'An old sage with deep knowledge of mystical forces.',
        'dialogues': {
            'intro': [
                "A figure cloaked in robes greets you. 'The path ahead is shrouded in darkness,' they say.",
                "'Only those who understand the mystical forces can navigate the challenges.'"
            ],
            'advice': [
                "'Seek the alignment of the stars; it will guide your way,' the sage advises.",
                "'The amulet you carry holds more power than you realize. Use it wisely.'"
            ],
            'mystic': [
                "'Beware the illusions that cloud your vision,' the sage warns. 'Not all is as it seems.'",
                "'The true power lies not in the treasure, but in your heart.'"
            ],
            'reveal': [
                "'The ancient prophecies speak of a great revelation for those who seek the truth.'",
                "'Trust in your instincts and the ancient knowledge you uncover.'"
            ]
        }
    },
    'Treasure Hunter': {
        'description': 'A fellow treasure hunter with a knack for uncovering hidden secrets.',
        'dialogues': {
            'intro': [
                "Another treasure hunter approaches. 'I've been searching for this place for years,' they say.",
                "'I’ve gathered some useful information. Care to share?'"
            ],
            'exchange': [
                "'Let’s trade information. I’ll tell you what I know if you share your findings.'",
                "'Knowledge is power. Let’s use it to our advantage.'"
            ],
            'warn': [
                "'Be wary of traps. This place is riddled with them,' the hunter warns.",
                "'The treasure is guarded by more than just puzzles. Stay sharp.'"
            ],
            'caution': [
                "'Many have tried to find the treasure and failed,' the hunter says. 'You must be cautious.'",
                "'The deeper you go, the more the ruins seem to change and mislead you.'"
            ]
        }
    },
    'Guardian of Secrets': {
        'description': 'A mystical being guarding ancient secrets.',
        'dialogues': {
            'intro': [
                "The Guardian of Secrets appears, cloaked in ethereal light. 'I guard the knowledge of ages,' they say.",
                "'Only those pure of heart may access the deepest secrets.'"
            ],
            'test': [
                "'To prove your worth, you must pass a series of trials,' the Guardian declares.",
                "'Each trial will test your intellect, bravery, and morality.'"
            ],
            'guide': [
                "'Follow the stars and the symbols. They will lead you to the truth.'",
                "'Trust in your wisdom and strength to overcome the trials ahead.'"
            ],
            'reveal': [
                "'The true nature of the treasure is not what it seems. It holds great power and responsibility.'",
                "'Use the knowledge wisely, for it can change the course of history.'"
            ]
        }
    },
    'Ancient Scholar': {
        'description': 'An ancient scholar who offers knowledge about the ruins.',
        'dialogues': {
            'intro': [
                "An ancient scholar emerges from the shadows. 'You seek knowledge, but are you prepared for its burden?'",
                "'The ruins hold the secrets of an entire civilization.'"
            ],
            'explain': [
                "'The inscriptions and symbols tell the story of the ancient people. Study them carefully.'",
                "'Each symbol holds a piece of the puzzle. Only by understanding them can you succeed.'"
            ],
            'advise': [
                "'Be prepared for deception and false leads. The ruins are designed to mislead.'",
                "'Trust your instincts and the wisdom you gather along the way.'"
            ],
            'conclude': [
                "'In the end, it is not just about finding the treasure but understanding its significance.'",
                "'The true value lies in the journey and the lessons learned.'"
            ]
        }
    }
}

# Expanded story scenes with detailed ASCII art
story_scenes = {
    'start': {
        'text': "Welcome to the ruins of the Lost Civilization! Your adventure begins here. Do you...",
        'art': "   ____    _   \n  |    |  | |  \n  |    |__| |  \n  |____|  |_|  \n           / /   \n          / /   \n         /_/   \n"
    },
    'explore_ruins': {
        'text': "The ruins are ancient and mysterious. You find yourself at a crossroads. Do you...",
        'art': "   _______   \n  /       \\  \n |  ____  | \n | |    | | \n | |____| | \n |________| \n"
    },
    'left_path': {
        'text': "Taking the left path, you encounter a chest. Do you...",
        'art': "   _______   \n  |       |  \n  |_______|  \n  |_______|  \n   _______   \n  |_______|  \n"
    },
    'right_path': {
        'text': "The right path leads to a lever. Do you...",
        'art': "   _______   \n  |       |  \n  |_______|  \n   _______   \n  |_______|  \n"
    },
    'open_chest': {
        'text': "You find gold and a mysterious amulet in the chest. Do you...",
        'art': "   _______   \n  |   $   |  \n  |_______|  \n   _______   \n  |_______|  \n"
    },
    'pull_lever': {
        'text': "Pulling the lever reveals a hidden passage. You can now...",
        'art': "   _______   \n  |       |  \n  |       |  \n  |_______|  \n  |_______|  \n"
    },
    'meet_stranger': {
        'text': "You meet a mysterious stranger who offers cryptic advice. Do you...",
        'art': "   _______   \n  /       \\  \n |  ???  |  \n  \\______/  \n"
    },
    'meet_historian': {
        'text': "You encounter a local historian who shares ancient knowledge. Do you...",
        'art': "   _______   \n  /       \\  \n |  📜  |  \n  \\______/  \n"
    },
    'ancient_library': {
        'text': "You discover an ancient library filled with scrolls. Do you...",
        'art': "   _______   \n  |       |  \n  |  📚  |  \n  |_______|  \n"
    },
    'decode_scroll': {
        'text': "Deciphering the scroll reveals a prophecy about a guardian. Do you...",
        'art': "   _______   \n  |  📜  |  \n  |       |  \n  |_______|  \n"
    },
    'confront_guardian': {
        'text': "You meet the Ancient Guardian who challenges you with a riddle. Do you...",
        'art': "   _______   \n  |   🕵️  |  \n  |_______|  \n   _______   \n  |_______|  \n"
    },
    'solve_riddle': {
        'text': "Successfully solving the riddle grants you access to deeper secrets. Do you...",
        'art': "   _______   \n  |  🧩  |  \n  |_______|  \n"
    },
    'fail_riddle': {
        'text': "Failing the riddle triggers a trap. Do you...",
        'art': "   _______   \n  |   ⚠️  |  \n  |_______|  \n"
    },
    'local_knowledge': {
        'text': "With local knowledge, you avoid traps and navigate hidden passages. Do you...",
        'art': "   _______   \n  |  📖  |  \n  |_______|  \n"
    },
    'unexpected_betrayal': {
        'text': "A trusted ally betrays you. Do you...",
        'art': "   _______   \n  |   💔  |  \n  |_______|  \n"
    },
    'new_allies': {
        'text': "New allies help you overcome obstacles. Do you...",
        'art': "   _______   \n  |   🤝  |  \n  |_______|  \n"
    },
    'rivalry_revenge': {
        'text': "You face a rival in a dramatic showdown. Do you...",
        'art': "   _______   \n  |  ⚔️  |  \n  |_______|  \n"
    },
    'treasure_found': {
        'text': "You find the treasure but face its curse. Do you...",
        'art': "   _______   \n  |  💰  |  \n  |_______|  \n"
    },
    'escape_unscathed': {
        'text': "You escape the ruins with minor injuries. Do you...",
        'art': "   _______   \n  |  🚪  |  \n  |_______|  \n"
    },
    'return_to_village': {
        'text': "Returning to the village, you share your experiences. Do you...",
        'art': "   _______   \n  |  🏡  |  \n  |_______|  \n"
    },
    'seek_expert_help': {
        'text': "Seeking expert help sheds light on the treasure’s origins. Do you...",
        'art': "   _______   \n  |  🧑‍🔬  |  \n  |_______|  \n"
    },
    'ancient_rivalry': {
        'text': "Uncovering an ancient rivalry between factions leads to conflict. Do you...",
        'art': "   _______   \n  |  🏛️  |  \n  |_______|  \n"
    },
    'fateful_decision': {
        'text': "A fateful decision impacts your quest. Do you...",
        'art': "   _______   \n  |  ⚖️  |  \n  |_______|  \n"
    },
    'final_showdown': {
        'text': "The final showdown awaits. Your decisions lead to one of many possible endings.",
        'art': "   _______   \n  |  🏆  |  \n  |_______|  \n"
    }
}

# Expanded endings with detailed descriptions
endings = {
    'Treasure': "Congratulations! You have found the treasure and secured your place in history as a legendary adventurer. 🏆",
    'Escape': "You have managed to escape the ruins with valuable artifacts, but the true treasure remains elusive. 🚀",
    'Rivalry': "Your betrayal has led to a dark reputation. You have the treasure, but at what cost to your conscience? ⚔️",
    'Curse': "The treasure’s curse haunts you, leading to a tragic downfall despite your wealth and fame. 💀",
    'Growth': "Leaving the quest behind, you find personal growth and a new purpose, learning the true value of the journey. 🌟",
    'Betrayal': "Your trust in your allies has been betrayed, leading to a challenging escape and a re-evaluation of your path. 😞",
    'Victory': "You and your allies have achieved victory, overcoming all challenges and securing the treasure. 🌟",
    'Failure': "Despite your efforts, you failed to find the treasure and returned with nothing but lessons learned. 📉",
    'Mystery': "The true nature of the treasure remains a mystery, leaving you with more questions than answers. 🕵️‍♂️",
    'Redemption': "Through trials and tribulations, you find redemption and learn the true meaning of friendship and courage. ❤️",
    'Legacy': "Your adventure becomes a legend, inspiring future generations with tales of bravery and wisdom. 📜",
    'Discovery': "You uncover the true purpose of the treasure, leading to a groundbreaking discovery in history. 🔍"
}

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_ascii_art(art):
    """Display ASCII art."""
    print(art)

def show_main_menu():
    """Display the main menu."""
    clear_screen()
    ascii_art = """
     _____  _____  _______  _______ 
    /     \/     \/       \/       \\
    \_____/_____/_______/_______/ 
    """
    print(ascii_art)
    print("Welcome to 'Treasure Hunt'!")
    print(f"\n{author_signature}\n")
    print("1. Start Game")
    print("2. Highscore")
    print("3. Controls")
    print("4. Exit")

def show_highscores():
    """Display highscores."""
    clear_screen()
    print("Highscores are not yet implemented.")
    input("Press Enter to return to the main menu.")

def display_controls():
    """Display game controls."""
    clear_screen()
    print("Controls:")
    print("1. Use the number keys to make choices.")
    print("2. Follow the prompts to navigate the story.")
    print("3. Choices will affect the storyline and outcomes.")
    input("Press Enter to return to the main menu.")

def verify_signature():
    """Verify the author's signature to prevent tampering."""
    signature = author_signature
    with open(__file__, 'r') as file:
        content = file.read()
    if signature not in content:
        print("Signature not found. This script has been tampered with. Exiting...")
        sys.exit(1)

def choose_character():
    """Select a character for the game."""
    clear_screen()
    print("Choose your character:")
    for idx, char in enumerate(characters.keys(), start=1):
        print(f"{idx}. {char} - {characters[char]['description']}")
    
    while True:
        choice = input("Select a character (1/2/3/4/5): ").strip()
        if choice in ['1', '2', '3', '4', '5']:
            selected_character = list(characters.keys())[int(choice) - 1]
            print(f"You have selected: {characters[selected_character]['name']}")
            return selected_character
        else:
            print("Invalid choice. Please select a valid character.")

def interact_with_npc(npc_name):
    """Interact with the selected NPC."""
    npc = npcs[npc_name]
    print(f"\n{npc['description']}")
    print("1. Ask for help")
    print("2. Request a warning")
    print("3. Inquire about the challenge")
    print("4. Seek deceitful information")
    
    while True:
        choice = input("Select an option (1/2/3/4): ").strip()
        if choice == '1':
            print("\n" + random.choice(npc['dialogues']['help']))
            return 'help'
        elif choice == '2':
            print("\n" + random.choice(npc['dialogues']['warn']))
            return 'warn'
        elif choice == '3':
            print("\n" + random.choice(npc['dialogues']['challenge']))
            return 'challenge'
        elif choice == '4':
            print("\n" + random.choice(npc['dialogues']['deceive']))
            return 'deceive'
        else:
            print("Invalid choice. Please select a valid option.")

def navigate_scene(scene_key):
    """Navigate to a specific scene."""
    clear_screen()
    scene = story_scenes[scene_key]
    print(f"\n{scene['text']}")
    display_ascii_art(scene['art'])
    
    if scene_key == 'start':
        print(f"\n{author_signature}\n")
    
    if scene_key in ['meet_stranger', 'meet_historian', 'confront_guardian']:
        print("\nChoose an NPC to interact with:")
        for idx, npc in enumerate(npcs.keys(), start=1):
            print(f"{idx}. {npc} - {npcs[npc]['description']}")
        
        npc_choice = input("Select an NPC (1/2/3/4/5/6): ").strip()
        if npc_choice in ['1', '2', '3', '4', '5', '6']:
            npc_name = list(npcs.keys())[int(npc_choice) - 1]
            interaction_result = interact_with_npc(npc_name)
            if interaction_result == 'deceive':
                print("The information you received may not be trustworthy. Proceed with caution.")
            elif interaction_result == 'warn':
                print("Heed the warning. The dangers ahead may be greater than anticipated.")
            elif interaction_result == 'help':
                print("The help provided might give you a strategic advantage. Use it wisely.")
            elif interaction_result == 'challenge':
                print("Prepare for the challenge ahead. It may test your resolve.")
    
def main_gameplay(selected_character):
    """Main gameplay loop."""
    navigate_scene('start')
    
    while True:
        print("\nChoose an action:")
        print("1. Explore")
        print("2. Interact with NPC")
        print("3. Exit")
        
        action = input("Select an action (1/2/3): ").strip()
        
        if action == '1':
            navigate_scene('explore_ruins')
            
            print("\nChoose a path:")
            print("1. Left Path")
            print("2. Right Path")
            
            path_choice = input("Select a path (1/2): ").strip()
            
            if path_choice == '1':
                navigate_scene('left_path')
                print("\nDo you want to open the chest?")
                print("1. Yes")
                print("2. No")
                
                chest_action = input("Select an option (1/2): ").strip()
                
                if chest_action == '1':
                    navigate_scene('open_chest')
                    print("You've found gold and a mysterious amulet!")
                else:
                    print("You chose not to open the chest.")
                
            elif path_choice == '2':
                navigate_scene('right_path')
                print("\nDo you want to pull the lever?")
                print("1. Yes")
                print("2. No")
                
                lever_action = input("Select an option (1/2): ").strip()
                
                if lever_action == '1':
                    navigate_scene('pull_lever')
                else:
                    print("You chose not to pull the lever.")
        
        elif action == '2':
            print("\nChoose an NPC to interact with:")
            print("1. Mysterious Stranger")
            print("2. Local Historian")
            print("3. Ancient Guardian")
            print("4. Rival Adventurer")
            print("5. Wise Sage")
            print("6. Treasure Hunter")
            
            npc_choice = input("Select an NPC (1/2/3/4/5/6): ").strip()
            
            if npc_choice in ['1', '2', '3', '4', '5', '6']:
                npc_name = list(npcs.keys())[int(npc_choice) - 1]
                interaction_result = interact_with_npc(npc_name)
                
                if interaction_result == 'deceive':
                    print("The information you received may not be trustworthy. Proceed with caution.")
                elif interaction_result == 'warn':
                    print("Heed the warning. The dangers ahead may be greater than anticipated.")
                elif interaction_result == 'help':
                    print("The help provided might give you a strategic advantage. Use it wisely.")
                elif interaction_result == 'challenge':
                    print("Prepare for the challenge ahead. It may test your resolve.")
            
            else:
                print("Invalid NPC name. Please choose a valid NPC.")
        
        elif action == '3':
            print("Thank you for playing! Have a great day!")
            break
        
        else:
            print("Invalid action. Please choose to Explore, Interact, or Exit.")

def main():
    """Main function to start the game."""
    verify_signature()
    
    while True:
        show_main_menu()
        choice = input("Select an option (1/2/3/4): ").strip()
        
        if choice == '1':
            selected_character = choose_character()
            main_gameplay(selected_character)
        
        elif choice == '2':
            show_highscores()
        
        elif choice == '3':
            display_controls()
        
        elif choice == '4':
            print("Exiting the game. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
