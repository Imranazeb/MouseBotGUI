import PySimpleGUI as sg
import time
import random
import pyautogui as pg
import datetime as dt
from sys import exit

# DEFINE VARIABLES

hours = [int(hour)+1 for hour in range(12)]
init_time = 5
init_state = False

sg.set_options(font=('arial', 14, 'bold'))
sg.theme('dark')

# GET INPUT

layout = [
    [sg.Text("Please enter start time: ", key='-DISPLAY-')],
    [sg.DD(hours, default_value='9', key='-TIME-')],
    [sg.Radio('AM', 'time', default=True, key='-AM-'),
     sg.Radio('PM', 'time', key='-PM-')],
    [sg.Button('OK'),
     sg.Button('Exit')]
]

window = sg.Window("Main window", layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        exit()

    if event == 'OK':
        shift_start = int(values['-TIME-'])
        if values['-AM-'] == True:
            is_start_day = True
        else:
            is_start_day = False
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
            is_end_day = True
        else:
            is_end_day = False
            shift_end += 12  # ADD 12 IF INPUT IS PM.
        break

window.close()


if is_start_day == False and is_end_day == True:
    is_night_shift = True
    night_shift_start_day = (dt.datetime.now().day)

else:
    is_night_shift = False
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
    layout,
    size=(480, 100),
    element_justification='center',
    keep_on_top=True
)

init_start_time = time.time()

while not init_state:
    event, values = window.read(timeout=10)
    if event == (sg.WIN_CLOSED):
        break

    elasped_time = round(time.time()-init_start_time)
    if elasped_time > init_time:
        init_state = True
        shift_is_on = True
        break
    else:
        timer = (round(init_time-elasped_time))
        window['-text_init-'].update(
            f'Please place cursor at desired location within {timer} seconds')

# GET MOUSE POSITION AFTER INIT:
mouse_target_x = pg.position().x
mouse_target_y = pg.position().y

# MAIN PROGRAM

while shift_is_on:
    event, values = window.read(timeout=10)
    if event == (sg.WIN_CLOSED):
        break

    current_time_hour = int(dt.datetime.now().hour)
    current_time_min = int(dt.datetime.now().minute)
    current_time_day = int(dt.datetime.now().day)
    is_next_day = current_time_day > night_shift_start_day  # BOOLEAN

    
    # FIGURE OUT NIGHT SHIFT PART 

    if is_night_shift and not is_next_day:
        night_adjuster = -24
    else:
        night_adjuster = 0
    
    if (current_time_hour > shift_start) and (current_time_hour < shift_end - night_adjuster):
        pg.click(mouse_target_x, mouse_target_y)
        random_pause = random.randint(3*60, 5*60)
        start_counter = time.time()
        pause_completed = False
        time_left_hr = shift_end - current_time_hour
        time_left_min = 60 - current_time_min
        if not is_night_shift or is_next_day:
            window['-text_init-'].update(
                f'{time_left_hr-1} hour(s) and {time_left_min} minutes to go!')
        else:
            print("This is night shift", shift_start, shift_end)
            window['-text_init-'].update(
                f'{(12-shift_start) + shift_end} hour(s) and {time_left_min} minutes to go!')

        while not pause_completed:
            event, values = window.read(timeout=10)
            if event == (sg.WIN_CLOSED):
                break

            elasped_counter = round(time.time()-start_counter)
            countdown = round(random_pause - elasped_counter)
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
    shift_is_on = False

window.close()
exit()