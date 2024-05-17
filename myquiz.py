import mysql.connector as db;


mydb = db.connect(
    host="localhost",
    user="root",
    password="Ankit@123",
    database="myquizdb"
)

def fetch_random_questions():
    cursor = mydb.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM dsa_questions ORDER BY RAND() LIMIT ")
    questions = cursor.fetchall()
    cursor.close()
    return questions

def check_answer(question_id, user_answer):
    cursor = mydb.cursor()
    cursor.execute("SELECT correct_option FROM dsa_questions WHERE id = %s", (question_id,))
    correct_option = cursor.fetchone()[0]
    cursor.close()
    return user_answer.upper() == correct_option

def attempt_quiz():
    questions = fetch_random_questions()  
    score = 0

    for question in questions:
        print(f"\nQuestion: {question['question_text']}")
        print(f"A. {question['option_a']}")
        print(f"B. {question['option_b']}")
        print(f"C. {question['option_c']}")
        print(f"D. {question['option_d']}")

        user_answer = input("Enter your answer (A/B/C/D) or Q to quit: ").strip().upper()
        
        if user_answer == 'Q':
            print("You have chosen to exit the quiz.")
            break
        
        if check_answer(question['id'], user_answer):
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! The correct answer was {question['correct_option']}.")

    print(f"\nYour total score: {score}/{len(questions)}")

def main():
    while True:
        print("\nMenu:")
        print("1. Register")
        print("2. Login")
        print("3. Attempt Quiz")
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            register()
        elif choice == 2:
            if login():
                print("You are now logged in.")
            else:
                print("incorrect email/password  or please register first")
        elif choice == 3:
            print("Please login before attempting the quiz.")
            if login(): 
             
             attempt_quiz()
        
        
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

def register():
    cursor = mydb.cursor()
    name = input("Enter your name: ")
    
    while True:
     email = input("Enter your email: ")
     if "@gmail.com" in email:
        break
     else:
        print("Please enter a valid email address with @gmail.com extension.")

    while True:
        password = input("Enter your password: ")
        password = input("Enter your password: ")
        re_password = input("Enter your password again: ")
        if password == re_password:
            print("Password created successfully")
            break
        else:
            print("Please re-enter password")
   
    sql = 'INSERT INTO registered_user (name, email, password) VALUES (%s, %s, %s)'
    val = (name, email, password)
    cursor.execute(sql, val)
    mydb.commit()
    cursor.close()
    
    print(f"Hello {name}, your account has been created successfully")

def login():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    
    cursor = mydb.cursor()
    sql = "SELECT * FROM registered_user WHERE email = %s AND password = %s"
    val = (email, password)
    cursor.execute(sql, val)
    result = cursor.fetchone()
    cursor.close()
    
    if result:
        print("Login successful! Welcome!")
        return True
    else:
        print("Invalid email or password.")
        return False


def exit_app():
    print("Exiting the application.")
    mydb.close()

if __name__ == "__main__":
    main()

     
