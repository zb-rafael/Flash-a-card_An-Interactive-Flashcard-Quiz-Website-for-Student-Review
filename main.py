# FLASH-A-CARD
# RAFAEL, ZYA KYNDER TARHATA B.
# LAURINO, JUSTINE MATTHEW B.
# DE GUZMAN, ALESSANDRA FIONA M.

def show_instructions():
    print("----- INSTRUCTIONS -----")
    print("Flash-a-card helps you review Grade 8 subjects using flashcards !")
    print("How to use:")
    print("1. Choose a topic.")
    print("2. Answer questions.")
    print("3. Explanations appear after answering.")
    print("4. View session summary at the end.")
    print("5. Start optional Pomodoro timer for extra focus.")
    input("Press ENTER to return to menu.")

def pomodoro_timer():

    study_time = 420   # 25 minutes
    break_time = 120  # 5 minutes

    print("Your 25-minute study session has started!")

    # STUDY TIMER
    for remaining in range(study_time, 0, -1):

        minutes = remaining // 60
        seconds = remaining % 60

        # heads-up every 5 minutes
        if remaining % 300 == 0 and remaining != study_time:
            print(f"Heads up! {minutes} minutes left in study session.")

        time.sleep(1)

    print("Study session finished!")

    print("\nBreak time started (5 minutes).")

    # BREAK TIMER
    for remaining in range(break_time, 0, -1):

        # reminder when 1 minute left
        if remaining == 60:
            print("Heads up! Only 1 minute left in your break!")

        time.sleep(1)

    print("Break finished! You can continue studying.")

def study_session():

    correct = 0
    incorrect = 0
    wrong_cards = []

    # Ask user to start Pomodoro only if no timer is currently active
    if not timer_running:
        start_timer = input("\nStart Pomodoro Timer? (Y/N): ").upper()
        if start_timer == "Y":
            start_pomodoro_in_background()

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
        "2": ("Physics", "Physics.csv")
    }

    while True:
        print("\n========= FLASH-A-CARD =========")
        print("1. Start Study Session")
        print("2. Instructions")
        print("3. Exit")

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
            print("Goodbye friend !")
            break

        else:
            print("Invalid choice.")


# Starts the code
main()