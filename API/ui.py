import curses


class UI:
    # initialize the program
    def __init__(self, output):
        self.scr = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        self.scr_height, self.scr_width = self.scr.getmaxyx()
        self.output_zone = curses.newwin(5, self.scr_height - 1, 5, 10)
        self.message = ""
        self.running = True
        self.output = output

    def draw_top_line(self):
        self.scr.addstr(0, 0, "(type q to quit)", curses.A_REVERSE)
        self.draw_line(1)

    def draw_bottom_line(self):
        self.scr.addstr(self.scr_height - 1, 0, ":", curses.color_pair(0))
        self.draw_line(self.scr_height - 2)

    def draw_output(self, output):
        z = self.scr_height - 3
        new_msg = len(output)
        if int(new_msg) >= 1:
            for i in output:
                    if z > 1:
                        try:
                            for i in output:
                                self.scr.addstr(self.scr_height - 3, 1, i)
                                self.scr.refresh()
                                new_msg -= 1
                                z -= 1
                        except Exception as err:
                            err = str(err)
                            print(err)
                            self.scr.addstr(self.scr_height - 3, 1, err)
                            self.scr.refresh()
                            exit()
                    else:
                        pass
        else:
            pass

    def get_user_input(self):
        # get user input
        self.input_y = self.scr_height - 1
        self.input_x = 1
        self.message = self.scr.getstr(self.input_y, self.input_x)
        print(self.message)

        # check if input is blank
        if len(self.message) == 0:
            pass
        # check if the input is quit
        elif str(self.message[0]) == "/quit":
            return quit()
            self.running = False
        else:  # else just draw it
            self.message = self.message.decode(encoding='UTF-8')
            self.output.append(self.message)
            self.draw_output(self.output)

    # kills the program correctly
    def die(self):
        curses.endwin()

    # draws a horizontal line at a given y-coordinate
    def draw_line(self, y):
        line = ""
        i = 0
        while i < self.scr_width:
            line += "-"
            i += 1
        self.scr.addstr(y, 0, line)

if __name__ == "__main__":
    output = ['hey']
    u = UI(output)
    while True:
        try:
            u.draw_top_line()
            u.draw_bottom_line()
            u.draw_output(output)
            u.get_user_input()
            u.scr.refresh()
        except KeyboardInterrupt:
            exit()