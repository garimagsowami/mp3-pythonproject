from tkinter import *
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()

root.title("MP3 Player")
root.geometry("500x400")

#initialise pygame
pygame.mixer.init()

#create a function to deal with time
def play_time():

	#check to se if song is stopped
	if stopped:
		return()
	#grab current time of song
	current_time = pygame.mixer.music.get_pos()
	#cncert song to time to time format  
	converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))


	#reconstruct song with directory structure
	song = playlist_box.get(ACTIVE)
	song = f'C:/mp3/audio/{song}.mp3'

	#find current song length
	song_mut = MP3(song)
	global song_length
	song_length = song_mut.info.length
	#convert to time format
	converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
 
 	#check to see if song is over
	if int(song_slider.get()) == int(song_length):
		stop()

	elif paused == True:
		#check to see if paused is so -pass
		pass
	else:
		#move slider along 1sec at a time
		next_time = int(song_slider.get()) + 1
		#output new time value to slider
		song_slider.config(to=song_length, value=next_time)
		# convert slider postion to time format
		converted_current_time = time.strftime('%M:%S', time.gmtime(int(song_slider,get())))
			#output slider
		status_bar.config(text=f'Time Elapsed : {converted_current_time} of {converted_song_length}  ')

	#add current time to status bar
	if current_time > 0:
		status_bar.config(text=f'Time Elapsed :{converted_current_time} of {converted_song_length}  ')
	
	#create loop to check time every second
	status_bar.after(1000,play_time)



# create function to add one song to playlist
def add_song():
	song = filedialog.askopenfilename(initialdir='audio/',title="choose a song", filetypes=(("mp3 Files", "*.mp3"), ))
	#strip out directory structure and .mp3 
	song = song.replace("C:/mp3/audio/", "")
	song = song.replace(".mp3", "")
	#add to end of playlist
	playlist_box.insert(END, song)


#create function to add many songs to playlist
def add_many_songs():
	songs = filedialog.askopenfilenames(initialdir='audio/' ,title="choose many songs",filetype=(("mp3 Files","*.mp3"),))
	
	#loop thru song list and replace directory
	for song in songs:
		#strio out directory structure and mp3
		song = song.replace("C:/mp3/audio/", "")
		song = song.replace(".mp3", "")
		#add to end of playlist
		playlist_box.insert(END, song)


#create function to delete one song
def delete_song():
	#delete the highlighted song from playlist
	playlist_box.delete(ANCHOR)

#create function to delete all the songs
def delete_all_songs():
	#delete all songs
 	playlist_box.delete(0, END)

#create play function
def play():

	#set stopped to false since sonf is now playing
	global stopped
	stopped = False
	#reconstruct song with directory structure
	song = playlist_box.get(ACTIVE)
	song = f'C:/mp3/audio/{song}.mp3'
	#load song with pygame mixer
	pygame.mixer.music.load(song)
	#play song with pygame mixer
	pygame.mixer.music.play(loops=0)
	#get song time
	play_time()

#create stopped variable
global stopped
stopped = False
def stop():
	#stop the song
	pygame.mixer.music.stop()
	#clear playlist bar
	playlist_box.selection_clear(ACTIVE)
	status_bar.config(text='')

	#set out slider to zero
	song_slider.config(value=0)

	#set stop variable to true
	global stopped
	stopped = True




#create paused variable
global paused
paused = False

def pause(is_paused):
	global paused
	paused = is_paused

	if paused:
		#unpause
		pygame.mixer.music.unpause()
		paused = False
	else:
		pygame.mixer.music.pause()
		paused = True

#create play next song function
def next_song():
	#reset slider position and status bar
	status_bar.config(text='')
	song_slider.config(value=0)
	#get current song selected
	next_one = playlist_box.curselection()
	#add one to the current song
	next_one = next_one[0] + 1 

	#grab the song title from the playlist
	song = playlist_box.get(next_one)

	#add directory structure to play next song
	song = f'C:/mp3/audio/{song}.mp3'
	#load song with pygame
	pygame.mixer.music.load(song)
	#play song
	pygame.mixer.music.play(loops=0)

	#clear active bar in playlist
	playlist_box.selection_clear(0,END)
	#move active bar to next song
	playlist_box.activate(next_one)
	#set the active bar to next one
	playlist_box.selection_set(next_one,last=None)


