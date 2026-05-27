# Predefined username and password 
predefined_username = "Ankur"
predefined_password = "2005"

username = input("Enter your username : ")
password = input("Enter your password : ")

# Username and password match
if(username==predefined_username):
    if(password==predefined_password):
        print("Welcome! Login Successfully")
    else:
        print("Incorrect Password!")
else:
    print("Invalid Username!")        
