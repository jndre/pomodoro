#! /usr/bin/python3

import time
import datetime
import argparse
from playsound import playsound

parser = argparse.ArgumentParser(description="Pomodoro timer")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-t", "--timer", type=int, help="Timer in minutes")
group.add_argument("-s", "--standard", action="store_true",
                   default=False, help="Standard pomodoro timer (25 min)")
group.add_argument("-d", "--double", action="store_true",
                   default=False, help="Double pomodoro timer (50 min)")
arguments = parser.parse_args()

#file paths
score_file_path = '/usr/local/share/pomodoro/score.txt'
sound_file_path = '/usr/local/share/pomodoro/error.mp3'

def update_score(to_add: int):
    score_file = open(score_file_path, 'r+')
    score_str = score_file.read()

    if score_str == '':
        score = 0
    else:
        score = int(score_str)

    score += to_add

    score_file.seek(0)
    score_file.write(str(score))
    score_file.truncate()
    score_file.close()


def timer(duration: int):
    start = datetime.datetime.now().replace(microsecond=0)
    for i in range(60*duration):
        now = datetime.datetime.now().replace(microsecond=0)
        print(str(now-start), end='\r')
        time.sleep(1)

    print('\033[93m' + '-- End --' + '\033[0m')
    playsound(sound_file_path)


def main():
    if arguments.standard:
        work_timer = 25
        break_timer = 5
    elif arguments.double:
        work_timer = 50
        break_timer = 10
    else:
        work_timer = arguments.timer
        break_timer = int(work_timer / 5)

    print("Work: " + str(work_timer) + " min")
    timer(work_timer)

    update_score(work_timer)

    print("Break: " + str(break_timer) + " min")
    timer(break_timer)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye!")
