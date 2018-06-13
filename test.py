class Student:
    count = 0

    def __init__(self, name, age):

        self.name = name
        self.age = age
        Student.count += 1

    def display(self):
        print("Student are: %d" % Student.count)

    def displayAll(self):
        print("student name:", self.name, " Student age: ", self.age)


s1 = Student("Pich", 20)
s2 = Student("Noob", 20)
s1.display()
s2.displayAll()
