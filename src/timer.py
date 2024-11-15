import time

class Timer:   
        
    def __init__(self) -> None:
        self.running:      bool  = False
        self.start_time:   float = 0.0
        self.current_time: float = 0.0
        self.elapsed_time: float = 0.0
        self.was_reset:    bool  = False

    def start(self) -> None:
        self.start_time = time.time() - self.elapsed_time
        self.running    = True   
        self.was_reset  = False   

    def stop(self) -> None:
        self.running= False

    def reset(self) -> None:
        self.start_time   = 0.0
        self.current_time = 0.0
        self.elapsed_time = 0.0
        self.was_reset    = True

    def get_elapsed_time(self) -> int:
        self.update_timer()
        self.elapsed_time = int(self.current_time - self.start_time)
        return self.elapsed_time

    def update_timer(self) -> None:
        if self.running == True:            
            self.current_time = time.time()   
