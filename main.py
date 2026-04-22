# FLASH-A-CARD: AN INTERACTIVE FLASHCARD QUIZ WEBSITE FOR STUDENT REVIEW
# 8 CAMIA
# RAFAEL, ZYA KYNDER TARHATA B.
# LAURINO, JUSTINE MATTHEW B.
# DE GUZMAN, ALESSANDRA FIONA M.

# Import required libraries for file handling, timing, and threading
import csv
import time
import threading

# Global variables used to control timer behavior across sessions
on_break = False
timer_running = False
timer_started_once = False

# Displays a simple guide explaining how the flashcard system works
def show_instructions():
        print("""
    ------------------------------------------------------------
    |                       INSTRUCTIONS                       |
    ------------------------------------------------------------
    | FLASH-A-CARD helps you review Grade 8 topics             |
    | using interactive flashcards for better learning.        |
    ------------------------------------------------------------
    | HOW TO USE:                                              |
    ------------------------------------------------------------
    | 1. Choose a subject                                      |
    | 2. Choose a topic                                        |
    | 3. Answer the questions                                  |
    | 4. View explanations after each answer                   |
    | 5. Check your session summary                            |
    | 6. Retry incorrect answers if needed                     |
    | 7. Optional Pomodoro timer for focus                     |
    ------------------------------------------------------------ """)

    # Pause the screen so the user can read instructions
        input("Press ENTER to return to menu.")


# Reads a CSV file and converts each row into a dictionary.
# Each dictionary represents one flashcard question.
def load_questions(filename):
    questions = []
    try:
        with open(filename, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                questions.append(row)

        if len(questions) == 0:
            print("Warning: No questions found in file.")
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []

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

    print("STUDY SESSION STARTED !")

    for remaining in range(study_time, 0, -1):
        minutes = remaining // 60
        if remaining % 300 == 0 and remaining != study_time:
            print(f"\nHeads up! {minutes} minutes left in study session.")
        time.sleep(1)

    print("STUDY SESSION FINISHED !")

    time.sleep(1)

    print("5 MINUTE BREAK TIME STARTED :]")

    for remaining in range(break_time, 0, -1):
        if remaining == 60:
            print("\nHeads up! Only 1 minute left in your break!")
        time.sleep(1)

    print("BREAK FINISHED !")

    # RESET so user can start again later
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
        print("-" * 70)
        print(" " + q["Question"])
        print("-" * 70)

        print("| " + q["ChoiceA"])
        print("| " + q["ChoiceB"])
        print("| " + q["ChoiceC"])
        print("| " + q["ChoiceD"])

        print("-" * 70)

        while True:
            answer = input("Your answer (A/B/C/D): ").upper()

            if answer in ["A", "B", "C", "D"]:
                break
            print("Invalid answer. Try again.")
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
    time_spent = round(end_time - start_time, 2)

    if total == 0:
        accuracy = 0
        avg_time = 0
    else:
        accuracy = (correct / total) * 100
        avg_time = round(time_spent / total, 2)

    print()
    print("-" * 70)
    print("                           SESSION SUMMARY                     ")
    print("-" * 70)

    print("| Total Cards        : " + str(total))
    print("| Correct            : " + str(correct))
    print("| Incorrect          : " + str(incorrect))
    print("| Accuracy           : " + str(round(accuracy, 2)) + " %")
    print("| Time Spent         : " + str(time_spent) + " seconds")
    print("| Avg Time / Card    : " + str(avg_time) + " seconds")

    print("-" * 70)

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
        """)
        time.sleep(3)
        print("""
                      ╔══════════════════════════════════════════════════╗
                      ║                    MAIN MENU                     ║
                      ╠══════════════════════════════════════════════════╣
                      ║  [1] Start Study Session                         ║
                      ║  [2] Instructions                                ║
                      ║  [3] Exit                                        ║
                      ╚══════════════════════════════════════════════════╝
        """)

        while True:
            choice = input("Choose option: ")

            if choice in ["1", "2", "3"]:
                break
            print("Invalid choice. Try again.")

        # START STUDY SESSION
        if choice == "1":
            print("\nSelect Subject:")
            for key, value in subjects.items():
                print(key + ".", value[0])
            while True:
                subject_choice = input("Choose subject: ")

                if subject_choice in subjects:
                    break
                print("Invalid subject. Try again.")
            subject_name, filename = subjects[subject_choice]

            # load question data
            questions = load_questions(filename)

            # extract available topics
            topics = get_topics(questions)

            print("\nAvailable Topics:")
            for i, topic in enumerate(topics):
                print(i + 1, ".", topic)

            while True:
                try:
                    topic_choice = int(input("Select topic number: "))

                    if 1 <= topic_choice <= len(topics):
                        break
                    else:
                        print("Number out of range. Try again.")

                except ValueError:
                    print("Invalid input. Enter a number.")

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
    
            """)
            break

        else:
            print("Invalid choice.")


# Starts the code
main()