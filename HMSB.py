import requests
from urllib.request import urlopen
from requests.models import parse_header_links
import simplejson as json
from discord_webhook import DiscordWebhook, DiscordEmbed
import time

def HM():
    with open('config.json') as f:
        conf = json.load(f)
        
    delay = conf['delay_mins']
    webhook_url = conf['webhookURL']
    
    records = {}
    
    inputFile = input("Enter text file URL :")
    urlsFile = urlopen(inputFile)
    
    while True:
        urlKeys = []
        for line in urlsFile:
            urlKeys.append(line.decode('utf-8').replace('\n', '').split('||'))
        
        for urlKey in urlKeys:
            res = requests.get(f"https://api.helium.io/v1/hotspots/{urlKey[0]}")
            statusCode = res.status_code
            res = res.json()
            
            if statusCode == 200:
                if urlKey[0] not in records:
                    records[urlKey[0]] = {'deName': urlKey[1], 'online': str(res['data']['status']['online']), 'listen_addrs': str(res['data']['status']['listen_addrs']), 'reward_scale': str(res['data']['reward_scale'])}
                    
                    webhook = DiscordWebhook(url=webhook_url)
                    embed = DiscordEmbed(title='HeliumBOT : Added to records', color=242424)
                    embed.add_embed_field(name='Device Address', value=urlKey[0])
                    embed.add_embed_field(name='Device Nickname', value=urlKey[1])
                    embed.add_embed_field(name='online', value=str(res['data']['status']['online']))
                    embed.add_embed_field(name='listen_addrs', value=str(res['data']['status']['listen_addrs']))
                    embed.add_embed_field(name='reward_scale', value=str(res['data']['reward_scale']))
                        
                    embed.set_footer(text='Sudobotz.com')
                    embed.set_timestamp()
                    webhook.add_embed(embed)
                    webhook.execute()
                    
                    time.sleep(1)
                    
                elif urlKey[0] in records:
                    if records[urlKey[0]]['online'] != str(res['data']['status']['online']):
                        newOnline = True
                    else:
                        newOnline = False
                    if records[urlKey[0]]['listen_addrs'] != str(res['data']['status']['listen_addrs']):
                        newAddrs = True
                    else:
                        newAddrs = False
                    if records[urlKey[0]]['reward_scale'] != str(res['data']['reward_scale']):
                        newReward = True
                    else:
                        newReward = False
                        
                    if newOnline == True or newAddrs == True or newReward == True:
                        webhook = DiscordWebhook(url=webhook_url)
                        embed = DiscordEmbed(title='HeliumBOT : New Update', color=242424)
                        embed.add_embed_field(name='Device Address', value=urlKey[0])
                        embed.add_embed_field(name='Device Nickname', value=urlKey[1])
                        
                        if newOnline == True:
                            embed.add_embed_field(name='online (Previous)', value=records[urlKey[0]]['online'])
                            embed.add_embed_field(name='online (New)', value=str(res['data']['status']['online']))
                        else:
                            embed.add_embed_field(name='Online', value=records[urlKey[0]]['online'])
                            
                        if newAddrs == True:
                            embed.add_embed_field(name='listen_addrs (Previous)', value=records[urlKey[0]]['listen_addrs'])
                            embed.add_embed_field(name='listen_addrs (New)', value=str(res['data']['status']['listen_addrs']))
                        else:
                            embed.add_embed_field(name='listen_addrs', value=records[urlKey[0]]['listen_addrs'])
                            
                        if newReward == True:
                            embed.add_embed_field(name='reward_scale (Previous)', value=records[urlKey[0]]['reward_scale'])
                            embed.add_embed_field(name='reward_scale (New)', value=str(res['data']['reward_scale']))
                        else:
                            embed.add_embed_field(name='reward_scale', value=records[urlKey[0]]['reward_scale'])
                            
                        embed.set_footer(text='Sudobotz.com')
                        embed.set_timestamp()
                        webhook.add_embed(embed)
                        webhook.execute()
                        
                        records[urlKey[0]] = {'online': str(res['data']['status']['online']), 'listen_addrs': str(res['data']['status']['listen_addrs']), 'reward_scale': str(res['data']['reward_scale'])}
                    else:
                        pass
            else:
                webhook = DiscordWebhook(url=webhook_url)
                embed = DiscordEmbed(title='HeliumBOT : Error', color=242424)
                embed.add_embed_field(name='Device Address', value=urlKey[0])
                embed.add_embed_field(name='Device Nickname', value=urlKey[1])
                embed.add_embed_field(name='Error Code', value=statusCode)
                embed.set_footer(text='Sudobotz.com')
                embed.set_timestamp()
                webhook.add_embed(embed)
                webhook.execute()
                
            time.sleep(1)
            
        print(f"\nChecking again in {delay} minutes...")
        time.sleep(int(delay)*60)
        
HM()
        
        
    