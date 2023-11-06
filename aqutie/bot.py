#!/bin/env python

import discord
#from dotenv import load_dotenv

from collections import defaultdict
from aq import qabbalize, plex, cumulate
from random import choice
from datetime import datetime
from math import ceil

import os

def file_to_string(filename):
    """reads contents of a file in as a string"""
    with open(filename) as infile:
        return infile.read().strip()

#text loaded in from configs
TOKEN = file_to_string("token.txt")
NOTICE_TXT = file_to_string("notice.txt")
HELP_TXT = file_to_string("help.txt")

#####other arbitrary configuration#####
#discord's character limit, adjusted for how we wrap everything in ```  ```
CHARACTER_LIMIT=2000 - 6
#local library file that we read from and write to
LIBRARYFILE = "words.txt"
# urbanomic's read-only dictionary
NUMMIFICATOR = "nummificator.txt"

#####command names#####
AQPLEXNOSAVE_CMD = '?aqplex '
HELP_CMD = '!help'
HI_CMD = '!hi'
TIME_CMD = '!time'
STATS_CMD = '!stats'
RANDOM_CMD = '!random'
VALUES_CMD = '!values'
PLEX_CMD = '!plex '
AQPLEX_CMD = '!aqplex '
DICTIONARY = defaultdict(set)

# initialize the client
client = discord.Client()

def odd(n):
    """determines if a number is odd or not."""
    return n % 2 == 1

def divide_list(lst, divisions):
    """divides a list 'lst' into a given number of equally sized segments"""
    n = len(lst) // divisions
    for i in range(0, len(lst), n):
        # check if this is the last block or not
        if odd(n) and i + n + 1 == len(lst):
            yield lst[i: i + n + 1]
            return
        else:
            yield lst[i: i+n]

# number of seconds from epoch to y2k
YETTUK = 946684800
def deadline_time():
    """returns a formatted string representing the current deadline time since Yettuk's arrival"""
    now = int(datetime.now().timestamp()) - YETTUK
    second = (now % 100)              # deadline seconds
    minute = (now % 10000) // 100     # deadline minutes
    hour =   (now % 1000000) // 10000 # deadline hours
    #if minute == 0:
    #    return f"{hour} o'clock"
    #else:
    #    return "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
    return "{:02d}:{:02d}:{:02d}".format(hour, minute, second)



def qabbalize_and_store(text):
    text = text.strip().upper()
    aq_value = qabbalize(text)
    if text not in DICTIONARY[aq_value]:
        print(f"adding {text} with aq value {aq_value} to library")
        DICTIONARY[aq_value].add(text)
        write_to_store(aq_value, text)
    return aq_value

def reverse_lookup(number):
    return DICTIONARY[number]

def write_to_store(number, text):
    with open(LIBRARYFILE, "a+") as store:
        store.write(f"{number}: {text}\n")

def random_aq_value():
    """returns one of the populated AQ values from the dictionary"""
    aq = choice(list(DICTIONARY.keys()))
    if not DICTIONARY[aq]: # check for empty set
        return random_aq_value() # found empty set, so try again
    else:
        return aq # return the value we found
    

def load_words(filename):
    if not os.path.exists(filename):
        with open(filename, 'w'):
            pass

    with open(filename) as infile:
        lines = infile.read().strip().splitlines()
        total = len(lines)
        for entry in map(lambda line: line.split(': ', 1), lines):
            key = int(entry[0])
            value = entry[1].strip().upper()
            DICTIONARY[key].add(value)
    print("loaded", total, "entries into AQ dictionary")

def library_statistics(filename):
    with open(filename) as infile:
        lines = infile.read().strip().splitlines()
        return len(lines)

# TODO: make this split up results based on number of characters
def format_rev_lookup(results):
    if len(results) == 0:
        return ["<no entries yet>"]
    else:
        combined_length =  len("AQ-=\n") + 5 + sum(map(len, results)) + len(results)
        divisions = ceil(combined_length / CHARACTER_LIMIT)
        divided = divide_list(sorted(results), divisions)
        return ["\n".join(l) for l in divided]

def revaq(num):
    print(f"attempting to perform reverse AQ lookup with {num}")
    lookup = format_rev_lookup(reverse_lookup(num))
    first = f"AQ-{num}=\n{lookup[0]}"
    return [first] + lookup[1:]

def aq_cmd(text, rev=False, store=True):
    normalized = text.strip().upper()
    if store:
        aq = qabbalize_and_store(normalized)
    else:
        aq = qabbalize(normalized)
    print(f"aqabbalized text {normalized} ={aq}")

    if rev:
        results = reverse_lookup(aq)
        fmt = format_rev_lookup(results)
        if store:
            first = f"AQ-{aq}=\n{fmt[0]}"
            #return f"{aq}=\n{fmt}"
        else:
            first = f"AQ-{aq}=\n{normalized}\n{fmt[0]}"
            #return f"{aq}=\n{normalized}\n{fmt}"
        return [first] + fmt[1:]
    else:
        return [f"{normalized} ={aq}"]

def make_chat_command(function, name, takes_argument=False, expected_type=str):
    """wraps a function to make it a chat command"""
    if takes_argument and expected_type is int:
        #print(f"making function {name} which takes a numeric argument")
        def wrapped(arg=None):
            """Checks to see if an argument is provided, attempts to cast it into an integer"""
            if arg is None:
                return [f"Please provide a numeric arg for command {name}"]
            try:
                num = int(arg)
                return function(num)
            except ValueError:
                return [f"Invalid number: {arg}"]

        #return the wrapped function
        return wrapped

    elif takes_argument and expected_type is str:
        def wrapped(arg=None):
            if arg is None:
                return [f"Please provide a numeric argument for command {name}"]
            else:
                return function(arg)

        # return the wrapped function
        return wrapped

    elif not takes_argument:
        return lambda: function()

    else:
        print("No behavior currently defined for this combination of arguments")
        

