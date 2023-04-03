# https://developers.facebook.com/docs/marketing-api/insights

from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.user import User
import pandas as pd
import fb_secrets

# initializing connection to facebook API using credentials
FacebookAdsApi.init(fb_secrets.app_id, fb_secrets.app_secret, fb_secrets.access_token)

# getting account details for 'me'
me = User(fbid='me')

# my_accounts holds list of accounts associated with 'me'
my_accounts = list(me.get_ad_accounts())

# establishing df_all as empty dataframe that will hold results from all campaigns & accounts
df_all = pd.DataFrame()

# 'summarize_campaign' function accesses each campaign and returns fields & params requested in function
def summarize_campaign(camp_id):
    
    params = {'level':'ad', 
           'date_preset': 'this_year',
           'use_unified_attribution_setting': True,
           'time_increment':1,
            }
    
    fields = ['account_name',
              'campaign_name',
              'adset_name',
              'ad_name',
              'actions',
              'impressions',
              'clicks',
              'ctr',
              'spend']
    
    insights = Campaign(camp_id).get_insights(params = params, fields = fields)
    
    df_camp = pd.DataFrame(insights)
    
    return df_camp


# 'get_conversions' function accesses the 'action_type' field returned from API & extracts FB Pixel Conversions
def get_conversions(df):
    
    # 'conversions_list' stores conversion values from each row based on conditions defined below
    conversions_list = []
    
    # iterates each value in 'actions' column ('action_type') from FB API documentation
    for row in df['actions']:
        
        # sets 'conversions' equal to 0 if the row equals 'None'
        if row == 'None':
            conversions = 0

        else:
            
            # 'offsite_conversion.fb_pixel_lead' is the action in FB representing a conversion. This value is what needs to be extracted
            value = 'offsite_conversion.fb_pixel_lead'
            
            # checking each dictionary (each value in column contains list of dictionaries)
            # if 'offsite_conversion.fb_pixel_lead' is not a value in any of the rows dictionaries, then conversions is set to 0.
            if any(value in d.values() for d in row) == False:

                conversions = 0

            else:
                
                # if 'offsite_conversion.fb_pixel_lead' is a value in the list of dictionaries, then within that same dictionary, return the value
                for dictionary in row:
                    if dictionary['action_type'] == value:
                        conversions = dictionary['value']
        
        # adds whatever 'conversion' is set to the 'conversions_list'
        conversions_list.append(conversions)
    
    # creates 'website_conversions' column to df
    df['website_leads'] = conversions_list
    
    # converts 'website_conversions' to integer
    df['website_leads'] = df['website_leads'].astype(int)
    
    
for account in my_accounts:
    my_account = AdAccount(account['id'])
    campaigns = my_account.get_campaigns()
    
    for campaign in campaigns:
    
        df_camp = summarize_campaign(campaign['id'])
        
        df_all = pd.concat([df_all, df_camp])


# below performs series of transformations to data
df_all['actions'].fillna('None', inplace = True)
df_all['clicks'] = df_all['clicks'].astype(int)
df_all['ctr'] = df_all['ctr'].astype(float)
df_all['date_start'] = pd.to_datetime(df_all['date_start'])
df_all['date_stop'] = pd.to_datetime(df_all['date_stop'])
df_all['spend'] = df_all['spend'].astype(float)
df_all['impressions'] = df_all['impressions'].astype(int)
df_all.rename({'date_stop':'date'}, inplace = True, axis = 1)

# calling 'get_conversions' function for df_all
get_conversions(df_all)

# dropping a few more unneeded columns after 'get_conversions' runs
df_all.drop(['date_start', 'actions'], inplace = True, axis = 1)

# putting final clean file to excel repo
df_all.to_excel('2023.xlsx',index=False)

# loading in previous full report
df_hist = pd.read_excel('fb_ad_performance.xlsx')

df_all = pd.concat([df_hist, df_all])
df_all.drop_duplicates(inplace = True, keep = 'last')

# putting final clean file to excel repo
df_all.to_excel('fb_ad_performance.xlsx', index=False)