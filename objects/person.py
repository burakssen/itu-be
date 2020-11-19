class Person():
    def __init__(self,username ,id_number, password, mail, account_type, faculty):
        self.username = username
        self.id_number = id_number
        self.password = password
        self.mail = mail
        self.account_type = account_type
        self.faculty = faculty
    
    def debug_person(self):
        print(self.username)
        print(self.id_number)
        print(self.mail)
        print(self.account_type)
        print(self.faculty)
        print("\n")
        print(self.password)