# it occurs to me that I could probably enforce arguments here,
# by wrapping the functions in some kind of lambda which does type/argument checking
PREFIX_BANG = "!"
PREFIX_QUERY = "?"
BANG= {}
BANG["time"] = make_chat_command(deadline_time, "time")
BANG["revaq"] = make_chat_command(revaq, "revaq", True, int)
BANG["aq"] = make_chat_command(aq_cmd, "aq", True)
BANG["aqqa"] = make_chat_command(lambda s: aq_cmd(s, rev=True), "aqqa", True)

QUERY = {}
QUERY["revaq"] = make_chat_command(revaq, "revaq", True, int)
QUERY["aq"] = make_chat_command(lambda s: aq_cmd(s, store=False), "aq", True)
QUERY["aqqa"] = make_chat_command(lambda s: aq_cmd(s, rev=True, store=False), "aqqa", True)

def dispatch(message):
    # preliminary formatting of command and arguments
    splitted = message.split(None, 1)
    cmdstr = splitted[0]
    msg = splitted[1] if len(splitted) > 1 else ""

    if cmdstr.rfind(PREFIX_BANG) == 0:
        print(f"recognized prefix {PREFIX_BANG} at the start of the message")
        handlerdict = BANG
        cmd_stripped = cmdstr[len(PREFIX_BANG):]
        prefix = PREFIX_BANG

    elif cmdstr.rfind(PREFIX_QUERY) == 0:
        print(f"recognized prefix {PREFIX_QUERY} at the start of the message")
        handlerdict = QUERY
        cmd_stripped = cmdstr[len(PREFIX_QUERY):]
        prefix = PREFIX_QUERY

    if cmd_stripped in handlerdict:
        print(f"matched command {prefix}{cmd_stripped}, with argument: {msg}")
        cmd = handlerdict[cmd_stripped]

        try:
            if msg:
                return cmd(msg)
            else:
                return cmd()
        except:
            print(f"Encountered an exception running command {cmdstr}")
    else:
        print(f"unrecognized command {prefix}{cmdstr}")

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(msg):
    def check_cmd(content, cmd):
        return content.lower().startswith(cmd) and len(content) > len(cmd)
    def check_short(content, cmd):
        return content.lower().startswith(cmd)

    content = msg.content
#    print(f"handling message from {msg.author}")
    # print(content, msg.author)
    if msg.author == client.user:
        return

    if not (content.rfind(PREFIX_QUERY) == 0 or content.rfind(PREFIX_BANG) == 0):
        return

    if check_short(content, STATS_CMD):
        message = f"""```statistics:
phrases: {library_statistics(LIBRARYFILE)}
```"""
        await msg.channel.send(message)

    elif check_short(content, RANDOM_CMD):
        value = random_aq_value()
        results = reverse_lookup(value)
        message = f"```{value}=\n{format_rev_lookup(results)}```"
        await msg.channel.send(message)

    elif content.lower().startswith(HI_CMD):
        await msg.channel.send(f"hi, {msg.author.name}!")

    elif check_cmd(content, PLEX_CMD):
        text = content[len(PLEX_CMD):]
        print(f"attempting to plex {text}")
        try:
            value = int(text)
            message = f"```{value} = {plex(value)}```"
            await msg.channel.send(message)
        except ValueError:
            await msg.channel.send(f"Invalid number: {text}")

    elif check_cmd(content, AQPLEX_CMD):
        text = content[len(AQPLEX_CMD):]
        aq = qabbalize_and_store(text)
        plex_value = plex(aq)
        message = f"```{text} = {aq} = {plex_value}```"
        await msg.channel.send(message)

    elif check_cmd(content, AQPLEXNOSAVE_CMD):
        text = content[len(AQPLEXNOSAVE_CMD):]
        aq = qabbalize(text.strip().upper())
        plex_value = plex(aq)
        message = f"```{text} = {aq} = {plex_value}```"
        await msg.channel.send(message)

    elif check_short(content, VALUES_CMD):
        await msg.channel.send("""```##########AQ VALUES##########
0=0, 1=1, 2=2, 3=3, 4=4,
5=5, 6=6, 7=7, 8=8, 9=9,
A=10, B=11, C=12, D=13, E=14,
F=15, G=16, H=17, I=18, J=19,
K=20, L=21, M=22, N=23, O=24,
P=25, Q=26, R=27, S=28, T=29,
U=30, V=31, W=32, X=33, Y=34,
Z=35```""")
    elif content.lower().startswith(HELP_CMD):
        message = f"""```{HELP_TXT}
```
```
{NOTICE_TXT}
```
"""
        await msg.channel.send(message)

#    elif content.lower().startswith("!debug") and str(msg.author) == MASTER:
#        print("debugging!")
#
#    elif content.lower().startswith("!bye") and str(msg.author) == MASTER:
#        await client.close()

    else:
        dispatched = dispatch(content)
        if dispatched:
            response = f"```{dispatched}```"
            for block in dispatched:
                response = f"```{block}```"
                await msg.channel.send(response)
        else:
            print("no response from the dispatcher, failing silently")

@client.event
async def on_disconnect():
    print("AQutie has disconnected")

@client.event
async def on_connect():
    print("AQutie has connected")


load_words(LIBRARYFILE)

#UNCOMMENT THIS IF YOU WANT TO INCLUDE THE NUMMIFICATOR'S WORDS
#load_words(NUMMIFICATOR)

def main():
    client.run(TOKEN)

if __name__ == "__main__":
    main()

