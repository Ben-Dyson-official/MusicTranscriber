from PIL import Image, ImageDraw, ImageFont
import time

def addTitle(bg, title): #adds a title at a set location in the file
    font = ImageFont.truetype('/Users/bendyson/Coding/NEA/Backend/SheetMusic/times new roman.ttf', 50)
    draw = ImageDraw.Draw(bg)
    draw.text((500, 30), title, font = font, align='centre')

def addAuthor(bg, author): #adds an author at a set location in the file
    font = ImageFont.truetype('/Users/bendyson/Coding/NEA/Backend/SheetMusic/times new roman.ttf', 30)
    draw = ImageDraw.Draw(bg)
    draw.text((1000, 120), author, font = font, align='centre')

def addTimeSignature(bg, timeSignature, i): #adds a time signature at a x y value
    if timeSignature=='34': #different time signatures have different formatting so I have distinguished between them
        signature = Image.open('/Users/bendyson/Coding/NEA/Backend/SheetMusic/34Time.png').convert('RGBA') #opens the saved image file
        bg.paste(signature, (180, 175+156*i), mask=signature) #actually prints to the image
        signature.close()
        nextNotePlace = 76 #set the distance to the next note for formatting
        beatsPerBar = 3 #set the amount of beats per bar to help formatting
    elif timeSignature=='44':
        signature = Image.open('/Users/bendyson/Coding/NEA/Backend/SheetMusic/44Time.png').convert('RGBA') #opens the saved image file
        bg.paste(signature, (180, 175+156*i), mask=signature) #actually prints to the image
        signature.close()
        nextNotePlace = 56  #set the distance to the next note for formatting
        beatsPerBar = 4 #set the amount of beats per bar to help formatting
    return nextNotePlace, beatsPerBar #return values that have been set by the function

def addBPM(bg, bpm): #Adds bpm to the piece in italian termns
    font = ImageFont.truetype('/Users/bendyson/Coding/NEA/Backend/SheetMusic/times new roman.ttf', 30)
    if bpm>0 and bpm<65: #picking which bpm and setting the text to the corresponding term
        text = 'Adagio'
    elif bpm>=65 and bpm<97:
        text = 'Andante'
    elif bpm>=97:
        text = 'Allegro'
    draw = ImageDraw.Draw(bg)
    draw.text((170, 120), text, font = font, align='left') #draws text to the image
    timeForCrotchet = 60/bpm*1000 #calculate the time that each crotchet will take and converts to ms
    return timeForCrotchet

def addTreble(bg, i): #Function to add a treble clef
    trebleClef = Image.open('/Users/bendyson/Coding/NEA/Backend/SheetMusic/trebleClef.png')
    bg.paste(trebleClef, (80, 150+i*156), mask=trebleClef)
    trebleClef.close() #closing for good practise

def addBass(bg, i): #Function to add a bass clef
    bassClef = Image.open('/Users/bendyson/Coding/NEA/Backend/SheetMusic/bassClef.png')
    bg.paste(bassClef, (80, 173+i*156), mask=bassClef)
    bassClef.close()

def addQuaver(bg, x, y): #Function to add a quaver
    quaver = Image.open('/Users/bendyson/Coding/NEA/Backend/SheetMusic/Quaver.png').convert('RGBA')
    bg.paste(quaver, (x, y), mask=quaver)
    quaver.close()

def addCrotchet(bg, x, y): #Function to add a crotchet
    crotchet = Image.open('/Users/bendyson/Coding/NEA/Backend/SheetMusic/Crotchet.png').convert('RGBA')
    bg.paste(crotchet, (x, y), mask=crotchet)
    crotchet.close()

def addMinim(bg, x, y): #Function to add a minim
    minim = Image.open('/Users/bendyson/Coding/NEA/Backend/SheetMusic/Minim.png').convert('RGBA')
    bg.paste(minim, (x, y), mask=minim)
    minim.close()

def addSemibreve(bg, x, y): #Function to add a semibreve
    y += 38 #as this doesnt have a stem it needs to be moved down a bit
    semiBreve = Image.open('/Users/bendyson/Coding/NEA/Backend/SheetMusic/SemiBreve.png').convert('RGBA')
    bg.paste(semiBreve, (x, y), mask=semiBreve)
    semiBreve.close()

