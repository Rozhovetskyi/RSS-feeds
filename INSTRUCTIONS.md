# Instructions for Scheduled Jules

This document outlines the procedure for updating the RSS feeds in this repository.

## Goal
Your task is to browse specific news sources, identify relevant articles, and update the corresponding RSS feed using the `rss_manager.py` script.

## Workflow

1.  **Browse Sources**
    *   Use your browser tool to visit the target website (e.g., Google News, TechCrunch, specific blogs).
    *   Look for the latest articles relevant to the topic.

2.  **Extract Information**
    *   For each article you find, extract:
        *   **Title**: The headline of the article.
        *   **Link**: The direct URL to the full article.
        *   **Summary**: A brief description or the first paragraph (optional but recommended).

3.  **Update Feed**
    *   Use the `rss_manager.py` script to add the article to the feed.
    *   **Do not edit the XML files manually.**
    *   The script handles creation, deduplication, and limit enforcement (max 7 items).

## Command Usage

Run the following command for each article you want to add:

```bash
python3 rss_manager.py --topic "TOPIC_NAME" --title "ARTICLE_TITLE" --link "ARTICLE_URL" --summary "ARTICLE_SUMMARY"
```

### Parameters
*   `--topic`: The name of the feed. This determines the filename (e.g., `Tech` -> `feeds/Tech.xml`). Keep this consistent for the same topic.
*   `--title`: The article title.
*   `--link`: The URL.
*   `--summary`: (Optional) A short description.

## Example Scenario: Updating "AI News"

1.  You search Google News for "Artificial Intelligence".
2.  You find an article:
    *   **Title**: "New AI Model Released"
    *   **Link**: "https://example.com/ai-model"
    *   **Summary**: "Company X has released a new transformer model."
3.  You run:

```bash
python3 rss_manager.py --topic "AI_News" --title "New AI Model Released" --link "https://example.com/ai-model" --summary "Company X has released a new transformer model."
```

4.  Repeat for other articles.
5.  Commit your changes.
