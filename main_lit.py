"""
# My first app
Here's our first attempt at using data to create a table:
"""


import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import streamlit as st
import streamlit.components.v1 as components




##########################################################
###### LAYOUT                              ###############


st.title("Bruder - es könnte schon krank werden!")
left_column, right_column = st.columns([0.7, 0.3])


##########################################################
###### SLIDERS / UI                        ###############

with right_column:
    user_var1 = st.select_slider(
        label='slide here to set impactor size [m]',
        options=[0.1, 1, 10],
        
        value=1)
    user_var2 = st.select_slider(
        label='slide here to set Helium enrichment factor in MIV plume [-]',
        options=[1, 10, 100],
        value=10)
    
scaling_factor = user_var1**3 * user_var2



##########################################################
###### DATA                                 ##############

times = [   100.,    200.,    500.,   1000.,   2200.,   4600.,  10000., 21500.,  46400., 100000.]
radial_steps = [    0,   500,  1000,  1500,  2000,  2500,  3000,  3500,  4000, 4500,  5000,  5500,  
                6000,  6500,  7000,  7500,  8000,  8500, 9000,  9500, 10000, 10500, 11000, 11500, 
                12000, 12500, 13000, 13500, 14000, 14500]
ext_psi_angles = [-90, -85, -80, -75, -70, -65, -60, -55, -50, -45, -40, -35, -30, -25, -20, -15, -10,  -5,   0,   
                  5,  10,  15,  20,  25,  30,  35, 40,  45,  50,  55,  60,  65,  70,  75,  80,  85,  90]


data_dict = dict()

for time in times:

    data = np.loadtxt(f"data_lit/density_grid_{int(time)}.txt")
    data_dict[time] = data

BG = np.loadtxt(f"data_lit/BG.txt")

D0 = np.ones(data.shape)


##########################################################
###### ANIMATION FUNC                       ##############

def animate(frame, grid_dict, mappable, txt):
    # for each frame, update the data stored on each artist.

    Gt = grid_dict[frame]

    Dt = scaling_factor*(Gt)/100**3
    ratio = Dt/BG
    ratio[ratio<=1] = 1.0
    #ratio[:, 0] = 1.0
    #ratio[:, -1] = 1.0


    #mappable.set_data(ratio)
    mappable.set_array(ratio.ravel())
    txt.set_text(f"t: {round(frame)} s")
    return mappable, txt, 



##########################################################
###### FIGURE SETUP                         ##############


font = {'size'   : 10}

matplotlib.rc('font', **font)

# create figure object
fig = plt.figure(figsize=[5,5])
# load axis box
ax = fig.add_axes([0.1,0.1,0.8,0.8], polar=True)
ax.set_theta_zero_location("N")
# set axis limit
ax.set_ylim([0,max(radial_steps)])
ax.set_xlim([-max(np.deg2rad(ext_psi_angles)),max(np.deg2rad(ext_psi_angles))])

ax.set_xlabel("Radial Distance [km]")
ax.set_ylabel("Polar Angle [deg]")
ax.set_title(f"Signature of Meteoroid Event \n in Helium Exophere")

ax.tick_params(axis='y', labelrotation=45)

cmp = ax.pcolormesh(np.deg2rad(ext_psi_angles),radial_steps, D0, norm=matplotlib.colors.LogNorm(vmin=0.9, vmax=1.0E2))

dyna_txt = ax.text(-0.1, -0.2, f"t: {int(0)} s", transform=ax.transAxes)

cbar = plt.colorbar(cmp)
cbar.ax.set_ylabel('Helium abundance w.r.t. background [-]', rotation=90)



##########################################################
###### PRODUCT                              ##############

ani = animation.FuncAnimation(fig, animate, frames=times, fargs=(data_dict, cmp, dyna_txt), interval=1000)

with left_column:
    
    components.html(ani.to_jshtml(), height=600)