import json
import os
import uuid

def save(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def read(filename):
    with open(filename, 'r') as f:
        return json.load(f)
        
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
    
    @staticmethod
    def from_json(json_dict):
        s = Scholarship()
        vars(s).update(json_dict)
        return s

    def add_to(self, data):
        data += [self.__dict__]
        save('scholarships.json', data)
        data[0:] = read('scholarships.json')

    def delete_from(self, scholarships, student_applicants):
        for idx, item in enumerate(scholarships):
            if item['id'] == self.id:
                scholarships[0:] = scholarships[:idx] + scholarships[idx+1:]
        save('scholarships.json', scholarships)
        # delete depending student applicants
        for idx, item in enumerate(student_applicants):
            if item['applied_scholarships'] == self.id:
                student_applicants[0:] = student_applicants[:idx] + student_applicants[idx+1:]
        save('student_applicants.json', student_applicants) 

    @staticmethod
    def get_from(scholarships, id):
        for idx, item in enumerate(scholarships):
            if item['id'] == id:
                return Scholarship.from_json(scholarships[idx])

    def view_all_applicants(self, student_applicants):
        ls = []
        for idx, item in enumerate(student_applicants):
            if item['applied_scholarships'] == self.id:
                ls += [student_applicants[idx]]
        return ls

class StudentApplicant:
    """
        a. What is the student’s first and last name?
        b. What is the student’s email student? 
        c. What is the student’s address?
    """
    def __init__(self, first_name='', last_name='', email='', address='', applied_scholarships='', id=None):
        self.id = id
        if not self.id:
            self.id = str(uuid.uuid1())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.address = address
        self.applied_scholarships = applied_scholarships

    @staticmethod
    def from_json(json_dict):
        sa = StudentApplicant()
        vars(sa).update(json_dict)
        return sa

    def add_to(self, data):
        data += [self.__dict__]
        save('student_applicants.json', data)
        data[0:] = read('student_applicants.json')

    def delete_from(self, data):
        for idx, item in enumerate(data):
            if item['id'] == self.id:
                data[0:] = data[:idx] + data[idx+1:]
        save('student_applicants.json', data)

    @staticmethod
    def get_from(student_applicants, id):
        for idx, item in enumerate(student_applicants):
            if item['id'] == id:
                return StudentApplicant.from_json(student_applicants[idx])


if not os.path.exists('scholarships.json'):
    with open('scholarships.json', 'w+') as f:
        json.dump([], f, indent=4)
if not os.path.exists('student_applicants.json'):
    with open('student_applicants.json', 'w+') as f:
        json.dump([], f, indent=4)

scholarships = read('scholarships.json')
student_applicants = read("student_applicants.json")


print("welcome to the admin panel")

while True:
    print("=================================")
    print("1 - Display information about scholarships")
    print("2 - Display a scholarship by id")
    print("3 - Add a scholarship")
    print("4 - Delete a scholarship")
    print("5 - Show all applications for a scholarship")
    print("6 - Display student applicants")
    print("7 - Display a scholarship by id")
    print("8 - Add a student applicant")
    print("9 - Delete a student applicant")
    print("q - quit")
    num = input("press number 1-7 to proceed, or letter `q` to quit\n")
    try:
        if num.strip() == "q":
            break
        elif num.strip() == "1":
            print(json.dumps(scholarships, indent=2))
        elif num.strip() == "2":
            s_id = input("please enter scholarship id e.g. `41d3db8a-3e00-11ea-99d2-e9cbc51cfe49`\n")
            s = Scholarship.get_from(scholarships, s_id)
            print(json.dumps(s.__dict__, indent=2))
        elif num.strip() == "3":
            description = input("please enter description\n")
            availability = input("please enter availability e.g. `undergraduate,graduate` or `graduate`\n")
            availability = availability.split(',')
            amount = input("please enter amount\n")
            aid_type = input("please enter aid_type e.g. `merit_based` or `financial_aid`\n")
            citizenship_requirements = bool(input("please enter citizenship_requirements e.g. `0` for False or `1` for True\n"))
            s = Scholarship(description, availability, amount, aid_type, citizenship_requirements)
            s.add_to(scholarships)
            print("added successfully")
        elif num.strip() == "4":
            s_id = input("please enter scholarship id e.g. `41d3db8a-3e00-11ea-99d2-e9cbc51cfe49`\n")
            s = Scholarship.get_from(scholarships, s_id)
            s.delete_from(scholarships, student_applicants)
            print("deleted successfully")
        elif num.strip() == "5":
            s_id = input("please enter scholarship id e.g. `41d3db8a-3e00-11ea-99d2-e9cbc51cfe49`\n")
            s = Scholarship.get_from(scholarships, s_id)
            print(json.dumps(s.view_all_applicants(student_applicants), indent=2))
        elif num.strip() == "6":
            print(json.dumps(student_applicants, indent=2))
        elif num.strip() == "7":
            sa_id = input("please enter student applicant id e.g. `41d3db8a-3e00-11ea-99d2-e9cbc51cfe49`\n")
            sa = StudentApplicant.get_from(student_applicants, sa_id)
            s = Scholarship.get_from(scholarships, sa.applied_scholarships)
            print("scholarship applied:\n", json.dumps(s.__dict__, indent=2))
            print(json.dumps(sa.__dict__, indent=2))
        elif num.strip() == "8":
            print(scholarships)
            first_name = input("please enter first_name\n")
            last_name = input("please enter last_name\n")
            email = input("please enter email\n")
            address = input("please enter address\n")
            applied_scholarships = input("please enter applied_scholarships by using the *id* of available scholarship. Example: `41d3db8a-3e00-11ea-99d2-e9cbc51cfe49`\n")
            sa = StudentApplicant(first_name, last_name, email, address, applied_scholarships)
            sa.add_to(student_applicants)
            print("added successfully")
        elif num.strip() == "9":
            sa_id = input("please enter student applicant id e.g. `41d3db8a-3e00-11ea-99d2-e9cbc51cfe49`\n")
            sa = StudentApplicant.get_from(student_applicants, sa_id)
            sa.delete_from(student_applicants)
            print("deleted successfully")
    except Exception as e:
        print("some errors occured, possibly incorrect input, try again.")
        print("the error is", e)