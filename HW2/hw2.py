import json
import os
import uuid

def save(filename, data):
    f = open(filename, 'w')
    json.dump(data, f, indent=4)
    return f

def read(filename):
    f = open(filename, 'r')
    return f, json.load(f)
        
class Scholarship:
    """
        a. What is the short description for the scholarship?
        b. Is the scholarship open to undergraduate students, graduate students or both?
        c. How much money will the scholarship be?
        d. Will the scholarship be based on academic merit or financial need?
        e. Are there any citizenship requirements?
    """
    def __init__(self, description="", availability=[], amount=0, aid_type="", citizenship_requirements=False, id=None):
        self.id = id
        if not self.id:
            self.id = str(uuid.uuid1())
        self.description = description
        self.availability = availability
        self.amount = amount
        self.aid_type = aid_type
        self.citizenship_requirements = citizenship_requirements

    def __str__(self):
        return json.dumps(self.__dict__, indent=2)

class Student:
    """
        a. What is the student’s first and last name?
        b. What is the student’s email student? 
        c. What is the student’s address?
    """
    def __init__(self, first_name='', last_name='', email='', address='', id=None):
        self.id = id
        if not self.id:
            self.id = str(uuid.uuid1())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.address = address

    def __str__(self):
        return json.dumps(self.__dict__, indent=2)

class StudentManager:
    def __init__(self, filename='students.json'):
        self.filename = filename
        self.studentFile, self.studentList = self.__loadStudentListFromFile()

    def displayStudentList(self):
        for item in self.studentList:
            print(item)

    def addStudent(self):
        first_name = input("please enter first_name\n")
        last_name = input("please enter last_name\n")
        email = input("please enter email\n")
        address = input("please enter address\n")
        s = Student(first_name, last_name, email, address)
        self.__storeStudentToFile(s)
        print("added successfully")

    def __loadStudentListFromFile(self):
        if not os.path.exists(self.filename):
            File = open(self.filename, 'w+')
            json.dump([], File, indent=4)
        File, JSONList = read(self.filename)
        List = []
        for item in JSONList:
            List += [self.__loadStudentFromFile(item)]
        return File, List

    def __loadStudentFromFile(self, json_dict):
        s = Student()
        vars(s).update(json_dict)
        return s

    def __storeStudentToFile(self, student):
        self.studentList += [student]
        self.__storeStudentListToFile()
        self.studentList[0:] = self.__loadStudentListFromFile()[1]

    def __storeStudentListToFile(self):
        JSONList = []
        for item in self.studentList:
            JSONList += [item.__dict__]
        save(self.filename, JSONList)

class ScholarshipManager:
    def __init__(self, filename='scholarships.json'):
        self.filename = filename
        self.scholarshipFile, self.scholarshipList = self.__loadScholarshipListFromFile()

    def displayScholarshipList(self):
        for item in self.scholarshipList:
            print(item)

    def addScholarship(self):
        description = input("please enter description\n")
        availability = input("please enter availability e.g. `undergraduate,graduate` or `graduate`\n")
        availability = availability.split(',')
        amount = input("please enter amount\n")
        aid_type = input("please enter aid_type e.g. `merit_based` or `financial_aid`\n")
        citizenship_requirements = bool(input("please enter citizenship_requirements e.g. `0` for False or `1` for True\n"))
        s = Scholarship(description, availability, amount, aid_type, citizenship_requirements)
        self.__storeScholarshipToFile(s)
        print("added successfully")

    def __loadScholarshipListFromFile(self):
        if not os.path.exists(self.filename):
            File = open(self.filename, 'w+')
            json.dump([], File, indent=4)
        File, JSONList = read(self.filename)
        List = []
        for item in JSONList:
            List += [self.__loadScholarshipFromFile(item)]
        return File, List

    def __loadScholarshipFromFile(self, json_dict):
        s = Scholarship()
        vars(s).update(json_dict)
        return s

    def __storeScholarshipToFile(self, scholarship):
        self.scholarshipList += [scholarship]
        self.__storeScholarshipListToFile()
        self.scholarshipList[0:] = self.__loadScholarshipListFromFile()[1]

    def __storeScholarshipListToFile(self):
        JSONList = []
        for item in self.scholarshipList:
            JSONList += [item.__dict__]
        save(self.filename, JSONList)

class ScholarshipSystem:
    def __init__(self):
        self.studentManager = StudentManager()
        self.scholarshipManager = ScholarshipManager()
    def displayAllStudents(self):
        self.studentManager.displayStudentList()
    def enterNewStudent(self):
        self.studentManager.addStudent()
    def displayAllScholarships(self):
        self.scholarshipManager.displayScholarshipList()
    def enterNewScholarship(self):
        self.scholarshipManager.addScholarship()

class ScholarshipClient:
    def main(self):
        ss = ScholarshipSystem()
        print("welcome to the admin panel")
        while True:
            print("=================================")
            print("1 - Display information about scholarships")
            print("2 - Add a scholarship")
            print("3 - Display student applicants")
            print("4 - Add a student applicant")
            print("q - quit")
            num = input("press number 1-4 to proceed, or letter `q` to quit\n")
            try:
                if num.strip() == "q":
                    break
                elif num.strip() == "1":
                    ss.displayAllScholarships()
                elif num.strip() == "2":
                    ss.enterNewScholarship()
                elif num.strip() == "3":
                    ss.displayAllStudents()
                elif num.strip() == "4":
                    ss.enterNewStudent()
            except Exception as e:
                print("some errors occured, possibly incorrect input, try again.")
                print("the error is", e)

if __name__ == "__main__":
    sc = ScholarshipClient()
    sc.main()