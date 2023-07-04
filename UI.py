import pickle
import pandas as pd
import math
import streamlit as st
import numpy as np
st.title("Start-Up Success Prediction")

col1, col2 = st.columns(2)
country = col1.selectbox(
    "Country",
    ('AFG', 'AGO', 'ALB', 'AND', 'ANT', 'ARA', 'ARE', 'ARG', 'ARM', 'ATG', 'AUS', 'AUT', 'AZE', 'BDI', 'BEL', 'BEN', 'BGD', 'BGR', 'BHR', 'BHS', 'BIH', 'BLR', 'BLZ', 'BMU', 'BOL', 'BRA', 'BRB', 'BRN', 'BWA', 'CAN', 'CHE', 'CHL', 'CHN', 'CIV', 'CMR', 'COL', 'CRI', 'CSS', 'CUB', 'CYM', 'CYP', 'CZE', 'DEU', 'DMA', 'DNK', 'DOM', 'DZA', 'ECU', 'EGY', 'ESP', 'EST', 'ETH', 'FIN', 'FRA', 'FST', 'GBR', 'GEO', 'GHA', 'GIB', 'GLP', 'GRC', 'GRD', 'GTM', 'HKG', 'HRV', 'HTI', 'HUN', 'IDN', 'IND', 'IOT', 'IRL', 'IRN', 'IRQ', 'ISL', 'ISR', 'ITA', 'JAM', 'JOR', 'JPN', 'KAZ', 'KEN', 'KGZ', 'KOR', 'KWT', 'LAO', 'LBN', 'LIE', 'LKA', 'LTU', 'LUX', 'LVA', 'MAR', 'MCO', 'MDA', 'MDG', 'MDV', 'MEX', 'MKD', 'MLT', 'MMR', 'MTQ', 'MUS', 'MYS', 'NAM', 'NCL', 'NFK', 'NGA', 'NLD', 'NOR', 'NPL', 'NRU', 'NZL', 'OMN', 'PAK', 'PAN', 'PCN', 'PER', 'PHL', 'POL', 'PRI', 'PRK', 'PRT', 'PRY', 'PST', 'QAT', 'REU', 'ROM', 'RUS', 'RWA', 'SAU', 'SDN', 'SEN', 'SGP', 'SLE', 'SLV', 'SMR', 'SOM', 'SUR', 'SVK', 'SVN', 'SWE', 'SWZ', 'SYC', 'SYR', 'THA', 'TTO', 'TUN', 'TUR', 'TWN', 'TZA', 'UGA', 'UKR', 'UMI', 'URY', 'USA', 'UZB', 'VCT', 'VEN', 'VGB', 'VIR', 'VNM', 'YEM', 'ZAF', 'ZMB', 'ZWE')
)
category = col2.selectbox(
    "Category",
    ('advertising', 'analytics', 'automotive', 'biotech', 'cleantech', 'consulting', 'design', 'ecommerce', 'education', 'enterprise', 'fashion', 'finance', 'games_video', 'government', 'hardware', 'health', 'hospitality', 'legal', 'local', 'manufacturing', 'medical', 'messaging', 'mobile', 'music', 'nanotech', 'network_hosting', 'news', 'nonprofit', 'other', 'pets', 'photo_video', 'public_relations', 'real_estate', 'search', 'security', 'semiconductor', 'social', 'software', 'sports', 'transportation', 'travel', 'web')
)

foundationDate = st.date_input(
    "Foundation Date"
)

col7,col8,col9 = st.columns(3)
investmentRounds = col7.number_input("Investment Rounds", step = 1)
timeInInvestment = -1
if investmentRounds > 0 :
    lastInvestmentOn = col8.date_input(
        "Last Investment On"
    )
    investedCompanies = col9.number_input("Invested Companies", step = 1)
    timeInInvestment = abs((lastInvestmentOn - foundationDate).days)
    try :
        a = math.exp(timeInInvestment)
    except OverflowError :
        a = float('inf')
    investmentAffinity = (investedCompanies * investmentRounds) / a

else :
    investmentAffinity = 0



fundingRounds = col7.number_input("Funding Rounds", step = 1)
timeInFunding = -1
if fundingRounds > 0 :
    lastFundingOn = col8.date_input(
        "Last Funding On"
    )
    fundingRaised = col9.number_input("Funding Raised ($)", step = 1)
    timeInFunding = abs((lastFundingOn - foundationDate).days)
    try :
        b = math.exp(timeInFunding)
    except OverflowError :
        b = float('inf')
    fundingAffinity = (fundingRaised * fundingRounds) / b
else :
    fundingAffinity = 0


milestones = col1.number_input("Achieved Milestones", step = 1)
timeInMilestone = -1
if milestones > 0 :
    lastMilestoneOn = col2.date_input(
        "Last Milestone On"
    )
    timeInMilestone = abs((lastMilestoneOn - foundationDate).days)

relationships = st.number_input(" Strong Relationships Start-Up Has", step = 1)

data = pd.read_csv("finaldata.csv")

min_funding = min(data["fundingaffinity"])
max_funding = max(data["fundingaffinity"])
fundingAffinity = (fundingAffinity - min_funding ) / (max_funding - min_funding)

min_time = min(data["timeinmilestone"])
max_time = max(data["timeinmilestone"])
timeInMilestone = (timeInMilestone - min_time) / (max_time)

min_relation = min(data["relationships"])
max_relation = max(data["relationships"])
relationships = (relationships - min_relation) / (max_relation - min_relation)

countryFreq = pd.read_csv("countrymeta.csv")
countryFrequency = countryFreq.loc[countryFreq["objectsDF$country_code"].eq(country)]["total"] / countryFreq["total"].sum()
country = countryFrequency.values[0]


categoryFreq = pd.read_csv("category.csv")
categoryFrequency = categoryFreq.loc[categoryFreq["Category"].eq(category)]["total"] / categoryFreq["total"].sum()
category = categoryFrequency.values[0]

topredict = {"countryfreq" : [country] ,"categoryfreq" : [category],"investmentaffinity" : [investmentAffinity],"fundingaffinity" : [fundingAffinity],"milestones" : [milestones],"timeinmilestone" : [timeInMilestone],"relationships" : [relationships]}
topredict = pd.DataFrame(topredict)

if st.button("Submit"):
    inputdata = np.array([[country, category, investmentAffinity, fundingAffinity, milestones, timeInMilestone, relationships]])
    logreg = pickle.load(open('lrmodel.pkl','rb'))
    if logreg.predict(inputdata) == 1 :
        st.title("Chances are HIGH !!!!")
    else :
        st.title("Chances are LOW !!!!")