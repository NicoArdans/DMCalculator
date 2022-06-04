#!/usr/bin/python3.9

import PySimpleGUI as sg
import DriverMeasure
import math

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

    if event == '-hourlyRate-':
        if textClick==False:
            textClick = True
            window['-hourlyRate-'].update("Daily Rate:")
            window['-shortRate-'].update(dm.VALUESTREAMS["Short"]["dailyRate"])
            window['-mediumRate-'].update(dm.VALUESTREAMS["Medium"]["dailyRate"])
            window['-longRate-'].update(dm.VALUESTREAMS["Long"]["dailyRate"])
        elif textClick==True:
            textClick = False
            window['-hourlyRate-'].update("Hourly Rate:")
            window['-shortRate-'].update(dm.VALUESTREAMS["Short"]["hourlyRate"])
            window['-mediumRate-'].update(dm.VALUESTREAMS["Medium"]["hourlyRate"])
            window['-longRate-'].update(dm.VALUESTREAMS["Long"]["hourlyRate"])

        # change the "output" element to be the value of "input" element
        # window['-OUTPUT-'].update(values['-IN-'])
        pass
window.close()
