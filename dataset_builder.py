'''
This is where we will gather all data for the graphs and tables.
'''
import pandas as pd


def build_table():
    '''This function builds the table for the top right quadrant of the storyboard (i.e. key stats)'''
    # get current month for use as column heading
    month = pd.Timestamp.now().strftime('%B %Y')
    # initialise dataframe
    df = pd.DataFrame(columns=['Summary Area', month, 'Target', 'Variance'])
    # each column is a dictionary
    stat_mand = {'Summary Area':'Statutory and Mandatory Training', month:'99%', 'Target':'99.9%', 'Variance':'-0.9%'}
    absence = {'Summary Area':'Absence', month:'2.11', 'Target':'4%', 'Variance':'1.89%'}
    bank_usage = {'Summary Area':'Bank Usage', month:'18 WTE', 'Target':'10 WTE', 'Variance':'+8 WTE'}
    KSF = {'Summary Area':'KSF', month:'70%', 'Target':'85%', 'Variance':'-15%'}
    inductions = {'Summary Area': 'Inductions', month:'70%', 'Target':'100%', 'Variance':'-30%'}
    suspensions = {'Summary Area':'Suspensions', month:'0', 'Target':'N/A', 'Variance':'N/A'}
    ER_Cases = {'Summary Area':'Active ER Cases', month:'1', 'Target':'N/A', 'Variance':'N/A'}
    attendance_cases = {'Summary Area':'Active Attendance Cases', month:'1', 'Target':'N/A', 'Variance':'N/A'}

    # append each dictionary to dataframe
    for i in [stat_mand,absence,bank_usage, KSF, inductions, suspensions, ER_Cases, attendance_cases]:
        df = df.append(i, ignore_index=True)

    return df
