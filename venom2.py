#!/usr/bin/python3

from API import ui
import threading


# UI code here #
def draw_ui(output):
    u.draw_top_line()
    u.draw_bottom_line()
    u.draw_output(output)
    u.scr.clear()
    u.scr.refresh()


# UI code ends #

# main loop code here #
def main(output):
    thread1 = threading.Thread(target=u.get_user_input())
    thread2 = threading.Thread(target=draw_ui(output))
    thread1.start()
    thread2.start()
    while running is True:
        try:
            u.scr.clear()
            u.draw_top_line()
            u.draw_bottom_line()
            u.draw_output(output)
            u.scr.refresh()
        except KeyboardInterrupt:
            u.die()
    u.die()


# main loop code ends #
# main program code here #
if __name__ == "__main__":
    running = True
    output = ['']
    u = ui.UI(output)
    main(output)
