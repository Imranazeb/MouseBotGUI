import PySimpleGUI as sg
# sg.main_sdk_help()

hours = [int(hour)+1 for hour in range(12)]

sg.set_options(font=('arial', 14, 'bold'))


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

print(f'shift starts at {shift_start}', 'AM' if is_start_day == True else 'PM')

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        exit()
    if event == 'OK':
        shit_end = int(values['-TIME-'])
        if values['-AM-'] == True:
            is_end_day = True
        else:
            is_end_day = False
        break

window.close()

print(f'shift starts at {shift_start}', 'AM' if is_start_day == True else 'PM',
      f'and ends at {shit_end}', 'AM' if is_end_day == True else 'PM'
      )  # DEBUG

if is_start_day == False and is_end_day == True:
    is_night_shift = True
else:
    is_night_shift = False

print(f'night shift is {is_night_shift}')  # DEBUG
