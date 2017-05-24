#scan through document looking for <x _____>
#x is a number indicating what rhyme it is.
#the rest is the contents of the rhyme.
#the end tag marks the end of the rhyme colouration.

#scan through document, looking for all <x ____>
#determine the number of different colours needed
#replace each <x ____> by the html colouration tag for that x

import os

TAG_START = '<'
TAG_END = '>'
COLOURS = {"1":"red","2":"green","3":"blue","4":"orange","5":"chocolate","6":"cyan","7":"magenta","8":"brown","9":"crimson","10":"mediumslateblue","11":"darkslateblue","12":"fuchsia","13":"greenyellow","14":"orangered","15":"ochre","16":"plum","17":"seagreen","18":"springgreen"}

INPUT_FILENAME = "./tests/test1"
INPUT_FILENAME_EXT = ".txt"

HTML_HEADER = "<HTML>\n<head></head>\n<body>\n"
HTML_FOOTER = "\n</body></HTML>"


#Parameters:
#   _fileName: A relative path at which the file will attempt to be opened.
#
#Return value:
#   lyrics: A string containing the contents of the specified file.
#      Contains the empty string if there was an issue opening the file.
#
def loadLyrics(_fileName):
    lyrics = ""
    with open(_fileName, 'r') as f:
        lyrics = f.read()

    return lyrics

#Parameters:
#   _fileName: A relative path at which the file will attempt to be saved.
#   _lyrics: A list of strings
#
#Return value:
#   None
#
def saveLyrics(_fileName, _lyrics):
    with open(_fileName, 'w') as f:

        f.write(HTML_HEADER)
        for line in _lyrics:
            f.write(line)
        f.write(HTML_FOOTER)

#Parameters:
#   _rhymeID: String, representing what rhyme is occurring in _content
#   _content: String, representing the content to be coloured.
#
#Return value:
#   formattedContent: String, containing an HTML element formatted with the colouration required by this rhyme id
#
def singleColouration(_rhymeID, _content):
    try:
        formattedContent = "<span style='color:"+COLOURS[_rhymeID]+"'>"+_content+"</span>"
    except KeyError:
        print "Oops something went wrong when you tried to get the colour for rhyme ID: "+str(_rhymeID)
        exit()

    return formattedContent

#Parameters:
#   _inputText: A string to be scanned
#   _numColours: The total number of colours needed to colour the text
#
#Return value
#   outputText: An HTML colour-formatted version of _inputText
#
def scan(_inputText, _numColours):
    inColourMode = False #Used to avoid unnecessary parsing
    colourations = dict() #A dictionary which associates each rhyme id (as a string) with a list of each string causing an occurrence.

    currentRhymeID = "" #Used to store the current rhyme id tag, in case it is more than one digit.
    currentContent = "" #Used to store the current colouration content, in the likely event that it is more than one character.
    outputText = "" #Used to store the running formatted output of the function.

    #scan through input text one character at a time
    for c in _inputText:
        print c

        #check to see if we should enter colourMode before skipping the character
        if c == TAG_START:
            #start of a colouration tag
            inColourMode = True
            continue

        #If c is a newline, then we want to stuff an HTML linebreak in there as well
        if ord(c) == 10:
            outputText += "<br />\n"
            continue

        #If we aren't altering the colour or format of this input text, it can go straight to the output text.
        if not inColourMode:
            outputText += c
            continue

        #If c is a number, it is indicating what colour to use for this tag.
        if (ord(c) >= ord('0')) and (ord(c) <= ord('9')):
            currentRhymeID += str(c)
            continue

        #end of a colouration tag
        if c == TAG_END:

            #Make sure we don't smoosh any rhyme occurrences that we've already stored.
            if (int(currentRhymeID) in colourations):
                colourations[int(currentRhymeID)].append(currentContent)
            else:
                colourations[int(currentRhymeID)] = [currentContent]

            outputText += singleColouration(currentRhymeID,currentContent)

            #reset colouration tag variables
            inColourMode = False
            currentRhymeID = ""
            currentContent = ""
            continue

        #If we haven't found any special tokens, then we can just take this input character directly.
        if inColourMode:
            currentContent += c
            continue


    return outputText

testLyrics = loadLyrics(INPUT_FILENAME+INPUT_FILENAME_EXT)
formattedLyrics = scan(testLyrics,13)

saveLyrics(INPUT_FILENAME+"_formatted.html",formattedLyrics)
