# FLASH-A-CARD: AN INTERACTIVE FLASHCARD QUIZ WEBSITE FOR STUDENT REVIEW
# 8 CAMIA
# RAFAEL, ZYA KYNDER TARHATA B.
# LAURINO, JUSTINE MATTHEW B.
# DE GUZMAN, ALESSANDRA FIONA M.

# import needed libraries
import csv
import time
import threading

# initializing variables
on_break = False
timer_running = False
timer_started_once = False

# Displays a simple guide explaining how the flashcard system works
def show_instructions():
    print("---------- INSTRUCTIONS ----------")
    print("Flash-a-card helps you review Grade 8 topics using flashcards !")
    print("How to use:")
    print("1. Choose a subject.")
    print("2. Choose a topic.")
    print("3. Answer the questions.")
    print("4. Explanations appear after answering.")
    print("5. View your session summary.")
    print("6. Retry incorrect questions if needed.")
    print("7. Optional Pomodoro timer for extra focus.")

    # Pause the screen so the user can read instructions
    input("Press ENTER to return to menu.")


# Reads a CSV file and converts each row into a dictionary.
# Each dictionary represents one flashcard question.
def load_questions(filename):
    questions = []  # list that will store all question dictionaries
    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)  # reads CSV as dictionaries
        for row in reader:
            questions.append(row)  # add each question to the list
    return questions


# Extracts all unique topic names from the questions list.
# Prevents duplicate topic entries from appearing in the menu.
def get_topics(questions):
    topics = []
    for q in questions:
        if q["Topic"] not in topics:
            topics.append(q["Topic"])
    return topics


# Returns only the questions that match the chosen topic.
def filter_by_topic(questions, selected_topic):
    return [q for q in questions if q["Topic"] == selected_topic]


# Runs a 25-minute study timer followed by a 5-minute break inspired by the Pomodoro Technique.
# The timer runs independently of the quiz using threading.
def pomodoro_timer():
    global timer_running, timer_started_once

    study_time = 1500
    break_time = 300

    print("⏳ STUDY SESSION STARTED\nStay focused. You got this.")

    for remaining in range(study_time, 0, -1):
        minutes = remaining // 60
        if remaining % 300 == 0 and remaining != study_time:
            print(f"Heads up! {minutes} minutes left in study session.")
        time.sleep(1)

    print("Study session finished!")

    print("☕ Break time started (5 minutes).")

    for remaining in range(break_time, 0, -1):
        if remaining == 60:
            print("Heads up! Only 1 minute left in your break!")
        time.sleep(1)

    print("Break finished! You can continue studying.")

    # 🔥 RESET so user can start again later
    timer_running = False
    timer_started_once = False


# Creates a separate thread so the timer runs while the user continues answering flashcard questions.
def start_pomodoro_in_background():
    global timer_running

    if not timer_running:
        timer_thread = threading.Thread(target=pomodoro_timer)
        timer_thread.daemon = True
        timer_thread.start()
        timer_running = True

# Handles the main quiz interaction:
def study_session(questions):
    global timer_running
    global on_break

    correct = 0
    incorrect = 0
    wrong_cards = []

    # Ask user to start Pomodoro only if no timer is currently active
    global timer_started_once

    # Ask ONLY once across the whole program
    if not timer_started_once:
        while True:
            start_timer = input("\nStart Pomodoro Timer? (Y/N): ").upper()

            if start_timer in ["Y", "N"]:
                break
            print("Invalid input. Try again.")

        if start_timer == "Y":
            start_pomodoro_in_background()
            timer_started_once = True
        else:
            timer_started_once = True  # don't ask again even if NO
    # Record session start time for performance statistics
    start_time = time.time()

    # If the Pomodoro timer enters break mode, questions pause until the break ends.
    for q in questions:
        while on_break:
            print("\nPomodoro break is active. Questions will resume after the break.")
            time.sleep(5)

    # Displays Flashcard Questions
    for q in questions:
        print()
        print("-" * 500)
        print("Question:", q["Question"])
        print(q["ChoiceA"])
        print(q["ChoiceB"])
        print(q["ChoiceC"])
        print(q["ChoiceD"])
        answer = input("Your answer: ").upper()
        # check if answer is correct
        if answer == q["Answer"].upper():
            print("Correct!")
            correct += 1
        else:
            print("Incorrect.")
            print("Correct answer:", q["Answer"])
            incorrect += 1
            wrong_cards.append(q)
        # show explanation after answering
        print("Explanation:", q["Explanation"])
    # record session end time
    end_time = time.time()

    # Calculates and shows session statistics
    total = correct + incorrect
    accuracy = (correct / total) * 100

    time_spent = round(end_time - start_time, 2)
    avg_time = round(time_spent / total, 2)

    print("\n----- SESSION SUMMARY -----")
    print("Total cards:", total)
    print("Correct:", correct)
    print("Incorrect:", incorrect)
    print("Accuracy:", round(accuracy, 2), "%")
    print("Time spent:", time_spent, "seconds")
    print("Average time per card:", avg_time, "seconds")

    # Retry incorrect questions
    # Allows students to review mistakes immediately
    if wrong_cards:
        retry = input("\nRetry incorrect questions? (Y/N): ").upper()
        if retry == "Y":
            study_session(wrong_cards)


