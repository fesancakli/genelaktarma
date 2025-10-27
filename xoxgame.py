import copy
from colorama import Fore
from colorama import Style
liste=[]
i=0
MAINTABLE=[[" "," "," "],
           [" "," "," ",],
           [" "," "," "]]
def define_user():
    global user1
    global user2
    user1 = input("Which character do you want to choose X OR O : ")
    if user1=="X":
        user2="O"
    elif user1=="O":
        user2="X"
    else:
        while user1!="X" and user1!="O":
            print(Fore.RED+"Enter a valid value X OR Y")
            print(Style.RESET_ALL)
            user1 = input("Which character do you want to choose X OR O : ")
            if user1=="X":
                user2="O"
            elif user1=="O":
                user2="X"
    print("user1->{}\tuser2->{}".format(user1,user2))
def take_input():
    global liste
    global i
    global x
    global y
    if i%2==0:
        print("user1 turn")
    else:
        print("user2 turn")
    chose=int(input("which point do you chose from 1-9 :"))
    if chose<1 or chose>9 or (chose in liste):
        print(Fore.RED+"Chose a valid place")
        print(Style.RESET_ALL)
        while chose<1 or chose>9 or (chose in liste):
            chose=int(input("which point do you chose from 1-9 :"))
            if chose<1 or chose>9 or (chose in liste):
                print(Fore.RED+"Chose a valid place")
                print(Style.RESET_ALL)
    liste.append(chose)
    x=(chose-1)//3
    y=(chose-1)%3
    if i%2==0:
        MAINTABLE[x][y]=copy.deepcopy(user1)
    else:
        MAINTABLE[x][y]=copy.deepcopy(user2)
def print_table():
    global MAINTABLE
    print("   {} | {} | {}\n"
      "-----------\n"
      "   {} | {} | {}\n"
      "-----------\n"
      "   {} | {} | {}\n".format( MAINTABLE[0][0], MAINTABLE[0][1], MAINTABLE[0][2],
    MAINTABLE[1][0], MAINTABLE[1][1], MAINTABLE[1][2],
    MAINTABLE[2][0], MAINTABLE[2][1], MAINTABLE[2][2])
      )
def iswin(board):
    linescheck = [
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)]
    ]
    for line in linescheck:
        temp = [board[row][col] for row, col in line]
        if temp == ['X', 'X', 'X'] or temp == ['O', 'O', 'O']:
            return True
    return False
define_user()
print("   {} | {} | {}\n"
      "-----------\n"
      "   {} | {} | {}\n"
      "-----------\n"
      "   {} | {} | {}\n".format(1,2,3,4,5,6,7,8,9)
    )
while i<9:
    take_input()
    print_table()
    i+=1
    if iswin(MAINTABLE):
        print(Fore.BLUE+"USER1 WON!!")
        print(Style.RESET_ALL)
        break
    if i==9:
        break
    take_input()
    print_table()
    i+=1
    if iswin(MAINTABLE):
        print(Fore.BLUE+"USER2 WON!!")
        print(Style.RESET_ALL)
        break
if i==9:
        print(Fore.RED+"NO ONE WON:(")
        print(Style.RESET_ALL)
