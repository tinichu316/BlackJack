import random


isVictory = False
suits = ['Spades', 'Clubs', 'Diamonds', 'Hearts']
numbers = ['Ace','2','3','4','5','6','7','8','9','10','Jack','Queen','King']
cardsDealt = 0
hand = []
houseHand = []

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
    """Deals one card to the player"""
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
    #moves the aces to the end for calculation sake
    for i in range(len(hand)):
        if hand[i][0] == 'Ace':
            hand.append(hand[i])
            del hand[i]

    while hand[-i][0] == 'Ace' and i < len(hand):
        numberAces = i
        i += 1

    for card in hand:
        if card[0] in ['Jack', 'Queen', 'King']:
            total += 10
        elif card[0] == 'Ace':
            if total + numberAces < 12:
                total += 11
            else:
                total += 1
        else:
            total += int(card[0])
        handStr += " {} of {}; ".format(card[0], card[1])
    return total, handStr


def printValue(hand):
    total, handStr = getValue(hand)
    print("Your hand: [" + handStr + "]")
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

def houseAI(hand):
    """Decides the perceived best move, with some randomness, whether it is to stand or hit."""
    #AIWeights = {'duplicates': {0: (0.45,0.60), 1: (0.25,0.35), 2:(0.05,0.10), 3: 0}}

    guessNextValue = list(range(1,14)) #The range of values (card values aka king = 13) of the next possible card with a respective possibility
    guessNextValue = [list(a) for a in zip(guessNextValue, [4/52]*len(guessNextValue))] #makes the probabilities a list of 2 item lists, also resets it and recalculates it
    value = getValue(hand)[0] #current point value
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
    for i in guessNextValue:
        print("Card {}. Probability: {:.3f}%".format(numbers[i[0] - 1], i[1]))

    #Now for determining whether or not to hold or stand:





#we want to have a  higher score than the dealer but a lower score than 21 (or bust!)


currentDeck = newRound()
deal(hand, currentDeck)
deal(hand, currentDeck)
printValue(hand)
print("You have: ", hand)

deal(houseHand, currentDeck)
deal(houseHand, currentDeck)
printValue(houseHand)
print("Dealer has: ", houseHand)
houseAI(houseHand)








