# FLASH-A-CARD: AN INTERACTIVE FLASHCARD QUIZ WEBSITE FOR STUDENT REVIEW
# 8 CAMIA
# RAFAEL, ZYA KYNDER TARHATA B.
# LAURINO, JUSTINE MATTHEW B.
# DE GUZMAN, ALESSANDRA FIONA M.
import csv
import time
import threading

on_break = False
timer_running = False

def show_instructions():
    print("----- INSTRUCTIONS -----")
    print("Flash-a-card helps you review Grade 8 subjects using flashcards !")
    print("How to use:")
    print("1. Choose a subject.")
    print("2. Choose a topic.")
    print("3. Answer the questions.")
    print("4. Explanations appear after answering.")
    print("5. View your session summary.")
    print("6. Retry incorrect questions if needed.")
    print("7. Optional Pomodoro timer for extra focus.")
    input("Press ENTER to return to menu.")

def load_questions(filename):
    questions = []
    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            questions.append(row)
    return questions

def get_topics(questions):
    topics = []
    for q in questions:
        if q["topic"] not in topics:
            topics.append(q["topic"])
    return topics

def filter_by_topic(questions, selected_topic):
    return [q for q in questions if q["topic"] == selected_topic]
    
def pomodoro_timer():
    study_time = 1500  # 25 minutes
    break_time = 300 # 5 minutes
    
    print("Your 25-minute study session has started!")
    # STUDY TIMER
    for remaining in range(study_time, 0, -1):
        minutes = remaining // 60
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

def start_pomodoro_in_background():
    global timer_running

    if not timer_running:
        timer_thread = threading.Thread(target=pomodoro_timer)
        timer_thread.daemon = True
        timer_thread.start()
        timer_running = True

def study_session(questions):
    global timer_running
    global on_break
    
    correct = 0
    incorrect = 0
    wrong_cards = []

   if not timer_running:
        start_timer = input("\nStart Pomodoro Timer? (Y/N): ").upper()

        if start_timer == "Y":
            start_pomodoro_in_background()

    start_time = time.time()

    for q in questions:

        while on_break:
            print("\nPomodoro break is active. Questions will resume after the break.")
            time.sleep(5)

    for q in questions:
        print("-"*500)
        print("Question:", q["question"])
        print(q["choiceA"])
        print(q["choiceB"])
        print(q["choiceC"])
        print(q["choiceD"])

        answer = input("Your answer: ").upper()

        if answer == q["answer"].upper():
            print("Correct!")
            correct += 1
        else:
            print("Incorrect.")
            print("Correct answer:", q["answer"])
            incorrect += 1
            wrong_cards.append(q)

        print("Explanation:", q["explanation"])

    end_time = time.time()

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

    if wrong_cards:
        retry = input("\nRetry incorrect questions? (Y/N): ").upper()
        if retry == "Y":
            study_session(wrong_cards)
            
def main():
    subjects = {
        "1": ("Chemistry", "Chemistry.csv")
    }

    while True:
        print("\n====== FLASH-A-CARD ======")
        print("1. Start Study Session")
        print("2. Instructions")
        print("3. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            print("\nSelect Subject:")
            for key, value in subjects.items():
                print(key + ".", value[0])

            subject_choice = input("Choose subject: ")

            if subject_choice not in subjects:
                print("Invalid subject.")
                continue

            subject_name, filename = subjects[subject_choice]

            questions = load_questions(filename)
            topics = get_topics(questions)

            print("\nAvailable Topics:")
            for i, topic in enumerate(topics):
                print(i + 1, ".", topic)

            topic_choice = int(input("Select topic number: "))
            selected_topic = topics[topic_choice - 1]

            filtered_questions = filter_by_topic(questions, selected_topic)
            study_session(filtered_questions)

        elif choice == "2":
            show_instructions()

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")
main()
