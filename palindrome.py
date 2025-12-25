#imports


#get the word,phrase,etc from the user
def get_user_word():
    word = str(input("please enter your word or phrase : "))
    return word
#check it if it is palidrome
def check_is_palindrome():
    phrase = get_user_word()
    rev = "".join(reversed(phrase))
    if rev == phrase:
        print("The string is a palindrome.")
    else:
        print("The string is not a palindrome")
#run the application
if __name__ == "__main__":
    check_is_palindrome()