# Main Menu
def main():
    # dictionary storing subjects and their CSV files
    subjects = {
        "1": ("Chemistry", "Chemistry.csv") ,
        "2": ("Physics", "Physics.csv") ,
        "3": ("Social Science", "Socsci.csv") ,
        "4": ("Earth Science", "EarthSci.csv"),
        "5": ("Computer Science", "Comsci.csv"),
        "6": ("Biology", "Biology.csv"),
        "7": ("Algebra", "Algebra.csv"),
        "8": ("English", "English.csv"),
        "9": ("Filipino", "Filipino.csv"),
        "10": ("Geometry", "Geometry.csv")
    }

    while True:

        print(r"""
         ███████╗██╗      █████╗ ███████╗██╗  ██╗     █████╗      ██████╗ █████╗ ██████╗ ██████╗
         ██╔════╝██║     ██╔══██╗██╔════╝██║  ██║    ██╔══██╗    ██╔════╝██╔══██╗██╔══██╗██╔══██╗
         █████╗  ██║     ███████║███████╗███████║    ███████║    ██║     ███████║██████╔╝██║  ██║
         ██╔══╝  ██║     ██╔══██║╚════██║██╔══██║    ██╔══██║    ██║     ██╔══██║██╔══██╗██║  ██║
         ██║     ███████╗██║  ██║███████║██║  ██║    ██║  ██║    ╚██████╗██║  ██║██║  ██║██████╔╝
         ╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    ╚═╝  ╚═╝     ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝
                                ✦ INTERACTIVE FLASHCARD SYSTEM ✦
        """)
        print("""
        ╔══════════════════════════════════════════════════╗
        ║                MAIN MENU                         ║
        ╠══════════════════════════════════════════════════╣
        ║  [1] Start Study Session                        ║
        ║  [2] Instructions                               ║
        ║  [3] Exit                                       ║
        ╚══════════════════════════════════════════════════╝
        """)
        choice = input("Choose option: ")

        # START STUDY SESSION
        if choice == "1":
            print("\nSelect Subject:")
            for key, value in subjects.items():
                print(key + ".", value[0])
            subject_choice = input("Choose subject: ")
            if subject_choice not in subjects:
                print("Invalid subject.")
                continue
            subject_name, filename = subjects[subject_choice]

            # load question data
            questions = load_questions(filename)

            # extract available topics
            topics = get_topics(questions)

            print("\nAvailable Topics:")
            for i, topic in enumerate(topics):
                print(i + 1, ".", topic)

            topic_choice = int(input("Select topic number: "))
            selected_topic = topics[topic_choice - 1]
            # filter questions by topic
            filtered_questions = filter_by_topic(questions, selected_topic)

            # start quiz session
            study_session(filtered_questions)

        # Show Instructions
        elif choice == "2":
            show_instructions()

        # End Program
        elif choice == "3":
            print(r"""
            ╔══════════════════════════════════════╗
            ║         THANK YOU FOR USING          ║
            ║            FLASH-A-CARD              ║
            ╠══════════════════════════════════════╣
            ║   Keep studying. Keep improving.     ║
            ╚══════════════════════════════════════╝
            """)

            print("Goodbye friend !")
            break

        else:
            print("Invalid choice.")


# Starts the code
main()