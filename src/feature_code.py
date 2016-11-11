


################################################
############ import the files
################################################
import sys
stream_payment_path = sys.argv[1]
batch_payment_path = sys.argv[2]

outfile_1 = sys.argv[3]
outfile_2 = sys.argv[4]
outfile_3 = sys.argv[5]

################################################
############ import the relevant packages
################################################
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime


##### creating a function to strip out the white spaces in the csv import
def strip(text):
    try:
        return text.strip()
    except AttributeError:
        return text


##### stream_payment.txt -- these are the current payments happening
stream_payment = pd.read_csv(open(stream_payment_path,'rU')
                                 , error_bad_lines=False
                                 , usecols=["time", " id1", " id2", " amount", " message"]
                                 , converters = {' amount' : strip}
                            )
##### batch_payment.txt -- previous payments. use this to build ecosystem
batch_payment = pd.read_csv(open(batch_payment_path,'rU')
                                 , error_bad_lines=False
                                 , usecols=["time", " id1", " id2", " amount", " message"]
                                 , converters = {' amount' : strip}
                           )

###### turn the csv's into pandas dataframes
stream_payment_df = pd.DataFrame(stream_payment)
batch_payment_df = pd.DataFrame(batch_payment)


######### doing some data cleaning
### make sure the amount field is a number
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


#### removing instances where the amount variable isn't a number
batch_payment_df['amount_test'] = batch_payment_df[' amount'].apply(is_number)
batch_payment_df = batch_payment_df[(batch_payment_df['amount_test'] == True)]
batch_payment_df = batch_payment_df[~batch_payment_df[' amount'].isnull()]
batch_payment_df[' amount'] = batch_payment_df[' amount'].astype(float)
#### changing the user ids to ints
batch_payment_df[' id1'] = batch_payment_df[' id1'].astype(int)
batch_payment_df[' id2'] = batch_payment_df[' id2'].astype(int)


stream_payment_df['amount_test'] = stream_payment_df[' amount'].apply(is_number)
stream_payment_df = stream_payment_df[stream_payment_df['amount_test'] == True]
stream_payment_df = stream_payment_df[~stream_payment_df[' amount'].isnull()]
stream_payment_df[' amount'] = stream_payment_df[' amount'].astype(float)
stream_payment_df[' id1'] = stream_payment_df[' id1'].astype(int)
stream_payment_df[' id2'] = stream_payment_df[' id2'].astype(int)



######################################################################################
### now I'm going to turn the pandas dataframes into a dictionary that
#### will be used to look up the relationships
######################################################################################


####### first step -- build a dictionary with all of the relationships. Each key will be the unique count of user_ids
batch_payment_df_trim = batch_payment_df[[' id1', ' id2']]

####### here I'm reversing the order so all combinations are captured for each user
batch_payment_df_trim_reverse = pd.DataFrame()
batch_payment_df_trim_reverse[' id1'] = batch_payment_df_trim[' id2']
batch_payment_df_trim_reverse[' id2'] = batch_payment_df_trim[' id1']


###### combine the datasets
frames = [batch_payment_df_trim, batch_payment_df_trim_reverse]
batch_payment_full_df = pd.concat(frames).drop_duplicates()

###### group up the user id and make a list of all the users they've interacted with
batch_payment_df_trim = pd.DataFrame(batch_payment_full_df.groupby(' id1')[' id2'].apply(list))
batch_payment_df_trim.reset_index(level=0, inplace=True)

###### finish creating the dictionary
batch_payment_df_trim = batch_payment_df_trim[[' id1', ' id2']].set_index(' id1').T
previous_payments_dict = batch_payment_df_trim.to_dict('list')





######################################################################################
######################################################################################
########### create functions to make the new files
######################################################################################
######################################################################################

def first_degree(series1, series2):
    ### take the first user and see if the second user is in their value list in the dictionary
    if previous_payments_dict.get(series1, None) is not None:
        if series2 in previous_payments_dict.get(series1, None)[0]:
            return 1
    else:
        pass


######################################################################################
### feature 2 --
### second degree friends should be able to interact without the notificaiton.
### even if they haven't interacted in the past
######################################################################################

def second_degree(series1, series2):
    #### check if they are first degree friends
    if first_degree(series1, series2) is not None:
        return first_degree(series1, series2)
    else:
        pass

    #### in this next step we check if anything overlaps between series1's children and series2's children
    if previous_payments_dict.get(series1, None) is not None and previous_payments_dict.get(series2, None) is not None:
        for x, y in [(x, y) for x in previous_payments_dict.get(series1, None)[0] for y in
                     previous_payments_dict.get(series2, None)]:
            if x in y or series2 == x or series1 in y:
                return 1
            else:
                pass
    else:
        pass


######################################################################################
### feature 3 --
######################################################################################

def fourth_degree(series1, series2):
    #### here we check to see if the children of 1 equal series2
    if previous_payments_dict.get(series1, None) is not None and previous_payments_dict.get(series2, None) is not None:
        if first_degree(series1, series2) is not None:
            return first_degree(series1, series2)
        else:
            pass

    ##### here we compare the children of 1 to the children of 2. We want to see if there are any overlaps
    if previous_payments_dict.get(series1, None) is not None and previous_payments_dict.get(series2, None) is not None:
        for x, y in [(x, y) for x in previous_payments_dict.get(series1, None)[0] for y in
                     previous_payments_dict.get(series2, None)]:
            if x in y or series2 == x or series1 in y:
                return 1
            else:
                pass
    else:
        pass

    ##### for each child from #1, compare it's children to the children from of 2
    ####### this is 3rd degree
    if previous_payments_dict.get(series1, None) is not None and previous_payments_dict.get(series2, None) is not None:
        for x in previous_payments_dict.get(series1, None)[0]:
            for b, c in [(b, c) for b in previous_payments_dict.get(x, None)[0] for c in
                         previous_payments_dict.get(series2, None)]:
                if b in c or series2 == b or series1 in c:
                    return 1

            ##### for each grand-child from #1, compare it's children to the children from of 2
            for e in previous_payments_dict.get(x, None)[0]:
                if e != series1:
                    for f, g in [(f, g) for f in previous_payments_dict.get(e, None)[0] for g in
                                 previous_payments_dict.get(series2, None)]:
                        if f in g or series2 == f or series1 in g:
                            return 1



######################################################################################
######################################################################################
######################################################################################
######################################################################################


######################################################################################
########## applying the functions
######################################################################################



output1 = stream_payment_df.apply(lambda x: first_degree(x[' id1'], x[' id2']), axis = 1)
output1_1 = np.where(output1 == 1, "trusted", "unverified")

with open(outfile_1, 'w') as o:
    for line in output1_1:
        o.write(line)


print("function 1 was used")

output2 = stream_payment_df.apply(lambda x: second_degree(x[' id1'], x[' id2']), axis = 1)
output2_1 = np.where(output2 == 1, "trusted", "unverified")

with open(outfile_2, 'w') as o2:
   for line in output2_1:
        o2.write(line)


print("function 2 was used")

output3 = stream_payment_df.apply(lambda x: fourth_degree(x[' id1'], x[' id2']), axis = 1)
output3_1 = np.where(output3 == 1, "trusted", "unverified")

with open(outfile_3, 'w') as o3:
    for line in output3_1:
       o3.write(line)


print("function 3 was used")

######################################################################################
######################################################################################
######################################################################################
######################################################################################



