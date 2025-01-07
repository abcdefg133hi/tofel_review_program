import os
import sys
import json
import random
from utils import initial_messages
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.live import Live
import datetime
import signal
import time

console = Console()
_should_speak = False

def yes_or_no():
    status = Prompt.ask("[bold green]If you think you are correct, type 'y'. Otherwise, type 'n'[/bold green]")
    if status == 'y' or status == 'Y':
        return 1
    elif status == 'n' or status == 'N':
        return 0
    console.print("[bold red]The input is neither y or n.[bold red] Will assume to be \'n\'...")
    return 0



def speak(problem):
    problem_chunk = problem.split(" ")
    current_problem = "[bold green]:clock1: Problem: "
    with Live(console=console, refresh_per_second=len(current_problem)) as live:
        for chunk in problem_chunk:
            current_problem += chunk + " "
            live.update(current_problem)
            time.sleep(0.2)
    seconds = 15
    with Live(console=console, refresh_per_second=15) as live:
        while seconds >= 0:
            table = Table()
            table.add_column("Time Left", justify="center", style="bold red", no_wrap=True)
            table.add_row(f"{seconds} seconds")
            live.update(table)
            time.sleep(1)
            seconds -= 1

    console.print("[bold green]Time's up! Please start your answer ...")
    seconds = 45
    with Live(console=console, refresh_per_second=45) as live:
        while seconds >= 0:
            table = Table()
            table.add_column("Time Left", justify="center", style="bold red", no_wrap=True)
            table.add_row(f"{seconds} seconds")
            live.update(table)
            time.sleep(1)
            seconds -= 1
    console.print("[bold green]Time's up! :tada:")


def speaking():
    with open("speaking/problems.json", 'r') as f:
        problem_corpus = json.load(f)
    while 1:
        os.system("clear")
        problem = Prompt.ask("Type the problem here. (\"None\" for using the problem from corpus)")
        probably_save = True
        if problem == "None" and len(problem_corpus) > 0:
            randno = random.randint(0,len(problem_corpus)-1)
            problem = problem_corpus[randno]
            probably_save = False
        elif problem == "None":
            console.log("Error! No problem in the corpus. Please type the problem ...")
            _ = input("Press Enter to continue ...")
            continue
        speak(problem)
        if probably_save:
            save_or_not = Prompt.ask("Do you want to save the problem into the corpus? (y/n)")
            if save_or_not == "Y" or save_or_not == "y":
                problem_corpus.append(problem)
                console.print("Successfully save the problem into the corpus. :tada:")
            else:
                console.print("Not saving the problem into the corpus.")
        status = Prompt.ask("Again or not. (y/n)")
        if status != "y" and status != "Y":
            with open("speaking/problems.json", 'w') as f:
                json.dump(problem_corpus, f)
            _ = input("Will back to the main page. Press Enter to continue ...")
            return


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
    os.system("clear")
    words_pool = prepare_words_pool("words_pool.json")
    if len(words_pool) == 0:
        console.print("There is no word in the words pool")
        _ = input("Press Enter to continue ...")
        return
    num_words_per_round = min(num_words_per_round, len(words_pool))
    print(f"Number of words practicing in one round is {num_words_per_round}.")
    while True:
        sampled_words = random.sample(list(words_pool.items()), num_words_per_round)
        num_correct_answering = 0
        table = Table()
        table.add_column("Word", justify="right", style="white", no_wrap=True)
        table.add_column("Meaning", style="white")
        table.add_column("Your Answer", style="white")
        table.add_column("Correct or not", style="white")
        for word, meaning in sampled_words:
            if word2meaning:
                os.system("clear")
                console.log(f"[bold red]Word: {word}.[/bold red]")
                answer = input("Type your answer here:")
                console.log(f"[bold blue]The true meaning is: {meaning}.[/bold blue]")
                _ = input("Press Enter to continue ...")
                if_correct = yes_or_no()
                num_correct_answering += if_correct
                table.add_row(word, meaning, answer, str(if_correct))
            else:
                raise NotImplementedError("Not implemenetd")
        console.print(table)
        console.log(f"Correct rate for this round: {num_correct_answering} / {num_words_per_round} = {num_correct_answering / num_words_per_round}")

        if_store = Prompt.ask("Store the practice record? (y/n)")
        if if_store == "y" or if_store == "Y":
            time_now = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            with open(f"practice_records/record_{time_now}.txt", 'w') as f:
                _file_console = Console(file=f)
                _file_console.print(table)
                _file_console.log(f"Correct rate for this round: {num_correct_answering} / {num_words_per_round} = {num_correct_answering / num_words_per_round}")
            with open("practice_records/record_hash.json", 'r') as fin:
                hash_table = json.load(fin)
            try:
                current_enum = hash_table["enum"][-1] + 1
            except:
                current_enum = 1
            hash_table["enum"].append(current_enum)
            hash_table[str(current_enum)] = f"record_{time_now}.txt"
            with open("practice_records/record_hash.json", 'w') as fout:
                json.dump(hash_table, fout)
        status = Prompt.ask("Continue to practice? (y/n)")
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
    _ = input(f"Successfully add the word, {word}. Press Enter to continue ...")

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
_CLEAR_RECORDS = "clear_record"
_PRINT_RECORD = "print_record"
_SPEAKING = "speaking"
_SPEAKING_ADD = "speaking_add"
_SPEAKING_CLEAR = "speaking_clear"
_SPEAKING_PRINT = "speaking_print"
_SPEAKING_REMOVE = "speaking_remove"

