def comps( df=n_c_y_df , i_key='Mobility period' ,  threshold=0.05, display='straight' , show_misses=True , indicate=False , proof=False  , count=True , output=True , means_only=False ):
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
        output
            >> True (default), returns all outcomes in list 
                >> if Flase , prints all outcomes  
        mean_only
            >> False by default
                >> if True , returns mean values only
                    >> all other outputs canceled 
    '''
    
    # outcomes will be output within a list
    if output==True:
        # initialize output list
        out = []

    # copy dataframe
    df = df.copy()
    
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

    def do_right( q , to_do=output ):
        '''
        inputs
            >> takes in object {q}
            >> based on to_do
                >> prints q (False) 
                >> appends q out (True)
        '''
        # check out vs print
        if to_do==True:
            # will happen if output=True
            out.append( q )                    
        # we will not be using the output , check instance , print appropriately
        else:
            # tuple
            if isinstance( q , tuple ):
                # print each
                print( _ for _ in q )
            # string
            if isinstance( q , str ):
                print( q )
            else:
                raise Exception( f'ERROR to_do ERROR\ntype = { type( q )}' )
    
    # top row to bottom row
    if display=='straight':
        # index dataframe
        df = df.set_index( i_key )
        # indicate % change in dataframe
        df = df.pct_change()
        # set variable of index values
        year_index = df.index
    # bottom row to top row
    if display=='reverse':
        # index dataframe
        df = df.set_index( i_key )
        # reverse index of df
        df = df.iloc[::-1]
        # indicate % change in dataframe
        df = df.pct_change()
        # set variable of reversed index values
        year_index = df.index       
        
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

            # if we want to paint out threshold instances and indicators
            if indicate==True:
   
                # if at least one value meets positive threshold
                if meets.sum()>=1:
                    # check for negative threshold
                    if n_meets.sum()>=1:
                        # keep count of how many times this has happened
                        pos_and_neg+=1
                        # output heads up on exceeding both + and - with dual thresh count
                        q = (f'*+-*  above&below = { pos_and_neg } *+-*')
                        # output
                        do_right( q )

                    # no instnaces of negative threshold
                    else:
                        # update number of positive threshold only
                        positive_only+=1
                        # output heads up on positive only threshold
                        q = (f'*+* above only = { positive_only } *+*')
                        # output
                        do_right( q )

                # at least one value meets negative threshold && no values met the positive threshold 
                elif n_meets.sum()>=1:
                    # update number of negative threshold only
                    negative_only+=1
                    # output heads up on negative only threshold
                    q = (f'*-*  below only = { negative_only } *-*')
                    # output
                    do_right( q )           
                # if not meeting positive or negative threshold
                else:
                    # update count of pairs failing to meet threshold
                    non_thresh+=1
                
                # asking for means only
                if means_only==True:
                    # output 'Mobility period' pair max change, min chage, mean change
                    q = ( f'{year_index[ _ ]}\n{year_index[ _+1 ]}\nmin = {df.iloc[ _+1 ].min()}\nmax = {df.iloc[ _+1 ].max()}\nmin v max = {df.iloc[ _+1 ].min() - df.iloc[ _+1 ].max()}\nmean = {df.iloc[ _+1 ].mean()}\n' )
                # 'regular' outcome
                else:
                    # output: 'Mobility period' of top then bottom column, change values, mean change
                    q = ( f'{year_index[ _ ]}\n{year_index[ _+1 ]}' ,'\n', df.iloc[ _+1 ] ,
                          '\n', 'mean =',df.iloc[ _+1 ].mean(), '\n')
                # output
                do_right( q )

            # output 'Mobility period' of top row then of bottom
            # along with the percent change from top row to bottom for each column
            else:
                # document pairs failing to meet/exceed threshold
                if show_misses==True:
                    #  show min/max/mean miss
                    if means_only==True:
                        # output 'Mobility period' pair max change, min chage, mean change
                        q = ( f'fail{year_index[ _ ]}\n{year_index[ _+1 ]}\nmin = {df.iloc[ _+1 ].min()}\nmax = {df.iloc[ _+1 ].max()}\nmin v max = {df.iloc[ _+1 ].min() - df.iloc[ _+1 ].max()}\nmean = {df.iloc[ _+1 ].mean()}\n' )
                    else:
                        # show 'regular' miss
                        q = ( f'{year_index[ _ ]}\n{year_index[ _+1 ]}\n', df.iloc[ _+1 ], '\n', 
                          'mean =',df.iloc[ _+1 ].mean() ,'\n')
                    # output
                    do_right( q )
        
        # if no pair (or; otherwise, bad measure) 
        else:
            
            # update list of non-pair instances
            non_pair.append( year_index[ _ ] )
            
            # if we ask for proof
            if proof==True:
                # output 'Mobility period' of row in question then for row below
                q = f'{year_index[ _ ]}\n{year_index[ _+1 ]}\n\n'
                # operate 
                do_right( q )

            # if we ask for simple proof
            elif proof=='simple':
                # output index and corresponding 'Mobility period'
                q = f'{_}  | {year_index[ _ ]}\n\n'
                # output
                do_right( q )
                
            else:
                if proof==False:
                    pass
    
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
            q = f'number_pairs={pairs}, met_threshold={sum_thresh_hits}, dont_meet={non_thresh}, paired={len(ip)}, non_paired={npi}, total_count={total}'
        else:
            # dont return met_threshold or dont_meet
            q = f'number_pairs={pairs}, paired={len(ip)}, non_paired={npi}, total_count={total}'
        # output
        do_right( q )
    # asking for one final output 
    if output==True:
        return out


# n_c_y_df.set_index('Mobility period').pct_change()
# i_mobility_change.iloc[6:9]

# copy dataframe
n_c_y_copy = n_c_y_df.copy()

# extract 2000-2001 rows
x = n_c_y_copy.iloc[ 6:9 ]

# drop SCHIP && set index
x = x.set_index( 'Mobility period' ).drop( '2000-2001 (SCHIP, 2000 controls)/5' )


def better_comps( data , key , proof=False , difference=False , calculations=False , match_recap=False , high_level=False ):
    '''
    inputs)
        > data
            >> dataframe
        > key
            >> column name to index on
        > proof
            >> if True, prints proof of findings
        > difference
            >> if True, prints winner of over_under
                >> over_under: 
                    >> if the absolute value of a straight value is less than the absolute value of the corresponding reverse value
                        >> subtract the absolute straight value from the absolute reverse value
                            >> and add the remainder to over_under
                    >> if the absolute value of a reverse value is less than the absolute value of the correcponding straight value
                        >> subtract the absolute reverse value from the absolute straight value
                            >> and subtract the remainder from over_under
        > calculations
            >> if True, prints compared min, max, and mean values 
        > high_level
            >> only see high level
            >> excludes all info except high_level from showing
    '''
    # copy data
    df = data.copy()
    # index data on {key}
    df = df.set_index( key )
    
    # times straight wins win_count and over_under
    straight_outright_wins = 0
    # times straight wins win_count but not over_under
    straight_win_count_wins = 0
    # times straight wins over_under but not win_count
    straight_over_under_wins = 0
    # times reverse wins win_count and over_under
    reverse_outright_wins = 0
    # times reverse wins win_count but not over_under
    reverse_win_count_wins = 0
    # times reverse wins over_under but not win_count
    reverse_over_under_wins = 0
    
    # iterate over the index values
    for _ in range( len( df.index ) - 1 ):
        
        # set instance
        instance = df.index[ _ ]
        # plus one
        instance_1 = df.index[ _ + 1 ]
        # if first 9 from current value are same as first 9 from next value
        if instance[:9] == instance_1[:9]:
            
            # make new dataframe only containing those rows
            one_on_one_df = df.copy()[_:_+2]
    
            # calculate change for straight
            straight_copy = one_on_one_df.pct_change()
            # and change for the flip
            reverse_copy = one_on_one_df.iloc[::-1].pct_change()

            # extract names form first rows
            s1n = straight_copy.iloc[0].name
            r1n = reverse_copy.iloc[0].name

            # tag 2nd rows
            s2 = straight_copy.iloc[1]
            r2 = reverse_copy.iloc[1]

            # extract names form 2nd rows
            s2n = s2.name
            r2n = r2.name
            
            # high_level excludes all info except high_level from showing
            if not high_level:
                # output the change information
                if proof:
                    print(f'{s1n} > {s2n}\nstraight\n{s2}\n')
                    print(f'{r1n} > {r2n}\nreverse\n{r2}\n')

            # string straight calculations
            s = f'min = {s2.min()}\nmax = {s2.max()}\nmin v max = {s2.min() - s2.max()}\nmean = {s2.mean()}'
            # list straight calculations
            s = s.split('\n')
            # string reverse calculations
            r = f'min = {r2.min()}\nmax = {r2.max()}\nmin v max = {r2.min() - r2.max()}\nmean = {r2.mean()}'
            # list reverse calculations
            r = r.split('\n')

            # track total amount won by (+straight -reverse)
            over_under = 0
            # track straight wins
            s_win = 0
            # track reverse wins
            r_win = 0
            
            # compare straight to reverse , value for value
            for i in range(len(s2)):
                
                # name of value
                n = s2[ i:i+1 ].index[0]
                # s value (float)
                sv = [ _ for _ in s2[ i:i+1]][0]
                # r value (float)
                rv = [_ for _ in r2[ i:i+1 ]][0]
                
                # determine which absolute value is closer to zero (0)
                closer = abs( sv ) < abs( rv )
                
                # output name , s value , r value , winner
                if closer == True:
                    # if we actually want this
                    if high_level==False:
                        # want proof
                        if proof:
                            print(f'{n}\ns = {sv}\nr = {rv}\nwinner = straight\n{rv-sv} less than reverse')
                    # add to over_under
                    a = abs(rv)-abs(sv)
                    if a < 0:
                        raise Exception(f'abs(rv)-abs(sv) < 0 ; { abs(rv)-abs(sv) } ; closer=={closer}')
                    over_under += a
                    # add to tally of straight wins
                    s_win += 1
                # sv is further away from 0 than rv
                elif closer == False:
                    if high_level==False:
                        # want proof
                        if proof:
                            print(f'{n}\ns = {sv}\nr = {rv}\nwinner = reverse\n{sv-rv} less than straight')
                    a = abs(sv)-abs(rv)
                    if a < 0:
                        raise Exception(f'abs(sv)-abs(rv) < 0 ; { abs(sv)-abs(rv) } ; closer=={closer}')
                    # subtract from over_under
                    over_under -= a
                    # add to tally of reverse winse
                    r_win += 1

            # high level info ONLY
            if high_level:
                if s_win > r_win:
                    if over_under > 0:
                        print(f'STRAIGHT WINS OUTRIGHT\n{s1n} >> {s2n}\nbetter than\n{r1n} >> {r2n}\n')
                        straight_outright_wins += 1
                    elif over_under < 0:
                        print(f'STRAIGHT wins win count (r={r_win} v s={s_win})\nbut REVERSE wins over_under ({over_under})\n{r1n} >> {r2n}\ninconclusive\n{s1n} >> {s2n}\n')
                        straight_win_count_wins += 1
                        reverse_over_under_wins += 1
                elif s_win < r_win:
                    if over_under < 0:
                        print(f'REVERSE WINS OUTRIGHT\n{r1n} >> {r2n}\nbetter than\n{s1n} >> {s2n}\n')
                        reverse_outright_wins += 1
                    elif over_under > 0:
                        print(f'REVERSE wins win count (r={r_win} v s={s_win})\nbut STRAIGHT wins over_under ({over_under})\n{r1n} >> {r2n}\ninconclusive\n{s1n} >> {s2n}\n')
                        reverse_win_count_wins += 1
                        straight_over_under_wins += 1
                else:
                    raise Exception(f'ERROR high_level ERROR s_win={s_win} r_win={r_win}')
            
            else:
                # determine who won more matchups
                if match_recap:
                    if s_win > r_win:
                        print(f'\nSTRAIGHT WINS\ntotal straight = {s_win}\ntotal reverse = {r_win}')
                    elif s_win < r_win:
                        print(f'\nREVERSE WINS\ntotal straight = {s_win}\ntotal reverse = {r_win}')
                    else:
                        raise Exception(f'TIE\ns_win = {s_win}\nr_win = {r_win}\nTIE')

                # determine who won over_under
                if difference: 
                    if over_under < 0:
                        print(f'REVERSE WINS\nover_under = {over_under}\n')
                    elif over_under > 0:
                        print(f'STRAIGHT WINS\nover_under = {over_under}\n')
                    elif over_under == 0:
                        raise Exception(f'TIE\nover_under = {over_under}\nTIE')

                # output calculations list vs list [min, max, mean] for compairson
                if calculations:
                    for n in range( len( s )):
                        s_larger = abs(float(s[ n ].split(' ').pop())) > abs(float(r[ n ].split(' ').pop()))
                        if s_larger == True:
                            print(f'st {s[ n ]}\nre {r[ n ]}\nstraight wins\n')
                        elif s_larger == False:
                            print(f'st {s[ n ]}\nre {r[ n ]}\nreverse wins\n')
    if high_level:
        print(f'straight_outright_wins = {straight_outright_wins}\nreverse_outright_wins = {reverse_outright_wins}\nstraight_win_count_wins = {straight_win_count_wins}\nreverse_win_count_wins = {reverse_win_count_wins}\nstraight_over_under_wins = {straight_over_under_wins}\nreverse_over_under_wins = {reverse_over_under_wins}')
        # tally up straight points
        straight_score = ( straight_outright_wins * 2 ) + straight_win_count_wins + straight_over_under_wins
        # tally up reverse points
        reverse_score = ( reverse_outright_wins * 2 ) + reverse_win_count_wins + reverse_over_under_wins
        # display scores
        print(f'straight_score = {straight_score}\nreverse_score = {reverse_score}')
        # return the winner
        if straight_score > reverse_score:
            return 'STRAIGHT IS CHAMPION'
        elif straight_score < reverse_score :
            return 'REVERSE IS CHAMPION'
        elif straight_score == reverse_score:
            return f'{straight_score} TIE {reverse_score}'
                        
            
                        
            