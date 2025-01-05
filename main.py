import os
import sys
import json
import random
from utils import initial_messages
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

console = Console()


def yes_or_no():
    console.print("[bold green]If you think you are correct, type 'y'. Otherwise, type 'n'[/bold green]")
    status = input()
    if status == 'y' or status == 'Y':
        return 1
    elif status == 'n' or status == 'N':
        return 0
    console.print("[bold red]The input is neither y or n.[bold red] Will assume to be \'n\'...")
    return 0



def prepare_words_pool(path):
    words_pool = None
    try:
        with open(path, 'r') as f:
            words_pool = json.load(f)
    except:
        words_pool = dict()
    return words_pool

def print_words():
    words_pool = prepare_words_pool("words_pool.json")
    table = Table()

    table.add_column("Word", justify="right", style="white", no_wrap=True)
    table.add_column("Meaning", style="white")


    for word, meaning in words_pool.items():
        table.add_row(word, meaning)
    console.print(table)
    _ = input("Press Enter to continue ...")

def practice(num_words_per_round, word2meaning=True):
    words_pool = prepare_words_pool("words_pool.json")
    num_words_per_round = min(num_words_per_round, len(words_pool))
    print(f"Number of words practicing in one round is {num_words_per_round}.")
    while True:
        sampled_words = random.sample(list(words_pool.items()), num_words_per_round)
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
    words_pool = prepare_words_pool("words_pool.json")
    words_pool[word] = meaning
    with open("words_pool.json", 'w') as f:
        json.dump(words_pool, f)

def clear_words_pool():
    with open("words_pool.json", 'w') as f:
        f.write("")
    _ = input("Successfully Clear all the words. Press Enter to continue ...")

def remove(target_word):
    words_pool = prepare_words_pool("words_pool.json")
    if target_word in words_pool.keys():
        _ =  words_pool.pop(target_word)
        with open("words_pool.json", 'w') as f:
            json.dump(words_pool, f)
        print(f"Successfully remove {target_word} ^_^")
    else:
        print(f"No such word, {target_word} , in the word pools _^_ ...")
    _ = input("Press Enter to continue ...")

_EXIT = "q"
_ADD_WORDS = "a"
_PRACTICE = "p"
_PRINT_WORDS = "print"
_REMOVE_WORDS = "r"
_CLEAR_WORDS_POOL = "c"

def main():
    if not os.path.isfile("./words_pool.json"):
        os.system("touch words_pool.json")
    console.print("[bold dark_slate_gray3]Welcome to tofel practice program developed by Mars.[bold dark_slate_gray3]")
    while 1:
        #console.rule("")
        initial_messages()
        #console.rule("")
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
        elif mode == _CLEAR_WORDS_POOL:
            clear_words_pool()
        elif mode == _REMOVE_WORDS:
            target_word = input("Type the target removed word. For example, apple:")
            remove(target_word)
        else:
            print("No such mode {mode}... _^_")

if __name__ == "__main__":
    main()
