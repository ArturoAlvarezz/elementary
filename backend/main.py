import json
import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

app = Flask(__name__)
CORS(app)

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
        # Video
        'YouTube': f'https://www.youtube.com/@{username}',
        'Twitch': f'https://www.twitch.tv/{username}',
        'Vimeo': f'https://vimeo.com/{username}',
        'Odysee': f'https://odysee.com/@{username}',
        # Gaming
        'Steam': f'https://steamcommunity.com/id/{username}',
        'Xbox Live': f'https://xboxgamertag.com/search/{username}',
        'PlayStation': f'https://psnprofiles.com/{username}',
        'Roblox': f'https://www.roblox.com/user.aspx?username={username}',
        'Minecraft': f'https://namemc.com/profile/{username}',
        'osu!': f'https://osu.ppy.sh/users/{username}',
        'Chess.com': f'https://www.chess.com/member/{username}',
        'Lichess': f'https://lichess.org/@/{username}',
        # Forums
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
        # Photography
        'Flickr': f'https://www.flickr.com/people/{username}/',
        'Unsplash': f'https://unsplash.com/@{username}',
        '500px': f'https://500px.com/p/{username}',
        'DeviantArt': f'https://www.deviantart.com/{username}',
        'ArtStation': f'https://www.artstation.com/{username}',
        # Dev Packages
        'Docker Hub': f'https://hub.docker.com/u/{username}/',
        'NPM': f'https://www.npmjs.com/~{username}',
        'PyPI': f'https://pypi.org/user/{username}/',
        'RubyGems': f'https://rubygems.org/profiles/{username}',
        # Blogs
        'Quora': f'https://www.quora.com/profile/{username}',
        'Substack': f'https://{username}.substack.com',
        'Hashnode': f'https://hashnode.com/@{username}',
        # Crypto
        'OpenSea': f'https://opensea.io/{username}',
        'Linktree': f'https://linktr.ee/{username}',
        'OnlyFans': f'https://onlyfans.com/{username}',
        'Patreon': f'https://www.patreon.com/{username}',
        'Tumblr': f'https://{username}.tumblr.com',
        'Mastodon': f'https://mastodon.social/@{username}',
        'Bluesky': f'https://bsky.app/profile/{username}.bsky.social',
        'Threads': f'https://www.threads.net/@{username}',
    }

@app.route('/search', methods=['POST'])
def search_username():
    data = request.get_json()
    username = data.get('username', '').strip()
    if not username:
        return jsonify({'error': 'Username requerido'}), 400
    
    sites = get_sites(username)
    results = []
    
    def check_site(site_name, url):
        try:
            response = requests.head(url, allow_redirects=True, timeout=5)
            exists = response.status_code == 200
            return {
                'platform': site_name,
                'url': url,
                'exists': exists,
                'username': username
            }
        except:
            return {
                'platform': site_name,
                'url': url,
                'exists': False,
                'username': username
            }
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(check_site, name, url): name 
                  for name, url in sites.items()}
        for future in as_completed(futures):
            results.append(future.result())
    
    return jsonify({
        'username': username,
        'results': results,
        'count': len(results),
        'found_count': len([r for r in results if r['exists']])
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'service': 'sherlock-backend'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
