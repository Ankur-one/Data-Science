print("Enter PCM marks out of 100")
Math = int(input("Enter Math marks : "))
Phy = int(input("Enter Physics marks : "))
Che = int(input("Enter Chemistry marks : "))

if(Math>=65 & Phy>=55 & Che>=50 & (Math+Phy+Che)>=180) | (Math+Phy+Che >= 140):
    print("You' re eligible")
else:
    print("You' re not eligible")    