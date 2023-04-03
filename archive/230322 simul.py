# ----------------------------------------------------------- #
#         SELF-STEERING BOAT AND CURRENTS SIMULATION          #
#  ©2023 Mathurin Roulier, PTSI Lycée Lesage, Vannes, France  #
# ----------------------------------------------------------- #

# ----------------------------------------------------------- #
#                       Import modules                        #
# ----------------------------------------------------------- #
import matplotlib.pyplot as plt
import numpy as np
import random as rd
from display import *

plt.ion()                                                                       # Interactive mode

# ----------------------------------------------------------- #
#                   Currents parameters                       #
# ----------------------------------------------------------- #

size = (160,90)                                                                 # Size of the map (X, Y)
dispersion = 0.3                                                                # Dispersion of currents
vmax = .7                                                                       # Max current speed

dispermin = 1 - dispersion
dispermax = 1 + dispersion

X_current, Y_current = np.meshgrid(np.arange(size[0]), np.arange(size[1]))      # Meshgrid for currents
currents_map = np.ones((2,size[1],size[0]))                                     # Currents map (composante, X, Y)
currents_map[:,0,0] = 1                                                         # Initial current at the bottom left

print(f"Currents max step : {round(vmax,2)} m/s")                               # Print currents max speed

# ----------------------------------------------------------- #
#                  Generate random currents                   #
# ----------------------------------------------------------- #
for i in range(1,size[1]-1):                                                    # Generate currents - line by line
    for j in range(1,size[0]-1):                                                # Generate currents - column by column
        currents_map[0,i+1,j+1] = np.average([currents_map[0,i,j] * rd.uniform(dispermin, dispermax), currents_map[0,i+1,j] * rd.uniform(dispermin, dispermax), currents_map[0,i,j+1] * rd.uniform(dispermin, dispermax)])      # Average of the currents at the bottom, left and bottom left - X component
        currents_map[1,i+1,j+1] = np.average([currents_map[1,i,j] * rd.uniform(dispermin, dispermax), currents_map[1,i+1,j] * rd.uniform(dispermin, dispermax), currents_map[1,i,j+1] * rd.uniform(dispermin, dispermax)])      # Average of the currents at the bottom, left and bottom left - Y component

currents_map[:,0,:] = currents_map[:,1,:]                                       # Set currents at the bottom as the currents just above
currents_map[:,:,-1] = currents_map[:,:,-2]                                     # Set currents at the left as the currents just right
currents_map[:,:,:] = currents_map[:,:,:] / np.max(currents_map[:,:,:]) * vmax  # Normalize currents to vmax

