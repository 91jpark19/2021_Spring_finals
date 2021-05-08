import pandas as pd
import re
from scipy import stats
import numpy
import seaborn as sns
import matplotlib.pyplot as plt

def preprocess_civil(filename)->pd.DataFrame:
    """
    Reads given filename and places the right column name for even rows and odd rows.
    After giving the right column name, merge even rows and odd rows to have them in one row.

    :param filename: filename as a string like: "09905-0002-Data.txt"
    :return: cleaned pd.DataFrame

    >>> preprocess_civil("09905-0002-Data.txt")['war number'].iloc[0]
    601

    >>> preprocess_civil("09905-0002-Data.txt")['fatalities'].iloc[0]
    7000
    """
    data = pd.read_csv(filename, header=None, delimiter=r"\s+")
    even = data.iloc[::2] #even rows dataframe
    odd = data.iloc[1::2] #odd rows dataframe
    odd = odd.iloc[:, :-4] #get rid of columns of NAs
    even.columns=[
    'war number', 'Singer-Small country code', 'year of war start', 'month of war start', 'day of war start',
    'year of war end', 'month of war end', 'day of war end', 'year of second war start', 'month of second war start',
    'day of second war start', 'year of second war end', 'month of second war end', 'day of second war end',
    'year of third war start', 'month of third war start', 'day of third war start', 'year of third war end',
    'month of third war end', 'day of third war end'
    ]
    odd.columns=[
    'outside intervention', 'fought in member of central sub-system', 'fought in major power', 'outcome of war',
    'western hemisphere', 'europe', 'africa', 'middle east', 'asia', 'oceania', 'fatalities', 'duration',
    'population before war', 'military', 'system membership', 'intervened by'
    ]
    even=even.reset_index(drop=True)
    odd = odd.reset_index(drop=True)
    civilwar = even.merge(odd, left_index=True, right_index=True)
    return civilwar

def preprocess_civilcodebook(filename) -> pd.DataFrame:
    """
    Read codebook to map the 'Singer-Small country code' to the country name

    :param filename: filename as a string like "09905-Codebook.txt"
    :return: cleaned pd.DataFrame

    >>> preprocess_civilcodebook("09905-Codebook.txt")['country'].iloc[0]
    'SPAIN'

    >>> preprocess_civilcodebook("09905-Codebook.txt")['war number'].iloc[0]
    601

    """
    with open(filename) as f:
        lines=f.readlines()
        x1=[]
        x2=[]
        for i in lines[1316:1467]:
            try:
                start_index=i.index('   ')
                end_index=i.index('(')
            except ValueError:
                continue
            x1.append(i[1:4])
            x2.append(re.sub(r" ?\[[^)]+\]", "", i[start_index:end_index].strip()))
            df=pd.DataFrame(x1, x2, columns=['war number'])
            df.reset_index(inplace=True)
            df=df.rename(columns={'index': 'country'})
            df['war number'] = df['war number'].astype(int)
        return df

def merge_civil_codebook(civil, codebook)->pd.DataFrame:
    """
    Takes cleaned civil war data and codebook and merge two DataFrames.
    In civil war data, the year was recorded without 1000.
    For instance, 1801 was recorded as 801.
    For compatibility, this function add 1000 to changes the year into 1801.

    :param civil: a pd.DataFrame from preprocess_civil() function
    :param codebook: a pd.DataFrame from preprocess_civilcodebook() function
    :return: a merged pd.DataFrame

    >>> merge_civil_codebook(civil, df)['year of war start'].iloc[0]
    1821

    >>> merge_civil_codebook(civil, df)['year of war end'].iloc[0]
    1823
    """

    #In the codebook, warnumber 601 is not recorded but it exists in the data
    #We lose 2 records. In total, we have 202 cases
    coded=civil.merge(codebook, left_on='war number', right_on='war number')
    #change the year
    coded['year of war start'] += 1000
    coded['year of war end'] += 1000
    for idx, row in coded.iterrows():
        if row['year of second war end'] != 0:
            coded['year of war end'].iloc[idx] = row['year of second war end'] + 1000
        else:
            continue
    coded=coded.drop(columns=['year of second war start', 'year of second war end',
                              'year of third war start', 'year of third war end'], axis=1)
    return coded

