# Pacemaker Design

Group Members:

Nicholas Koenig (koenin1)  

Luai Bashar (bashal1)  

Fraser Macfarlane (macfarlf)  

Karm Desai (desaik21)  

Matthew Mark (markm4)  

# About

The pacemaker design project is a term assignment where we were tasked to develop a pacemaker that was to be programmed using Simulink and Python and was built on the FRDM-K64F ARM development board. The group was split into two sub-teams responsible for either the DCM or Simulink portion of the project. Myself, being apart of the Simulink sub-team, heavily contributed to developing the rate adaptive modes that were used to track activity using the on-board accelerometer. Also, we worked together with the DCM sub-team to implement serial communication in order to transmit and receive information.

# Toolboxes Used

- MATLAB®
- Simulink®
- Simulink® Coder Support Package for NXP FRDM-K64F -> Segger’s J-Link OpenSDA V2 firmware
- DSP Toolbox

# Monitored Layer

![image](https://github.com/mgiancola9/Pacemaker_3K/assets/97264168/99241314-10c3-4fac-8372-b4020acf3fa4)

# Initialization Stateflow

![image](https://github.com/mgiancola9/Pacemaker_3K/assets/97264168/465dbc9e-69fb-4cd3-9a0c-8b81686c46d8)

# Send Parameters to DCM Function

![image](https://github.com/mgiancola9/Pacemaker_3K/assets/97264168/716b5039-0573-418d-b05c-17a09515d570)

# Pacemaker Modes Stateflow

![image](https://github.com/mgiancola9/Pacemaker_3K/assets/97264168/48b4c83f-a200-441d-81d1-117083576490)

# Rate Adaptability Stateflow

![image](https://github.com/mgiancola9/Pacemaker_3K/assets/97264168/a373a6e4-e97a-48b9-acbc-5e98bd914052)

# Output Layer












