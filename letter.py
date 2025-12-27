#imports


#get the text from user
def get_user_text():
    text = input("Please Enter Your Text: ")
    return text

#check
def check_text(text):
    text_list = text.split(" ")
    longest_word = max(text_list, key=len)
    count = 0
    for _ in longest_word:
        count += 1
    return f"the longest word(s) is : {longest_word}({count} letters)"
     

#main function
def main():
    text = get_user_text()
    print(check_text(text))

#run project
if __name__ == "__main__":
    main()
