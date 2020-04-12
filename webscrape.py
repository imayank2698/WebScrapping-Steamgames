
#Importing required libraries

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import pandas as pd




#Creating a connection and grabbing the required page

my_url="https://store.steampowered.com/search/?filter=topsellers"
uClient=uReq(my_url)
page_html=uClient.read()
uClient.close()


#Parsing the html

page_soup=soup(page_html,"html.parser")




#Extracting the required data from the page


list_of_games=[]
containers=page_soup.findAll("a",{"class":"search_result_row ds_collapse_flag"})


for container in containers:
    
    #title of game
    
    title_container=container.findAll("div",{"class":"col search_name ellipsis"})
    title=title_container[0].span.text
    
    #date of release
    
    date_container=container.findAll("div",{"class":"col search_released responsive_secondrow"})
    if date_container[0].text =='':
        released_date='NA'
    else:
        released_date=date_container[0].text
        
    
    #review of game
    
    review_container=container.findAll("div",{"class":"col search_reviewscore responsive_secondrow"})
    review=review_container[0].span["data-tooltip-html"].replace('<br>','|')
    
    
    #originalprice of game
    
    original_price_container=container.findAll("div",{"class":"col search_price discounted responsive_secondrow"})
        
    if len(original_price_container)==0:
        original_price='NA'
        discounted_price=container.findAll("div",{"class":"col search_price responsive_secondrow"})[0].text.strip()
    
    else:
        original_price = original_price_container[0].strike.text
        dp=original_price_container[0].text.split("₹")
        dp1 = dp[2].strip()
        discounted_price="₹ "+dp1
    
    
    #discountpercent
    
    discount_container=container.findAll("div",{"class":"col search_discount responsive_secondrow"})
    
    try:
        discount_percent=discount_container[0].span.text
    except AttributeError:
        discount_percent="NA"
    
    content=(title,released_date,review,original_price,discounted_price,discount_percent)
    list_of_games.append(content)
    
    #<<Test purposes>>#
    #print(title)
    #print(released_date)
    #print(review)
    #print(original_price)
    #print(discounted_price)
    #print(discount_percent)
    
    
    #print('\n')
    
    
    

#Initialising the dataframe and uploading the extracted data in it


game_columns=['Name','Date of release','Review','Original Price','New Price','Discount']
steam_games=pd.DataFrame(columns=game_columns,data=list_of_games)

#Storing the data in csv file
steam_games.to_csv('steamgames.csv')
