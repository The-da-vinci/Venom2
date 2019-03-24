import curses


class UI:
    # initialize the program
    def __init__(self, output):
        self.scr = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        self.scr_height, self.scr_width = self.scr.getmaxyx()
        self.output_zone = curses.newwin(5, self.scr_height - 1, 5, 10)
        self.command = ""
        self.running = True
        self.output = []

    def draw_top_line(self):
        self.scr.addstr(0, 0, "(type q to quit)", curses.A_REVERSE)
        self.draw_line(1)

    def draw_bottom_line(self):
        self.scr.addstr(self.scr_height - 1, 0, ':', curses.color_pair(0))
        self.draw_line(self.scr_height - 2)

    def draw_output(self, output):
        z = self.scr_height - 3
        new_msg = len(self.output) - 1
        while z > 1:
            for i in self.output:
                i = i.split(":")
                for a in i:
                    print(z)
                    print(a)
                    self.scr.addstr(z, 100, a)
                    new_msg -= 1
                    z -= 1

    def get_user_input(self):
        # get user input
        input_y = self.scr_height - 1
        input_x = self.scr_width - 1
        self.command = self.scr.getstr(input_y, input_x)
        print(self.command)

        # check if input is blank
        if len(self.command) == 0:
            pass
        # check if the input is quit
        elif str(self.command[0]) == "q":
            return quit()
            self.running = False
        else:  # else just draw it
            self.draw_output(self.command)

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
