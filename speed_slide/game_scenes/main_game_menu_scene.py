import time
from tui import *
from tui.controls import *
from speed_slide.io import safe_input, beep
from speed_slide.__game_consts import _Constants as Constants

class MainGameMenuScene(Scene):
    def __init__(self):
        super().__init__(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT, '*')

        self.background_rft.set_random_colours_to_all(except_foreground=[ForegroundColours.BLACK, ForegroundColours.WHITE])

        copyright_text = '(C) 2024 HKU ENGG1330 Semester 1 Group 1L3-3. All rights reserved.'
        lbl_copyright = TxtLabel('lbl_copyright', 110, 3, 0, 27, text=f'{copyright_text: ^110}',
                                 padding_top=1, padding_bottom=1, padding_left=1, padding_right=1, draw_borders=True,
                                 border_colour=ForegroundColours.BLUE)
        lbl_copyright.formatted_text.set_format(0, slice(len(copyright_text), ForegroundColours.BLUE))
        self.controls.append(lbl_copyright)

        self.render()


    def play(self):
        menu_dw = DialogueWindow('menu_dw', 60, 20, 25, 3, title="SpeedSlide Game Menu", border_colour=ForegroundColours.BLUE)
        # header
        lbl_header = TxtLabel('lbl_header', 50, 1, 5, 3, text='Select an option from the menu below:')
        # menu options
        lbl_options = TxtLabel('lbl_options', 50, 5, 5, 5, text="""## PLAY
    - [H]ow to Play?
    - [N]ew Game
    
## MISCELLANEOUS
    - [A]bout
    - [Q]uit""", auto_size=True,
                 padding_top=1, padding_bottom=1, padding_left=1, padding_right=1, draw_borders=True, border_colour=ForegroundColours.GREEN)
        lbl_footer = TxtLabel('lbl_footer', 50, 1, 5, 16, text='Only the first character of your input will be read.',
                 auto_size=True)
        lbl_footer.formatted_text.set_format(0, slice(9, 14), ForegroundColours.YELLOW, TextFormats.UNDERLINE)
        menu_dw.controls.extend([lbl_header, lbl_options, lbl_footer])

        self.show_dialogue(menu_dw, None)

        valid_inputs = ['N', 'H', 'A', 'Q']
        while True:
            user_option = safe_input(RichFormatText('Select an option: ').set_format(0, slice(19), ForegroundColours.MAGENTA)).upper()[:1]
            if user_option in valid_inputs:
                option_line = {
                    'H': (1, slice(4, 20)),
                    'N': (2, slice(4, 17)),
                    'A': (5, slice(4, 14)),
                    'Q': (6, slice(4, 13)),
                }[user_option]
                fg_colour, bg_colour, _ = lbl_options.formatted_text.get_format(*option_line)[0]
                lbl_options.formatted_text.set_format(*option_line, ForegroundColours.BLACK, BackgroundColours.GREEN)
                self.render()
                time.sleep(0.2)
                break

            # show error message
            invalid_option_dw = DialogueWindow('invalid_alert_dw',30, 10, 40, 6, title='ERROR!', border_colour=ForegroundColours.RED)
            lbl = TxtLabel('lbl', 28, 5, 1, 4, text=f'Option \"{user_option}\" is invalid! Please try again.',
                     padding_left = 2, padding_right = 2, auto_size=True)
            [lbl.formatted_text.set_format(y, slice(lbl.width), ForegroundColours.RED) for y in range(len(lbl.formatted_text))]
            invalid_option_dw.controls.append(lbl)
            beep()
            self.show_dialogue(invalid_option_dw, lambda _: safe_input(RichFormatText('Press any key to continue...')))

        return user_option