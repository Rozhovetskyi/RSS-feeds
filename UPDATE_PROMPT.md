You are tasked with updating the "Defect Detection" RSS feed.

1.  **Read Strategy**: First, read the file `SEARCH_STRATEGY.md` to get the latest arXiv API URL for the defect detection query.
2.  **Fetch Data**: Use your `view_text_website` tool to fetch the content from the arXiv API URL found in the strategy file.
3.  **Parse & Update**: For each of the top 7 most recent entries in the API response:
    *   Extract the **Title**, **Link** (use the `id`), and **Summary**.
    *   Run the `rss_manager.py` script to add the item to the feed.
    *   Command format:
        ```bash
        python3 rss_manager.py --topic "Defect_Detection" --title "PAPER_TITLE" --link "PAPER_URL" --summary "PAPER_SUMMARY"
        ```
4.  **Verify**: Read `feeds/Defect_Detection.xml` to ensure the new items were added correctly.
