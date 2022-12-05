

#
#
#:
#   mas -
#   num_hist - c
#:
#   histogramm -
#   size -
#   NUM_histogramm -

import numpy as np
    
def hist_complex(mas = None,num_hist = None): 
    n_hist_re = 1
    num = np.asarray(mas).size
    
    re = np.zeros((num,1))
    re = real(mas)
    im = np.zeros((num,1))
    im = imag(mas)
    
    re_max = np.amax(re)
    re_min = np.amin(re)
    im_max = np.amax(im)
    im_min = np.amin(im)
    
    step_re = (np.abs(re_max) + np.abs(re_min)) / num_hist
    step_im = (np.abs(im_max) + np.abs(im_min)) / num_hist
    
    ms_work = np.zeros((num_hist + 2,num_hist))
    for i in np.arange(1,num+1).reshape(-1):
        x = re_min
        n_hist_re = 1
        #    RE
        for j in np.arange(1,num_hist+1).reshape(-1):
            if (re(i,1) <= (x + step_re)):
                n_hist_re = j
                break
            else:
                x = x + step_re
        ms_work[num_hist + 1,n_hist_re] = ms_work(num_hist + 1,n_hist_re) + 1
        x = im_min
        n_hist_im = 1
        #    IM
        for j in np.arange(1,num_hist+1).reshape(-1):
            if (im(i,1) <= (x + step_im)):
                n_hist_im = j
                break
            else:
                x = x + step_im
        ms_work[n_hist_im,n_hist_re] = ms_work(n_hist_im,n_hist_re) + 1
    
    
    
    #for i=1:num_hist#02
#   sum=0;
    
    #  for j=1:num_hist
# sum=sum+ms_work(j,i);
#  end;
#  ms_work(num_hist+2,i)=ms_work(num_hist+1,i)+sum;
#  ms_work(num_hist+1,i)=(ms_work(num_hist+1,i)/num)*(sum/num);
    
    #end;#02
    
    for i in np.arange(1,num_hist+1).reshape(-1):
        ms_work[num_hist + 2,i] = ms_work(num_hist + 1,i)
        ms_work[num_hist + 1,i] = (ms_work(num_hist + 1,i) / num)
    
    
    # -   size
    histogramm = ms_work(num_hist + 1,:)
    NUM_histogramm = ms_work(num_hist + 2,:)
    size = num_hist
    return histogramm,size,NUM_histogramm
    
    return histogramm,size,NUM_histogramm