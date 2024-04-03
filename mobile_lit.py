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


title_str = "Can we see meteorite events in Mercury's Helium Exosphere?"
subheader_str1 = "While working on a steady-state model for Mercury's Helium exosphere, " \
                "we began to wonder if transient events, such as Meteorite Impact Events (MIEs), could cause a detectable enrichment of the Helium abundance. " \
                "We provide this platform so that you can explore the signature of MIEs yourself."

text_str1 = "Of course, the signature of an MIE depends on in the size of the impactor, whereby the population of impactors of a given size are modelled by the characteristic velocity of their polulation (see e.g. Mangano et al. 2007). " \
            "Another parameter, which influences the MIE signature substantially, is the 'Helium Source Volume'." \
            "The amount of substance released by MIE is typically modelled via stoichiometric vaporization (e.g. Mangano et al, 2007), in which case the Helium release equals the total amount of Helium in the vaporised volume. " \
            "Since Helium is extremely volatile and only very weakly accomodated in the regolith, it is possible that the brief and violent heating of the MIE causes the Helium to diffuse from ejecta and melt volume as well. " \
            "In this case the 'Source Volume' of Helium extends far beyond the vapor volume, potentially including ejecta and melt volume and leading to a Helium release up to x100 above that of stoichometric vaporisation. "



st.title(title_str)
st.divider()

st.subheader(subheader_str1, anchor=None, help=None, divider=False)
st.write(text_str1)



##########################################################
###### SLIDERS / UI                        ###############

st.divider()

text_str2 = "Use the two sliders to set values for these two parameters, and watch the how (and if) the released Helium can be seen against the steady state Helium exosphere!"
st.subheader(text_str2, anchor=None, help=None, divider=False)



def log_label_format_func(opt):

    return f'{round(10**opt, 1)}m'


def x_label_format_func(opt):

    return f'x{round(10**opt, 1)}'


st.write("\n")

user_var1 = st.select_slider(
    label=f'slide here to set impactor size [m]',
    options=[-1, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
    format_func=log_label_format_func,
    value=0)


st.write("\n")


user_var2 = st.select_slider(
    label='slide here to set Helium Source Volume, relative to Vapor Volume [-]',
    options=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2],
    format_func=x_label_format_func,
    value=0)
    
scaling_factor = (10**user_var1)**3 * (10**user_var2)
st.write("\n")


st.write("Use the Control Bar of the HTML to start replay of the animation.")
st.write("Hint: If you are not seeing any signature, you may need to change your input parameters!")
st.write('\n')



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
    ratio[:, 0] = 1.0
    ratio[:, -1] = 1.0


    #mappable.set_data(ratio)
    mappable.set_array(ratio.ravel())
    txt.set_text(f"t: {round(frame)} s")
    return mappable, txt, 



##########################################################
###### FIGURE SETUP                         ##############


font = {'size'   : 7}

matplotlib.rc('font', **font)
#matplotlib.rcParams['xtick.major.pad']='3'
matplotlib.rcParams['ytick.major.pad']='5'

# create figure object
fig = plt.figure(figsize=[3.5, 4], layout="constrained")
# load axis box
ax = fig.add_axes([0.1,0.1,0.8,0.8], polar=True)
ax.set_theta_zero_location("N")
# set axis limit
ax.set_ylim([0,max(radial_steps)])
ax.set_xlim([-max(np.deg2rad(ext_psi_angles)),max(np.deg2rad(ext_psi_angles))])

# ax.set_xlabel("Radial Distance [km]", loc='right')
ax.text(0.6, 0.1, f"Radial Distance [km]", transform=ax.transAxes)
# ax.set_ylabel("Polar Angle [deg]")
ax.set_title(f"Signature of MIE in Helium Exophere", fontsize=10)

ax.tick_params(axis='y', labelrotation=45)

angles_ticks = ext_psi_angles[0::6]
angles_ticks = angles_ticks[1:]
ax.set_xticks(np.deg2rad(angles_ticks), [f'{angle}$^\circ$ ' for angle in angles_ticks])

textstr = f'Impactor Radius: {log_label_format_func(user_var1)}\n' \
          f'Source Volume:   {x_label_format_func(user_var2)}'

# these are matplotlib.patch.Patch properties
props = dict(boxstyle='round', facecolor="#a484ac", alpha=0.3)

# place a text box in upper left in axes coords
ax.text(0.7, 0.95, textstr, transform=ax.transAxes, fontsize=7,
        verticalalignment='top', bbox=props)


cmp = ax.pcolormesh(np.deg2rad(ext_psi_angles),radial_steps, D0, norm=matplotlib.colors.LogNorm(vmin=0.9, vmax=1.0E2))

dyna_txt = ax.text(0.15, -0.22, f"t: {int(0)} s", transform=ax.transAxes)

cbar = plt.colorbar(cmp, orientation='horizontal', pad=-0.05)
cbar.ax.set_xlabel('Helium enrichment w.r.t. background [-]', rotation=0)



##########################################################
###### PRODUCT                              ##############

ani = animation.FuncAnimation(fig, animate, frames=times, fargs=(data_dict, cmp, dyna_txt), interval=1000)
components.html(ani.to_jshtml(), height=500, scrolling=True)


st.divider()

st.write("From this analysis we can conclude that typical 0.5-1m sized impactors can create a significant enhancement Helium exosphere, the temporal and spatial extend of which depends on the Helium Source Volume. "
         "With Helium release from all melt and ejecta (i.e. x100), a 0.5m object creates is visible at a detectable signature over an extend of +/- 30$^\circ$, which exists for a few thousand seconds within our domain of interest.")



##########################################################
###### OUTRO                                ##############


st.divider()
st.write('\n')
st.write('\n')
col1, col2, col3 = st.columns(3)

with col2:
    st.image("portrait_circle_black.jpg", width=200, caption="Thank you for visiting!")

st.divider()


footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 300;
bottom: 0;
width: 18.5%;
min-width: 400px;
background-color: #a484ac;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Brough to you with ❤ by <a style='display: block; text-align: center;' href="www.linkedin.com/in/jhener" target="_blank">Jonas Hener | Uni Bern </a></p>
</div>
"""


st.markdown(footer,unsafe_allow_html=True)