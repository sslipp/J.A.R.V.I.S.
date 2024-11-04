from pynput import mouse

def on_mouse_click(x, y, button, pressed):
    if button == mouse.Button.left and pressed:
        print(f'X:{x} Y:{y}')

listener = mouse.Listener(on_click=on_mouse_click)
listener.start()
listener.join()