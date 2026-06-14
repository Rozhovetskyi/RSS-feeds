from ddgs import DDGS

keywords = [
    'Synthetic data generation for defects',
    'YOLO for custom objects',
    'Autoencoder anomaly detection code',
    'OpenCV industrial inspection'
]

for keyword in keywords:
    print(f"\n--- Searching for: {keyword} ---")
    query = f'site:towardsdatascience.com "{keyword}"'
    try:
        results = list(DDGS().text(query, max_results=5))
        if results:
            for r in results:
                print(r)
    except Exception as e:
        pass
