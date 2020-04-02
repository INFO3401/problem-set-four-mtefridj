from utils import *
import pandas as pd
from pollingData import *
pol_data = localandCleanData('demo_poll_data.csv')
test_df = normalizeData(pol_data)
candidate_names = []
candidate_names = list(test_df.columns[3:11])
candidate_names.append('Undecided')


new_other_df = cleanSample(test_df)
already_correlated = []

for x in candidate_names:
    plotCandidate(str(x),test_df)
    print('Average polling stats for ' + x+ ':',statsPerCandidate(test_df,str(x)))
    #Biden is polling more averages then anyone else
    print('Average weighted polling stats for ' + x + ':', weightedStatsPerCandidate(new_other_df, str(x)))
    #Based on the new weigted polls, I still think that Biden will probably beat Sanders
    already_correlated.append(str(x))
    for y in candidate_names:
        if x == y or str(y) in already_correlated:
            continue
        else:
            print('Correlation for ' + x + ' and ' + y + ':', computeCorrelation(x,y,new_other_df))
            #Biden and Bloomberg has the strongest correlation with -0.68


st_df = superTuesday(new_other_df)
print('Average polling stats for Sanders:', statsPerCandidate(st_df, 'SandersST'))
print('Average polling stats for Biden:', statsPerCandidate(st_df, 'BidenST'))
print('Average weighted polling stats for Sanders:', weightedStatsPerCandidate(st_df, 'SandersST'))
print('Average weighted polling stats for Biden:', weightedStatsPerCandidate(st_df, 'BidenST'))
print('CI For Sanders ST ', statsPerCandidate(st_df,'SandersST') - computeConfidenceInterval(st_df['SandersST']), statsPerCandidate(st_df, 'SandersST') + computeConfidenceInterval(st_df['SandersST']))
print('CI For Biden ST ', statsPerCandidate(st_df,'BidenST') - computeConfidenceInterval(st_df['BidenST']), statsPerCandidate(st_df, 'BidenST') + computeConfidenceInterval(st_df['BidenST']))
#It did change my opinion that Sanders has a stronger chance then I predicted
print(runTTest(st_df['Biden'],st_df['Sanders']))
brand_new_data = localandCleanData('2020_democratic_presidential_nomination-6730.csv')
new_new = cleanSample(brand_new_data)
brand_new_data = new_new
print('Average polling stats for Sanders:', statsPerCandidate(brand_new_data, 'Sanders'))
print('Average polling stats for Biden:', statsPerCandidate(brand_new_data, 'Biden'))
print('Average weighted polling stats for Sanders:', weightedStatsPerCandidate(brand_new_data,'Sanders'))
print('Average weighted polling stats for Biden:', weightedStatsPerCandidate(brand_new_data, 'Biden'))
print('CI For Sanders ST ', statsPerCandidate(brand_new_data,'Sanders') - computeConfidenceInterval(brand_new_data['Sanders']), statsPerCandidate(brand_new_data, 'Sanders') + computeConfidenceInterval(brand_new_data['Sanders']))
print('CI For Biden ST ', statsPerCandidate(brand_new_data,'Biden') - computeConfidenceInterval(brand_new_data['Biden']), statsPerCandidate(brand_new_data, 'Biden') + computeConfidenceInterval(brand_new_data['Biden']))
print(runTTest(brand_new_data['Biden'],brand_new_data['Sanders']))
#My Prediction was way off and it seems that Biden is the clear winner