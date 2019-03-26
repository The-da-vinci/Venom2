import curses


class UI:
    # initialize the program
    def __init__(self, msg_buf):
        self.scr = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        self.scr_height, self.scr_width = self.scr.getmaxyx()
        self.msg_buf_zone = curses.newwin(5, self.scr_height - 1, 5, 10)
        self.message = ""
        self.running = False
        self.msg_buf = msg_buf

    def draw_top_line(self):
        self.scr.addstr(0, 0, "(type q to quit)", curses.A_REVERSE)
        self.draw_line(1)

    def draw_bottom_line(self):
        self.scr.addstr(self.scr_height - 1, 0, ":", curses.color_pair(0))
        self.draw_line(self.scr_height - 2)

    def draw_output(self, msg_buf):
        z = self.scr_height - 3
        new_msg = len(msg_buf)
        if int(new_msg) >= 1:
            for i in msg_buf:
                    if z > 1:
                        try:
                            self.scr.addstr(z, 0, i)
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
        self.message = self.message.decode(encoding='UTF-8')

        # check if input is blank
        if len(self.message) == 0:
            pass
        # check if the input is quit
        elif str(self.message[0]) == "/quit":
            quit()
            self.running = False
        else:  # else just draw it
            self.msg_buf.append(self.message)
            self.draw_output(self.msg_buf)

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

    def manage_screen_buffer(self):
            try:
                # If we've got screen full of text, scroll it
                if (len(msg_buf) == self.scr_height):
                        for i in range(2, self.scr_height - 3):
                                msg_buf[i - 1] = msg_buf[i]
                for y in range(1, len(msg_buf)):
                    if msg_buf[y] is None:
                        pass
                    else:
                        self.scr.clear()
                        self.draw_top_line()
                        self.draw_bottom_line()
                        self.scr.addstr(1, y, msg_buf[y])
                        self.scr.refresh()
            except Exception as err:
                print(err)
                msg_buf.append(str(err))


if __name__ == "__main__":
    msg_buf = []
    u = UI(msg_buf)
    while True:
        try:
            u.manage_screen_buffer()
            u.scr.refresh()
            u.get_user_input()
        except KeyboardInterrupt:
            exit()
