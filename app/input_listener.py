from pynput import keyboard


def start_keyboard_listener(signals):
    def on_press(key):
        if key == keyboard.Key.tab:
            signals.show_overlay.emit()

    def on_release(key):
        if key == keyboard.Key.tab:
            signals.hide_overlay.emit()

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
