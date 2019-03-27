def comps( df=n_c_y_df , i_key='Mobility period' ,  threshold=0.05, show_misses=True , indicate=False , proof=False  , count=True):
    '''
    inputs)
        df 
            >> dataframe
        i_key 
            >> what to index df on
        threshold
            >> level of change required in at least one column for pair to be of interest
        show_misses 
            >> show paired instances failing to meet threshold
        indicate
            >> display count of + , - , or both instances above each instance
            >> include hit , miss rate in final output (if count==True)
        proof
            >> display proof that instances do not pair
            >> if 'simple' 
                >> only display current instance , do not show instance it failed to pair with 
        count
            >> return number of: pairs, paired instances, non paired instances, total instances
            >> if indicate==True
                >> include met_threshold and dont_meet (threshold) counts in final output
    '''
    
    
    # copy dataframe
    df = df.copy()
    # index dataframe
    df = df.set_index( i_key )
    # indicate % change in dataframe
    df = df.pct_change()
    # set variable of index values
    year_index = df.index
    
    # non-threshold-meeting instances
    non_thresh=0
    # count total 
    total=0
    # count number of pairs
    pairs=0
    # instances of only positive threshold
    positive_only=0
    # instances of only negative threshold
    negative_only=0
    # instances of both positive and negative threshold
    pos_and_neg=0
    
    # record instances that don't paired
    non_pair=[]
    # record instances that pair
    ip=[]
    
    # for the length of the index -1 (last row unable to compare to next indexed row)
    for _ in range( len( year_index ) - 1 ):
        # update total count
        total+=1
        
        # year range (from 'Mobility period') for row at this index is same as row at next index
        if year_index[ _ ][ :9 ] == year_index[ _+1 ][ :9 ]:
            # we have a pair, so update count
            pairs+=1
            # add instance to list of instances which can pair
            ip.append( year_index[ _ ] )
            # add paired instance to list of instances which can pair (not for count, do not mind duplicates)
            ip.append( year_index[ _+1 ] )
            
            
            # determine how many of the changes are 0.5%+ and positive
            meets = df.iloc[ _+1 ] >= threshold
            # determine how many of the changes are 0.5%+ and negative
            n_meets = df.iloc[ _+1 ] <= -(threshold)
            
            """
            NOTE:
                - don't forget about compairing them the other way around
                - let's set an indicator that returns filter with less change 
                * see /whiteboard_pics/flip_change.jpg
            """
            # flip the rows in a copy of origional dataframe 


            # if we want to paint out threshold instances and indicators
            if indicate==True:
   
                # if at least one value meets positive threshold
                if meets.sum()>=1:
                    # check for negative threshold
                    if n_meets.sum()>=1:
                        # keep count of how many times this has happened
                        pos_and_neg+=1
                        # output heads up on exceeding both + and - with dual thresh count
                        print(f'*+-*  above&below = { pos_and_neg } *+-*')
                    # no instnaces of negative threshold
                    else:
                        # update number of positive threshold only
                        positive_only+=1
                        # output heads up on positive only threshold
                        print(f'+** above only = { positive_only } **+')
                
                # at least one value meets negative threshold && no values met the positive threshold 
                elif n_meets.sum()>=1:
                    # update number of negative threshold only
                    negative_only+=1
                    # output heads up on negative only threshold
                    print(f'-**  below only = { negative_only } **-')
                
                # if not meeting positive or negative threshold
                else:
                    # update count of pairs failing to meet threshold
                    non_thresh+=1
                
                # output: 'Mobility period' of top then bottom column, change values
                print( year_index[ _ ] ,'\n', year_index[ _+1 ] ,'\n', df.iloc[ _+1 ] ,
                      '\n', 'mean =',df.iloc[ _+1 ].mean(), '\n\n')
                
            # output 'Mobility period' of top row then of bottom
            # along with the percent change from top row to bottom for each column
            else:
                if show_misses:
                    print( year_index[ _ ] ,'\n', year_index[ _+1 ] ,'\n', df.iloc[ _+1 ], '\n', 
                          'mean =',df.iloc[ _+1 ].mean() ,'\n\n')
        
        # if no pair (or; otherwise, bad measure) 
        else:
            # update list of non-pair instances
            non_pair.append( year_index[ _ ] )
            
            # if we ask for proof
            if proof==True:
                # output 'Mobility period' of row in question then for row below
                print( year_index[ _ ], '\n' , year_index[ _+1 ] ,'\n\n')
            # if we ask for simple proof
            elif proof=='simple':
                # output index and corresponding 'Mobility period'
                print( _ , ' | ', year_index[ _ ],'\n\n' )
    
    # determine number of instances that were never paired
    comped_non_pair = [ i for i in non_pair if i not in ip ]
    
    # if we request the counts
    if count:      
        # sum non-paired instances
        npi = len( comped_non_pair )
        # sum total threshold hits 
        sum_thresh_hits = positive_only + negative_only + pos_and_neg
        # if looking for threshold indicators
        if indicate==True:
            # return how many times the threshold was hit
            return f'number_pairs={pairs}, met_threshold={sum_thresh_hits}, dont_meet={non_thresh}, paired={len(ip)}, non_paired={npi}, total_count={total}'
        else:
            # dont return met_threshold or dont_meet
            return f'number_pairs={pairs}, paired={len(ip)}, non_paired={npi}, total_count={total}'
            

# let's see
comps( df=n_c_y_df , i_key='Mobility period' ,  threshold=0.05, show_misses=False , indicate=True , proof=False  , count=True)
