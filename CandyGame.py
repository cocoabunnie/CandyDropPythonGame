#The Candy Drop Game

#This is a drop game that I made using Tkinter and Python for an internship
#The goal of the game is to use your left and right arrow keys to move the
#character left and right

#Catch the colorful candies to gain points!

#HOWEVER if you catch the red ones, you will lose points.

#When your score passes 20 points, you win!

#~~~~~~~~ IMPORTANT!! ~~~~~~~~~~~
#Please keep in mind that in order for this game to run in the Python IDLE, you also
#need the greenChar.gif file in the same folder as the CandyGame.py file

from tkinter import *
import random

#creating a window and a title
window = Tk()
window.title('The Candy Monster Game')

#creating a canvas so we can put objects on the screen (objects like the monster image and the shapes/candies that fall from the sky)
canvas = Canvas(window, width=400, height=400, bg='black')
canvas.pack()

#This is the welcome screen where the player will get the title and the instructions on what to do.
#this is displayed for 3 seconds, and then the game starts
title = canvas.create_text(200,200, text='The Candy Monster', fill='white', \
font=('Helvetica', 30))

directions = canvas.create_text(200,275, text='Collect candy but avoid \
the red ones', fill='white', font=('Helvetica', 15))

#add label to display the score
scoreadd = 1
score = 0
score_display = Label(window, text="Score :" + str(score))
score_display.pack()

#add label to display the level
level = 1
level_display = Label(window,text="Level :" + str(level))
level_display.pack()

#creating an image object (the green monster) using a file saved to computer
player_image = PhotoImage(file='greenChar.gif') #<-- IMPORTANT make sure this greenChar.gif file is saved in the same folder at this python file or it will CRASH
mychar = canvas.create_image(200,360, image=player_image)

#variables and lists needed for managing candy
candy_list = [] #list containing all candy created, empty at start
bad_candy_list = [] #list containing all bad candy created, empty at start
candy_speed = 5 #initial speed of falling candy
candy_color_list = ['red', 'yellow', 'green', 'purple', 'pink', 'white']

#function to make candy at random places
def make_candy():
    #pick a random x position
    xposition = random.randint(1,400)
    #pick a random color
    candy_color = random.choice(candy_color_list)
    #create a candy of size 30 at random position and color
    candy = canvas.create_oval(xposition, 0, xposition+30, 30, fill= candy_color)
    #add candy to list
    candy_list.append(candy)
    #if color of candy is red - add it to bad_candy_list
    if candy_color == 'red':
        bad_candy_list.append(candy)
    #schedule this function to make candy again
    window.after(1000, make_candy)

#function moves candy downwards, and schedules call to move_candy
def move_candy():
    #loop through list of candy and change y position
    for candy in candy_list:
        canvas.move(candy, 0, candy_speed)
        #check if end of screen - restart at random position
        if canvas.coords(candy)[1] > 400:
            xposition = random.randint(1,400)
            canvas.coords(candy,xposition, 0, xposition+30, 30)
    #schedule this function to move candy again
    window.after(50, move_candy)

#destroys the instructions on the screen (to start the game)
def end_title():
    canvas.delete(title)
    canvas.delete(directions)
    
#function to update score
def update_score():
    global score, level, candy_speed, scoreadd #use of global since variables are changed
    score = score + scoreadd
    score_display.config(text="Score :" + str(score))

#changes the level by one every 5 points the user gets
#once the user gets 20 points, it destroys the window and ends the game.
    if score > 5 and score <= 10:
        candy_speed = 10
        level = 2
        level_display.config(text="Level :" + str(level))
    elif score > 11 and score <= 20:
        candy_speed = 15
        level = 3
        level_display.config(text="Level :" + str(level))
    elif score > 20:
        window.destroy() #end the game when the user hits 20 points


# check distance between 2 objects and return true if they are touching. This is to keep track of when the monster collects the candy
def collision(item1, item2, distance):
    xdistance = abs(canvas.coords(item1)[0] - canvas.coords(item2)[0])
    ydistance = abs(canvas.coords(item1)[1] - canvas.coords(item2)[1])
    overlap = xdistance < distance and ydistance < distance
    return overlap

# define function check_hits to see if character and candy collided
# if character collides with candy in candy_list, the program deletes it (character "eats" it) and update score
def check_hits():
    global scoreadd
    
    for candy in candy_list:
        if collision(mychar, candy, 30):
            canvas.delete(candy)
            candy_list.remove(candy)

            if candy in bad_candy_list:
                scoreadd = -1 #take away a point if it's bad candy (red)
            else:
                scoreadd = 1 #add point if its a good candy 
            
            update_score()
    window.after(100, check_hits) #schedule check_hits again

#tracks which direction player is moving
move_direction = 0

#function handles when user presses arrow keys (you can only use left and right arrows
def check_press(event): 
    global move_direction
    key = event.keysym
    if key == "Right":
        move_direction = "Right"
    if key == "Left":
        move_direction = "Left"

#function handles when user stops pressing arrow keys
def end_press(event):
    global move_direction
    move_direction = "None"

#this function keeps the character from moving off screen
def move_character():
    if move_direction == "Right" and canvas.coords(mychar)[0] < 400:
        canvas.move(mychar, 10, 0)
    if move_direction == "Left" and canvas.coords(mychar)[0] > 0:
        canvas.move(mychar, -10, 0)
    window.after(16, move_character) #move char at 60 frames per second

#binding the keyboard to the game so the user can use them to move the character
canvas.bind_all('<KeyPress>', check_press)
canvas.bind_all('<KeyRelease>', end_press)
    
#start game loop by scheduling all functions here:
window.after(3000, end_title)
window.after(3000, make_candy)
window.after(3000, move_candy)
window.after(3000, check_hits)
window.after(3000, move_character) #handle keyboard controls

window.mainloop()








