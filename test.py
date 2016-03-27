#!/usr/bin/env python

import nltk

# Captive Chatbot - try to make Jack Bauer talk

reflections = {
    "am"     : "are",
    "was"    : "were",
    "I"      : "you",
    "I'm"    : "you're",
    "I'd"    : "you'd",
    "I've"   : "you've",
    "I'll"   : "you'll",
    "my"     : "your",
    "are"    : "am",
    "you're" : "I'm",
    "you've" : "I've",
    "you'll" : "I'll",
    "your"   : "my",
    "yours"  : "mine",
    "you"    : "me",
    "you"      : "me",
    "your"     : "my",
    "yours"    : "mine",
    "me"     : "you"
}

# Note: %1/2/etc are used without spaces prior as the chat bot seems
# to add a superfluous space when matching.

pairs = (
    # suggestions
    (r".*([Ww]hat if we|[Ww]e will|[Ww]e'll|[Ww]e're going to|[Dd]o you want us to|[Hh]ow about we)(.*)(bollito misto|Britney Spears)(.*)[?]*",
    ( "oh no, don't %2%3%4, anything but that!",
      "%2%3%4? How could you be so evil. I'll do anything you ask",
      "you bastards, don't %2%3%4")),
    (r".*([Dd]o you want|[Hh]ow about)(.*)(bollito misto|Britney Spears)(.*)[?]*",
    ( "oh no, not %2%3%4, anything but that!",
      "%2%3%4? How could you be so evil. I'll do anything you ask",
      "you bastards, not %2%3%4!")),
    # anything else
    (r'(.*)',
        (
            "I won't tell you anything",
            "Try an make me talk",
            "Over my dead body",
            "You'll have to kill me first",
            "You'll never get anything out of me",
            "[Silence]",
            "[Spits]",
            "No comment"
        )
     )
)

captive_chatbot = nltk.chat.Chat(pairs, reflections)

def captive_chat():
    print "Jack Bauer is your prisoner\n---------"
    print 'Interrogate him to find out his plans.  Enter "quit" when done.'
    print '='*72
    print "Torture me, do what you will, but I won't tell you anything. "

    captive_chatbot.converse()

def demo():
    captive_chat()

if __name__ == "__main__":
    demo()


