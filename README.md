# facebook_insights_api
This repo includes script to download Facebook Ad Reporting by calling the Facebook Insights API

## Prerequisites
- Facebook App ID
- Facebook App Secret
- Facebook Access Token

## How it works

This script calls the Facebook Insights API (docs: https://developers.facebook.com/docs/marketing-api/insights). After initializing a connection to API using credentials (stored in fb_secrets.py, not included in this repo) a list of ad accounts associated with the API connection/app is generated. The script then accesses a list of campaigns associated with each ad account. The insights API is called at the campaign level and information such as 'impressions', 'click', 'ctr', and 'spend' are pulled along with several others. For this use-case, the organizations this script was built for utilized Facebook Pixels to track events that happen outside of Facebook. They have a pixel included on their main web-page to help track conversions that stem from a Facebook session. The 'get_conversions' function created for this use-case extracts the number of conversions and adds 'website_leads' as a new field in the dataframe.

## How it is used

For now, this script is run daily and downloads all performance of interest from the previous week and updates a master file with the results. Ideally, this would be loaded into a data warehouse or comparable solution. However, the organization this was created for lacks the infrastructure and is currently using Sharepoint to store marketing related reporting and is where this file is stored and updated weekly. 
