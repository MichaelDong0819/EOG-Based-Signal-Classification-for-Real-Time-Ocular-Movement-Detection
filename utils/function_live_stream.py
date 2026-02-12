import numpy as np
import pandas as pd

def live_streamer(model, data_chunk):
    
    predictions = model.predict(data_chunk)

    event_counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
    for p in predictions:
        event_counts[p] += 1

    event = max(event_counts, key=event_counts.get)

    return event



def live_streamer_KNN(model, data):
    event_amp_int = []
    event_amp_up = []
    event_amp_down = []
    event_int_width = []
    event_amp_width_up = []
    event_amp_width_down = []


    # Extract time and amplitude, center amplitude at 0
    time = data['Time'].values
    amp = data['Frequency'].values - np.median(data['Frequency'].values)
    # print(np.median(data['Frequency'].values))
    #amp[:] = amp[::-1]
    
    # Time increment
    dt = time[1] - time[0]
    
    # Calculate left integral
    event_integral = np.zeros_like(amp)
    for i in range(len(amp)-1):
        event_integral[i+1] = dt/2 * (amp[i+1] + amp[i]) + event_integral[i]
    
    rounded_int = np.round(10*event_integral)
    rounded_amp = np.round(amp)
        
    event_amp_up.append(np.max(amp))
    event_amp_down.append(np.min(amp))

    # Store minimum left integral and maximum time difference
    if np.max(event_integral)>np.abs(np.min(event_integral)):
        event_amp_int.append(np.max(10*event_integral))
        threshold_int = np.round(0.5*np.max(10*event_integral))

    else:
        event_amp_int.append(np.min(10*event_integral))
        threshold_int = np.round(0.5*np.min(10*event_integral))
    
    # Calculate time differences
    time_difference_int = np.diff(time[rounded_int == threshold_int])
    
    threshold_amp_up = np.round(0.5*np.max(amp))
    threshold_amp_down = np.round(0.5*np.min(amp))

    time_difference_amp_up = np.diff(time[rounded_amp == threshold_amp_up])
    time_difference_amp_down = np.diff(time[rounded_amp == threshold_amp_down])
    
    # Use time differences to determine the full width half maximum 
    # event_int_width.append(np.max(time_difference_int))
    event_amp_width_up.append(np.max(time_difference_amp_up))
    event_amp_width_down.append(np.max(time_difference_amp_down))
    
    x = np.vstack((event_amp_int,event_amp_up,event_amp_width_up,event_amp_width_down,event_amp_down)).T
    return x

def process_low_pass_fft(t,data_t,f_limit):
    nfft = len(data_t) # number of points
    dt = t[1]-t[0]  # time interval
    maxf = 1/dt     # maximum frequency
    df = 1/np.max(t)   # frequency interval
    f_fft = np.arange(-maxf/2,maxf/2+df,df)          # define frequency domain

    ## DO FFT
    data_f = np.fft.fftshift(np.fft.fft(data_t)) # FFT of data

    ## low pass FILTER
    data_f_filtered = data_f
    data_f_filtered[np.abs(f_fft)>f_limit] = 0 +0j   # set frequency magnitudes to 0 above cutoff frequency
    data_t_filtered = np.fft.ifft(np.fft.ifftshift(data_f_filtered))    # bring filtered signal in time domain
    return data_t_filtered.real

def process_gaussian_fft(t,data_t,sigma_gauss):
    nfft = len(data_t) # number of points\n",
    dt = t[1]-t[0]  # time interval\n",
    maxf = 1/dt     # maximum frequency\n",
    df = 1/np.max(t)   # frequency interval\n",
    f_fft = np.arange(-maxf/2,maxf/2+df,df)          # define frequency domain
     ## DO FFT
    data_f = np.fft.fftshift(np.fft.fft(data_t)) # FFT of data
    sigma_gauss = 25  # width of gaussian - defined in the function\n",
    gauss_filter = np.exp(-(f_fft)**2/sigma_gauss**2)   # gaussian filter used\n",
    data_f_filtered= data_f*gauss_filter    # gaussian filter spectrum in frquency domain\n",
    data_t_filtered = np.fft.ifft(np.fft.ifftshift(data_f_filtered))    # bring filtered signal in time domain\n",
    return data_t_filtered
