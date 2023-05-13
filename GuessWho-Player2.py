
# -*- coding: utf-8 -*-
"""
Created on Wednesday 22 March 10:31:41 2023

@author: Julie
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import imageio.v2 as imageio
import imageio
import os
import pygame, sys
from button import Button
import matplotlib.patches as patches
import time
from datetime import datetime

def listdir_nohidden(path):
    files = os.listdir(path)
    for f in files:
        if f.startswith('.'):
            files.remove(f)
    return files

def get_names(files):
    names = []
    for f in files:
        names.append(f.split('.')[0])
    return names

####################### GAME BOARD ##########################

now = datetime.now()
start_hour_game = now.strftime("%Y-%m-%d_%Hh%Mm%Ss")


def game_board(args_dict):
    mpl.rcParams['mathtext.fontset'] = 'cm'
    mpl.rcParams['mathtext.rm'] = 'serif'
    mpl.rcParams['savefig.dpi'] = 300       # Number of dpi of saved figures
    mpl.rcParams['font.size'] = 12
    mpl.rcParams['axes.formatter.limits'] = (-3, 3)
    mpl.rcParams['axes.formatter.use_mathtext'] = True
    mpl.rcParams['toolbar'] = 'None'        # Remove toolbar

    mpl.rcParams['font.family'] = 'STIXGeneral'
    mpl.rcParams['mathtext.rm'] = 'Bitstream Vera Sans'
    mpl.rcParams['mathtext.it'] = 'Bitstream Vera Sans:italic'
    mpl.rcParams['mathtext.bf'] = 'Bitstream Vera Sans:bold'


    colorOff = 'crimson'
    colorOn = 'Navy'

    pathImages = 'assets/Images/'

    files = listdir_nohidden(pathImages)
    names = get_names(files)

    figZoom = None # Global variable to control zoom figure
    
    start_time = time.time()
    time_since_last = 0
    
    index_to_guess = args_dict["index_to_guess"]
    current_guess = args_dict["current_guess"]
    path_clues_complete = args_dict["path_clues_complete"]
    indexClue = args_dict["indexClue"]
    to_guess = args_dict["to_guess"]
    n_to_guess = args_dict["n_to_guess"]
    random_index = args_dict["random_index"]
    start_hour_game = args_dict["start_hour_game"]
    mode = args_dict["mode"]
    start_time = args_dict["start_time"]
    time_since_last = args_dict["time_since_last"]


    # Load all images with names
    images = []
    clicked_character = []
    

    for (i,n) in enumerate(names):
        fileImg = pathImages + n + '.png'
        try:
            im = imageio.v2.imread(fileImg)
            images.append(im)
            
        except:
            print('File {:s} not found'.format(fileImg))
            im = np.random.randn(100, 100)  # Fake image
            images.append(im)
            
    nx = 6
    ny = 5
    

    isOn = np.ones(len(names))  # Table storing the state of the ith axis

    
    fig, axs = plt.subplots(ny, nx, figsize=(14,12))
    
    # ========================================== BG
    # create rectangles for the background
    c1 = (250/255, 234/255, 177/255)
    c2 = (250/255, 248/255, 241/255) 
    upper_bg = patches.Rectangle((-0.01, 0.81), width=1.02, height=0.20, 
                                 transform=fig.transFigure,      # use figure coordinates
                                 facecolor=c1,                   # define color
                                 edgecolor='#C58940',                  # remove edges
                                 lw=5,
                                 zorder=-10)                     # send it to the background
    lower_bg = patches.Rectangle((0, 0), width=1, height=0.81, 
                                 transform=fig.transFigure,      # use figure coordinates
                                 facecolor=c2,                   # define color
                                 edgecolor='None',               # remove edges
                                 zorder=-10)                     # send it to the background
    
    # add rectangles to the figure
    fig.patches.extend([upper_bg, lower_bg])
    # ==========================================
    
    manager = plt.get_current_fig_manager()
    manager.window.setWindowTitle("Loading...")
    plt.tight_layout()
    #plt.subplots_adjust(hspace=0.6)

    #Add circle to the bottom center of the figure
    ax_clue = fig.add_subplot(nx, ny, nx*ny)
    ax_clue.set_position([(nx-1)/(2*nx), (ny+3.35)/(2*ny), .14, .14])     # Set ny - 4.75 to put it below the board
    ax_clue.set_facecolor('none')  # Make the axis background transparent
    ax_clue.set_xticks([])  # Remove x ticks
    ax_clue.set_yticks([])  # Remove y ticks
    ax_clue.spines['bottom'].set_color('#C58940') # Change clue border color
    ax_clue.spines['bottom'].set_linewidth(2)
    ax_clue.spines['top'].set_color('#C58940') # Change clue border color
    ax_clue.spines['top'].set_linewidth(2)
    ax_clue.spines['left'].set_color('#C58940') # Change clue border color
    ax_clue.spines['left'].set_linewidth(2)
    ax_clue.spines['right'].set_color('#C58940') # Change clue border color
    ax_clue.spines['right'].set_linewidth(2) 
    
    
    # Custom previous clue button
    ax_previous_clue = fig.add_subplot(nx, ny, nx*ny)
    ax_previous_clue.set_position([(nx-4)/(2*nx), (ny+3.35)/(2*ny), .14, .14])    
    ax_previous_clue.set_facecolor('none')
    ax_previous_clue.set_xticks([])  
    ax_previous_clue.set_yticks([])
    ax_previous_clue.spines.clear()
    im_previous = imageio.v2.imread("assets/return.png")
    im_previous_clue = ax_previous_clue.imshow(im_previous)
    
    
    # Custom next clue button
    ax_next_clue = fig.add_subplot(nx, ny, nx*ny)
    ax_next_clue.set_position([(nx+2)/(2*nx), (ny+3.35)/(2*ny), .14, .14])    
    ax_next_clue.set_facecolor('none')
    ax_next_clue.set_xticks([])  
    ax_next_clue.set_yticks([])
    ax_next_clue.spines.clear()
    im_next = imageio.v2.imread("assets/clue_button.png")
    im_next_clue = ax_next_clue.imshow(im_next)
    

    # Comment this loop if indices are shown below the board    
    for (i, a) in enumerate(axs.ravel()[0:nx]):
        a.set_axis_off()
            
    ax_imgs = []
    all_crosses = []
   
    for (i, a) in enumerate(axs.ravel()[nx::]):
        a.set_axis_off()
        if i < len(names):
            #a.set_title(names[i], color=colorOn)  # Comment if you want to remove names above images
            ax_imgs.append(a.imshow(images[i], alpha=1))
            
            cross = a.scatter(0.5, 0.5, s=4000, c='crimson', 
                                   transform=a.transAxes, 
                                   marker='X', clip_on=False)
            cross.set_alpha(0.0)
            all_crosses.append(cross)
    
    def onclick(event):
        '''
        Event handler for button_press_event
        @param event MouseEvent
        '''
        global figZoom
        global index_to_guess
        global start_time
        global good_answer
        global bad_answer 
        global time_since_last
        global start_hour_game
        
        # Close figZoom figure
        try:
            plt.close(figZoom)
        except:
            nothing = 1
        
        
        current_guess = to_guess[random_index[index_to_guess]]
        
        # Click on clues
        if event.button == 1:
            if event.inaxes == ax_previous_clue:
                global indexClue
                indexClue -= 1
                try:
                    for i in range(n_to_guess):
                        im_clue = imageio.v2.imread(path_clues_complete+current_guess+'/clue{:d}.png'.format(indexClue))
                        im = ax_clue.imshow(im_clue)
                        plt.draw()
                        fig.canvas.flush_events()
                        break
                except:
                    nothing=1
                    
            if event.inaxes == ax_next_clue:
                indexClue += 1       
                try:
                    for i in range(n_to_guess):
                        im_clue = imageio.v2.imread(path_clues_complete+current_guess+'/clue{:d}.png'.format(indexClue))
                        im = ax_clue.imshow(im_clue)
                        plt.draw()
                        fig.canvas.flush_events()
                        break
                except:
                    nothing=1
                        
                        

            for i, ax in enumerate(axs.ravel()[nx::]): # Remove [nx::] if want clues below the board
                # For infomation, print which axes the click was in
                if ax == event.inaxes:
                    if isOn[i] == 1:  # If the axis is on
                        #print('Click is in axes ax{}'.format(i+1))
                        #ax.set_title(names[i], color=colorOff)  # Comment if you want to remove names above images
                        ax_imgs[i].set_alpha(0.2)
                        all_crosses[i].set_alpha(1)
                        plt.draw()
                        
                        clicked_character.append(names[i])
                        isOn[i] = 0   
                    
                     
                    else:   # If axis is off, reshow it
                        #print('Click is in axes ax{}'.format(i+1))
                        #ax.set_title(names[i], color=colorOn) # Comment if you want to remove names above images
                        ax_imgs[i].set_alpha(1)
                        all_crosses[i].set_alpha(0)
                        plt.draw()
                        fig.canvas.flush_events()

                        clicked_character.remove(names[i])

                        isOn[i] = 1

                    #print(np.sum(isOn))
                    break
                
        if event.button == 3:
            for i, ax in enumerate(axs.ravel()[nx::]):  # Remove [nx::] if want clues below the board
                # For infomation, print which axes the click was in
                if ax == event.inaxes:
                    figZoom, ax = plt.subplots(figsize=(8,8))
                    figZoom.tight_layout()
                    ax.imshow(images[i])
                    ax.set_axis_off()
                    manager = plt.get_current_fig_manager()
                    manager.window.setWindowTitle(names[i])
                    break

                              
        removed_characters = clicked_character
        
        
        # Display right character with colors in function of the remaining character on the gameboard
        if np.sum(isOn) == 1:
            reinitialise_board()
            new_character()
            if current_guess not in removed_characters:
                clicked_character.clear()
                # Open a new window with the correct character
                figWin, ax = plt.subplots(figsize=(10,10))
                figWin.tight_layout()
                #figWin.set_facecolor('green') # Change full bg color in matplotlib window
                manager = plt.get_current_fig_manager()
                manager.window.setWindowTitle(current_guess)
                im_character = imageio.v2.imread(path_clues_complete+current_guess+'/right_solution.png')
                ax.imshow(im_character)
                ax.set_axis_off()
                plt.pause(4)
                plt.close(figWin)
                
                good_answer += 1
                end_time = time.time()

                time_since_last = (end_time - start_time) - time_since_last 
                correct = 1
                elapsed_time = end_time - start_time                        
                 
                
                performance = open("./Tests/performance_"+ mode + "_" + start_hour_game + ".txt", "a+")
                performance.write('\n' + 'Character:{}, Duration:{:.3f}, Correct:{}, Total good answers:{}, Total bad answers:{}, Elapsed time session:{:.3f}'.format(current_guess, time_since_last, correct, good_answer, bad_answer, elapsed_time))
                performance.close()
                
                                
            else:
                clicked_character.clear()
                figDefeat, ax = plt.subplots(figsize=(10,10))
                figDefeat.tight_layout()
                manager = plt.get_current_fig_manager()
                manager.window.setWindowTitle(current_guess)
                im_character = imageio.v2.imread(path_clues_complete+current_guess+'/wrong_solution.png')
                ax.imshow(im_character)
                ax.set_axis_off()
                plt.pause(4)
                plt.close(figDefeat)

                bad_answer += 1
                end_time = time.time()
                
                time_since_last = (end_time - start_time) - time_since_last 
                correct = 0
                elapsed_time = end_time - start_time
            
                
                performance = open("./Tests/performance_"+ mode + "_" + start_hour_game + ".txt", "a+")
                performance.write('\n' + 'Character:{}, Duration:{:.3f}, Correct:{}, Total good answers:{}, Total bad answers:{}, Elapsed time session:{:.3f}'.format(current_guess, time_since_last, correct, good_answer, bad_answer, elapsed_time))
                performance.close()
                clicked_character.clear()

                                


    def reinitialise_board():
        for (i, a) in enumerate(axs.ravel()[nx::]): # Remove [nx::] if want clues below the board
            #a.set_title(names[i], color=colorOn) # Comment if you want to remove names above images
            ax_imgs[i].set_alpha(1.0)
            all_crosses[i].set_alpha(0.0)
            isOn[i] = 1
        return
     

    def new_character():
        global indexClue
        global index_to_guess
        index_to_guess += 1
        indexClue = 1

            
        if index_to_guess == n_to_guess:  
            plt.close(fig)
            
        else: 
            current_guess = to_guess[random_index[index_to_guess]]
            #clicked_character.clear()
            
            im_clue = imageio.v2.imread(path_clues_complete+current_guess+'/clue1.png')
            im = ax_clue.imshow(im_clue)

       
            
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    

    return ax_clue

    

####################### TRAINING ############################

mode = '' 
path_clues = './assets/Clues/'
path_clues_complete = ''
index_to_guess = 0
current_guess = ''
indexClue = 1
seed = 45
time_since_last = 0
start_time = time.time()
wait_till_next_participant = True
show_again = False



def training():    
    global good_answer
    global bad_answer

    mode = "Training"
    good_answer = 0
    bad_answer = 0 
    
    np.random.seed(seed)

    path_clues_complete = path_clues + mode +'/'

    if os.path.isfile(path_clues_complete+'.DS_Store'):    
        os.remove(path_clues_complete+'.DS_Store')
        
    to_guess = os.listdir(path_clues_complete)
    n_to_guess = len(to_guess)
    random_index = np.random.choice(np.arange(0, n_to_guess), 
                                             n_to_guess, replace=False)
    
    current_guess = to_guess[random_index[index_to_guess]]

    args_dict = {"index_to_guess":index_to_guess, 
                 "current_guess":current_guess,
                 "path_clues_complete":path_clues_complete,
                 "indexClue":indexClue,
                 "to_guess": to_guess,
                 "n_to_guess": n_to_guess,
                 "random_index": random_index,
                 "start_hour_game": start_hour_game,
                 "mode": mode,
                 "start_time": start_time,
                 "time_since_last": time_since_last,
                 }
        
    ax_clue = game_board(args_dict)
    manager = plt.get_current_fig_manager()
    manager.window.setWindowTitle("Entraînement")
        
    im_clue = imageio.v2.imread(path_clues_complete+current_guess+'/clue1.png')
    im = ax_clue.imshow(im_clue)
        

####################### SOLO ###############################



def solo():
    global good_answer
    global bad_answer
    global indexClue 
    global index_to_guess
    
    indexClue = 1

    mode = "Solo"
    good_answer = 0
    bad_answer = 0 
    
    
    np.random.seed(seed)

    index_to_guess = 0
    path_clues_complete = path_clues + 'Solo/'

    if os.path.isfile(path_clues_complete+'.DS_Store'):    
        os.remove(path_clues_complete+'.DS_Store')
            
    to_guess = os.listdir(path_clues_complete)
    n_to_guess = len(to_guess)
    random_index = np.random.choice(np.arange(0, n_to_guess), 
                                             n_to_guess, replace=False)
    
    current_guess = to_guess[random_index[index_to_guess]]
        
    args_dict = {"index_to_guess":index_to_guess, 
                 "current_guess":current_guess,
                 "path_clues_complete":path_clues_complete,
                 "indexClue":indexClue,
                 "to_guess": to_guess,
                 "n_to_guess": n_to_guess,
                 "random_index": random_index,
                 "start_hour_game": start_hour_game,
                 "mode": mode,
                 "start_time": start_time,
                 "time_since_last": time_since_last,
                 "good_answer": good_answer,
                 "bad_answer": bad_answer,
                 }
    
    print(indexClue)
    print(current_guess)
    print(path_clues_complete)
    
    ax_clue = game_board(args_dict)
    manager = plt.get_current_fig_manager()
    manager.window.setWindowTitle("Solo")
        
    im_clue = imageio.v2.imread(path_clues_complete+current_guess+'/clue1.png')
    im = ax_clue.imshow(im_clue)
    

####################### PLAYER 1 ###############################



def player1():
    global good_answer
    global bad_answer
    global indexClue 
    global index_to_guess
    
    indexClue = 1

    mode = "Player1"
    good_answer = 0
    bad_answer = 0 
    
    np.random.seed(seed)

    index_to_guess = 0
    path_clues_complete = path_clues + 'Player 1/'

    if os.path.isfile(path_clues_complete+'.DS_Store'):    
        os.remove(path_clues_complete+'.DS_Store')
            
            
    to_guess = os.listdir(path_clues_complete)
    n_to_guess = len(to_guess)
    random_index = np.random.choice(np.arange(0, n_to_guess), 
                                             n_to_guess, replace=False)

    current_guess = to_guess[random_index[index_to_guess]]
        
    args_dict = {"index_to_guess":index_to_guess, 
                 "current_guess":current_guess,
                 "path_clues_complete":path_clues_complete,
                 "indexClue":indexClue,
                 "to_guess": to_guess,
                 "n_to_guess": n_to_guess,
                 "random_index": random_index,
                 "start_hour_game": start_hour_game,
                 "mode": mode,
                 "start_time": start_time,
                 "time_since_last": time_since_last,
                 "good_answer": good_answer,
                 "bad_answer": bad_answer,
                 "show_again":show_again,
                 }
        
    ax_clue = game_board(args_dict)
    manager = plt.get_current_fig_manager()
    manager.window.setWindowTitle("Joueur 1")
        
    im_clue = imageio.v2.imread(path_clues_complete+current_guess+'/clue1.png')
    im = ax_clue.imshow(im_clue)
    
    
    
####################### PLAYER 2 ###############################


def player2():    
    global good_answer
    global bad_answer
    global indexClue 
    global index_to_guess
    
    indexClue = 1
    
        
    mode = "Player2"
    good_answer = 0
    bad_answer = 0 
    
    np.random.seed(seed)

    path_clues_complete = path_clues + 'Player 2/'

    if os.path.isfile(path_clues_complete+'.DS_Store'):    
        os.remove(path_clues_complete+'.DS_Store')
        
    to_guess = os.listdir(path_clues_complete)
    n_to_guess = len(to_guess)
    random_index = np.random.choice(np.arange(0, n_to_guess), 
                                             n_to_guess, replace=False)

    
    current_guess = to_guess[random_index[index_to_guess]]
        
    args_dict = {"index_to_guess":index_to_guess, 
                 "current_guess":current_guess,
                 "path_clues_complete":path_clues_complete,
                 "indexClue":indexClue,
                 "to_guess": to_guess,
                 "n_to_guess": n_to_guess,
                 "random_index": random_index,
                 "start_hour_game": start_hour_game,
                 "mode": mode,
                 "start_time": start_time,
                 "time_since_last": time_since_last,
                 "good_answer": good_answer,
                 "bad_answer": bad_answer,
                 }
    
    ax_clue = game_board(args_dict)
    manager = plt.get_current_fig_manager()
    manager.window.setWindowTitle("Joueur 2")
        
    im_clue = imageio.v2.imread(path_clues_complete+current_guess+'/clue1.png')
    im = ax_clue.imshow(im_clue)
    
        
####################### MENU ###################################
    

def menu_screen():
    # Initialize pygame
    pygame.init()
    
    size = (1655,930) #(1655, 930)
    SCREEN = pygame.display.set_mode(size) # add .pygame.RESIZABLE if you want to resize the menu window
    pygame.display.set_caption("Qui est-ce ?")

    BG = pygame.image.load("assets/Background_Disney.png")
    

    programIcon = pygame.image.load('assets/icon.png')
    
    pygame.display.set_icon(programIcon)


    def get_font(size): # Returns Press-Start-2P in the desired size
        return pygame.font.Font("assets/font_main_menu.otf", size)

    def get_font2(size): # Returns Press-Start-2P in the desired size
        return pygame.font.Font("assets/font_modes.otf", size)       
    
    while True:
            SCREEN.blit(BG, (0, 0))
    
            MENU_MOUSE_POS = pygame.mouse.get_pos()
    
            MENU_TEXT = get_font(100).render("Menu principal", True, "white")
            MENU_RECT = MENU_TEXT.get_rect(center=(827.5, 270))
    
            TRAINING_BUTTON = Button(image=None, pos=(827.5, 400), 
                                text_input="Entraînement", font=get_font2(70), base_color="white", hovering_color="#E6B325") # 827.5 pour background disney
            SOLO_BUTTON = Button(image=None, pos=(827.5, 500), 
                                text_input="Solo", font=get_font2(70), base_color="white", hovering_color="#E6B325")
            MULTIJOUEUR_BUTTON = Button(image=None, pos=(827.5, 600),
                                text_input="Multijoueur", font=get_font2(70), base_color="white", hovering_color="#E6B325")
            QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(827.5, 750), 
                                text_input="QUITTER", font=get_font2(75), base_color="White", hovering_color="Red")
    
            SCREEN.blit(MENU_TEXT, MENU_RECT)

            for button in [TRAINING_BUTTON, SOLO_BUTTON, MULTIJOUEUR_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(SCREEN)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if TRAINING_BUTTON.checkForInput(MENU_MOUSE_POS):
                        training()
                            
                            
                    if SOLO_BUTTON.checkForInput(MENU_MOUSE_POS):
                        solo()
                          
                        
                    if MULTIJOUEUR_BUTTON.checkForInput(MENU_MOUSE_POS):
                        player2()


                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()
                        
            pygame.display.update()

menu_screen()