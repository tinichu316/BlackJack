import random
defaultMult = 2

def simulateGame(multToStop, chanceNothing, bet, rounds ):
    initialWallet = 1000000 #1million
    bet *= defaultMult
    wallet = initialWallet
    percentWin = chanceNothing
    multiplier = defaultMult
    r = 0
    while r < rounds:
        if multiplier == multToStop:
            wallet += bet*multiplier
            multiplier = defaultMult
            r += 1
        else:
            wallet -= bet
            luck = random.randrange(0, 100001)
            chance = int(percentWin * 100000)
            if luck > chance:
                multiplier *= 2
            else:
                multiplier = defaultMult
    if multiplier > 1:
        #print("Final Cashout.")
        wallet += bet*multiplier
        
    #print("After {} rounds, cashing out at {}x, betting ${} at {}% to win..".format(r, multToStop, bet, 1-chanceNothing))
    #print("The profit is: ${}.".format(wallet - initialWallet))
    return wallet - initialWallet

def changeMult(maxMult, timesEach, winPercent):
    mults = [2]
    mult = 2
    averageAmt = 1000
    while mult < maxMult:
        mult *= 2
        mults.append(mult)
    profit = [0]*len(mults)
    for i in range(len(mults)):
        averageProfit = 0
        for x in range(averageAmt):
            averageProfit += simulateGame(mults[i], winPercent, 5, timesEach)
        profit[i] = averageProfit/averageAmt
    table = zip(mults, profit)
    print("For the given multiplier X, the profit is:")
    print("X | Profit")
    for i in table:
        print("{:>1} | {:1}".format(i[0], i[1]))
    return mults, profit

for i in range(10):
    print("At {}% lose chance,".format((i+43)/100))
    changeMult(128, 10, (i+43)/100)      
       
#def changePercent(low, high):
    #tables = [0]*(high - low + 1)    
    #lowD = int(low*100)
    #highD = int(high*100)
    #m = low
    #for i in range(high-low + 1):
        #print(i)
        #print('poop', i + low)
        #[mults, profit] = changeMult(128, 5, (i + lowD)/100)
        #tables[i] = [mults, profit]
        #print("Did percent {}x.".format((i + lowD)/100))
    #for table in tables:
        #print("For the given multiplier X, @{}%, the profit is:".format((m + low)//100))
        #print("X | Profit")
        #m += 1
        #for i in table:
            #print("{:>1} | {:1}".format(i[0], i[1]))   
            
      

            
     

        


