import json
import os
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
        'Bluesky': f'https://bsky.app/profile/{username}.bsky.social',
        'Mastodon': f'https://mastodon.social/@{username}',
        'Tumblr': f'https://{username}.tumblr.com',
        'Threads': f'https://www.threads.net/@{username}',
        'Discord': f'https://discord.com',
        
        # Video/Streaming
        'YouTube': f'https://www.youtube.com/@{username}',
        'Twitch': f'https://www.twitch.tv/{username}',
        'Vimeo': f'https://vimeo.com/{username}',
        'DailyMotion': f'https://www.dailymotion.com/{username}',
        'Odysee': f'https://odysee.com/@{username}',
        
        # Gaming
        'Steam': f'https://steamcommunity.com/id/{username}',
        'PlayStation': f'https://psnprofiles.com/{username}',
        'Roblox': f'https://www.roblox.com/user.aspx?username={username}',
        'Minecraft': f'https://namemc.com/profile/{username}',
        'osu!': f'https://osu.ppy.sh/users/{username}',
        'Chess.com': f'https://www.chess.com/member/{username}',
        'Lichess': f'https://lichess.org/@/{username}',
        
        # Forums/Community
        'Reddit': f'https://www.reddit.com/user/{username}',
        'Stack Overflow': f'https://stackoverflow.com/users/{username}',
        'GitLab': f'https://gitlab.com/{username}',
        'Bitbucket': f'https://bitbucket.org/{username}/',
        'Hacker News': f'https://news.ycombinator.com/user?id={username}',
        'Dev.to': f'https://dev.to/{username}',
        'Medium': f'https://medium.com/@{username}',
        'Vercel': f'https://vercel.com/{username}',
        
        # Music
        'Spotify': f'https://open.spotify.com/user/{username}',
        'SoundCloud': f'https://soundcloud.com/{username}',
        'Last.fm': f'https://www.last.fm/user/{username}',
        'Bandcamp': f'https://www.bandcamp.com/{username}',
        
        # Professional
        'Behance': f'https://www.behance.net/{username}',
        'Dribbble': f'https://dribbble.com/{username}',
        'Figma': f'https://www.figma.com/@{username}',
        'Product Hunt': f'https://www.producthunt.com/@{username}',
        
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
        'GitHub Gist': f'https://gist.github.com/{username}',
        
        # Writing/Blogs
        'Quora': f'https://www.quora.com/profile/{username}',
        'Substack': f'https://{username}.substack.com',
        'Hashnode': f'https://hashnode.com/@{username}',
        
        # Crypto/Web3
        'OpenSea': f'https://opensea.io/{username}',
        
        # Other
        'Linktree': f'https://linktr.ee/{username}',
        'Patreon': f'https://www.patreon.com/{username}',
        'Buy Me a Coffee': f'https://www.buymeacoffee.com/{username}',
        'Ko-fi': f'https://ko-fi.com/{username}',
        'OnlyFans': f'https://onlyfans.com/{username}',
    }

@app.route('/search', methods=['POST'])
def search_username():
    data = request.get_json()
    username = data.get('username', '').strip()
    
    if not username:
        return jsonify({'error': 'Username requerido'}), 400
    
    sites = get_sites(username)
    results = []
    found_count = 0
    
    def check_site(site_name, url):
        try:
            response = requests.head(url, allow_redirects=True, timeout=5, headers={'User-Agent': 'Mozilla/5.0 (compatible; Sherlock/0.16.0)'})
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
    
    # Parallel processing with limited workers
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(check_site, name, url): name 
                  for name, url in sites.items()}
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            if result['exists']:
                found_count += 1
    
    return jsonify({
        'username': username,
        'results': results,
        'count': len(results),
        'found_count': found_count
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'service': 'sherlock-backend'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
