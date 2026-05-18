class Cat:
    def __init__(self, name, age, colour, owner):
        self.name = name
        self.age = age
        self.colour = colour
        self.owner = owner

    def describe(self):
        print(f"{self.name} is a {self.colour} cat. "
              f"{self.name} is {self.age} years old and is owned by {self.owner}.")


# Instance from the task
cat1 = Cat("Cookie", 3, "ginger", "Steve")

# Two more instances
cat2 = Cat("Luna", 2, "black", "Aisha")
cat3 = Cat("Milo", 5, "white", "Ben")

# Output all cat descriptions
cat1.describe()
cat2.describe()
cat3.describe()
