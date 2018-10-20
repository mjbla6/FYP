# Function to convert values into the correct unit or correct
# representation of unit. eg. nm -> um or 100*10^-9m -> 100nm 
def str2float(string,unit):
    value = float(string)
    ## add more units in here when needed
    if unit == "nm":
        value = value * 1000000000
    elif unit == "um":
        value = value * 1000000
    elif unit == "dBm":
        value = value * 1 
    elif unit == "dB":
        value = value * 1 
    elif unit == "us":
        value = value * 1000000
    elif unit == "s":
        value = value * 1
    elif unit == "Ang":
        value = value * 10000000000
    elif unit == "W":
        value = (10**(value/10))/1000
    elif unit == "mW":
        value = value * 1000
    elif unit == "uW":
        value = value * 1000000
    elif unit == "nW":
        value = value * 1000000000
    elif unit == "pW":
        value = value * 1000000000000
    elif unit == "kHz": 
        value = value/1000
    elif unit == 'GHz':
        value = (299,792,458/value)/1000000000
    elif unit == 'THz':
        value = (299,792,458/value)/1000000000000
    elif unit == 'Ang':
        value = value * 0.0000000001
    else:
        raise ValueError("Incorrect unit entered.")
    return value




