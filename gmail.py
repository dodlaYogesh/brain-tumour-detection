name=input("enter your name: ")
rno=input("enter ur hall Ticket Number: ")
college=input('college (Acet/Adtp) :')
if college.lower() == "acet":
    code="Acet.ac.in"
elif college.lower() == "adtp":
    code="Adtp.edu.in"
else:
    print("please enter correct code: ")
print(rno+"@"+code)
