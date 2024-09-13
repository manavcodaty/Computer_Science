import time


def encrypt():    
    print("Enter desired word: ")
    word = input()

    print("Enter the shift value: ")

    shift = int(input())

    encrypted_word = ""

    for i in range(len(word)):
        char = word[i]
        char = chr(ord(char) + shift)
        encrypted_word += char
        
    print("The encrypted word is: ", encrypted_word)
    time.sleep(2)
    main()
    
def decrypt():
    print("Enter the encrypted word: ")
    word = input()
    
    print("Enter the shift value: ")
    shift = int(input())
    
    decrypted_word = ""
    
    for i in range(len(word)):
        char = word[i]
        char = char.lower()
        char = chr(ord(char) - shift)
        decrypted_word += char
        
    print("The decrypted word is: ", decrypted_word)
    time.sleep(2)
    main()
    
    
def main():
    print("1. Encrypt")
    print("2. Decrypt")
    choice = int(input())
    
    if choice == 1:
        encrypt()
    else:
        decrypt()
        
main()