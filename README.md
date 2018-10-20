# Monash ECSE Final Year Project 2018


PACKAGED APPS CAN BE DOWNLOADED AND RUN DIRECTLY - SEE USER MANUAL FOR DETAILS ON INSTALLATION AND OPERATION.
DOWNLOAD APPS FROM: https://www.dropbox.com/sh/cyy4km6tcwa6pzo/AAAIRtHRyspVcUJJYMlMy8rha?dl=0

Desctiption of code modules:

Visa Manager

The VISA manager module controls the connection and set up of the GPIB devices connected to the computer. The function was created to automatically query the USB connection of GPIB devices and return the information and address of each device, allowing the interface to connect to and communicate with each instrument reliably. This function makes use of both the PyVISA and math modules to operate, using the PyVISA module to connect to the GPIB instruments and the math module to round down some numbers where needed.The function works in the following way:

- The resources connected to the USB are found and loaded into the variable
resources using the PyVISA module. This query loads the device data into the
variable.
- The address of each GPIB is then found from this resources variable by searching for
words matching “GPIB”. This finds only GPIB devices and loads it into the variable
GPIB_Address.
- To obtain the number of devices connected to the USB, the length of the
GPIB_Address variable is queried, and the length is divided by 16. 16 is the length in Page | 21
Virtual Lab Over Dark Fibre Mitch Blair & Issac Naylor
characters of each GPIB address, so taking the floor(length(GPIB_Address)/16)
returns the number of connected devices
- A loop is then run to assign the information for each address
- Each GPIB address is assigned to the array GPIB which formats the address
correctly.
- Using the PyVISA module, the code connects to the current GPIB address
- The information of the instrument is queried using the command *IDN? and loaded
into the variable info. This returns the make, model and address information of the
instrument
- The make and model information are then found from this variable by separating the
string by (,)
- The variable GPIB_info is loaded with the address, make and model information
- The variable GPIB_model_info is loaded with the make and model information
- The start and end variables are incremented by 17, this allows the next address to be
found correctly on the next iteration of the loop
- If the address = “GPIB0::25:INSTR” then the program manually assigns this as the
ANDO AQ-4303. This is because this instrument cannot be queried with *IDN? and therefore the program cannot find the information relating to the instrument . The GPIB address is manually assigned at the back of the instrument so the program can manually search for the address
- The function then returns the two arrays GPIB_model_info and GPIB, as well as the variable num_GPIB ready to use in the main function


Conversions

The conversions function handles all of the value conversions for the program. It operates by being passed the value that needs to be converted (the value variable) and the unit that it needs to be converted into (unit variable). The function works in the following way:

- The conversions function is called in the Agilent86142B function and is passed two arguments: the value pulled from the instrument and the unit that it needs to be converted to
- Various checks are then run to determine which unit the value needs to be converted to
- When the correct unit is found, the value is converted by the appropriate values to obtain the desired result
- If the unit entered cannot be found, then a value error is raised to let the user know that an error has occurred
- The function then returns the converted value
The function was designed in this way to ensure a simple way of adding more units for conversion. To add further units that needed to be converted, all that needs to be done is to add a simple loop to check for that particular unit. The appropriate conversion then needs to be determined and applied. This method creates a simple way of converting values that is both simple and adaptable for future changes.


Main

The main module controls the upper level functions of the entire program, controlling the creation of the program window and connections to other modules. The module operates by connecting to different instruments depending on what options are selected by the user. The module operates as follows:

- All associated modules are imported. This includes the necessary modules
discussed above
- The visa_manager module is used to connect to the visa devices and return the
associated address and information about these devices
- The main window is loaded, and the user interface is created, loading in associated
functions such as ‘New Instrument’ and ‘Close Instrument’
- If the new instrument option is selected, the instrument select class is connected. If
the close instrument option is selected, the current instrument will be exited, or the
program will exit if no instruments are open
- The instrument select window is loaded which opens a new window. This window is
populated with the connected devices found by the visa_manager
- If the refresh button is clicked, the visa_manager will be queried again, and the
connected devices will be reloaded and added back into the instrument select
window
- If a device is selected, the openInstrument function is loaded. This function
determines which device was selected and connects to that instrument’s module

Agilent 86142B Module
The module created for the Agilent OSA contains all of the code necessary to remotely control the instrument. This includes all menu options, GUI imports, calculations and plotting commands. The module can be thought as four different components that interact with each other to obtain the correct functionality. These segments are:

- Start-up functions
- Menu functions
- Marker and trace update and plotting functions
- Display updating functions