def addSlur(bg, x, y, stretch): #Function to add a slur
    x += 5 #This and the below declaration move the slur to the bottom of the first note
    y += 55
    slur = Image.open('/Users/bendyson/Coding/NEA/Backend/SheetMusic/Slur.png').convert('RGBA')
    slur = slur.resize((stretch, round(225//11))) #resize the slur to tie to next note
    bg.paste(slur, (x, y), mask=slur)
    slur.close()

def addSharp(bg, x, y): #Function to add a slur
    x = x-15 #Moving the sharp to the left of the note
    y = y+30
    sharp = Image.open('/Users/bendyson/Coding/NEA/Backend/SheetMusic/Sharp.png').convert('RGBA')
    bg.paste(sharp, (x, y), mask=sharp)
    sharp.close()

def addCLine(bg, x, y):
    line = ImageDraw.Draw(bg)
    line.line([(x-3, y+46), (x+20, y+46)], fill=None, width=2)

def mainSheetMusic(notes, beats, title, timeSignature, bpm, SheetDirectory, author): #Main function that is called in the main program
    #Below is the y coordinates for the note C4-C5 the only notes allowed by my program
    notePlaces = {'C4':196, 'C#4':196, 'D4':189, 'D#4': 189, 'E4': 183, 'F4': 176, 'F#4': 176, 'G4': 170, 'G#4': 170, 'A4': 163, 'A#4': 163, 'B4': 157, 'C5': 150}
    stavesUsed = 0 #This variable will  record how many staves have been used
    barsUsed = 0 #This variable will record how many bars have been used
    beatsUsed = 0 #This variable will record how many beats have been used
    nextNote = 220 #This is the position of each not starting at x = 220 
    bpm = int(bpm) #makes the string input into a number

    bg = Image.open('/Users/bendyson/Coding/NEA/Backend/SheetMusic/BlankManuscript-barlines.png') #opens the background images that will be overlayed onto

    addTitle(bg, title)
    addAuthor(bg, author)
    timeForCrotchet = addBPM(bg, bpm)

    for i in range(9): #Prints treble clef and time signature on every stave
        addTreble(bg, i)
        nextNotePlace, beatsPerBar = addTimeSignature(bg, timeSignature, i)
        
    for i, chord in enumerate(notes):
        if not(i==len(beats)-1):
            beatType = (beats[i+1]-beats[i])/timeForCrotchet

        if beatType<0.7 and beatType>0.3: #quaver

            if barsUsed==4: #each stave line has 4 bars 
                barsUsed=0 #resets bars used
                stavesUsed+=1 #increments staves used
                nextNote=220 #resets next note to the first x position
            
            if beatsUsed+beatType >= beatsPerBar:

                for j, note in enumerate(chord):
                    if note[1]=='#': #checks for sharp and add it
                        addSharp(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                    if note=='C4'or note=='C#4':
                        addCLine(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                    if j==len(chord)-1:
                        addQuaver(bg, nextNote, notePlaces[note]+(stavesUsed*156)) # adds a quaver for the top note
                    else:
                        addCrotchet(bg, nextNote, notePlaces[note]+(stavesUsed*156)) #add a crotchet for chords for formatting
                nextNote = nextNote + int(0.5*nextNotePlace)+15 # next note is half the distance for the crotchet
                beatsUsed += 0.5 #add to beats used

                barsUsed += 1 #at the end of the bar increments bars used
                nextNote = 220 + barsUsed*246 #sets next note to the next bar
                beatsUsed=0
                
            else:
                for j, note in enumerate(chord):
                    if note[1]=='#': #checks for sharp and add it
                        addSharp(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                    if note=='C4'or note=='C#4':
                        addCLine(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                    if j==len(chord)-1:
                        addQuaver(bg, nextNote, notePlaces[note]+(stavesUsed*156)) # adds a quaver for the top note
                    else:
                        addCrotchet(bg, nextNote, notePlaces[note]+(stavesUsed*156)) #add a crotchet for chords for formatting
                nextNote = nextNote + int(0.5*nextNotePlace)+10 # next note is half the distance for the crotchet
                beatsUsed += 0.5 #add to beats used

        elif beatType<1.3 and beatType>0.7: #crotchet

            #checking for next stave line
            if barsUsed==4: #each stave line has 4 bars 
                barsUsed=0 #resets bars used
                stavesUsed+=1 #increments staves used
                nextNote=220 #resets next note to the first x position

            #Checking for next bar
            if beatsUsed+beatType >= beatsPerBar:
                beatsLeft = beatsPerBar-beatsUsed #calculating whats left in the bar

                #prints whatevers left in the current bar
                if beatsLeft==0.5: #quaver
                    for j, note in enumerate(chord):
                        if note[1]=='#': #checks for sharp and add it
                            addSharp(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                        if note=='C4'or note=='C#4':
                            addCLine(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                        if j==len(chord)-1:
                            addQuaver(bg, nextNote, notePlaces[note]+(stavesUsed*156)) # adds a quaver for the top note
                        else:
                            addCrotchet(bg, nextNote, notePlaces[note]+(stavesUsed*156)) #add a crotchet for chords for formatting
                    addSlur(bg, nextNote, notePlaces[note]+(stavesUsed*156), 220 + (barsUsed+1)*246-nextNote)
                    nextNote = nextNote + int(0.5*nextNotePlace)
                    beatsUsed += 0.5

                elif beatsLeft==1: #crotchet
                    for j, note in enumerate(chord):
                        if note[1]=='#':
                            addSharp(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                        if note=='C4'or note=='C#4':
                            addCLine(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                        addCrotchet(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                    nextNote = int(nextNote) + int(nextNotePlace)
                    beatsUsed += 1

                barsUsed += 1 #at the end of the bar increments bars used
                nextNote = 220 + barsUsed*246 #sets next note to the next bar
                beatsNext = beatType-beatsLeft
                beatsUsed=0

                if beatsNext<0.6 and beatsNext>0.4: #quaver
                    for j, note in enumerate(chord):
                        if note[1]=='#': #checks for sharp and add it
                            addSharp(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                        if note=='C4'or note=='C#4':
                            addCLine(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                        if j==len(chord)-1:
                            addQuaver(bg, nextNote, notePlaces[note]+(stavesUsed*156)) # adds a quaver for the top note
                        else:
                            addCrotchet(bg, nextNote, notePlaces[note]+(stavesUsed*156)) #add a crotchet for chords for formatting
                    nextNote = nextNote + int(0.5*nextNotePlace)
                    beatsUsed += 0.5
            else:
                for j, note in enumerate(chord):
                    if note[1]=='#':
                        addSharp(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                    if note=='C4'or note=='C#4':
                        addCLine(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                    addCrotchet(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                nextNote = int(nextNote) + int(nextNotePlace)
                beatsUsed += 1

        elif beatType<2.5 and beatType>1.5: #minim
            #checking for next stave line
            if barsUsed==4:
                barsUsed=0
                stavesUsed+=1
                nextNote=220

            #Checking for next bar
            if beatsUsed+beatType >= beatsPerBar:
                beatsLeft = beatsPerBar-beatsUsed
                #prints whatevers left in the current bar
                if beatsLeft==0.5:
                    for j, note in enumerate(chord):
                        if note[1]=='#': #checks for sharp and add it
                            addSharp(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                        if note=='C4'or note=='C#4':
                            addCLine(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                        if j==len(chord)-1:
                            addQuaver(bg, nextNote, notePlaces[note]+(stavesUsed*156)) # adds a quaver for the top note
                        else:
                            addCrotchet(bg, nextNote, notePlaces[note]+(stavesUsed*156)) #add a crotchet for chords for formatting
                    addSlur(bg, nextNote, notePlaces[note]+(stavesUsed*156), 220 + (barsUsed+1)*246-nextNote)
                    nextNote = nextNote + int(0.5*nextNotePlace)
                    beatsUsed += 0.5

                elif beatsLeft==1:
                    for j, note in enumerate(chord):
                        if note[1]=='#':
                            addSharp(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                        if note=='C4'or note=='C#4':
                            addCLine(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                        addCrotchet(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                    addSlur(bg, nextNote, notePlaces[note]+(stavesUsed*156), (220 + (barsUsed+1)*246)-nextNote)
                    nextNote = nextNote + int(nextNotePlace)
                    beatsUsed += 1

                elif beatsLeft==2:
                    for j, note in enumerate(chord): #adding minim
                        if note[1]=='#':
                            addSharp(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                        if note=='C4'or note=='C#4':
                            addCLine(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                        addMinim(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                    nextNote = int(nextNote) + int(2*nextNotePlace)
                    beatsUsed += 2

                barsUsed += 1
                nextNote = 220 + barsUsed*246
                beatsNext = beatType-beatsLeft
                beatsUsed=0
                
                #print the rest in the final bar
                if beatsNext<0.7 and beatsNext>0.3: #quaver
                    for j, note in enumerate(chord):
                        if note[1]=='#': #checks for sharp and add it
                            addSharp(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                        if note=='C4'or note=='C#4':
                            addCLine(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                        if j==len(chord)-1:
                            addQuaver(bg, nextNote, notePlaces[note]+(stavesUsed*156)) # adds a quaver for the top note
                        else:
                            addCrotchet(bg, nextNote, notePlaces[note]+(stavesUsed*156)) #add a crotchet for chords for formatting
                    nextNote = nextNote + int(0.5*nextNotePlace)
                    beatsUsed +=0.5

                elif beatsNext<1.3 and beatsNext>0.7:
                    for j, note in enumerate(chord):
                        if note[1]=='#':
                            addSharp(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                        if note=='C4'or note=='C#4':
                            addCLine(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                        addCrotchet(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                    nextNote = nextNote + int(0.5*nextNotePlace)
                    beatsUsed+=1
            else:
                for j, note in enumerate(chord): #adding minim
                    if note[1]=='#':
                        addSharp(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                    if note=='C4'or note=='C#4':
                        addCLine(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                    addMinim(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                nextNote = int(nextNote) + int(2*nextNotePlace)
                beatsUsed += 2

        elif beatType<5 and beatType>3: #semibreve
        #checking for next stave line
            if barsUsed==4:
                barsUsed=0
                stavesUsed+=1
                nextNote=220

            #Checking for next bar
            if beatsUsed+beatType >= beatsPerBar:
                beatsLeft = beatsPerBar-beatsUsed
                #prints whatevers left in the current bar
                if beatsLeft==0.5:
                    for j, note in enumerate(chord):
                        if note[1]=='#': #checks for sharp and add it
                            addSharp(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                        if note=='C4'or note=='C#4':
                            addCLine(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                        if j==len(chord)-1:
                            addQuaver(bg, nextNote, notePlaces[note]+(stavesUsed*156)) # adds a quaver for the top note
                        else:
                            addCrotchet(bg, nextNote, notePlaces[note]+(stavesUsed*156)) #add a crotchet for chords for formatting
                    addSlur(bg, nextNote, notePlaces[note]+(stavesUsed*156), 220 + (barsUsed+1)*246-nextNote)
                    nextNote = nextNote + int(0.5*nextNotePlace)
                    beatsUsed += 0.5

                elif beatsLeft==1:
                    for j, note in enumerate(chord):
                        if note[1]=='#':
                            addSharp(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                        if note=='C4'or note=='C#4':
                            addCLine(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                        addCrotchet(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                    addSlur(bg, nextNote, notePlaces[note]+(stavesUsed*156), (220 + (barsUsed+1)*246)-nextNote)
                    nextNote = nextNote + int(nextNotePlace)
                    beatsUsed += 1

                elif beatsLeft==2:
                    for j, note in enumerate(chord):
                        if note[1]=='#':
                            addSharp(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                        if note=='C4'or note=='C#4':
                            addCLine(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                        addMinim(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                    addSlur(bg, nextNote, notePlaces[note]+(stavesUsed*156), (220 + (barsUsed+1)*246)-nextNote)
                    nextNote = nextNote + int(2*nextNotePlace)
                    beatsUsed += 2

                elif beatsLeft==4:
                    for j, note in enumerate(chord): #adding semibreve
                        if note[1]=='#':
                            addSharp(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                        if note=='C4'or note=='C#4':
                            addCLine(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                        addSemibreve(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                    nextNote = int(nextNote) + int(4*nextNotePlace)
                    beatsUsed += 4

                barsUsed += 1
                nextNote = 220 + barsUsed*246
                beatsNext = beatType-beatsLeft
                beatsUsed=0

                #print the rest in the final bar
                if beatsNext<0.7 and beatsNext>0.3: #quaver
                    for j, note in enumerate(chord):
                        if note[1]=='#': #checks for sharp and add it
                            addSharp(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                        if note=='C4'or note=='C#4':
                            addCLine(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                        if j==len(chord)-1:
                            addQuaver(bg, nextNote, notePlaces[note]+(stavesUsed*156)) # adds a quaver for the top note
                        else:
                            addCrotchet(bg, nextNote, notePlaces[note]+(stavesUsed*156)) #add a crotchet for chords for formatting
                    nextNote = nextNote + int(0.5*nextNotePlace)
                    beatsUsed +=0.5

                elif beatsNext<1.3 and beatsNext>0.7:
                    for j, note in enumerate(chord):
                        if note[1]=='#':
                            addSharp(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                        if note=='C4'or note=='C#4':
                            addCLine(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                        addCrotchet(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                    nextNote = nextNote + int(nextNotePlace)
                    beatsUsed+=1

                elif beatsNext<2.5 and beatsNext>1.5:
                    for j, note in enumerate(chord):
                        if note[1]=='#':
                            addSharp(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                        if note=='C4'or note=='C#4':
                            addCLine(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                        addMinim(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                    nextNote = nextNote + int(2*nextNotePlace)
                    beatsUsed+=2

            else:
                for j, note in enumerate(chord): #adding semibreve
                    if note[1]=='#':
                        addSharp(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                    if note=='C4'or note=='C#4':
                        addCLine(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                    addSemibreve(bg, nextNote, notePlaces[note]+(stavesUsed*156))
                nextNote = int(nextNote) + int(4*nextNotePlace)
                beatsUsed += 4

    if not(SheetDirectory is None):
        bg.save(SheetDirectory)

if __name__=='__main__':
    notes = []
    beats = []
    title = ''
    timeSignature = ''
    bpm = ''
    SheetDirectory = None
    author = ''
    mainSheetMusic(notes, beats, title, timeSignature, bpm, SheetDirectory, author)
    bg.show()



#bar width is 246 starting from 200
#bar x-coor

# #end of staves
# line.line([(1184, 175), (1184, 228)], fill=None, width=2)#end of stave 1
# line.line([(1184, 331), (1184, 381)], fill=None, width=2)#end of stave 2
# line.line([(1184, 487), (1184, 537)], fill=None, width=2)#end of stave 3
# line.line([(1184, 643), (1184, 693)], fill=None, width=2)#end of stave 4
# line.line([(1184, 799), (1184, 849)], fill=None, width=2)#end of stave 5
# line.line([(1184, 955), (1184, 1005)], fill=None, width=2)#end of stave 6
# line.line([(1184, 1110), (1184, 1160)], fill=None, width=2)#end of stave 7
# line.line([(1184, 1266), (1184, 1316)], fill=None, width=2)#end of stave 8
# line.line([(1184, 1421), (1184, 1471)], fill=None, width=2)#end of stave 9

# #bar 0 of staves
# line.line([(200, 175), (200, 228)], fill=None, width=2)#end of stave 1
# line.line([(200, 331), (200, 381)], fill=None, width=2)#end of stave 2
# line.line([(200, 487), (200, 537)], fill=None, width=2)#end of stave 3
# line.line([(200, 643), (200, 693)], fill=None, width=2)#end of stave 4
# line.line([(200, 799), (200, 849)], fill=None, width=2)#end of stave 5
# line.line([(200, 955), (200, 1005)], fill=None, width=2)#end of stave 6
# line.line([(200, 1110), (200, 1160)], fill=None, width=2)#end of stave 7
# line.line([(200, 1266), (200, 1316)], fill=None, width=2)#end of stave 8
# line.line([(200, 1421), (200, 1471)], fill=None, width=2)#end of stave 9

# #bar 1 stave lines
# line.line([(446, 175), (446, 228)], fill=None, width=2)#end of stave 1
# line.line([(446, 331), (446, 381)], fill=None, width=2)#end of stave 2
# line.line([(446, 487), (446, 537)], fill=None, width=2)#end of stave 3
# line.line([(446, 643), (446, 693)], fill=None, width=2)#end of stave 4
# line.line([(446, 799), (446, 849)], fill=None, width=2)#end of stave 5
# line.line([(446, 955), (446, 1005)], fill=None, width=2)#end of stave 6
# line.line([(446, 1110), (446, 1160)], fill=None, width=2)#end of stave 7
# line.line([(446, 1266), (446, 1316)], fill=None, width=2)#end of stave 8
# line.line([(446, 1421), (446, 1471)], fill=None, width=2)#end of stave 9

# #bar 2 stave lines
# line.line([(692, 175), (692, 228)], fill=None, width=2)
# line.line([(692, 331), (692, 381)], fill=None, width=2)
# line.line([(692, 487), (692, 537)], fill=None, width=2)
# line.line([(692, 643), (692, 693)], fill=None, width=2)
# line.line([(692, 799), (692, 849)], fill=None, width=2)
# line.line([(692, 955), (692, 1005)], fill=None, width=2)
# line.line([(692, 1110), (692, 1160)], fill=None, width=2)
# line.line([(692, 1266), (692, 1316)], fill=None, width=2)
# line.line([(692, 1421), (692, 1471)], fill=None, width=2)

# #bar 3 stave lines
# line.line([(938, 175), (938, 228)], fill=None, width=2)
# line.line([(938, 331), (938, 381)], fill=None, width=2)
# line.line([(938, 487), (938, 537)], fill=None, width=2)
# line.line([(938, 643), (938, 693)], fill=None, width=2)
# line.line([(938, 799), (938, 849)], fill=None, width=2)
# line.line([(938, 955), (938, 1005)], fill=None, width=2)
# line.line([(938, 1110), (938, 1160)], fill=None, width=2)
# line.line([(938, 1266), (938, 1316)], fill=None, width=2)
# line.line([(938, 1421), (938, 1471)], fill=None, width=2)