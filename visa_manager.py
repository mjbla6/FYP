import visa
import math

def returnVisa():
    
    # Obtaining the resources found on the bus
    rm = visa.ResourceManager()
    resources =  rm.list_resources()

    # Searching for GPIB devices and obtaining address
    sub = 'GPIB'
    GPIB_Address = "\n".join(s for s in resources if sub.lower() in s.lower())
    GPIB_Address = str(GPIB_Address)
    
    # Obtaining number of GPIB devices
    length = len(GPIB_Address)
    num_GPIB = math.floor(length/16)

    # Predefining variables
    i = 0
    start = 0
    end = 16
    GPIB = [0] * num_GPIB
    GPIB_info = [0] * num_GPIB
    GPIB_model_info = [0] * num_GPIB

    # Iterating through each device to obtain the make and model information
    while i < num_GPIB:
        GPIB[i] = GPIB_Address[start:end]
        if GPIB[i] == "GPIB0::25::INSTR":
            my_instrument = rm.open_resource('%s' %GPIB[i])
            make = 'ANDO'
            model = 'AQ-4303'
            GPIB_info[i] = '%s, %s %s' %(GPIB[i],make,model)
            GPIB_model_info[i] = '%s %s' %(make,model)
            start += 17
            end += 17
            i += 1
        else:
            my_instrument = rm.open_resource('%s' %GPIB[i])
            info = str(my_instrument.query('*IDN?'))
            make_location = info.index(',')
            temp = info[make_location+1::]
            model_location = temp.index(',')
            make = info[0:make_location]
            model = temp[0:model_location]
            GPIB_info[i] = '%s, %s %s' %(GPIB[i],make,model)
            GPIB_model_info[i] = '%s %s' %(make,model)
            start += 17
            end += 17
            i += 1

    return GPIB_model_info,GPIB,num_GPIB
