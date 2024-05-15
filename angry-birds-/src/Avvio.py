import multiprocessing

def run_main():
    import Menu
    Menu.run()

def run_virtual_mouse():
    import VirtualMouse
    VirtualMouse.run()

if __name__ == '__main__':
    process1 = multiprocessing.Process(target=run_main)
    process2 = multiprocessing.Process(target=run_virtual_mouse)

    process1.start()
    process2.start()