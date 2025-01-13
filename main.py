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
import atexit
import pyttsx3
import math


RED = """[bold red]{}[/bold red]"""


def release_lock():
    os.system("rm -f .tofel.lock")


atexit.register(release_lock)
console = Console()
_should_speak = False
engine = pyttsx3.init()

def yes_or_no():
    status = Prompt.ask("[bold green]If you think you are correct, type 'y'. Otherwise, type 'n'[/bold green]")
    if status == 'y' or status == 'Y':
        return 1
    elif status == 'n' or status == 'N':
        return 0
    console.print("[bold red]The input is neither y or n.[bold red] Will assume to be \'n\'...")
    return 0



def speak(problem):
    console.print(f"[bold green]:clock1: Problem: {problem}")
    engine.setProperty('rate', 150)
    voices = engine.getProperty('voices')
    voice_from = 0
    engine.setProperty('voice', voices[voice_from].id)
    engine.say(problem)
    engine.runAndWait()
    """
    problem_chunk = problem.split(" ")
    current_problem = "[bold green]:clock1: Problem: "
    with Live(console=console, refresh_per_second=len(current_problem)) as live:
        for chunk in problem_chunk:
            current_problem += chunk + " "
            live.update(current_problem)
            time.sleep(0.2)
    """
    seconds = 15
    with Live(console=console, refresh_per_second=15) as live:
        while seconds >= 0:
            table = Table()
            table.add_column("Time Left", justify="center", style="bold red", no_wrap=True)
            table.add_row(f"{seconds} seconds")
            live.update(table)
            time.sleep(1)
            seconds -= 1

    engine.say("Time's up! Please start your answer.")
    engine.runAndWait()
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

def practice(num_words_per_round, sound=False):
    os.system("clear")
    words_pool = prepare_words_pool("words_pool.json")
    if sound:
        engine.setProperty('rate', 200)
        voices = engine.getProperty('voices')

    if len(words_pool) == 0:
        console.print("There is no word in the words pool")
        _ = input("Press Enter to continue ...")
        return
    with open(".setting", 'r') as f:
        setting = json.load(f)
    practice_rate = int(setting["practice_rate"])
    _idx = 1
    word_weights = []
    for i in range(len(words_pool)):
        if i / len(words_pool) > _idx / practice_rate:
            _idx += 1
        word_weights.append(_idx)
    num_words_per_round = min(num_words_per_round, len(words_pool))
    print(f"Number of words practicing in one round is {num_words_per_round}.")
    while True:
        sampled_words = random.choices(list(words_pool.items()), weights=word_weights, k=num_words_per_round)
        num_correct_answering = 0
        table = Table()
        table.add_column("Word", justify="right", style="white", no_wrap=True)
        table.add_column("Meaning", style="white")
        table.add_column("Your Answer", style="white")
        table.add_column("Correct or not", style="white")
        for word, meaning in sampled_words:
            os.system("clear")
            if sound:
                console.print("Carefully listen :wink:")
                #voice_from = random.randint(0,len(voices))
                #engine.setProperty('voice', voices[voice_from].id)
                engine.say(word)
                engine.runAndWait()
            else:
                console.log(f"[bold red]Word: {word}.[/bold red]")
            if sound:
                answer = Prompt.ask("Type the word and your answer here. eg: apple;蘋果")
                if answer.split(";")[0] == word:
                    console.log("[bold white]You spell the word correctly. :1st_place_medal:")
                else:
                    console.log("[bold red]You spell the word wrong ... _^_")
            else:
                answer = Prompt.ask("Type your answer here")
            if sound:
                console.log(f"[bold blue]The word is {word}.[/bold blue]:wink:[bold blue]The true meaning is: {meaning}.[/bold blue]")
            else:
                console.log(f"[bold blue]The true meaning is: {meaning}.[/bold blue]")
            _ = input("Press Enter to continue ...")
            if_correct = yes_or_no()
            num_correct_answering += if_correct
            if if_correct:
                table.add_row(word, meaning, answer, str(if_correct))
            else:
                table.add_row(RED.format(word), RED.format(meaning), RED.format(answer), RED.format(str(if_correct)))
        console.print(table)
        console.log(f"Correct rate for this round: {num_correct_answering} / {num_words_per_round} = {num_correct_answering / num_words_per_round}")

        if_store = Prompt.ask("Store the practice record? (y/n)")
        if if_store == "y" or if_store == "Y":
            time_now = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            if sound:
                file_name = f"practice_records/record_with_listening_{time_now}.txt"
            else:
                file_name = f"practice_records/record_{time_now}.txt"
            with open(file_name, 'w') as f:
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
            if sound:
                hash_table[str(current_enum)] = f"record_with_listening_{time_now}.txt"
            else:
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
_PRACTICE_WITH_SOUND = "ps"
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
_SETTING = "set"

def check_lock():
    try:
        with open('.tofel.lock', 'x') as file:
            pass
    except FileExistsError:
        print("Error: You have another process running the program. You can only run the program once at a time.", file=sys.stderr)
        sys.exit(1)


def main():
    os.system("clear")
    if not os.path.isfile("./words_pool.json"):
        os.system("touch words_pool.json")
    if not os.path.isdir("speaking"):
        os.makedirs("speaking", exist_ok=False)
    if not os.path.isfile("speaking/problems.json"):
        with open("speaking/problems.json", 'w') as f:
            json.dump([], f)
    if not os.path.isfile(".setting"):
        with open(".setting", 'w') as f:
            json.dump({
            "practice_rate": 3,
                }, f)
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
                _ = input("Your input is in the wrong format. Press Enter to continue ...")
                os.system("clear")
                continue
            word, meaning = word_meaning_pair[0], word_meaning_pair[1]
            add_words(word, meaning)
            print(f"Successfully adding word: {word} and meaning {meaning} into word pools ^_^")
        elif mode == _PRACTICE:
            num_words_per_round = int(input("Type the number of words you want to practice per round. For example, 10:"))
            practice(num_words_per_round)
        elif mode == _PRACTICE_WITH_SOUND:
            num_words_per_round = int(input("Type the number of words you want to practice per round. For example, 10:"))
            practice(num_words_per_round, sound=True)
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
        elif mode == _SETTING:
            with open(".setting", 'r') as f:
                setting = json.load(f)
            table = Table()
            for key in setting.keys():
                if key == "practice_rate":
                    key += "\n(The total level of practicing.)"
                table.add_column(key, style="white")
            #for value in setting.values():
            table.add_row(*[str(val) for val in setting.values()])
            console.print(table)
            answer = Prompt.ask("Which setting do you want to change? And change to what value? (For example: practice_rate;10) Enter for no changes and go back to the main page")
            if answer == "":
                os.system("clear")
                continue
            answer = answer.split(";")
            if answer[0] == "practice_rate":
                try:
                    if int(answer[1]) > 0:
                        setting[answer[0]] = answer[1];
                        with open(".setting", 'w') as f:
                            json.dump(setting, f, indent=4)
                        console.print("Successfully update the setting")
                    else:
                        console.print(f"Error: {answer[1]} is an invalid value...")
                except:
                    console.print(f"Error: {answer[1]} is an invalid value...")
            else:
                console.print(f"Error: {answer[0]} is an invalid key...")
            _ = input("Press Enter to continue...")
        else:
            print(f"No such mode {mode}... _^_")
            _ = input("Press Enter to continue...")
        os.system("clear")

if __name__ == "__main__":
    check_lock()
    main()
    release_lock()
