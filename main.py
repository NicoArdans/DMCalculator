#!/usr/bin/python3.9

import PySimpleGUI as sg
import DriverMeasure
import math
from pathlib import Path
import csv

sg.theme('GrayGrayGray')  # please make your windows colorful

layout = [[
        sg.Column([
            [
                sg.Text('Value Stream:')
            ],
            [
                sg.Text('Short Cycle:')
            ],
            [
                sg.Text('Medium Cycle:')
            ],
            [
                sg.Text('Long Cycle:')
            ]
            ]),
        sg.Column([
            [
                sg.Text('Hourly Rate:', enable_events=True, key='-hourlyRate-')
            ],
            [
                sg.Input(key='-shortRate-', size=5)
            ],
            [
                sg.Input(key='-mediumRate-', size=5)
            ],
            [
                sg.Input(key='-longRate-', size=5),
            ]
            ]),
        sg.Column([
            [
                sg.Text('Flats:')
            ],
            [
                sg.Input(key='-shortFlats-', size=5)
            ],
            [
                sg.Input(key='-mediumFlats-', size=5)
            ],
            [
                sg.Input(key='-longFlats-', size=5)
            ]
            ]),
        sg.Column([
            [
                sg.Text('Crew:')
            ],
            [
                sg.Text(key='-shortCrew-')
            ],
            [
                sg.Text(key='-mediumCrew-')
            ],
            [
                sg.Text(key='-longCrew-')
            ]
            ], element_justification="center")
        ],
        [
            sg.VPush()
        ],
        [
            sg.Button('Generate Excel File', key='-generateExcel-')
        ],
        [
            sg.Button('Calculate Crew Size', key='-calculate-'),
            sg.Button('Quit', key='-quit-')
        ]
]


dm = DriverMeasure.DriverMeasure()

textClick = False
dataIsGenerated = False

window = sg.Window('Picking Driver Measure Calculator', layout, size=(550, 300))
while True:  # Event Loop=
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == '-quit-':
        break
    if event == '-calculate-':

        dm.generate_data("Short", int(values["-shortRate-"]), int(values["-shortFlats-"]))
        dm.generate_data("Medium", int(values["-mediumRate-"]), int(values["-mediumFlats-"]))
        dm.generate_data("Long", int(values["-longRate-"]), int(values["-longFlats-"]))

        window["-shortCrew-"].update(dm.VALUESTREAMS["Short"]["crewSize"])
        window["-mediumCrew-"].update(dm.VALUESTREAMS["Medium"]["crewSize"])
        window["-longCrew-"].update(dm.VALUESTREAMS["Long"]["crewSize"])
        dataIsGenerated = True

    if event == '-hourlyRate-':
        if not textClick:
            textClick = True
            window['-hourlyRate-'].update("Daily Rate:")
            window['-shortRate-'].update(dm.VALUESTREAMS["Short"]["dailyRate"])
            window['-mediumRate-'].update(dm.VALUESTREAMS["Medium"]["dailyRate"])
            window['-longRate-'].update(dm.VALUESTREAMS["Long"]["dailyRate"])
        elif textClick:
            textClick = False
            window['-hourlyRate-'].update("Hourly Rate:")
            window['-shortRate-'].update(dm.VALUESTREAMS["Short"]["hourlyRate"])
            window['-mediumRate-'].update(dm.VALUESTREAMS["Medium"]["hourlyRate"])
            window['-longRate-'].update(dm.VALUESTREAMS["Long"]["hourlyRate"])

    if event == '-generateExcel-':
        if not dataIsGenerated:
            sg.popup_ok("Please Calculate Crew Size First!")
        elif dataIsGenerated:
            file_path = sg.popup_get_file('Save as', no_window=True, save_as=True, file_types=(('Comma Separated Values', '*.csv'),))
            if file_path:
                dm.generate_driver_measure()
                file = Path(file_path)
                rows = []
                for VS in dm.VALUESTREAMS:
                    rows.append([str(VS)])
                    rows.append(['Time', 'Target', 'Target Accumulative'])
                    for key in range(1, 11):
                        if len(dm.VALUESTREAMS[VS]["predictions"][key]) == 3:
                            time_interval = str(dm.VALUESTREAMS[VS]["predictions"][key][0])
                            target = str(dm.VALUESTREAMS[VS]["predictions"][key][1])
                            target_accumulative = str(dm.VALUESTREAMS[VS]["predictions"][key][2])
                            rows.append([time_interval, target, target_accumulative])
                with open(file, 'w') as f:
                    write = csv.writer(f)
                    write.writerows(rows)
        # change the "output" element to be the value of "input" element
        # window['-OUTPUT-'].update(values['-IN-'])
        pass
window.close()