def main():
    os.system("clear")
    if not os.path.isfile("./words_pool.json"):
        os.system("touch words_pool.json")
    if not os.path.isdir("speaking"):
        os.makedirs("speaking", exist_ok=False)
    if not os.path.isfile("speaking/problems.json"):
        with open("speaking/problems.json", 'w') as f:
            json.dump([], f)
    console.print("[bold dark_slate_gray3]Welcome to tofel practice program developed by Mars.[bold dark_slate_gray3]")
    if not os.path.isdir("practice_records"):
        os.makedirs("practice_records", exist_ok=False)
        hash_table = dict(); hash_table["enum"] = []
        with open("practice_records/record_hash.json", 'w') as f:
            json.dump(hash_table, f)
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
        elif mode == _CLEAR_RECORDS:
            try:
                os.system("rm -rf practice_records")
            except:
                pass
            os.makedirs("practice_records", exist_ok=False)
            hash_table = dict(); hash_table["enum"] = []
            with open("practice_records/record_hash.json", 'w') as f:
                json.dump(hash_table, f)
            console.print("Successfully clear all the records...")
            _ = input("Press Enter to continue...")
        elif mode == _PRINT_RECORD:
            hash_table = None
            with open("practice_records/record_hash.json", 'r') as f:
                hash_table = json.load(f)
            table = Table(title="Here is the current record files table...")
            table.add_column("Index", justify="right", style="white", no_wrap=True)
            table.add_column("Record_Name", style="white")
            for key, values in hash_table.items():
                if key == "enum":
                    continue
                table.add_row(key, values)
            console.print(table)
            index = Prompt.ask("Please type the file index that you want to query")
            if index not in hash_table.keys():
                console.log("No such index... Will terminate and the print record program ...")
                _ = input("Press Enter to continue...")
                os.system("clear")
                continue
            os.system("clear")
            print(hash_table[index])
            os.system(f"cat practice_records/{hash_table[index]}")
            _ = input("Press Enter to continue...")
        elif mode == _SPEAKING:
            speaking()
        elif mode == _SPEAKING_ADD:
            problem = Prompt.ask("Type the problem here")
            with open("speaking/problems.json", 'r') as f:
                problem_corpus = json.load(f)
            problem_corpus.append(problem)
            with open("speaking/problems.json", 'w') as f:
                json.dump(problem_corpus, f)
            console.print(f"Successfully adding problem, {problem}, into the corpus.")
            _ = input("Press Enter to continue...")
        elif mode == _SPEAKING_CLEAR:
            with open("speaking/problems.json", 'w') as f:
                json.dump([], f)
            console.print("Successfully clearing all the problems in the corpus.")
            _ = input("Press Enter to continue...")
        elif mode == _SPEAKING_PRINT:
            with open("speaking/problems.json", 'r') as f:
                problem_corpus = json.load(f)
            table = Table()
            table.add_column("ID", justify="right", style="white", no_wrap=True)
            table.add_column("Problem", style="white")
            for idx, problem in enumerate(problem_corpus):
                table.add_row(str(idx+1), problem)
            console.print(table)
            _ = input("Press Enter to continue...")
        elif mode == _SPEAKING_REMOVE:
            with open("speaking/problems.json", 'r') as f:
                problem_corpus = json.load(f)
            table = Table()
            table.add_column("ID", justify="right", style="white", no_wrap=True)
            table.add_column("Problem", style="white")
            for idx, problem in enumerate(problem_corpus):
                table.add_row(str(idx+1), problem)
            console.print(table)
            _id = Prompt.ask("Please input the ID that you want to remove")
            try:
                if int(_id) == len(problem_corpus):
                    problem_corpus.pop()
                elif int(_id) <= 0:
                    console.log("Your input is not a valid ID. Will directly return back to main ...")
                else:
                    problem_corpus[int(_id) - 1] = problem_corpus[-1]
                    problem_corpus.pop()
            except:
                console.log("Your input is not a valid ID. Will directly return back to main ...")
            with open("speaking/problems.json", 'w') as f:
                json.dump(problem_corpus, f)
            console.print(f"Successfully removing the problem from the corpus.")
            _ = input("Press Enter to continue...")
        else:
            print(f"No such mode {mode}... _^_")
            _ = input("Press Enter to continue...")
        os.system("clear")

if __name__ == "__main__":
    main()
