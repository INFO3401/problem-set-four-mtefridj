from new_utils import *
import pandas as pd
import matplotlib.pyplot as plt
def normalizeData(df):
    new_df = df
    new_df['Undecided'] = 0
    for i, data in new_df.iterrows():
        total_sum = data['Sanders':'Steyer'].values
        new_total = 0
        for x in total_sum:
            if x == '--':
                x = 0
            new_total += float(x)
        new_df.iloc[i, -1] = 100 - new_total
    return new_df
def plotCandidate(name, df):
    other_df = df.groupby('Poll').mean().reset_index()
    new_name = str(name)
    new_df= other_df[['Poll', new_name]]
    ax = plt.gca()
    plt.scatter(new_df['Poll'],new_df[new_name])
    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right', fontsize='x-small')
    plt.title(label=new_name + ' Polls')
    plt.show()
def statsPerCandidate(df, name):
    avg = df[name].mean()

    return avg
def cleanSample(df):
    new_df = df
    new_df['Sample Type'] = ''
    new_df['Sample Size'] = 0
    for index, rows in new_df.iterrows():
        sample_type = rows['Sample'][-2:]
        sample_size = rows['Sample'][:len(rows['Sample']) - 2].strip()
        rows['Sample Type'] = sample_type
        rows['Sample Size'] = int(sample_size)
        new_df.iloc[index] = rows
    return new_df

def computePollWeight(df, poll_name):
    total_sample = df['Sample Size'].sum()
    poll_weighted = df.groupby('Poll')['Sample Size'].mean().reset_index()
    actual_poll = poll_weighted[poll_weighted['Poll'] == poll_name]
    weight = float(actual_poll['Sample Size']) / float(total_sample)
    return weight
def weightedStatsPerCandidate(df, cand_name):
    poll_candidate = df.groupby('Poll')[cand_name].mean().reset_index()
    for index, c in poll_candidate.iterrows():
        poll_weight = computePollWeight(df, c['Poll'])
        cand_score = c[cand_name]
        c[cand_name] = poll_weight * cand_score
        poll_candidate.iloc[index] = c
    return poll_candidate[cand_name].mean()
def computeCorrelation(cand1, cand2, df):
    cand1_data = df[cand1]
    cand2_data = df[cand2]
    correlation = cand1_data.corr(cand2_data)
    return correlation
def superTuesday(df):
    new_df = df
    new_df['BidenST'] = 0
    new_df['SandersST'] = 0
    candidates_name = ['Bloomberg', 'Warren', 'Buttigieg', 'Klobuchar', 'Gabbard', 'Steyer']
    for i, data in new_df.iterrows():
        total_sand = data['Sanders']
        total_biden = data['Biden']
        for z in candidates_name:
            corr_sand = computeCorrelation('Sanders',z,new_df)
            corr_biden = computeCorrelation('Biden',z,new_df)
            if corr_sand > corr_biden:
                total_sand += data[z]
            elif corr_biden > corr_sand:
                total_biden += data[z]
        data['SandersST'] = total_sand
        data['BidenST'] = total_biden
        new_df.iloc[i] = data
    return new_df