# ----------------------------------------------------------- #
#                       Boat parameters                       #
# ----------------------------------------------------------- #
start_pos = (5,size[1]//2-5)                                                    # Initial position of the boat
goal_pos = (size[0]-5, size[1]//2-5)                                            # Goal position of the boat

ini_dir = np.arctan((goal_pos[1]-start_pos[1])/(goal_pos[0]-start_pos[0]))      # Initial direction of the boat
print(f"Initial heading : {round(360 - ini_dir/np.pi*180,1)}°")                 # Print initial heading

drift = 1                                                                       # Drift coefficient
step = 1                                                                        # Simulation step


# ----------------------------------------------------------- #
#                   Boat movement - Inert                     #
#                No movement, just drifting                   #
# ----------------------------------------------------------- #

boat_pos_inert = np.array([[start_pos[0]], [start_pos[1]]])

i = 0
ini_dir = np.pi / 2
# Repeat while boat is inside the plot or far from the goal
while (0 <= int(boat_pos_inert[0, -1:]) < size[0]) and (0 <= int(boat_pos_inert[1, -1:]) < size[1]) and (np.sqrt((boat_pos_inert[0, -1:]-goal_pos[0])**2 + (boat_pos_inert[1, -1:]-goal_pos[1])**2) > 1):
    # Append to boat_pos array the future position : last + current drift
    boat_pos_inert = np.append(boat_pos_inert,
                        boat_pos_inert[:,-1:] \
                            + currents_map[:, int(boat_pos_inert[0,i:i+1]), int(boat_pos_inert[1,i:i+1])] * drift,
                        axis=1)
    i+=1

# ----------------------------------------------------------- #
#                  Boat movement - Model 1                    #
#         The boat just follow the initial heading            #
# ----------------------------------------------------------- #
boat_pos = np.array([[start_pos[0]], [start_pos[1]]])                           # Boat position array with initial position

i = 0
ini_dir = np.pi / 2                                                             # Initial direction
# Repeat while boat is inside the plot or far from the goal
while (0 <= int(boat_pos[0, -1:]) < size[0]) and (0 <= int(boat_pos[1, -1:]) < size[1]) and (np.sqrt((boat_pos[0, -1:]-goal_pos[0])**2 + (boat_pos[1, -1:]-goal_pos[1])**2) > 1):
    # Append to boat_pos array the future position : last + current drift + initial heading
    boat_pos = np.append(boat_pos,
                        boat_pos[:,-1:] \
                            + currents_map[:, int(boat_pos[0,i:i+1]), int(boat_pos[1,i:i+1])] * drift \
                            + step * np.array([[np.sin(ini_dir)], [np.cos(ini_dir)]]),
                        axis=1)
    i+=1

# ----------------------------------------------------------- #
#                  Boat movement - Model 2                    #
#         The boat follow the direction to the goal           #
# ----------------------------------------------------------- #
boat_pos2 = np.array([[start_pos[0]], [start_pos[1]]])                          # Boat position array
i         = 0

# Repeat while boat is inside the plot or far from the goal
while (0 <= int(boat_pos2[0, -1:]) < size[0]) and \
      (0 <= int(boat_pos2[1, -1:]) < size[1]) and \
      (np.sqrt((boat_pos2[0, -1:]-goal_pos[0])**2 + (boat_pos2[1, -1:]-goal_pos[1])**2) > 1):
    
    # Append to boat_pos array the future position : last + current drift + direction to goal
    direction = np.arctan( (([goal_pos[1]] - boat_pos2[1,-1:]) / \
                            ([goal_pos[0]] - boat_pos2[0,-1:])) )
    boat_pos2 = np.append(boat_pos2,
                        boat_pos2[:,-1:] \
                            + currents_map[:, int(boat_pos[0,i:i+1]), int(boat_pos[1,i:i+1])] * drift \
                            + step * np.array([np.cos(direction), np.sin(direction)]),
                        axis = 1)
    i += 1
    
# ----------------------------------------------------------- #
#                       Plot currents                         #
# ----------------------------------------------------------- #
plt.figure("Self-steering boat within a currents field")                        # Create a new figure

plt.contourf(X_current, Y_current, currents_map[0]**2 + currents_map[1]**2, \
             levels = np.linspace(np.min(currents_map[0]**2 + currents_map[1]**2), \
                                  np.max(currents_map[0]**2 + currents_map[1]**2), 20))                            # Plot currents speed
plt.colorbar(label=r"$Vitesse\ (m/s)$")                                          # Add a colorbar
plt.streamplot(X_current, Y_current, currents_map[0], currents_map[1], color='k', density=1.5, linewidth=0.5, arrowsize=0.5)    # Plot currents direction
plt.gca().set_aspect('equal', adjustable='box')                                 # Set the plot aspect ratio to 1

# ----------------------------------------------------------- #
#                         Plot boat                           #
# ----------------------------------------------------------- #
plt.plot([start_pos[0], goal_pos[0]], [start_pos[1], goal_pos[1]], ':r', label='Direct path')   # Plot direct path between start and goal
plt.plot(boat_pos_inert[0], boat_pos_inert[1], 'gray', label='Drifting inert boat')             # Plot inert boat trajectory
plt.plot(boat_pos[0], boat_pos[1], 'g', label='Model 1')                                        # Plot model 1 boat trajectory
plt.plot(boat_pos2[0], boat_pos2[1], 'm', label='Model 2')                                      # Plot model 2 boat trajectory
plt.plot(start_pos[0], start_pos[1], '*g', markersize=10)                                       # Plot start position
plt.plot(goal_pos[0], goal_pos[1], '*r', markersize=10)                                         # Plot goal position

# ----------------------------------------------------------- #
#                         Plot style                          #
# ----------------------------------------------------------- #

plt.xticks(np.arange(0,size[0],10))                                             # Set x ticks
plt.yticks(np.arange(0,size[1],10))                                             # Set y ticks

plt.xlabel("x (m)")                                                             # Set x label
plt.ylabel("y (m)")                                                             # Set y label
plt.title('Self-steering boat trajectory simulation')                           # Set title
plt.legend(loc = 'upper center', bbox_to_anchor = (0.5, -0.2),
          fancybox = True, ncol = 3)                                            # Set legend

plt.xlim(0,size[0]-1)                                                           # Set x limits
plt.ylim(0,size[1]-1)                                                           # Set y limits
plt.grid(True)                                                                  # Set grid

plt.show() ## JPC
plt.savefig('last.png', dpi=300)                                                # Save figure

plt.pause(-1)