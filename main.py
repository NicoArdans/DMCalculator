#!/usr/bin/python3.9

import PySimpleGUI as SG
import DriverMeasure
from pathlib import Path
import csv
import webbrowser

SG.theme('TanBlue')
SG.set_options(font='Calibri 20')

layout = [[
        SG.Column([
            [
                SG.Text('Value Stream:')
            ],
            [
                SG.Text('Short Cycle:')
            ],
            [
                SG.Text('Medium Cycle:')
            ],
            [
                SG.Text('Long Cycle:')
            ]
            ]),
        SG.Column([
            [
                SG.Text('Hourly Rate:', enable_events=True, key='-hourlyRate-')
            ],
            [
                SG.Input(default_text="36", key='-shortRate-', size=5)
            ],
            [
                SG.Input(default_text="29", key='-mediumRate-', size=5)
            ],
            [
                SG.Input(default_text="15", key='-longRate-', size=5)
            ]
            ]),
        SG.Column([
            [
                SG.Text('Flats:')
            ],
            [
                SG.Input(key='-shortFlats-', size=5)
            ],
            [
                SG.Input(key='-mediumFlats-', size=5)
            ],
            [
                SG.Input(key='-longFlats-', size=5)
            ]
            ]),
        SG.Column([
            [
                SG.Text('Crew:')
            ],
            [
                SG.Text(key='-shortCrew-')
            ],
            [
                SG.Text(key='-mediumCrew-')
            ],
            [
                SG.Text(key='-longCrew-')
            ]
            ], element_justification="center")
        ],
        [
            SG.Button('Generate Excel File', key='-generateExcel-', border_width=0)
        ],
        [
            SG.Button('Calculate Crew Size', key='-calculate-', border_width=0),
            SG.Button('Quit', key='-quit-', border_width=0)
        ]
]


dm = DriverMeasure.DriverMeasure()

textClick = False
dataIsGenerated = False

window = SG.Window('Picking Driver Measure Calculator', layout,  use_default_focus=False)
while True:
    event, values = window.read()
    print(event, values)
    if event == SG.WIN_CLOSED or event == '-quit-':
        break
    if event == '-calculate-':
        if values['-shortRate-'].isnumeric() and values['-shortFlats-'].isnumeric() and values['-mediumRate-'].isnumeric() and values['-mdiumFlat-'].isnumeric() and values['-longRate-'].isnumeric() and values['-longFlats-'].isnumeric():
            dm.generate_data("Short", int(values["-shortRate-"]), int(values["-shortFlats-"]))
            dm.generate_data("Medium", int(values["-mediumRate-"]), int(values["-mediumFlats-"]))
            dm.generate_data("Long", int(values["-longRate-"]), int(values["-longFlats-"]))
            window["-shortCrew-"].update(dm.VALUESTREAMS["Short"]["crewSize"])
            window["-mediumCrew-"].update(dm.VALUESTREAMS["Medium"]["crewSize"])
            window["-longCrew-"].update(dm.VALUESTREAMS["Long"]["crewSize"])
            dataIsGenerated = True
        else:
            SG.popup_ok('Please Enter Numeric Values!')
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
            SG.popup_ok("Please Calculate Crew Size First!")
        elif dataIsGenerated:
            file_path = SG.popup_get_file('Save as', no_window=True, save_as=True, file_types=(('Comma Separated'
                                                                                                ' Values', '*.csv'),))
            if file_path:
                dm.generate_driver_measure()
                file = Path(file_path)
                rows = []
                for VS in dm.VALUESTREAMS:
                    rows.append([str(VS) + ' Cycle'])
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
                webbrowser.open(str(file))
            break
        pass
window.close()
