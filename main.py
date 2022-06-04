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
                sg.Text('Hourly Rate:', key='-hourlyRate-')
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

window = sg.Window('Picking Driver Measure Calculator', layout, size=(550, 300))
while True:  # Event Loop=
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == '-calculate-':
        dm.VALUESTREAMS["Short"]["hourlyRate"] = int(values["-shortRate-"])
        dm.VALUESTREAMS["Short"]["flats"] = int(values["-shortFlats-"])
        dm.VALUESTREAMS["Short"]["dailyRate"] = dm.VALUESTREAMS["Short"]["hourlyRate"] * 7
        dm.VALUESTREAMS["Short"]["crewSize"] = math.ceil(dm.VALUESTREAMS["Short"]["flats"] / dm.VALUESTREAMS["Short"]["dailyRate"])

        dm.VALUESTREAMS["Medium"]["hourlyRate"] = int(values["-mediumRate-"])
        dm.VALUESTREAMS["Medium"]["flats"] = int(values["-mediumFlats-"])
        dm.VALUESTREAMS["Medium"]["dailyRate"] = dm.VALUESTREAMS["Medium"]["hourlyRate"] * 7
        dm.VALUESTREAMS["Medium"]["crewSize"] = math.ceil(dm.VALUESTREAMS["Medium"]["flats"] / dm.VALUESTREAMS["Medium"]["dailyRate"])

        dm.VALUESTREAMS["Long"]["hourlyRate"] = int(values["-longRate-"])
        dm.VALUESTREAMS["Long"]["flats"] = int(values["-longFlats-"])
        dm.VALUESTREAMS["Long"]["dailyRate"] = dm.VALUESTREAMS["Long"]["hourlyRate"] * 7
        dm.VALUESTREAMS["Long"]["crewSize"] = math.ceil(dm.VALUESTREAMS["Long"]["flats"] / dm.VALUESTREAMS["Long"]["dailyRate"])

        window["-shortCrew-"].update(dm.VALUESTREAMS["Short"]["crewSize"])
        window["-mediumCrew-"].update(dm.VALUESTREAMS["Medium"]["crewSize"])
        window["-longCrew-"].update(dm.VALUESTREAMS["Long"]["crewSize"])



        # change the "output" element to be the value of "input" element
        # window['-OUTPUT-'].update(values['-IN-'])
        pass
window.close()