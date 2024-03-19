import psycopg2
from datetime import datetime
class StudentDB:
    def __init__(self):
        self.conn = psycopg2.connect(
            user = "usr1",
            password = "pwd1!@#$",
            host = "localhost",
            port = "5432",
            database = "A3"
        )
        self.cur = self.conn.cursor()

    def getAllStudents(self):
        self.cur.execute("SELECT * FROM students;")
        rows = self.cur.fetchall()
        for row in rows:
            print(row)

    def addStudent(self, first_name, last_name, email, enrollment_date):
        try:
            # Validate the date
            datetime.strptime(enrollment_date, '%Y-%m-%d')
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
            print("Student not added.")
            return

        self.cur.execute("INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s);", 
                         (first_name, last_name, email, enrollment_date))
        self.conn.commit()

    def updateStudentEmail(self, student_id):
        self.cur.execute("SELECT * FROM students WHERE student_id = %s;", (student_id,))
        student = self.cur.fetchone()
        if student is None:
            print("No student found with the given id.")
            return

        new_email = input("Enter the new email: ")
        self.cur.execute("UPDATE students SET email = %s WHERE student_id = %s;", (new_email, student_id))
        self.conn.commit()
        print("Student email updated successfully.")



    def deleteStudent(self, student_id):
        self.cur.execute("SELECT * FROM students WHERE student_id = %s;", (student_id,))
        student = self.cur.fetchone()
        if student is None:
            print("No student found with the given id.")
            return

        self.cur.execute("DELETE FROM students WHERE student_id = %s;", (student_id,))
        self.conn.commit()
        print("Student deleted successfully.")


    def close(self):
        self.cur.close()
        self.conn.close()

def print_menu():
    print()
    print("Assignment 3 COMP 3005 CLI")
    print("Please choose the function that you want to use:")
    print()
    print("1. Retrieve and display all records from the students table.")
    print("2. Insert a new student record into the students table.")
    print("3. Update the email address for a student.")
    print("4. Delete the record of a student.")
    print("5. Exit")
    print()
    
def main():
    print_menu()

    db = StudentDB()

    while True:
        choice = input("Enter your choice (1-5): ")
        if choice == '1':
            db.getAllStudents()
            
        elif choice == '2':
            first_name = input("Enter the first name: ")
            last_name = input("Enter the last name: ")
            email = input("Enter the email: ")
            enrollment_date = input("Enter the enrollment date (YYYY-MM-DD): ")
            
            db.addStudent(first_name, last_name, email, enrollment_date)
            
        elif choice == '3':
            student_id = int(input("Enter the student id: "))
            db.updateStudentEmail(student_id)

        elif choice == '4':
            student_id = int(input("Enter the student id: "))
            
            db.deleteStudent(student_id)
            
        elif choice == '5':
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
        print_menu()
    db.close()

if __name__ == "__main__":
    main()