#create function to play previous song
def previous_song():
	#reset slider position and status bar
	status_bar.config(text='')
	song_slider.config(value=0)
	#get current song selected
	next_one = playlist_box.curselection()
	#add one to the current song
	next_one = next_one[0] -  1 

	#grab the song title from the playlist
	song = playlist_box.get(next_one)

	#add directory structure to play next song
	song = f'C:/mp3/audio/{song}.mp3'
	#load song with pygame
	pygame.mixer.music.load(song)
	#play song
	pygame.mixer.music.play(loops=0)

	#clear active bar in playlist
	playlist_box.selection_clear(0,END)
	#move active bar to next song
	playlist_box.activate(next_one)
	#set the active bar to next one
	playlist_box.selection_set(next_one,last=None)


#create volume function

def volume(x):
	pygame.mixer.music.set_volume(volume_slider.get())

#create a slide function for song positioning
def slide(x):
	#reconstruct song with directory structure
	song = playlist_box.get(ACTIVE)
	song = f'C:/mp3/audio/{song}.mp3'
	#load song with pygame mixer
	pygame.mixer.music.load(song)
	#play song with pygame mixer
	pygame.mixer.music.play(loops=0, start=song_slider.get())
#create main frame
 
main_frame = Frame(root )
main_frame.pack(pady=20)

#create volume slider frame
volume_frame = LabelFrame(main_frame, text= "Volume",fg="red")
volume_frame.grid(row=0,column=1, padx=20, pady=10)


#create volume slider
volume_slider = ttk.Scale(volume_frame,from_=0,to=1, orient=VERTICAL,length=125,value=1,command=volume)
volume_slider.pack(pady=20)
#create song slider
song_slider = ttk.Scale(main_frame,from_=0,to=100, orient=HORIZONTAL,length=360,value=0,command=slide)
song_slider.grid(row=2,column=0,pady=20 )

#create playlist box
playlist_box = Listbox(main_frame, bg="black", fg="green", width=60, selectbackground="black", selectforeground="white")
playlist_box.grid(row=0,column=0)

#define button images for controls
back_btn_img = PhotoImage(file='images/back50.png')
forward_btn_img = PhotoImage(file='images/forward50.png')
play_btn_img = PhotoImage(file='images/play50.png')
pause_btn_img = PhotoImage(file='images/pause50.png')
stop_btn_img = PhotoImage(file='images/stop50.png')
#create button frame
control_frame = Frame(main_frame)
control_frame.grid(row=1,column=0,pady=20)


back_button = Button(control_frame, image=back_btn_img, borderwidth=0, command= previous_song)
forward_button = Button(control_frame, image=forward_btn_img, borderwidth=0 ,command= next_song)
play_button = Button(control_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button = Button(control_frame, image=pause_btn_img, borderwidth=0, command=lambda:pause(paused))
stop_button = Button(control_frame, image=stop_btn_img, borderwidth=0, command=stop)

back_button.grid(row=0,column=0, padx=1)
forward_button.grid(row=0,column=1, padx=1)
play_button.grid(row=0,column=2 ,padx=1)
pause_button.grid(row=0,column=3, padx=1)
stop_button.grid(row=0,column=4, padx=1)


#create menu
my_menu = Menu(root)
root.config(menu=my_menu)

#create add song menu dropdowns
add_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="songs", menu=add_song_menu)

#add one song to the playlist
add_song_menu.add_command(label="add one song to playlist",command=add_song)

#add many songs to playlist
add_song_menu.add_command(label="add many songs to playlist",command=add_many_songs)


#delete song menu
remove_song_menu = Menu(my_menu, tearoff=0)

my_menu.add_cascade(label="remove songs",menu=remove_song_menu)
#delete one song
remove_song_menu.add_command(label="delete song from playlist", command=delete_song)
#delete all songs
remove_song_menu.add_command(label="delete all songs from playlist", command=delete_all_songs)

#create status bar
status_bar = Label(root,text='', bd=1,relief=GROOVE, anchor=E)
status_bar.pack(fill=X,side=BOTTOM, ipady=2)


#temporary label
my_label = Label(root,text='')
my_label.pack(pady=20)




root.mainloop()