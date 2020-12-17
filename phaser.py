import curses
import requests
import time
import json

images = {
    "new_moon": ["   _..._   ", " .:::::::. ", ":::::::::::", ":::::::::::", "`:::::::::'", "  `':::''  "],
    "waxing_crescent":  ["   _..._   ", " .::::. `. ", ":::::::.  :", "::::::::  :", "`::::::' .'", "  `'::'-'  "],
    "first_quarter": ["   _..._   ", " .::::  `. ", "::::::    :", "::::::    :", "`:::::   .'", "  `'::.-'  "],
    "waxing_gibbous": ["   _..._   ", " .::'   `. ", ":::       :", ":::       :", "`::.     .'", "  `':..-'  "],
    "full_moon": ["   _..._   ", " .'     `. ", ":         :", ":         :", "`.       .'", "  `-...-'  "],
    "waning_gibbous": ["   _..._   ", " .'   `::. ", ":       :::", ":       :::", "`.     .::'", "  `-..:''  "],
    "last_quarter": ["   _..._   ", " .'  ::::. ", ":    ::::::", ":    ::::::", "`.   :::::'", "  `-.::''  "],
    "waning_cresent": ["   _..._   ", " .' .::::. ", ":  ::::::::", ":  ::::::::", "`. '::::::'", "  `-.::''  "]
}

def get_phase():
    current_time = int(time.time())
    response = requests.get("http://api.farmsense.net/v1/moonphases/?d={}".format(current_time))
    phase = json.loads(response.content)[0]["Phase"]
    image_title = phase.replace(" ", "_").lower()
    description = json.loads(response.content)[0]["Moon"]
    return [phase, image_title, description]

def c_main(stdscr, phase, images) -> int:
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_WHITE)
    stdscr.bkgd(' ', curses.color_pair(1) | curses.A_BOLD)
    phase, image_title, description = phase
    image = images[image_title]
    while True:
        for counter, line in enumerate(image):
            stdscr.insstr(counter + 1, 3, line)
            stdscr.move(0, len(line)+3)
            stdscr.addstr("\n")
        stdscr.insstr(8, 1 , phase)
        stdscr.insstr(9, 1, description[0])
        stdscr.move(9, len(description[0])+1)
        char = stdscr.getch()
        break
    return 0

def main() -> int:
    phase = get_phase()
    return curses.wrapper(c_main, phase, images)

if __name__ == '__main__':
    exit(main())