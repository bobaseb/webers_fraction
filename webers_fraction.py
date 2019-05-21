from scipy.special import erfc
import numpy as np
from numpy import sqrt
from scipy.optimize import minimize
import pandas as pd

def webers_prediction(w,smaller_number,larger_number,rt=np.array([])):
    if rt.size==0:
        x = ((larger_number-smaller_number)/(sqrt(2*w)*sqrt(smaller_number**2+larger_number**2)))
        #print('hello')
        #print(x)
    else:
        x = ((larger_number-smaller_number)/(sqrt(2*w*(1/rt))*sqrt(smaller_number**2+larger_number**2)))
    expected_accuracy = 1-0.5*erfc(x)
    #print(expected_accuracy)
    return expected_accuracy

def main_weber(w,params,optim=1):
    stim_left,stim_right,actual_response,rt=params
    which_bigger = np.array(stim_left>stim_right)
    #print(which_bigger)
    diff_pred=[]
    model_preds=[]
    for i in range(len(actual_response)):
        if which_bigger[i]==1:
            smaller_number = stim_right[i]
            larger_number = stim_left[i]
        elif which_bigger[i]==0:
            smaller_number = stim_left[i]
            larger_number = stim_right[i]
        if rt.size==0:
            expected_response = webers_prediction(w,smaller_number,larger_number)
            #print('hello2',expected_response)
        else:
            expected_response = webers_prediction(w,smaller_number,larger_number,rt[i])
        model_preds.append(expected_response)
        #print(expected_response, actual_response[i])
        diff_pred.append((expected_response-actual_response[i])**2)
    if optim==1:
        #now calculate your models error
        total_diff = np.sum(diff_pred)
        #print(w,total_diff)
        return total_diff
    else:
        return np.hstack(model_preds)

def run_wrapper(w0,params):
    res = minimize(main_weber,w0,args=(params,),method='nelder-mead')
    webers_w=res.x
    print(res.message)
    rmse = np.sqrt(res.fun)/len(params)
    print('RMSE: ', rmse)
    print('Webers w: ', webers_w)
    return webers_w, rmse

#load data
#pwd = '/home/seb/Dropbox/merari/'
pwd = '/media/seb/HD_Numba_Juan/Dropbox/merari/'
#fn = pwd + 'testds.csv' #'Weber.csv'
task = 'symbolic_' #'dots_' #
fn = pwd + task + '100519.csv'
ds = pd.read_csv(fn)
idx = 'ID_spss'

#initialize a starting w
w0=0.11

#lets do some preselection by condition
#ds = ds[ds.Subject != '766'] #exclude Subject 766 (no data)
unique_ids = np.unique(ds[idx])
#ds = ds[ds.condition==1] #small
#ds = ds[ds.condition==2] #large

ws=[]
all_model_preds=[]
model_errors=[]
model_accs=[]
for id in unique_ids:
    print('Subject: ', id)
    #get fixed params and run per subject
    stim_left = np.array(ds.loc[ds[idx]==id,'Stim_Left' ])
    stim_right = np.array(ds.loc[ds[idx]==id,'Stim_Right' ])
    correct_answer = np.array(ds.loc[ds[idx]==id,'Correct_Answer' ])
    #rt = np.array(ds.loc[ds['ID']==id,'Stimulus.RT' ])/1000 #convert to seconds
    rt = np.array([])
    params = np.array([stim_left,stim_right,correct_answer,rt])
    w_fit, rmse = run_wrapper(w0,params)
    model_errors.append(rmse)
    ws.append(w_fit)
    model_preds = main_weber(w_fit,params,optim=0)
    all_model_preds.append(model_preds)
    model_acc = np.sum(np.round(model_preds)==np.hstack(correct_answer))/float(len(model_preds))
    print('Model accuracy: ', model_acc)
    model_accs.append(model_acc)

#all_model_preds = np.vstack(all_model_preds)
ws = np.hstack(ws)

output_ds = np.array(np.hstack([np.matrix(unique_ids).T,np.matrix(ws).T,np.matrix(model_accs).T,np.matrix(model_errors).T]))
output_labels = ['Subject ID','Webers W', 'Model Accuracy','Model Root Mean Squared Error (RMSE)']

output_df = pd.DataFrame(output_ds,columns=output_labels)
output_df.set_index('Subject ID',inplace=True)

output_df.to_csv(pwd + task + 'webers_fraction.csv')
