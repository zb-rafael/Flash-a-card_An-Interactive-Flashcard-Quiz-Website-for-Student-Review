# FLASH-A-CARD
# RAFAEL, ZYA KYNDER TARHATA B.
# LAURINO, JUSTINE MATTHEW B.
# DE GUZMAN, ALESSANDRA FIONA M.
import csv
import time
import threading

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
    timer_thread = threading.Thread(target=pomodoro_timer)
    timer_thread.daemon = True 
    timer_thread.start()

def study_session():
    start_timer = input("Start Pomodoro Timer? (Y/N): ").upper()
    if start_timer == "Y":
        pomodoro_timer()
        
study_session()
