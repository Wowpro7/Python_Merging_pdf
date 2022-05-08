import PySimpleGUI as sg
import merge_functions

TEXT_OUTLINE_SIZE = 11
INITAL_BROWSE_FOLDER = 'C:/Users/Public'
MERGING_STYLES_LIST = merge_functions.MERGING_STYLES_LIST


def build_layout():
    sg.theme('Dark Blue 3')  # please make your windows colorful
    layout = [[sg.Text('Choose files to build from')],
              [sg.Text('Leading File:      ', size=(TEXT_OUTLINE_SIZE)), sg.InputText(key='first_input_File'),
               sg.FileBrowse(initial_folder=INITAL_BROWSE_FOLDER, key='first_browse')],
              [sg.Text('Merging File: ', size=(TEXT_OUTLINE_SIZE), key='txt_merging_file'), sg.InputText(key='second_input_file'),
               sg.FileBrowse(initial_folder=INITAL_BROWSE_FOLDER, key='second_browse')],
              [sg.Text('New File Name:', size=(TEXT_OUTLINE_SIZE)), sg.InputText(key='User_named')],
              [sg.Text('Merging style:', size=(TEXT_OUTLINE_SIZE)), sg.Combo(MERGING_STYLES_LIST\
                                                                             , default_value='Sequence', # sg.Combo - enable_event=True creates an event when Combo choice is changed. has a default value
                                                                             key='options_list', enable_events=True,
                                                                             readonly=True), \
               sg.Text('Start Page:', size=(8), key='txt_start_page', visible=False), sg.InputText(key='input_start_page', size=(6), visible=False),\
               sg.Text('Stop Page:', size=(8),  key='txt_stop_page',visible=False), sg.InputText(key='input_stop_page', size=(6), visible=False)],
              [sg.Text('Save at: ', size=(TEXT_OUTLINE_SIZE)), sg.InputText(key='saving_path'),
               sg.FolderBrowse(initial_folder=INITAL_BROWSE_FOLDER)],
              [sg.Button(key='Submit_files_paths', button_text='DO ME!!'), sg.Exit(visible=False)]]
    return layout


def main():
    layout = build_layout()
    window = sg.Window('PDF Builder', layout)
    start_page = None
    stop_page = None

    Sequence = True
    Middle = False
    odd_even = False
    cut = False
    Spin_right = False

    while True:
        event, values = window.read()  # event = type of the widget, you can write key value in it and change
        # and change the name its addressed through. values = key name of the widget when they are no
        # buttons.
        #print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':  # close the program
            break
        elif event == 'options_list':
            Sequence = False
            Middle = False
            odd_even = False
            cut = False
            Spin_right = False

            if values['options_list'] == 'Middle Merger' or values['options_list'] == 'Cut' or values['options_list'] == 'Spin Right':  # display the additional options
                window['txt_start_page'].update(visible=True)
                window['input_start_page'].update(value='', visible=True)
                window['txt_merging_file'].update(visible=False)
                window['second_input_file'].update(visible=False)
                window['second_browse'].update(visible=False)
                window['txt_stop_page'].update(visible=False)
                window['input_stop_page'].update(value='', visible=False)  # reset the chosen page number

                if values['options_list'] == 'Cut':  # if he style is 'cut'
                    window['txt_stop_page'].update(visible=True)
                    window['input_stop_page'].update(visible=True)
                    cut = True

                elif values['options_list'] == 'Spin Right': # input format:  <page_number>:<degree(90,180,270)>,<start_page-stop_page>:<degree(90,180,270)>
                    window['input_start_page'].update(value='<page_number>:<degree(90,180,270)>,<start_page-stop_page>:<degree(90,180,270)>')
                    Spin_right = True

                else:  # else the cut is 'middle'
                    #window['input_stop_page'].update('')  # reset the chosen page number
                    window['txt_merging_file'].update(visible=True)
                    window['second_input_file'].update(visible=True)
                    window['second_browse'].update(visible=True)
                    Middle = True

            else:  # disable txt and input pages visibility
                window['txt_start_page'].update(visible=False)
                window['input_start_page'].update(visible=False)
                window['txt_stop_page'].update(visible=False)
                window['input_stop_page'].update(visible=False)

                window['txt_merging_file'].update(visible=True)
                window['second_input_file'].update(visible=True)
                window['second_browse'].update(visible=True)
                start_page = None

                if values['options_list'] == 'Sequence':
                    Sequence = True

                elif values['options_list'] == 'Odd - Even':
                    odd_even = True

        elif event == 'Submit_files_paths':
            if values['options_list'] == 'Middle Merger' or values['options_list'] == 'Cut':
                start_page = values['input_start_page']
                if not start_page.isdigit():
                    sg.popup_error('"Start Page" - is invalid page number')  # Shows red error button
                    continue  # start wait for new events
                else:
                    start_page = int(start_page)-1
                    if start_page < 0:
                        sg.popup_error('"Start Page" - is invalid page number')  # Shows red error button
                        continue  # start wait for new events

                if values['options_list'] == 'Cut':
                    stop_page = values['input_stop_page']
                    if not stop_page.isdigit():
                        sg.popup_error('"Stop Page" - is invalid number')  # Shows red error button
                        continue  # start wait for new events
                    else:
                        stop_page = int(stop_page)-1
                        if stop_page < 0:
                            sg.popup_error('"Stop Page" - is invalid page number')  # Shows red error button
                            continue  # start wait for new events
            elif values['options_list'] == 'Spin Right':
                start_page = values['input_start_page']

            user_named_file = values['User_named']
            if user_named_file == '':
                sg.popup_error('please enter the new file name')  # Shows red error button
                continue

            saving_path = values['saving_path'] + '/'#.replace('\\', '/') + '/'  # in case the use added the '/' at he end
            if saving_path == '/':
                sg.popup_error('please choose where to save')  # Shows red error button
                continue

            if values['options_list'] != 'Cut' and values['options_list'] != 'Spin Right':
                second_path = values['second_input_file']
            else:
                second_path = None
            first_path = values['first_input_File']

            merging_style = {'Sequence': Sequence, 'Middle Merger': Middle, 'Odd - Even': odd_even, 'Cut': cut, 'Spin Right': Spin_right}
            new_file_name = merge_functions.merge(first_path, second_path, saving_path=saving_path,
                                                  first_pdf_leads=True, User_named=user_named_file, merging_style=merging_style, start_page=start_page, stop_page=stop_page)
            if not new_file_name.endswith(
                    '.pdf'):  # if the file was created the return will be its new name others wise there is a problem
                sg.popup_error('something went wrong: ', new_file_name)  # Shows red error button
                continue
            else:
                sg.popup('%s was successfully created' % new_file_name)

    window.close()

#TODO:
    '''
    1.add a split option :
        *user enters one file path.
        *start page.
        *new file name. the code uses this name to create 2 files, one ending with '_1' and the other wth '_2'
    2.change 'merge_functions.py' in away that will decrease the amount of code in 'def merge'.
    3. add 'Rotate Right' option, in the page number input default value is the syntax: '<page_number>:<degree(90,180,270)>,<start_page-stop_page>:<degree(90,180,270)'
    
    '''
if __name__ == '__main__':
    main()
