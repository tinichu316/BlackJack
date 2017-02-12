import random

isVictory = False
suits = ['♠', '♣', '♦', '♥']
numbers = ['Ace','2','3','4','5','6','7','8','9','10','Jack','Queen','King']
cardsDealt = 0
hand = []
houseHand = []
bet = 0
wallet = 1000

#below 19 means the value to add per hand value below 19 to continue hitting.
#above 18 means the value to minus per hand value above 18 to stop hitting
#rand deviation means the standard deviation centered at 0 to stop or continue hitting
AIWeights = {"below19": 0.04, "above18" : 0.2, 'randDeviation' : 0.04}


def generateCards():
    """Populates the deck so I don't have to manually type out all 52 cards."""
    cards = []
    for number in range(13):
        for suit in range(4):
            card = [numbers[number], suits[suit]]
            cards.append(card)
    return cards

def shuffle(cards):
    return random.sample(cards,len(cards))

def deal(hand, deck):
    """Deals one card to the hand"""
    global cardsDealt
    hand.append(deck.pop(0))
    cardsDealt += 1


def newRound():
    """Resets the deck."""
    y = shuffle(generateCards())
    return y

def getValue(hand):
    total = 0
    numberAces = 0
    handStr = ""
    aceIndexes = [] #indexes of the Aces so we can remove them later
    #moves the aces to the end for calculation sake
    for i in range(len(hand)):
        if hand[i][0] == 'Ace':
            hand.append(hand[i])
            aceIndexes.append(i)
    #removes the extra aces
    for index in aceIndexes[::-1]:
        del hand[index]
    
    #counts the number of aces
    for x in range(len(hand)):
        if hand[::-1][x][0] == 'Ace':
            numberAces += 1

    for card in hand:
        if card[0] in ['Jack', 'Queen', 'King']:
            total += 10
        elif card[0] == 'Ace':
            if total + numberAces < 12:
                total += 11
            else:
                total += 1
        elif card[0] == 'Hidden':
            total += 0
        else:
            total += int(card[0])
        handStr += " {} {}; ".format(card[0], card[1])
    return total, handStr


def printValue(hand, isPlayer):
    total, handStr = getValue(hand)
    print("{}: [".format("Your hand" if isPlayer else "Dealer has") + handStr + "]")
    print("Value: {}".format(total))

def numberDuplicates(num, nums):
    duplicates, k = 0, []
    for i in nums:
        k.append(i)
    k.remove(num)
    while num in k:
        duplicates += 1
        k.remove(num)
    return duplicates

def chanceBustorStay(value, guessNextProbabilities): #no aces in hand
    chanceB = 0.00
    chanceS = 0.00
    # we need both probabilities since the percentages don't add up to 1 (we don't know the player's hand)
    for i in guessNextProbabilities:
        if value < 11:
            chanceB = 0.00
            chanceS = 1.00
        elif value + i[0] > 21:
            chanceB += i[1]
        else:
            chanceS += i[1]
    #print("The chance of busting is {}. The chance of staying is {}.".format(chanceB, chanceS))
    return chanceB, chanceS

def holdorStay(hand, guessNextValue):
    weights = AIWeights
    #Now for determining whether or not to hold or stand:
    value = getValue(hand)[0]
    #should add a modifier based on current value.
    modifier = 0.00
    if value < 19:
        modifier += weights['below19']*(18-value) #lower the value, higher the modifier
    else:
        modifier += -0.80 + (21-value)*weights['above18']
    #print("The modifier is: ", modifier)

    randModifier = random.normalvariate(0, weights['randDeviation'])
    #print("The random modifier is: ", randModifier)

    if any(card[0] == "Ace" for card in hand): #if there is an ace in the hand
        total = 0
        for card in hand:
            if card[0] in ['Jack', 'Queen', 'King']:
                total += 10
            elif card[0] == 'Ace':
                    total += 1
            else:
                total += int(card[0])
        bust, stay = chanceBustorStay(total, guessNextValue)
        if bust > stay + modifier + randModifier: #will be likely to bust
            return "stay"
        else:
            return "hit"
    else:
        bust, stay = chanceBustorStay(value, guessNextValue)
        if bust > stay + modifier + randModifier: #will be likely to bust
            return "stay"
        else:
            return "hit"

def houseAI(hand):
    """Decides the perceived best move, with some randomness, whether it is to stand or hit."""
    #AIWeights = {'duplicates': {0: (0.45,0.60), 1: (0.25,0.35), 2:(0.05,0.10), 3: 0}}

    guessNextValue = list(range(1,14)) #The range of values (card values aka king = 13) of the next possible card with a respective possibility
    guessNextValue = [list(a) for a in zip(guessNextValue, [4/52]*len(guessNextValue))] #makes the probabilities a list of 2 item lists, also resets it and recalculates it
    #sees if there are any multiples in the hand
    cardValues = [] #values of all the cards in the hand (card numbers 1-13)
    for card in hand:
        if card[0] in ['Jack', 'Queen', 'King']:
            cardV = (['Jack', 'Queen', 'King'].index(card[0]) + 11)
        elif card[0] == 'Ace':
            cardV = 1
        else:
            cardV = int(card[0])
        cardValues.append(cardV)

    for num in cardValues:
        #each card that we have we want to reduce the percieved probability of drawing another card of that type
        dupes = numberDuplicates(num, cardValues)
        guessNextValue[num - 1][1] = (3 - dupes)/(52 - cardsDealt)
    #recalculate the other percentages
    for i in guessNextValue:
        if i[0] not in cardValues: #the house does not have this card, increase the likelyhood of drawing it
            i[1] = 4/(52 - cardsDealt)

    #Just prints the probabilities out for debugging purposes.
    #for i in guessNextValue:
    #   print("Card {}. Probability: {:.3f}%".format(numbers[i[0] - 1], i[1]))

    return holdorStay(hand,guessNextValue)

