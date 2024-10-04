import time


class Timer:   
        
    def __init__(self):
        self.running: bool = False
        self.start_time: float   = 0.0
        self.current_time: float = 0.0
        self.elapsed_time: float = 0.0

    def start(self):
        self.start_time = time.time()
        self.running = True        

    def stop(self):
        self.running= False

    def reset(self):
        self.current_time = 0.0

    def get_elapsed_time(self):
        self.update_timer()
        self.elapsed_time = self.current_time - self.start_time
        return round(self.elapsed_time)

    def update_timer(self):
        if self.running == True:            
            self.current_time = time.time()
            
            
 #use tkinter after() method to delay the update in gui this keeps ui responsive

 