import time
import os
import random

script_folder = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_folder)


def markov_chain2(text):
    '''Takes a string file and generates a Markov-chain of length 2
    
    text: string
    
    return: dict of keys of strings and values of list of strings'''
    #print("\nCreating Markov Chain 2")
    words = text.split()
    markov_dict = dict()
    for index in range(len(words) - 2):  
        #if index % 1000 == 0:
        #    print(".", end="")
        word = words[index] + words[index + 1]
        next_word = words[index + 2]
        if word in markov_dict:
            markov_dict[word].append(next_word)
        else:
            markov_dict[word] = [next_word]
    return markov_dict

def markov_chain1(text):
    '''Takes a string file and generates a Markov-chain of length 1
    
    text: string
    
    return: dict of keys of strings and values of list of strings'''
    #print("\nCreating Markov Chain 1")
    words = text.split()
    markov_dict = dict()
    for index in range(len(words) - 1):  
        #if index % 1000 == 0:
        #    print(".", end="")
        word = words[index] 
        next_word = words[index + 1]
        if word in markov_dict:
            markov_dict[word].append(next_word)
        else:
            markov_dict[word] = [next_word]
    return markov_dict

def preprocess(text):
    '''Preprocesses a text from a Project Gutenberg-file to make
    it usable for function markov_chain
    
    text: string of a filename
    return: string'''
    completestring = ""
    begun = False
    loader = 0
    #print("Loading", text)
    print("Generating a random text of Project Gutenberg book called")
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            loader += 1
            #if loader% 1000 == 0:
            #    print(".", end="")
            if "Title:" in line:
                print(line[7:])
            if "Author:" in line:
                print("by", line[8:])
            if begun == True:
                completestring += line
            if "***" in line:
                if begun == True:
                    begun = False
                else:
                    begun = True
    completestring = completestring.strip()
    return completestring

def generate_text(md1, md2, sw, num = 100):
    '''Generate a text based on a markov-chain and possible start words
    
    md1: dictionary of strings as keys with list of sttings as values
    md2: dictionary of strings as keys with list of sttings as values

    sw: list of list of strings

    num: integer

    return: string
    '''
    #print("\nGenerating text:")
    chose_startwords = random.randint(0, len(sw) - 1)
    text = sw[chose_startwords]
    for i in range(num):  
        time.sleep(0.02) #dramatic effect - remove if annoying
        act_word = text[i] + text[i+1]
        if i % 15 == 0: # break lines for every 15th word
            print("\n", end = "") 
        if act_word not in md2: # if words not in markov-chain2 then lookup markov chain1
            print(text[i], end = " ", flush = True)
            candidates = md1[act_word]
            chosen = random.randint(0, len(candidates)-1)
            text.append(candidates[chosen])
        else:
            print(text[i], end = " ", flush = True)
            candidates = md2[act_word]
            chosen = random.randint(0, len(candidates)-1)
            text.append(candidates[chosen])

def starter_words(text):
    '''Takes a text, and finds a possible pair of starting words
    
    text: string
    return: list of lists of strings
    '''
    #print("\nGenerating starter words.")
    words = text.split()
    starter_words = []
    for i in range(len(words) - 1):
        if words[i] != words[i].lower():
            starter_words.append([words[i], words[i+1]])
    return starter_words

def markovize_this(filename, num = 100):
    text = preprocess(filename)
    start_words = starter_words(text)
    words1 = markov_chain1(text)
    words2 = markov_chain2(text)
    generated = generate_text(words1, words2, start_words, num)
    return generated

def getfile():
    a = input("Filename? ")
    if ".txt" in a:
        return a
    else:
        a = a + ".txt"
        return a

def getnumber():
    try:
        b = int(input("How long? Integer please: "))
    except ValueError:
        b = 100
    return b

filename = getfile()
number = getnumber()
generated_text = markovize_this(filename, int(number))

