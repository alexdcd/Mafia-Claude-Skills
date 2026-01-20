import json
import os
import urllib.request
import urllib.error

# Configuration
CONFIG_FILE = os.path.join(os.path.dirname(__file__), '../data/external-skills.json')
GITHUB_API_BASE = "https://api.github.com/repos"

def get_headers():
    headers = {'User-Agent': 'Mafia-Claude-Skills-Sync'}
    token = os.environ.get('GITHUB_REFRESH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if token:
        headers['Authorization'] = f'token {token}'
    return headers

def fetch_contents(repo, path):
    url = f"{GITHUB_API_BASE}/{repo}/contents/{path}"
    req = urllib.request.Request(url, headers=get_headers())
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Error fetching {url}: {e}")
        if e.code == 403:
            print("Rate limit likely exceeded. Set GITHUB_TOKEN environment variable.")
        return None

def download_file(url, local_path):
    print(f"Downloading {url} to {local_path}...")
    req = urllib.request.Request(url, headers=get_headers())
    try:
        with urllib.request.urlopen(req) as response:
            content = response.read()
            # Write content
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with open(local_path, 'wb') as f:
                f.write(content)
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def process_item(item, local_base_path):
    name = item['name']
    if item['type'] == 'file':
        local_file_path = os.path.join(local_base_path, name)
        download_file(item['download_url'], local_file_path)
    elif item['type'] == 'dir':
        # Recurse
        print(f"Entering directory {name}...")
        repo_path = item['path'] # Interestingly, the API response for content listing includes 'path' which is the full repo path
        # But wait, fetch_contents was called with the parent path.
        # We need to call fetch_contents for this new directory.
        # Ideally, we extract the repo and path from the current context or the 'url'.
        # Actually github api item return has 'url' pointing to its api endpoint.
        # But we can just use the path provided in the item which is relative to repo root.
        # We need the repo name though. We can pass it down.
        pass # To be implemented if we need recursion, but for now let's see if the initial logic handles it.
        # Wait, the structure of 'item' from 'contents' endpoint:
        # { "name": "foo.txt", "path": "dir/foo.txt", "sha": "...", "type": "file", "download_url": "..." }
        pass

def sync_path(repo, path, local_dir):
    contents = fetch_contents(repo, path)
    if not contents:
        return

    if not isinstance(contents, list):
        # It's a single file if 'path' pointed to a file, but we expect a dir.
        print(f"Unexpected response type for {path}")
        return

    for item in contents:
        if item['type'] == 'file':
            local_file_path = os.path.join(local_dir, item['name'])
            download_file(item['download_url'], local_file_path)
        elif item['type'] == 'dir':
            new_local_dir = os.path.join(local_dir, item['name'])
            sync_path(repo, item['path'], new_local_dir)

def main():
    if not os.path.exists(CONFIG_FILE):
        print(f"Config file not found: {CONFIG_FILE}")
        return

    try:
        with open(CONFIG_FILE, 'r') as f:
            skills = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error reading config: {e}")
        return

    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    for skill in skills:
        print(f"Syncing {skill['name']} from {skill['repo']}...")
        local_path = os.path.join(root_dir, skill['local_path'])
        sync_path(skill['repo'], skill['path'], local_path)
        print(f"Finished syncing {skill['name']}.\n")

if __name__ == "__main__":
    main()
