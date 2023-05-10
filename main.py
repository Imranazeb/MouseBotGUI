import PySimpleGUI as sg
import time
import random
import pyautogui as pg
import datetime as dt
from sys import exit
import os

path = os.getcwd()
myImg = os.path.join(path, "favicon.ico")


myImg = "favicon.ico"

# DEFINE VARIABLES

hours = [int(hour)+1 for hour in range(12)]
startCountInit = 10
initialized = False

sg.set_options(font=('arial', 14, 'bold'))
sg.theme('SystemDefaultForReal')

# GET INPUT

layout = [
    [sg.Text("Please enter start time: ", key='-DISPLAY-', pad=(0, 20)),
        sg.DD(hours, default_value='9', key='-TIME-'),
        sg.Radio('AM', 'time', default=True, key='-AM-'),
        sg.Radio('PM', 'time', key='-PM-')],
    [sg.Push(), sg.Button('OK', size=(6, 0), pad=((0, 10), (0, 30))),
     sg.Button('Exit', size=(6, 0), pad=((10, 0), (0, 30))), sg.Push()]
]

window = sg.Window("Main window", icon=myImg).Layout(layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        exit()

    if event == 'OK':
        shift_start = int(values['-TIME-'])
        if values['-AM-'] == True:
            startsDay = True
        else:
            startsDay = False
        break

window['-DISPLAY-'].update("Please enter end time: ")
window['-PM-'].update(value=True)


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        exit()
    if event == 'OK':
        shift_end = int(values['-TIME-'])
        if values['-AM-'] == True:
            endsDay = True
        else:
            endsDay = False
            shift_end += 12  # ADD 12 IF INPUT IS PM.
        break

window.close()


if startsDay == False and endsDay == True:
    isNightShift = True
    night_shift_start_day = (dt.datetime.now().day)

else:
    isNightShift = False
    night_shift_start_day = (dt.datetime.now().day)


# INITIALIZE

layout = [
    [sg.VPush()],
    [sg.Text(f'txt',
             justification='center',
             font=("arial", 12, "bold"),
             key='-text_init-')
     ],
    [sg.Text(f'',
             justification='center',
             font=("arial", 12, "bold"),
             key='-text_countdown-')
     ],
    [sg.VPush()],
]


window = sg.Window(
    'Mouse Click Emulator',
    icon=myImg,
    size=(480, 100),
    element_justification='center',
    keep_on_top=True
).Layout(layout)

init_start_time = time.time()

while not initialized:
    event, values = window.read(timeout=10)
    if event == (sg.WIN_CLOSED):
        break

    elasped_time = round(time.time()-init_start_time)
    if elasped_time > startCountInit:
        initialized = True
        onTheClock = True
        break
    else:
        timer = (round(startCountInit-elasped_time))
        window['-text_init-'].update(
            f'Please place cursor at desired location within {timer} seconds')

# GET MOUSE POSITION AFTER INIT:
mouse_target_x = pg.position().x
mouse_target_y = pg.position().y

# MAIN PROGRAM


def determineParams():
    current_time_hour = int(dt.datetime.now().hour)
    current_time_min = int(dt.datetime.now().minute)
    current_time_day = int(dt.datetime.now().day)
    dayHaspassed = current_time_day > night_shift_start_day  # BOOLEAN
    return current_time_hour, current_time_min, current_time_day, dayHaspassed


def timeLeft(shift_end):
    current_time_hour, current_time_min, current_time_day, dayHaspassed = determineParams()
    time_left_hr = shift_end - current_time_hour
    time_left_min = 60 - current_time_min
    return time_left_hr, time_left_min


while onTheClock:
    event, values = window.read(timeout=10)
    if event == (sg.WIN_CLOSED):
        break

    current_time_hour, current_time_min, current_time_day, dayHaspassed = determineParams()

    # FIGURE OUT NIGHT SHIFT PART

    night_adjuster = -24 if isNightShift and not dayHaspassed else 0

    onTheClock = (current_time_hour >= shift_start) and (
        current_time_hour < shift_end - night_adjuster)  # bool

    if (current_time_hour >= shift_start) and (current_time_hour < shift_end - night_adjuster):
        pg.click(mouse_target_x, mouse_target_y)
        random_pause = random.randint(3*60, 5*60)

        start_counter = time.time()
        pause_completed = False

        time_left_hr, time_left_min = timeLeft(shift_end)

        if not isNightShift or dayHaspassed:  # dayshift
            window['-text_init-'].update(
                f'{time_left_hr-1} hour(s) and {time_left_min} minutes to go!')
        else:  # nightshift
            window['-text_init-'].update(
                f'{(12-shift_start) + shift_end} hour(s) and {time_left_min} minutes to go!')

        while not pause_completed:
            event, values = window.read(timeout=10)
            if event == (sg.WIN_CLOSED):
                break

            elasped_counter = round(time.time()-start_counter)
            countdown = round(random_pause - elasped_counter)

            time_left_hr, time_left_min = timeLeft(shift_end)

            if not isNightShift or dayHaspassed:  # dayshift
                window['-text_init-'].update(
                    f'{time_left_hr-1} hour(s) and {time_left_min} minutes to go!')
            else:  # nightshift
                window['-text_init-'].update(
                    f'{(12-shift_start) + shift_end} hour(s) and {time_left_min} minutes to go!')

            current_time_hour, current_time_min, current_time_day, dayHaspassed = determineParams()
            night_adjuster = -24 if isNightShift and not dayHaspassed else 0

            if (current_time_hour >= shift_start) and (current_time_hour < shift_end - night_adjuster):
                pass
            else:
                onTheClock = False
                pause_completed = True
                break

            if countdown > 0:
                window['-text_countdown-'].update(
                    f'Next mouse click in {countdown} seconds')
            else:
                pause_completed = True

    else:
        break

while True:
    window['-text_init-'].update(
        f'Conratulations! End of shift')
    window['-text_countdown-'].update(
        f'')
    event, values = window.read(timeout=10)

    if event == (sg.WIN_CLOSED):
        break
    onTheClock = False

window.close()
exit()
