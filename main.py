#!/usr/bin/env python
#
#   Copyright 2014 Frite M.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


import time
import datetime
import lib.twitterService as twitterService
import lib.dbService as db
import lib.alertsClass as alerts

global cKey
cKey = ''

global cSecret
cSecret = ''

global atKey
atKey = ''

global atSecret
atSecret = ''

global szName
szName = ''


def is_protected(user):
    # Check whether a user's profile is protected or not.
    if user.protected is True:
        oTextColor.warning("\tUser %s profile is protected" % user.screen_name)
        return False
    else:
        return True


def get_all_tweets(user):
    # Fetch all tweets of user.
    now = datetime.datetime.now()
    print "\t[*]\tGetting the tweets of %s at %s" % (user.screen_name, str(now))
    tweets = twitter.get_tweets(name=user.screen_name)
    now = datetime.datetime.now()
    print "\t[*]\tFinished getting the tweets of %s at %s" % (user.screen_name, str(now))
    return tweets


def status():
    oTextColor.header("\t\tIn God we trust, all others we monitor")
    oTextColor.okblue("	 ______            _                    _       ")
    oTextColor.okblue("	|  ____|          | |                  (_)      ")
    oTextColor.okblue("	| |__  _   _ _ __ | |__   ___ _ __ ___  _  __ _ ")
    oTextColor.okblue("	|  __|| | | | '_ \| '_ \ / _ \ '_ ` _ \| |/ _` |")
    oTextColor.okblue("	| |___| |_| | |_) | | | |  __/ | | | | | | (_| |")
    oTextColor.okblue("	|______\__,_| .__/|_| |_|\___|_| |_| |_|_|\__,_|")
    oTextColor.okblue("		    | |                                 ")
    oTextColor.okblue("		    |_|                                 ")
    oTextColor.okblue("\t[*]\tEuphemia twitter crawler v0.2\t[*]")
    oTextColor.okblue("\t[*]\tDeveloped by frite\t\t[*]")
    oTextColor.okgreen("\t[*]\tInitializing...\t\t\t[*]")


def fetch_user(username):
    user = twitter.get_user(name=username)
    db.store_user(user)
    if is_protected(user):
        tweets = get_all_tweets(user)
        db.store_tweets(tweets, user)
        followers = twitter.get_followers(user)
        db.store_followers(followers, user)
        friends = twitter.get_friends(user.screen_name)
        db.store_friends(friends, user)
    answer = raw_input('\tGet Another User (y/n):')
    if answer.lower() == 'y':
        question_user()
    else:
        return


def question_user():
    userSeed = raw_input("\tInsert the user to fetch from:")
    fetch_user(str(userSeed))


if __name__ == "__main__":
    try:
        global oTextColor
        oTextColor = alerts.textAlert()
        status()
        global twitter
        global db
        twitter = twitterService.TwitterService(cKey, cSecret, atKey, atSecret, szName)
        question_user()
        oTextColor.okgreen('\tExiting...')
        oTextColor.endc('')
    except (KeyboardInterrupt, SystemExit):
        oTextColor.warning("\t[WARNING]\t Exiting...")
        oTextColor.endc(' ')