def control_country(coded)-> df.DataFrame:
    """
    Takes cleaned pd.DataFrame from merge_civil_codebook() and control the country name
    1) Correct typos
    2) Match the country names between pd.DataFrame from democracy data
    e.g., LAOS into Lao Pdr, SOUTH YEMEN into Yemen Pdr

    :param coded: a pd.DataFrame after merging codebook and civil data
    :return: a pd.DataFrame changed the country name

    >>> control_country(coded)['country'].iloc[54]
    'RUSSIAN FEDERATION'

    """
    for idx, val in coded.iterrows():
        #for Austria-hungary I splited into two countries. So we have 203 records
        if val['country']=='AUSTRIA-HUNGARY':
            val[4]='AUSTRIA'
            coded.loc[len(coded)]=val
            val[4]='HUNGARY'
            coded.loc[len(coded)]=val
            coded=coded.drop(idx)
        if val['country']=='BRUNDI':
            val[4]='BURUNDI'
            coded.loc[idx]=val
        if val['country']=='FINNISH':
            val[4]='FINLAND'
            coded.loc[idx]=val
        if val['country']=='RUMANIA':
            val[4]='ROMANIA'
            coded.loc[idx]=val
        if val['country']=='TURKEY/OTTOMAN EMPIRE':
            val[4]='TURKEY'
            coded.loc[idx]=val
        if val['country']=='UGANDAN':
            val[4]='UGANDA'
            coded.loc[idx]=val
        if val['country']=='RUSSIA/SOVIET UNION':
            val[4]='RUSSIA'
            coded.loc[idx]=val
        if val['country']=='KAMPUCHEA':
            val[4]='CAMBODIA'
            coded.loc[idx]=val
        #name matching with democracy dataset
        if val['country']=='BOSNIA':
            val[4]='Bosnia and Herzegov'
            coded.loc[idx]=val
        if val['country']=='BURMA':
            val[4]='Myanmar'
            coded.loc[idx]=val
        if val['country']=='IRAN':
            val[4]='Iran, Islamic Rep'
            coded.loc[idx]=val
        if val['country']=='LAOS':
            val[4]='Lao Pdr'
            coded.loc[idx]=val
        if val['country']=='RUSSIA':
            val[4]='Russian Federation'
            coded.loc[idx]=val
        if val['country']=='SOUTH YEMEN':
            val[4]='Yemen Pdr'
            coded.loc[idx]=val
        if val['country']=='UNITED STATES OF AMERICA':
            val[4]='United States'
            coded.loc[idx]=val
        if val['country']=='TAKJIKISTAN':
            val[4]='Tajikistan'
            coded.loc[idx]=val
        if val['country']=='VIETNAM, REPUBLIC OF':
            val[4]='Vietnam, North'
            coded.loc[idx]=val
        if val['country']=='YEMEN ARAB REPUBLIC':
            val[4]='Yemen, Rep.'
            coded.loc[idx]=val
    coded['country']=coded['country'].str.upper()
    coded=coded.rename(columns={'country':'ctryname'})
    coded.reset_index(drop=True)
    return coded

def preprocess_democracy(filename)-> pd.DataFrame:
    """
    Reads filename and if democracy index is NA and liberty index is NA, get rid of the rows.

    :param filename: a string like "20440-0001-Data.tsv"
    :return: a cleaned pd.DataFrame

    >>> preprocess_democracy("20440-0001-Data.tsv")['ctryname'].loc[15634]
    'FIJI'

    """
    #SARDINA is not in the democracy data file
    democracy=pd.read_csv(filename, sep='\t')
    democracy['ctryname']=democracy['ctryname'].str.upper()
    ###delete
    democ_index=democracy[democracy['democ']!='-99']
    democ_index=democ_index[democ_index['democ']!='-88']
    democ_index=democ_index[democ_index['democ']!='-77']
    democ_index=democ_index[democ_index['democ']!='-66']
    democ_index=democ_index[democ_index['democ']!='-55']
    democ_index=democ_index[democ_index['democ']!= ' ']
    ###
    democ_index=democ_index[democ_index['liberty']!= ' ']
    democ_index=democ_index[democ_index['liberty']!= '-99']
    return democ_index

