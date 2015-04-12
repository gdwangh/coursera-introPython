# template for "Stopwatch: The Game"
import simplegui

# define global variables
counter = 0
stop_time = 0
suc_time = 0
is_run = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    #pass
    int_D = t % 10
    int_BC = t // 10
    if int_BC >= 60:
        int_A = int_BC//60
        int_BC = int_BC % 60
    else:
        int_A = 0
    
    if int_BC < 10:
        ft = str(int_A)+":0"+str(int_BC)+"."+str(int_D)
    else:
        ft = str(int_A)+":"+str(int_BC)+"."+str(int_D)
    
    return ft

# define event handlers for buttons; "Start", "Stop", "Reset"
def start_handler():
    timer.start()
    
    global is_run
    is_run = True

def stop_handler():
    timer.stop()
    
    global stop_time, suc_time
    global is_run
    if is_run == True:
        is_run = False
        stop_time+=1
        if counter%10 == 0: 
            suc_time += 1
        
    
def reset_handler():
    global counter, stop_time, suc_time, is_run
    timer.stop()
    is_run = False
    counter = 0
    stop_time = 0
    suc_time = 0

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global counter
    counter += 1
    
# define draw handler
def draw_handler(canvas):
    canvas.draw_text(format(counter), [100,150], 30, "White")
    canvas.draw_text(str(suc_time)+"/"+str(stop_time), [260,15],15, "White")
    
# create frame
frame = simplegui.create_frame("Stopwatch", 300, 300)

# register event handlers
timer = simplegui.create_timer(100, timer_handler)
frame.set_draw_handler(draw_handler)
frame.add_button("Start", start_handler, 100)
frame.add_button("Stop", stop_handler, 100)
frame.add_button("Reset", reset_handler,100)

# start frame
frame.start()

# Please remember to review the grading rubric
