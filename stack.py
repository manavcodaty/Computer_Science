import sys


class Stack:
  def __init__(self):
    self.stack = []

  def push(self, element):
    self.stack.append(element)

  def pop(self):
    if self.isEmpty():
      return "Stack is empty"
    return self.stack.pop()

  def peek(self):
    if self.isEmpty():
      return "Stack is empty"
    return self.stack[-1]

  def isEmpty(self):
    return len(self.stack) == 0

  def size(self):
    return len(self.stack)

# Create a stack
myStack = Stack()

def main():
    print("1. Insert")
    print("2. Remove")
    print("3. View")
    print("4. Empty")
    print("5. Size")
    print("6. Exit")

    choice = int(input("What is your choice?"))


    if choice == 1:
        insertion = int(input("Input element to insert"))
        myStack.push(insertion)
        main()
    if choice == 2:
        myStack.pop()
        main()
    if choice == 3:
        myStack.peek()
        main()
    if choice == 4:
        myStack.isEmpty()
        main()
    if choice == 5:
        myStack.size()
        main()
    if choice == 6:
        sys.exit()



main()


