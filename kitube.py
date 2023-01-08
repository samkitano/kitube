from pytube import YouTube
import PySimpleGUI as sg
import os, sys, copy
from configparser import ConfigParser


cfg           = ConfigParser()
user_path     = os.path.expanduser( '~' )
app_data_path = user_path + '\AppData\Local\Kitube'
ini_path      = app_data_path + '\config.ini'
theme         = 'Black'
lang          = 'EN'
themes        = ['Black', 'BlueMono', 'BluePurple', 'BrightColors', 'BrownBlue',
                 'Dark', 'Dark2', 'DarkAmber', 'DarkBlack', 'DarkBlack1', 'DarkBlue',
                 'DarkBlue1', 'DarkBlue10', 'DarkBlue11', 'DarkBlue12', 'DarkBlue13',
                 'DarkBlue14', 'DarkBlue15', 'DarkBlue16', 'DarkBlue17', 'DarkBlue2',
                 'DarkBlue3', 'DarkBlue4', 'DarkBlue5', 'DarkBlue6', 'DarkBlue7', 'DarkBlue8',
                 'DarkBlue9', 'DarkBrown', 'DarkBrown1', 'DarkBrown2', 'DarkBrown3', 'DarkBrown4',
                 'DarkBrown5', 'DarkBrown6', 'DarkBrown7', 'DarkGreen', 'DarkGreen1', 'DarkGreen2',
                 'DarkGreen3', 'DarkGreen4', 'DarkGreen5', 'DarkGreen6', 'DarkGreen7', 'DarkGrey',
                 'DarkGrey1', 'DarkGrey10', 'DarkGrey11', 'DarkGrey12', 'DarkGrey13', 'DarkGrey14',
                 'DarkGrey15', 'DarkGrey2', 'DarkGrey3', 'DarkGrey4', 'DarkGrey5', 'DarkGrey6',
                 'DarkGrey7', 'DarkGrey8', 'DarkGrey9', 'DarkPurple', 'DarkPurple1', 'DarkPurple2',
                 'DarkPurple3', 'DarkPurple4', 'DarkPurple5', 'DarkPurple6', 'DarkPurple7', 'DarkRed',
                 'DarkRed1', 'DarkRed2', 'DarkTanBlue', 'DarkTeal', 'DarkTeal1', 'DarkTeal10',
                 'DarkTeal11', 'DarkTeal12', 'DarkTeal2', 'DarkTeal3', 'DarkTeal4', 'DarkTeal5',
                 'DarkTeal6', 'DarkTeal7', 'DarkTeal8', 'DarkTeal9', 'Default', 'Default1',
                 'DefaultNoMoreNagging', 'GrayGrayGray', 'Green', 'GreenMono', 'GreenTan',
                 'HotDogStand', 'Kayak', 'LightBlue', 'LightBlue1', 'LightBlue2', 'LightBlue3',
                 'LightBlue4', 'LightBlue5', 'LightBlue6', 'LightBlue7', 'LightBrown', 'LightBrown1',
                 'LightBrown10', 'LightBrown11', 'LightBrown12', 'LightBrown13', 'LightBrown2',
                 'LightBrown3', 'LightBrown4', 'LightBrown5', 'LightBrown6', 'LightBrown7',
                 'LightBrown8', 'LightBrown9', 'LightGray1', 'LightGreen', 'LightGreen1', 'LightGreen10',
                 'LightGreen2', 'LightGreen3', 'LightGreen4', 'LightGreen5', 'LightGreen6', 'LightGreen7',
                 'LightGreen8', 'LightGreen9', 'LightGrey', 'LightGrey1', 'LightGrey2', 'LightGrey3',
                 'LightGrey4', 'LightGrey5', 'LightGrey6', 'LightPurple', 'LightTeal', 'LightYellow',
                 'Material1', 'Material2', 'NeutralBlue', 'Purple', 'Python', 'PythonPlus', 'Reddit',
                 'Reds', 'SandyBeach', 'SystemDefault', 'SystemDefault1', 'SystemDefaultForReal', 'Tan',
                 'TanBlue', 'TealMono', 'Topanga']
langs         = ['English', 'Português', 'Español']
lang_codes    = ['EN', 'PT', 'ES', 'FR']
r_menu        = ['', ['Paste']]
menus         = {
    'EN': [
            ['Settings', [
                'Language', langs,
                f"Theme", themes
                ]
            ]],
    'PT': [
            ['Definições', [
                'Idioma', langs,
                f"Tema", themes
                ]
            ]],
    'ES': [
            ['Configuración', [
                'Idioma', langs,
                f"Tema", themes
                ]
            ]]
    }
