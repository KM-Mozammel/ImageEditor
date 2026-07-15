from ui.window import ImageEditor

app = ImageEditor()
app.run()
# app.run() call হয়; ভিতরে self.window.mainloop() run হয়। 
# এটাই Tkinter Event Loop। এখন program আর নিচে নামে না। এটা continuously অপেক্ষা করে।

#while True:
#    keyboard event?
#    mouse event?
#    button click?
#    slider moved?
#    window resized?
#    redraw?