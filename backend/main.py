import json
import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

app = Flask(__name__)
CORS(app)

# Extended list of platforms (100+ sites)
def get_sites(username):
    return {
        # Social Media
        'GitHub': f'https://github.com/{username}',
        'Twitter/X': f'https://x.com/{username}',
        'Instagram': f'https://www.instagram.com/{username}/',
        'TikTok': f'https://www.tiktok.com/@{username}',
        'Facebook': f'https://www.facebook.com/{username}',
        'LinkedIn': f'https://www.linkedin.com/in/{username}',
        'Snapchat': f'https://www.snapchat.com/add/{username}',
        'Pinterest': f'https://www.pinterest.com/{username}/',
        
        # Video/Streaming
        'YouTube': f'https://www.youtube.com/@{username}',
        'Twitch': f'https://www.twitch.tv/{username}',
        'Vimeo': f'https://vimeo.com/{username}',
        'DailyMotion': f'https://www.dailymotion.com/{username}',
        'Odysee': f'https://odysee.com/@{username}',
        
        # Gaming
        'Steam': f'https://steamcommunity.com/id/{username}',
        'Xbox Live': f'https://xboxgamertag.com/search/{username}',
        'PlayStation': f'https://psnprofiles.com/{username}',
        'Epic Games': f'https://fortnitetracker.com/profile/all/{username}',
        'Roblox': f'https://www.roblox.com/user.aspx?username={username}',
        'Minecraft': f'https://namemc.com/profile/{username}',
        'osu!': f'https://osu.ppy.sh/users/{username}',
        'Chess.com': f'https://www.chess.com/member/{username}',
        'Lichess': f'https://lichess.org/@/{username}',
        
        # Forums/Community
        'Reddit': f'https://www.reddit.com/user/{username}',
        'Discord': f'https://discord.com/users/{username}',
        'Stack Overflow': f'https://stackoverflow.com/users/{username}',
        'GitLab': f'https://gitlab.com/{username}',
        'Bitbucket': f'https://bitbucket.org/{username}/',
        'Hacker News': f'https://news.ycombinator.com/user?id={username}',
        'Dev.to': f'https://dev.to/{username}',
        'Medium': f'https://medium.com/@{username}',
        'Vercel': f'https://vercel.com/{username}',
        'Netlify': f'https://app.netlify.com/teams/{username}',
        
        # Music
        'Spotify': f'https://open.spotify.com/user/{username}',
        'SoundCloud': f'https://soundcloud.com/{username}',
        'Last.fm': f'https://www.last.fm/user/{username}',
        'Bandcamp': f'https://{username}.bandcamp.com',
        
        # Professional
        'Behance': f'https://www.behance.net/{username}',
        'Dribbble': f'https://dribbble.com/{username}',
        'Figma': f'https://www.figma.com/@{username}',
        'Product Hunt': f'https://www.producthunt.com/@{username}',
        'AngelList': f'https://angel.co/u/{username}',
        
        # Photography/Art
        'Flickr': f'https://www.flickr.com/people/{username}/',
        'Unsplash': f'https://unsplash.com/@{username}',
        '500px': f'https://500px.com/p/{username}',
        'DeviantArt': f'https://www.deviantart.com/{username}',
        'ArtStation': f'https://www.artstation.com/{username}',
        
        # Development
        'Docker Hub': f'https://hub.docker.com/u/{username}/',
        'PyPI': f'https://pypi.org/user/{username}/',
        'NPM': f'https://www.npmjs.com/~{username}',
        'RubyGems': f'https://rubygems.org/profiles/{username}',
        'Packagist': f'https://packagist.org/users/{username}/',
        'NuGet': f'https://www.nuget.org/profiles/{username}',
        'Crates.io': f'https://crates.io/users/{username}',
        'Hex': f'https://hex.pm/users/{username}',
        
        # Writing/Blogs
        'Quora': f'https://www.quora.com/profile/{username}',
        'Wattpad': f'https://www.wattpad.com/user/{username}',
        'Substack': f'https://{username}.substack.com',
        'Ghost': f'https://{username}.ghost.io',
        'Hashnode': f'https://hashnode.com/@{username}',
        
        # Crypto/Web3
        'OpenSea': f'https://opensea.io/{username}',
        'Rarible': f'https://rarible.com/{username}',
        'Foundation': f'https://foundation.app/@{username}',
        'Coinbase': f'https://www.coinbase.com/user/{username}',
        
        # Other
        'Tinder': f'https://tinder.com/@{username}',
        'Grindr': f'https://grindr.com/{username}',
        'OnlyFans': f'https://onlyfans.com/{username}',
        'Patreon': f'https://www.patreon.com/{username}',
        'Ko-fi': f'https://ko-fi.com/{username}',
        'Buy Me a Coffee': f'https://www.buymeacoffee.com/{username}',
        'Linktree': f'https://linktr.ee/{username}',
        'Carrd': f'https://{username}.carrd.co',
        'Bio.link': f'https://bio.link/{username}',
        'Lynkheard': f'https://lynkheard.com/{username}',
        
        # More Social
        'Tumblr': f'https://{username}.tumblr.com',
        'Mastodon': f'https://mastodon.social/@{username}',
        'Bluesky': f'https://bsky.app/profile/{username}.bsky.social',
        'Threads': f'https://www.threads.net/@{username}',
        'Truth Social': f'https://truthsocial.com/@{username}',
        'Gab': f'https://gab.com/{username}',
        'Parler': f'https://parler.com/{username}',
        
        # Dating
        'OkCupid': f'https://www.okcupid.com/profile/{username}',
        'Plenty of Fish': f'https://www.pof.com/username={username}',
        'Match': f'https://www.match.com/profile/{username}',
        
        # Sports/Fitness
        'Strava': f'https://www.strava.com/athletes/{username}',
        'Nike Run Club': f'https://www.nike.com/member/profile/{username}',
        
        # Shopping
        'Etsy': f'https://www.etsy.com/shop/{username}',
        'Amazon': f'https://www.amazon.com/gp/profile/{username}/',
        'eBay': f'https://www.ebay.com/usr/{username}',
        'Depop': f'https://www.depop.com/{username}/',
        
        # Travel
        'Couchsurfing': f'https://www.couchsurfing.com/people/{username}/',
        'Airbnb': f'https://www.airbnb.com/users/show/{username}',
        'Booking.com': f'https://www.booking.com/user/{username}.html',
        
        # Food
        'Yelp': f'https://www.yelp.com/user_details?userid={username}',
        'AllTrails': f'https://www.alltrails.com/members/{username}',
        'Untappd': f'https://untappd.com/user/{username}',
        
        # Wiki/Knowledge
        'Wikipedia': f'https://en.wikipedia.org/wiki/User:{username}',
        'Wikia/Fandom': f'https://community.fandom.com/wiki/User:{username}',
        
        # Forums
        'IGN': f'https://www.ign.com/boards/members/{username}/',
        'GameFAQs': f'https://gamefaqs.gamespot.com/community/{username}/',
        'NeoGAF': f'https://www.neogaf.com/members/{username}/',
        'ResetEra': f'https://www.resetera.com/members/{username}/',
        
        # More Dev
        'Launchpad': f'https://launchpad.net/~{username}',
        'SourceForge': f'https://sourceforge.net/u/{username}/',
        'Codeberg': f'https://codeberg.org/{username}',
        'Gitea': f'https://gitea.com/{username}',
        'Gitee': f'https://gitee.com/{username}',
        
        # Design/Creative
        'Canva': f'https://www.canva.com/{username}',
        'Adobe Portfolio': f'https://{username}.myportfolio.com',
        'Cargo': f'https://{username}.cargo.site/',
        
        # Hosting
        'Heroku': f'https://dashboard.heroku.com/apps/{username}',
        'Railway': f'https://railway.app/user/{username}',
        'Render': f'https://dashboard.render.com/user/{username}',
    }

@app.route('/search', methods=['POST'])
def search_username():
    data = request.get_json()
