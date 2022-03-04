# Derived from : https://stackoverflow.com/questions/63395415/how-to-change-focus-to-pygame-window

def focus_window(title):
    ### TODO: make this work in general

    try:
        # noinspection PyPackageRequirements
        import win32gui

        def enum_windows(hwnd):
            windows.append((hwnd, win32gui.GetWindowText(hwnd)))

        windows = []
        win32gui.EnumWindows(enum_windows)
        for key, name, *others in windows:
            if name == title:
                win32gui.ShowWindow(key, 5)
                win32gui.SetForegroundWindow(key)
                return
        print('Window not found:', title)
    except Exception as e:
        print(e)