def join_df_democ(coded, democ_index, restore_year):
    dfcols=['ctryname', 'score before year', 'score before', 'fatal', 'pop', 'ratio', 'score after year', 'score after', 'delta']
    df=pd.DataFrame(columns=dfcols)
    for idx, val in coded.iterrows():
        if val['ctryname'] in democ_index['ctryname'].values:
            try:
                df=df.append(
                pd.Series(
                    [val['ctryname'],
                    val['year of war start'],
                    democ_index[(democ_index['ctryname']==val['ctryname']) & (democ_index['year']==val['year of war start'])]['democ'].to_numpy()[0],
                    val['fatalities'],
                    democ_index[(democ_index['ctryname']==val['ctryname']) & (democ_index['year']==val['year of war start'])]['poptotal'].to_numpy()[0],
                    0,
                    val['year of war end']+restore_year,
                    democ_index[(democ_index['ctryname']==val['ctryname']) & (democ_index['year']==val['year of war end']+restore_year)]['democ'].to_numpy()[0],
                    0
                    ], index=dfcols), ignore_index=True)
            except IndexError:
                continue
    for idx, val in df.iterrows():
        val['pop']=val['pop']+'000'
        try:
            df['score before'][idx]=int(df['score before'][idx][0])
        except IndexError:
            df['score before'][idx]=0
        try:
            df['score after'][idx]=int(df['score after'][idx][0])
        except IndexError:
            df['score after'][idx]=0
        try:
            val['ratio']=float(val['fatal'])/float(val['pop'])
        except:
            val['ratio']=0
    df['delta']=df['score after']-df['score before']
#     df['pop']=df['pop']
    return df

def join_df_liberty(coded, democ_index, restore_year):
    dfcols=['ctryname', 'score before year', 'score before', 'fatal', 'pop', 'ratio', 'score after year', 'score after', 'delta']
    df=pd.DataFrame(columns=dfcols)
    for idx, val in coded.iterrows():
        if val['ctryname'] in democ_index['ctryname'].values:
            try:
                df=df.append(
                pd.Series(
                    [val['ctryname'],
                    val['year of war start'],
                    democ_index[(democ_index['ctryname']==val['ctryname']) & (democ_index['year']==val['year of war start'])]['liberty'].to_numpy()[0],
                    val['fatalities'],
                    democ_index[(democ_index['ctryname']==val['ctryname']) & (democ_index['year']==val['year of war start'])]['poptotal'].to_numpy()[0],
                    0,
                    val['year of war end']+restore_year,
                    democ_index[(democ_index['ctryname']==val['ctryname']) & (democ_index['year']==val['year of war end']+restore_year)]['liberty'].to_numpy()[0],
                    0
                    ], index=dfcols), ignore_index=True)
            except IndexError:
                continue
    for idx, val in df.iterrows():
        val['pop']=val['pop']+'000'
        try:
            val['ratio']=float(val['fatal'])/float(val['pop'])
        except:
            val['ratio']=0
    df['delta']=df['score after'].astype(float)-df['score before'].astype(float)
    df['pop']=df['pop']
    return df

civil=preprocess_civil("09905-0002-Data.txt")[['war number', 'fatalities', 'year of war start',
               'year of war end', 'year of second war start',
               'year of second war end', 'year of third war start',
               'year of third war end']]

democ_index=preprocess_democracy("20440-0001-Data.tsv")

df=preprocess_civilcodebook("09905-Codebook.txt")

coded=merge_civil_codebook(civil, df)
coded=control_country(coded)

ang=coded.groupby(['ctryname','fatalities']).size()
ang=pd.DataFrame(ang, columns=['counts'])
ang.reset_index(inplace=True)
ang['total']=ang['fatalities'].astype(int) * ang['counts'].astype(int)
fatalities_per_country=pd.DataFrame(ang.groupby('ctryname')['total'].sum().reset_index())
fatalities_per_country.sort_values(by='total', ascending=False)

for idx, val in fatalities_per_country.iterrows():
    fatalities_per_country['t-test'].loc[idx]="{:.3f}".format(stats.ttest_ind(democ_index[democ_index['ctryname']==val['ctryname']]['liberty'].astype(int),
               democ_index[democ_index['ctryname']==val['ctryname']]['democ'].astype(int))[1])

df_democ5=join_df_democ(coded, democ_index, 5)
df_democ10=join_df_democ(coded, democ_index, 10)
df_democ20=join_df_democ(coded, democ_index, 20)

df_liberty5=join_df_liberty(coded, democ_index, 5)
df_liberty10=join_df_liberty(coded, democ_index, 10)
df_liberty20=join_df_liberty(coded, democ_index, 20)

x=df_democ20['ratio'].to_numpy().astype('int64')
y=df_democ20['delta'].to_numpy().astype('int64')
sns.scatterplot('ratio', 'delta', data=df_democ20, hue='ctryname')
plt.legend(bbox_to_anchor=(1,0), loc='lower left', ncol=1)
plt.show()

plt.plot(x, y, 'o', label='original data')
plt.plot(x, res.intercept + res.slope*x, 'r', label='fitted line')
plt.legend()
plt.show()

res=stats.libregress(x, y)
res.slope
res.pvalue