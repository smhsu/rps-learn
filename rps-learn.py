from collections import deque
import random
import sys
 
SAVE_ROUNDS = 10 # Length of player weapons history
LRATE = 0.01 # Learn rate for losses
TIE_LRATE = 0.005 # Learn rate for ties
ROCK = 0 # If you change these, modify all random generator calls too!
PAPER = 1
SCIS = 2
GUN = 3
 
def recordRecentWeapon(weapon, record):
    if weapon == ROCK: addMe = -0.33
    elif weapon == PAPER: addMe = 0.33
    elif weapon == SCIS: addMe = 1
    else: assert False, "Invalid weapon"   
 
    record.pop()
    record.appendleft(addMe)
 
def askWeapon():
    validWeapon = False
    while not validWeapon:
        player = raw_input("Rock paper scissors.  Choose: ").lower()
        if player in ["rock", "r"]:
            return ROCK
        elif player in ["paper", "p"]:
            return PAPER
        elif player in ["scissors", "s"]:
            return SCIS
        elif player == "gun":
            return GUN
        elif player in ["q", "quit", "exit"]:
            sys.exit(0)
        else:
            print "Sorry, that is not a valid weapon. Try again."
 
def weaponThatBeats(weapon):
    if weapon == ROCK:
        return PAPER
    elif weapon == PAPER:
        return SCIS
    elif weapon == SCIS:
        return ROCK
    else: assert False, "Invalid weapon"
 
"""
Player loss: -1
Tie: 0
Player win: 1
Player win w/ gun: 2
"""
def getResult(player, comp):
    if player == ROCK:
        if comp == ROCK:
            print "Computer chooses rock. Tie."
            return 0
        elif comp == PAPER:
            print "Your rock died. To paper. It must be allergic. wtf?! Computer wins!"
            return -1
        elif comp == SCIS:
            print "Your rock was a cut above the computer's scissors. You win!"
            return 1
        else:
            assert False, "Computer chose invalid weapon?"
 
    elif player == PAPER:
        if comp == ROCK:
            print "The computer's rock suffocates as you wrap it with your paper. You win!"
            return 1
        elif comp == PAPER:
            print "Computer chooses paper. Tie."
            return 0
        elif comp == SCIS:
            print "Your poor paper was cut in half. What a tragedy. Computer wins!"
            return -1
        else:
            assert False, "Computer chose invalid weapon?"
 
    elif player == SCIS:
        if comp == ROCK:
            print "You try as hard as you can to cut rock in half, but fail. You do succeed in breaking your scissors, though.  Computer wins!"
            return -1
        elif comp == PAPER:
            print "The computer's paper falls under the mecriless snips of your scissors. You win!"
            return 1
        elif comp == SCIS:
            print "Computer chooses scissors. Tie."
            return 0
        else:
            assert False, "Computer chose invalid weapon?"
 
    elif player == GUN:
        print "You have a f'ing gun.  What more needs to be said?"
        return 2
 
        else:
            assert False, "Player chose invalid weapon?"
 
def printScores(playerScore, compScore, rounds):
    print "Player score:", playerScore
    print "Computer score:", compScore
    print "Rounds played:", rounds
 
def dotProduct(values, weights):
    assert len(values) == len(weights)
    return sum(float(value) * weight for value, weight in zip(values, weights))
 
def pred(record, weights):
    scores = []
    for weapon in weights:
        scores.append(dotProduct(record, weapon))
 
    if scores[0] == scores[1] and scores[1] == scores[2]:
        return random.randint(0,2)
 
    return scores.index(max(scores))
 
def updateWeights(weights, record, correct, wrong):
    for i in range(len(record)):
        weights[correct][i] += LRATE * record[i]
        weights[wrong][i] -= LRATE * record[i]
 
def updateWeights_tie(weights, record, correct):
    for i in range(len(record)):
        weights[correct][i] += TIE_LRATE * record[i]
 
def intro():
    print "rps-learn.py"
    print "Silas Hsu, August 2013"
    print ""
    print "Welcome to machine learning rock-paper-scissors! I will try to",
    print "defeat you based off your choices."
    print "At the weapon selection prompt,",
    print "you may also type 'r', 'p', or 's' as shortcuts; or",
    print "'q', 'quit', or 'exit' to stop playing."
    print ""
 
def main():
    # A bunch of initialization that has to be done...
    numR, numP, numS = 0, 0, 0 # Number of times player has choosen each weapon
    playerScore, compScore = 0, 0
    rounds = 1
    roundsInclGun = 0
 
    global LRATE, TIE_LRATE
    weights = [[0.0]*(SAVE_ROUNDS+3) for i in range(3)] # 3 for each weapon
    record = deque([0.0]*SAVE_ROUNDS)
    weaponFreq = [0.0, 0.0, 0.0]
    inVector = list(record)
    inVector.extend(weaponFreq)
 
    playerWeapon = -1
    compWeapon = random.randint(0,2)
    intro()
 
    try:
        while True:
            roundsInclGun += 1
            playerWeapon = askWeapon()
            # Decide who wins
            result = getResult(playerWeapon, compWeapon)
            if result == -1:
                compScore += 1
            elif result == 0: # Tie, update weights!
                updateWeights_tie(weights, inVector, weaponThatBeats(playerWeapon))
            elif result == 1: # Player won, update weights!
                playerScore += 1
                updateWeights(weights, inVector, weaponThatBeats(playerWeapon), compWeapon) 
            elif result == 2: # Gun
                playerScore += 1
                printScores(playerScore, compScore, roundsInclGun)
                continue
 
            printScores(playerScore, compScore, roundsInclGun)
 
            # Update records, get computer's next weapon
            recordRecentWeapon(playerWeapon, record)
            if rounds < SAVE_ROUNDS: # Will trigger (SAVE_ROUNDS - 1) times
                LRATE += 0.09/(SAVE_ROUNDS-1)
                TIE_LRATE = LRATE/2
 
            if playerWeapon == ROCK:
                numR += 1
            elif playerWeapon == PAPER:
                numP += 1
            elif playerWeapon == SCIS:
                numS += 1
            weaponFreq[0] = float(numR)/float(rounds)
            weaponFreq[1] = float(numP)/float(rounds)
            weaponFreq[2] = float(numS)/float(rounds)
 
            inVector = list(record)
            inVector.extend(weaponFreq)
            compWeapon = pred(inVector, weights)
 
            rounds += 1
 
    except KeyboardInterrupt:
        print ""
        sys.exit(0)
 
 
if __name__ == "__main__":
    main()
	