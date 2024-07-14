import requests
import urllib.parse
import sys
from bs4 import BeautifulSoup

def get_endpoints(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    parsed_url = urllib.parse.urlparse(url)
    endpoints = []
    if "api" in parsed_url.path or "json" in parsed_url.path:
        # If the URL is an API documentation endpoint, recursively fetch all endpoints
        response_json = response.json()
        for path in response_json["paths"]:
            for method in response_json["paths"][path]:
                endpoint = f"{url}{path}.{method.lower()}"
                endpoints.append(endpoint)

    eps = ["/", "/v1/", "/api/", "/docs/", "/admin/", "/api/v2/", "/v2/api/", "/:id/", "/:id/details/", "/search/", "/login/", "/auth/"]
    for suffix in eps:
        new_url = f"{url}{suffix}"
        if requests.head(new_url).status_code == 200:
            endpoints.append(new_url)

    return endpoints

def recurse_directory_tree(url):
    resp = requests.get(url)
    content = resp.content.decode('utf-8')      
    dir_tree = {}
    for line in content.splitlines():
        if line.startswith('<a href="') or line.startswith('<A HREF="'):
            link = urllib.parse.urljoin(url, line.strip().split('"')[1])
            dir_tree[link] = {}
        elif line.startswith('<dir>'):
            dir_tree[line.strip().replace('<dir>', '')] = {}
    return dir_tree

def crawl_directory_tree(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    dir_tree = {}
    for tag in soup.find_all(['div', 'ul', 'ol']):
        if tag.name == 'div' and tag.has_attr('id'):
            dir_tree[tag['id']] = {}
            for child_tag in tag.find_all(True):
                if child_tag.name == 'a':
                    link = child_tag['href']
                    if link.startswith('/'):
                        link = url + link
                    elif not link.startswith('http'):
                        link = url + '/' + link
                    dir_tree[tag['id']][link] = {}
        elif tag.name in ['ul', 'ol']:
            for child_tag in tag.find_all(['li']):
                if child_tag.a:
                    link = child_tag.a['href']
                    if link.startswith('/'):
                        link = url + link
                    elif not link.startswith('http'):
                        link = url + '/' + link
                    dir_tree[tag['id']][link] = {}
    return dir_tree


def main():
    if len(sys.argv) != 2:
        print("Usage: python enum_url.py <URL>")
        sys.exit(1)
    dt = {}
    url = urllib.parse.unquote(sys.argv[1])
    endpoints = get_endpoints(url)
    for endpoint in endpoints:
        print(crawl_directory_tree(endpoint))
        dt[str(endpoint)] = recurse_directory_tree(url)
    return dt


if __name__ == "__main__":
    res = main()
    print(res)