#we want to have a  higher score than the dealer but a lower score than 21 (or bust!)

"""
currentDeck = newRound()
deal(hand, currentDeck)
deal(hand, currentDeck)
printValue(hand)
print("You have: ", hand)

deal(houseHand, currentDeck)
deal(houseHand, currentDeck)
printValue(houseHand)
print("Dealer has: ", houseHand)
print(houseAI(houseHand))
deal(houseHand, currentDeck)
printValue(houseHand)
print(houseAI(houseHand))
"""

def gameStart():
    global currentDeck, hand, houseHand
    hand, houseHand = [], []
    currentDeck = newRound()
    deal(hand, currentDeck)
    deal(hand, currentDeck)
    deal(houseHand, currentDeck)
    deal(houseHand, currentDeck)

def isBust(hand):
    return True if getValue(hand)[0] > 21 else False

def printFiller():
    print("""=====================================================================================""")

def playAnotherRound():
    print("Play another round?")
    resp = input("[Player]: ")
    if resp == "yes" or resp == 'y':
        gameStart()
        printFiller()
    elif resp == 'bet' or resp == 'b':
        bettingMode()
        gameStart()
        printFiller()
    elif resp == "no" or resp == 'n':
        exit()
    else:
        playAnotherRound()

def bettingMode():
    global bet
    isBetting = True
    while isBetting:
        bet = input("How much would you like to bet per round? ($1-$100) ") #assuming its an int.
        if bet.isdigit():
            if int(bet) in range(1, 101):
                bet = int(bet)
                isBetting = False
            else:
                print("That number is not in the range!")
        else:
            print("That's not an integer number!")

bettingMode()




gameStart()
while wallet >= bet: #actually just goes forever right now
    if not isBust(hand):
        printValue(hand, True)
        houseHidden = [houseHand[0],["Hidden", "Card"]]
        printValue(houseHidden, False)
        print("Do you hit or stay?")
        resp = input("[Player]: ").lower()
        if resp == "hit" or resp == 'h':
            deal(hand, currentDeck)
            printFiller()
        elif resp == 'surrender':
            printFiller()
            wallet -= (bet//2)
            print("You have surrendered this round! You lose half of your bet.")
            printValue(houseHand, False)
            print("You still have [${}].".format(wallet))
            gameStart()
            printFiller()
        elif resp == 'exit' or resp == 'quit':
            printFiller()
            print("Would you like to leave the Blackjack table?")
            resp2 = input("[Player]: ").lower()
            if resp2 == 'yes' or resp2 == 'y':
                # update player's wallet in the main function; save it.
                break
        elif resp == "stay" or resp == 's':
            printFiller()
            #run the dealer's AI
            #unlike some rules of blackjack where the dealer must hit if their card value is below 18, our dealer is smart.. Might want to implement machine learning with weights stored in a .json file
            printValue(houseHand, False)
            while houseAI(houseHand) == 'hit': #will be 'stay' or 'hit'
                print("I'll take a hit!")
                deal(houseHand, currentDeck)
                printValue(houseHand, False)
            if isBust(houseHand):  # If the house busts
                wallet += bet
                print("Darn! I bust! The money's yours.")
                print("You still have [${}].".format(wallet))
                playAnotherRound()

            else:
                print("I will stay.")
                printFiller()
                playerValue = getValue(hand)[0]
                houseValue = getValue(houseHand)[0]
                if playerValue == 21 and houseValue == 21:
                    print("Both Blackjacks! You get a pass. No money is lost.")
                elif playerValue == houseValue:
                    print("Wow, we tied! You get a pass. No money is lost.")
                elif playerValue > houseValue:
                    wallet += bet
                    print("Congratulations! You won this round.")
                elif houseValue == 21:
                    wallet -= bet
                    print("I had a Blackjack all along. It was only natural that you lost.")
                else:
                    wallet -= bet
                    print("Ouch, I guess a {} is bigger than a {} after all ;)".format(houseValue, playerValue))
                print("You still have [${}].".format(wallet))
                playAnotherRound()

    else:
        printValue(hand, True)
        wallet -= bet
        print("Ouch! looks like you busted!")
        printValue(houseHand, False)
        print("You still have [${}].".format(wallet))
        playAnotherRound()




#m = [['Ace', '♠'], ['Ace','♠'], ['Ace','♠']]
#print(getValue(m))










