from random import shuffle
from graphics import *


def DrawPicture(filename, x, y, win):
    img = Image(Point(x, y), filename)
    img.draw(win)
    return img

def DecideWhichCard(images, x, y):
    for i in range(len(images)):
        img = images[i]
        p = img.getAnchor()
        if (x >= p.getX() - 0.35 and x <= p.getX() + 0.35) and (y >= p.getY() - 0.75 and y <= p.getY() + 0.75): return i
    return -1

def HasItBeenClickedBefore(images, exposedList, x, y):
    index = DecideWhichCard(images, x, y)
    if index == -1: return False
    return exposedList[index]
	
def CheckMatches(card1, card2):
    return card1 == card2

def InsertInsideTheTopPlayer(playerName, timeElapsed, totalMoves):
    filename = "TopPlayersScores.txt"
    data = []
    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if line == "" or line == "\n": continue
                try: 
                    (name, moves, elapsed) = line.split()
                    data.append((float(elapsed), name, int(moves)))
                except: pass
                
    except: # File not found -> create new and insert first record
        pass
    data.append((timeElapsed, playerName, totalMoves))
    data.sort()    
    # Save new updated information
    with open(filename, "w") as f:
        for i in range(min(5, len(data))):
            elapsed, name, moves = data[i]
            f.write(name + " " + str(moves) + " " + str(elapsed) + "\n")



def main():
    # Define list of picture file names
    FileNames = [ "0.gif", "1.gif", "2.gif", "3.gif", "4.gif", "5.gif", "6.gif", "7.gif" ]
    # Define list of picture names used for game (its just two times "FileNames")
    PicturesNamesList = list(FileNames) + list(FileNames)
    # Shuffle list of picture names using shuffle from random module
    shuffle (PicturesNamesList)
    # Create boolean list
    IsItExposedList = [False for i in range(len(PicturesNamesList))]
    win = GraphWin("Match the animals")
    win.setCoords(0,0,10,10)
    # Draw background image
    bgImg = DrawPicture("background.gif", 5, 5, win)
    
    # Create text labels and Entry for username
    t1 = Text(Point(5,7), "MATCH THE ANIMALS")
    t1.setFill("white")
    t1.setFace("arial")
    #t1.setStyle("bold")
    t1.setSize(20)
    t1.draw(win)
    t2 = Text(Point(5,6), "ENTER YOUR NAME")
    t2.setFill("white")
    t2.setFace("arial")
    t2.setSize(14)
    t2.draw(win)
    e = Entry(Point(5,5), 10)
    e.draw(win)
    keyText = Text(Point(5,4), "CLICK TO CONTINUE")
    keyText.setFill("white")
    keyText.setFace("arial")
    keyText.setSize(14)
    keyText.draw(win)
    # Wait untill user enter something into Entry and click 
    while len(e.getText()) == 0:
        win.getMouse()
        t2.setFill("red")
    t1.move(-3.5, 1)
    t1.setText("MATCH THE\nANIMALS")
    t2.move(-3.5, 0)
    t2.setFill("white")
    t2.setSize(15)
    t2.setText(e.getText())
    keyText.move(-3.5, 0.75)
    keyText.setSize(15)
    matchesText = Text(Point(1.5, 4), "")
    matchesText.setFill("white")
    matchesText.setFace("arial")
    matchesText.setSize(15)
    matchesText.draw(win)
    statusText = Text(Point(6, 0.5), "Status: ")
    statusText.setFill("green")
    statusText.setSize(15)
    statusText.draw(win)
      
    # Draw left box that will hold current game stats
    p1 = Polygon(Point(0.25,7), Point(2.75,7), Point(2.75, 3), Point(0.25, 3) )
    p1.setOutline("white")
    p1.draw(win)
    # Remove Entry box
    e.undraw()
    # Draw right box that will hold images 
    p2 = Polygon(Point(3, 9), Point(9, 9), Point(9, 1), Point(3, 1) )
    p2.setOutline("white")
    p2.draw(win)
    # Draw images
    offset_x, offset_y = 3.75, 2
 
    PicturesList, Covers = [], []
    for i in range(4):
        for j in range(4):
            index = i * 4 + j
            PicturesList.append(DrawPicture(PicturesNamesList[index], offset_x + 1.5 * j, offset_y + 2 * i, win))
            Covers.append(DrawPicture("cover.gif", offset_x + 1.5 * j, offset_y + 2 * i, win))
            #win.getMouse()
    # B part
    BeginTime = time.time()
    # C part
    PlayerMoves, MatchesSoFar = 0, 0
    #DrawPicture(PicturesNamesList[0], 1, 1, win)
    prevCard = None
    statusText.setText("Select a card")
    # Part D. Game loop
    while MatchesSoFar * 2 != len(PicturesNamesList):
        keyText.setText("Key: " + str(MatchesSoFar))
        matchesText.setText("Move: " + str(PlayerMoves))
        # Get user mouse click coords
        p = win.getMouse()
        statusText.setFill("green")
        # Find card on whitch was user click
        index = DecideWhichCard(PicturesList, p.getX(), p.getY())
        # This was not a card -> show warning message
        if index == -1: 
            statusText.setFill("red")
            statusText.setText("Please select a card")
            continue
        # Otherwise prevent doubleclick for same card 
        if HasItBeenClickedBefore(PicturesList, IsItExposedList, p.getX(), p.getY()) == False:
            # Count as finished movemet
            PlayerMoves += 1
            # Mark card as 'exposed'
            IsItExposedList[index] = True
            # Remove cover
            Covers[index].undraw()
            # If this is first uncovered card
            if prevCard == None: 
                # Show information about next movement
                statusText.setFill("green")
                statusText.setText("Pick one more card")
                # Remember current card index
                prevCard = index
            # This was second uncovered card click. -> check if previous and current cards have same names
            elif CheckMatches(PicturesNamesList[prevCard], PicturesNamesList[index]):
                # Pair found -> Show message to user about this
                statusText.setFill("green")
                statusText.setText("Congratz you found pair of cards ! Keep goin...")
                # One more pair uncovered
                MatchesSoFar += 1
                # Zerofill previous card index for next matches
                prevCard = None
            else: # This was second uncovered click but card names differ
                # Show warning message
                statusText.setFill("red")
                statusText.setText("Sorry your picks does not matchs. Try again")
                # Update user score information
                keyText.setText("Key: " + str(MatchesSoFar))
                matchesText.setText("Move: " + str(PlayerMoves))
                # Wait until user make second click
                win.getMouse()
                # Draw cover for both clicked cards 
                p1, p2 = PicturesList[index].getAnchor(), PicturesList[prevCard].getAnchor()                
                Covers[index] = DrawPicture("cover.gif", p1.getX(), p1.getY(), win)
                Covers[prevCard] = DrawPicture("cover.gif", p2.getX(), p2.getY(), win)
                IsItExposedList[index], IsItExposedList[prevCard] = False, False
                prevCard = None
    elapsedTime = time.time() - BeginTime
    # Game succesfuly over
    keyText.setText("Key: " + str(MatchesSoFar))
    matchesText.setText("Move: " + str(PlayerMoves))   
    statusText.setFill("green")
    statusText.setText("Congratulations You win the game !\n Total time elapsed: "  + str(int(elapsedTime)) + " (sec)")# Click to close window")
    # Update top 5 score file
    InsertInsideTheTopPlayer(t2.getText(), elapsedTime, PlayerMoves)
    win.getMouse()
    win.close()

if __name__ == "__main__":
    main()