class Univariate():

    def quanqual(dataset):
        quan=[]
        qual=[]
        for ColumnName in dataset.columns:
            if (dataset[ColumnName].dtype=='O'):
                qual.append(ColumnName)
            else:
                quan.append(ColumnName)
        return quan,qual

    def descriptive(dataset,quan):
        import pandas as pd
        import numpy as np
        descriptive=pd.DataFrame(index=['Mean','Median','Mode','Q1-25%','Q2-50%','Q3-75%','99%','Q4-100%','IQR','1.5 RULE','Lesser','Greater','Skewness','Kurtosis','Min','Max'],columns=quan)
        for ColumnName in quan:
            descriptive[ColumnName]['Mean']=dataset[ColumnName].mean()
            descriptive[ColumnName]['Median']=dataset[ColumnName].median()
            descriptive[ColumnName]['Mode']=dataset[ColumnName].mode()[0]
            descriptive[ColumnName]['Q1-25%']=dataset.describe()[ColumnName]['25%']
            descriptive[ColumnName]['Q2-50%']=dataset.describe()[ColumnName]['50%']
            descriptive[ColumnName]['Q3-75%']=dataset.describe()[ColumnName]['75%']
            descriptive[ColumnName]['99%']=np.percentile(dataset[ColumnName],99)
            descriptive[ColumnName]['Q4-100%']=dataset.describe()[ColumnName]['max']
            descriptive[ColumnName]['IQR']=descriptive[ColumnName]['Q3-75%']-descriptive[ColumnName]['Q1-25%']
            descriptive[ColumnName]['1.5 RULE']=1.5*descriptive[ColumnName]['IQR']
            descriptive[ColumnName]['Lesser']=descriptive[ColumnName]['Q1-25%']-descriptive[ColumnName]['1.5 RULE']
            descriptive[ColumnName]['Greater']=descriptive[ColumnName]['Q3-75%']+descriptive[ColumnName]['1.5 RULE']
            descriptive[ColumnName]['Min']=dataset[ColumnName].min()
            descriptive[ColumnName]['Max']=dataset[ColumnName].max()
            descriptive[ColumnName]['Skewness']=dataset[ColumnName].skew()
            descriptive[ColumnName]['Kurtosis']=dataset[ColumnName].kurtosis()
        return descriptive

    def finding_outliers(quan,descriptive):
        lesser=[]
        greater=[]
        for ColumnName in quan:
            if(descriptive[ColumnName]['Min']<descriptive[ColumnName]['Lesser']):
                lesser.append(ColumnName)
            if(descriptive[ColumnName]['Max']>descriptive[ColumnName]['Greater']):
                greater.append(ColumnName)
        return lesser,greater

    def replacing_outliers(dataset,descriptive,lesser,greater):
        for ColumnName in lesser:
            dataset[ColumnName][dataset[ColumnName]<descriptive[ColumnName]['Lesser']]=descriptive[ColumnName]['Lesser']
        for ColumnName in greater:
            dataset[ColumnName][dataset[ColumnName]>descriptive[ColumnName]['Greater']]=descriptive[ColumnName]['Greater'] 
        return lesser,greater

    def FreqTable(dataset,ColumnName):
        import pandas as pd
        FreqTable=pd.DataFrame(columns=('Unique_values','Frequency','Relative_Frequency','Cumsum'))
        FreqTable['Unique_values']=dataset[ColumnName].value_counts().index
        FreqTable['Frequency']=dataset[ColumnName].value_counts().values
        FreqTable['Relative_Frequency']=FreqTable['Frequency']/len(dataset[ColumnName].value_counts())
        FreqTable['Cumsum']=FreqTable['Relative_Frequency'].cumsum()
        return FreqTable 