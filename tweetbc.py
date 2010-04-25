#!/usr/bin/env python
# encoding: utf-8
"""
tweetbc.py

Created by Hilary Mason on 2010-04-25.
Copyright (c) 2010 Hilary Mason. All rights reserved.
"""

import sys, os
import subprocess
import tweepy # Twitter API class: http://github.com/joshthecoder/tweepy


class tweetBC(object):
    TWITTER_USERNAME = 'bc_l' # configure me
    TWITTER_PASSWORD = 'XXX' # configure me
    DM_CACHE = 'last_seen.txt' # possibly configure me
    
    def __init__(self):
        api = self.init_twitter(self.TWITTER_USERNAME, self.TWITTER_PASSWORD)

        last_dm_id = self.get_last_seen()
        dms = api.direct_messages(since_id=last_dm_id)

        for m in dms:
            p = subprocess.Popen("bc -l", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            out, err = p.communicate(m.text + "\n")
            answer = out.strip()
            if answer:
                print "@%s %s = %s" % (m.sender_screen_name, m.text, answer)
            
                try:
                    api.update_status("@%s %s = %s" % (m.sender_screen_name, m.text, answer))
                except:
                    pass
            
            last_dm_id = m.id
            
        f = open(self.DM_CACHE, 'w')
        f.write(str(last_dm_id))
        f.close()
    
    def get_last_seen(self):
        try:
            f = open(self.DM_CACHE, 'r')
            last_dm_id = f.read()
            f.close()
        except IOError:
            last_dm_id = None
            
        return last_dm_id

    def init_twitter(self, username, password):
        auth = tweepy.BasicAuthHandler(username, password)
        api = tweepy.API(auth)
        return api
        


if __name__ == '__main__':
    t = tweetBC()
