import urllib.request

urls = [
    'https://towardsdatascience.com/train-yolo-for-object-detection-on-a-custom-dataset-using-python-e4fe5eb94673/',
    'https://towardsdatascience.com/how-to-create-a-simple-object-detection-system-with-python-and-imageai-ee1bcaf6b111/'
]

for url in urls:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            print(f"Loaded {url}, size: {len(html)}")
    except Exception as e:
        print(f"Error {url}: {e}")
