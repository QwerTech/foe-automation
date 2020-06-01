import logging
import re
from time import sleep

import win32com.client
import win32con
import win32gui

shell = win32com.client.Dispatch("WScript.Shell")
shell.SendKeys('%')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(threadName)s:%(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""

    def __init__(self):
        """Constructor"""
        self._handles = []

    def find_window(self, class_name, window_name=None):
        """find a window by its class_name"""
        self._handles = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        title = str(win32gui.GetWindowText(hwnd))
        if re.match(wildcard, title) is not None:
            logging.info("Found %s: %s", title, hwnd)
            self._handles.append(hwnd)

    def find_window_wildcard(self, wildcard):
        """find a window whose title matches the wildcard regex"""
        self._handles = []
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        """put the window in the foreground"""
        for window in self._handles:
            sleep(3)
            logging.info("activation %s", window)
            win32gui.SetForegroundWindow(window)
            win32gui.SetActiveWindow(window)
            win32gui.ShowWindow(window, win32con.SW_SHOW)


w = WindowMgr()
w.find_window_wildcard(".*Forge of Empires.*")
w.set_foreground()
