import os
import sys
import json
import random
from utils import initial_messages


def yes_or_no():
    status = input("If you think you are correct, type \'y\'. Otherwise, type \'n\'")
    if status == 'y' or status == 'Y':
        return 1
    elif status == 'n' or status == 'N':
        return 0
    print("The input is neither y or n. Will assume to be \'n\'...")
    return 0



def prepare_word_pools(path):
    word_pools = None
    try:
        with open(path, 'r') as f:
            word_pools = json.load(f)
    except:
        word_pools = dict()
    return word_pools

def print_words():
    word_pools = prepare_word_pools("word_pools.json")
    for word, meaning in word_pools.items():
        print("------------------------------------------------")
        print(f"Word: {word}, Meaning: {meaning}")
    print("------------------------------------------------")
    _ = input("Press Enter to continue ...")

def practice(num_words_per_round, word2meaning=True):
    word_pools = prepare_word_pools("word_pools.json")
    num_words_per_round = min(num_words_per_round, len(word_pools))
    print(f"Number of words practicing in one round is {num_words_per_round}.")
    while True:
        sampled_words = random.sample(list(word_pools.items()), num_words_per_round)
        num_correct_answering = 0
        for word, meaning in sampled_words:
            if word2meaning:
                print("--------------------------------------------")
                _ = input(f"Word: {word}.\nPress Enter to get the meaning")
                print(f"The meaning is: {meaning}.")
                _ = input("Press Enter to continue ...")
                num_correct_answering += yes_or_no()
            else:
                raise NotImplementedError("Not implemenetd")
        print("--------------------------------------------")
        print(f"Correct rate for this round: {num_correct_answering} / {num_words_per_round} = {num_correct_answering / num_words_per_round}")


        status = input("Continue to practice? [y/n]")
        if status == "n" or status == "N":
            break
        elif status == "y" or status == "Y":
            continue
        else:
            print(f"No such status {status}, will assume to stop ...")
            break

def add_words(word, meaning):
    word_pools = prepare_word_pools("word_pools.json")
    word_pools[word] = meaning
    with open("word_pools.json", 'w') as f:
        json.dump(word_pools, f)

def clear_word_pools():
    with open("word_pools.json", 'w') as f:
        f.write("")
    _ = input("Successfully Clear all the words. Press Enter to continue ...")

def remove(target_word):
    word_pools = prepare_word_pools("word_pools.json")
    if target_word in word_pools.keys():
        _ =  word_pools.pop(target_word)
        with open("word_pools.json", 'w') as f:
            json.dump(word_pools, f)
        print(f"Successfully remove {target_word} ^_^")
    else:
        print(f"No such word, {target_word} , in the word pools _^_ ...")
    _ = input("Press Enter to continue ...")

_EXIT = "q"
_ADD_WORDS = "a"
_PRACTICE = "p"
_PRINT_WORDS = "print"
_REMOVE_WORDS = "r"
_CLEAR_WORD_POOLS = "c"

def main():
    print("Welcome to tofel practice program developed by Mars.")
    while 1:
        print(initial_messages)
        mode = input("Please type the mode:")
        if mode == _EXIT:
            print("Start to exit ... Thank you for your usage ^_^")
            break
        elif mode == _ADD_WORDS:
            word_meaning_pair = input("Type your input word. The format should be [word;meaning]. For example, apple;蘋果:")
            word_meaning_pair = word_meaning_pair.split(";")
            if len(word_meaning_pair) != 2:
                print("Your input is in the wrong format. The program would terminate ...", file=sys.stderr)
                sys.exit(1)
            word, meaning = word_meaning_pair[0], word_meaning_pair[1]
            add_words(word, meaning)
            print(f"Successfully adding word: {word} and meaning {meaning} into word pools ^_^")
        elif mode == _PRACTICE:
            num_words_per_round = int(input("Type the number of words you want to practice per round. For example, 10:"))
            practice(num_words_per_round, word2meaning=True)
        elif mode == _PRINT_WORDS:
            print_words()
        elif mode == _CLEAR_WORD_POOLS:
            clear_word_pools()
        elif mode == _REMOVE_WORDS:
            target_word = input("Type the target removed word. For example, apple:")
            remove(target_word)
        else:
            print("No such mode {mode}... _^_")

if __name__ == "__main__":
    main()
