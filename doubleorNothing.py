import random
percentWin = 0.50 #percent that it is NOTHING
#0.44 found through many trials and tests for default multiplier of 1
#0.50 is good for 2x or nothing
defaultMultiplier = 2


# Could try to make this a simulation and run it a bunch with the user always tapping out at a certain multiplier and see the overall profit.
wallet = 1000
bet = 0
multiplierText = {1: """
  ██╗
████║
╚═██║
  ██║
  ██║
  ╚═╝
               """,
                  2: """
██████╗
╚════██╗
 █████╔╝
██╔═══╝
███████╗
╚══════╝
               """,
                  3: """
██████╗
╚════██╗
 █████╔╝
 ╚═══██╗
██████╔╝
╚═════╝
               """,
                  4: """
██╗  ██╗
██║  ██║
███████║
╚════██║
     ██║
     ╚═╝
               """,
                  5: """
███████╗
██╔════╝
███████╗
╚════██║
███████║
╚══════╝
               """,
                  6: """
 ██████╗
██╔════╝
███████╗
██╔═══██╗
╚██████╔╝
 ╚═════╝
               """,
                  7: """
███████╗
╚════██║
    ██╔╝
   ██╔╝
   ██║
   ╚═╝
                  """,
                  8: """
 █████╗
██╔══██╗
╚█████╔╝
██╔══██╗
╚█████╔╝
 ╚════╝
               """,
                  9: """
 █████╗
██╔══██╗
╚██████║
 ╚═══██║
 █████╔╝
 ╚════╝
                  """,
                  0: """
 ██████╗
██╔═████╗
██║██╔██║
████╔╝██║
╚██████╔╝
 ╚═════╝
               """,
                  'x': """
██╗  ██╗
╚██╗██╔╝
 ╚███╔╝
 ██╔██╗
██╔╝ ██╗
╚═╝  ╚═╝
               """,
                  'tabs': """






               """
                  }
isBetting = True

while isBetting:
    bet = input("How much would you like to bet per go? ($1-$5) ")
    bet = bet[-1]
    if bet.isdigit():
        if int(bet) in range(1, 6):
            bet = int(bet)
            isBetting = False
        else:
            print("That number is not in the range!")
    else:
        print("That's not an integer number!")


def addPara(para1, para2):  # adds two characters together
    para1 = para1.split('\n')
    para2 = para2.split('\n')
    #adds trailing spaces aka padding based on the width of the 3rd/4th line
    width = str(len(para1[3])) if len(para1[3]) > len(para1[2]) else str(len(para1[2]))
    for i in range(len(para1)):
        string = '{:' + width + '}'
        para1[i] = string.format(para1[i])

    newChar = [''] * len(para1)  # times the height
    for i in range(len(para1)):  # going down each line
        newChar[i] = para1[i] + ' ' + para2[i]
    newChar = '\n'.join(newChar)
    return newChar


def printMultiplier(mult):
    mult = str(mult)
    multStr = multiplierText[int(mult[0])]
    if len(mult) > 1:
        for digit in range(1,len(mult)):
            multStr = addPara(multStr, multiplierText[int(mult[digit])])
    multStr = addPara(multStr, multiplierText['x'])

    print(multStr)

def printMoney(amt):
    print("You have [${}] and are betting [${}].".format(amt, bet))

def printFiller():
    print("""=====================================================================================""")

multiplier = defaultMultiplier
bet *= defaultMultiplier
isPlaying = True

while isPlaying:
    printMoney(wallet)
    print("Your bet will be multiplied by {}.".format(multiplier))
    printMultiplier(multiplier)
    print("Do you go or stop?")
    resp = input("[Player]: ").lower()
    printFiller()
    if resp == "go" or resp == 'g':
        wallet -= bet
        luck = random.randrange(0,100001)
        chance = int(percentWin *100000)
        if luck > chance:
            multiplier *= 2
        else:
            while multiplier > defaultMultiplier: #lose animation
                printMultiplier(multiplier)
                multiplier -= 1
            multiplier = defaultMultiplier

    elif resp == 'stop' or resp == 's':
        if multiplier > defaultMultiplier:
            print("You have cashed out ${}!".format(bet*multiplier))
            wallet += bet*multiplier
            multiplier = defaultMultiplier
        else:
            print("You have not put in any money! (Type 'quit' to exit)")

    elif resp == 'exit' or resp == 'quit':
        print("Would you like to leave the Double or Nothing machine?")
        resp2 = input("[Player]: ").lower()
        if resp2 == 'yes' or resp2 == 'y':
            #update player's wallet in the main function; save it.
            break








      