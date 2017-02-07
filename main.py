import random


isVictory = False
suits = ['Spades', 'Clubs', 'Diamonds', 'Hearts']
numbers = ['Ace','2','3','4','5','6','7','8','9','10','Jack','Queen','King']
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
    hand.append(deck.pop(0))

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
            numberAces += 1
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
    total, handStr = getValue(hand)[0], getValue(hand)[1]
    print("Your hand: [" + handStr + "]")
    print("Value: {}".format(total))

def numberDuplicates(num, nums):
    duplicates, k = 0, nums
    k.remove(num)
    while num in k:
        duplicates += 1
        k.remove(num)
    return duplicates

def houseAI(hand):
    """Decides the correct move to play, with some randomness, whether it is to stand or hit."""
    value = getValue(hand)[0]
    #sees if there are any multiples in the hand
    multiplesWeight = 0.0 #
    cardValues = []
    for card in hand:
        if card[0] in ['Jack', 'Queen', 'King']:
            cardV = (['Jack', 'Queen', 'King'].index(card[0]) + 11)
        elif card[0] == 'Ace':
            cardV = 1
        else:
            cardV = int(card[0])
        cardValues.append(cardV)

    for num in cardValues:
        if numberDuplicates(num, cardValues) > 0:







#we want to have a  higher score than the dealer but a lower score than 21 (or bust!)


currentDeck = newRound()
print(currentDeck)
deal(hand, currentDeck)
deal(hand, currentDeck)
printValue(hand)
print(hand, currentDeck)