main_menu     = menus['EN']
msgs          = {
    'EN': {
        'btna': '\u2193 Video',
        'btnb': '\u2193 MP3',
        'lnk': 'Paste a link, dude!',
        'no': 'No no no. Not working!',
        'ok': 'Done!',
        'wait': 'Wait...'
        },
    'PT': {
        'btna': '\u2193 Vídeo',
        'btnb': '\u2193 MP3',
        'lnk': 'Cola um link, pá!',
        'no': 'Népias. Não funciona!',
        'ok': 'Já tá!',
        'wait': 'Já vai...'
        },
    'ES': {
        'btna': 'Bajar Video',
        'btnb': 'Bajar MP3',
        'lnk': 'Pega un enlace, a qué esperamos?',
        'no': 'Joooeee, no funciona!',
        'ok': 'Pó ya está!',
        'wait': 'Tranqui, en eso estamos...'
        }
}


def write_cfg(section, value):
    """Write settings to .ini file

    Args:
        section (str): INI section
        value (str): Setting value
    """

    cfg.set('USER', section, value)

    with open(ini_path, 'w') as configfile:
        cfg.write(configfile)


def check_ini():
    """Chek for ini file. Write a new one if needed.
    """

    if not os.path.exists(app_data_path):
        os.mkdir(app_data_path)

    if not os.path.exists(ini_path):
        cfg['USER'] = {'theme': theme,'lang': lang}

        with open(ini_path, 'w') as configfile:
            cfg.write(configfile)

    else:
        cfg.read(ini_path)


def translate(text):
    """Translate a message

    Args:
        text (str): message

    Returns:
        str: translated message
    """

    return msgs[lang][text]


def make_window():
    """Builds the window object

    Returns:
        sg.window: The window object
    """

    global lang, theme

    theme = cfg.get('USER', 'theme')
    lang  = cfg.get('USER', 'lang')

    sg.theme(theme)

    main_menu = copy.deepcopy(menus[lang])

    # I know! Don't judge!
    main_menu[[0][0]][1][2] = f"{main_menu[[0][0]][1][2]} ({theme})"

    layout = [
        [
            sg.Menu(main_menu, k = '-MENU-')]
        ,
        [
            sg.Text('URL:'),
            sg.In(size = (54, 1), enable_events = True, key = "-URL-", right_click_menu = r_menu)
        ],
        [
            sg.HSeparator()
        ],
        [
            sg.Button(translate('btna'), k = "V", size = (25)),
            sg.Button(translate('btnb'), k = "A", size = (25))
        ],
        [
            sg.HSeparator(),
        ],
        [
            sg.StatusBar(translate('lnk'), key="-SB-", size=(50, 1), background_color = "grey")
        ]
    ]

    window = sg.Window('Kitube - YouTube Downloads', layout)

    return window


def allOK():
    """All went good message
    """

    window["-URL-"].update("")
    window['-SB-'].update(text_color = "green")
    window['-SB-'].update(translate('ok'))

    window.refresh()


def err():
    """Dasnotgud message
    """

    window["-URL-"].update("")
    window['-SB-'].update(text_color = "red")
    window['-SB-'].update(translate('no'))

    window.refresh()


def pls_wait(title=''):
    """just wait, man. what's the hurry?

    Args:
        title (str, optional): Message to display. Defaults to ''.
    """

    window['-SB-'].update(text_color = "black")

    if title == '':
        window['-SB-'].update(translate('wait'))
    else:
        window['-SB-'].update('\u2193 ' + title)

    window.refresh()


def dldAudio(url):
    """Download MP4 file

    Args:
        url (str): Youtube link (url)
    """

    pls_wait()

    try:
        yt    = YouTube(url)
        video = yt.streams.filter(only_audio = True).first()

        pls_wait(video.title)

        out_file  = video.download()
        base, ext = os.path.splitext(out_file)
        new_file  = base + '.mp3'

        os.rename(out_file, new_file)

        allOK()

    except:
        err()


def dldVideo(url):
    """Download MP4 file

    Args:
        url (str): Youtube link (url)
    """

    pls_wait()

    try:
        video = YouTube(url)
        pls_wait(video.title)
        video = video.streams.get_highest_resolution()

        video.download()

        allOK()

    except:
        err()


check_ini()


window = make_window()


while True:
    """Main loop
    """
    event, values = window.read()

    # print(event, values) # uncomment for debugging

    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    url = values["-URL-"]

    if event == "A":
        if url == '':
            err()
        else:
            dldAudio(url)

    if event == "V":
        if url == '':
            err()
        else:
            dldVideo(url)

    if event == 'Paste':
        window['-URL-'].update(window.TKroot.clipboard_get())
        window.refresh()

    if event in langs:
        _v = values['-MENU-']
        if _v != lang:
            _idx = langs.index(_v)

            write_cfg('lang', lang_codes[_idx])

            window.close()
            window = make_window()

    if event in themes:
        _v = values['-MENU-']
        if _v != sg.theme():
            sg.theme(_v)

            write_cfg('theme', _v)

            window.close()
            window = make_window()

window.close()
