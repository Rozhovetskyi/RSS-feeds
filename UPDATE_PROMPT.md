# Scheduled Task: Update Defect Detection Feed

You are a scheduled agent tasked with maintaining the "Defect Detection" RSS feed. Follow the protocols defined in the repository to ensure compliance and data integrity.

## Prerequisites & Context
1.  **Read Instructions**: First, strictly review `INSTRUCTIONS.md`. This file governs the workflow, specifically:
    *   The requirement to use `rss_manager.py` for all updates.
    *   The prohibition against manual XML editing.
    *   The standard command format.
2.  **Read Strategy**: Review `SEARCH_STRATEGY.md`. This file contains:
    *   The precise Boolean search logic.
    *   The **arXiv API URL** required to fetch the latest data.

## Execution Steps
1.  **Fetch Data**:
    *   Use the `view_text_website` tool to retrieve the Atom/RSS feed from the arXiv URL found in `SEARCH_STRATEGY.md`.
2.  **Process Entries**:
    *   Identify the top 7 most recent papers from the fetched data.
    *   For each paper, extract the `Title`, `Link` (arXiv ID/URL), and `Summary`.
3.  **Update Feed**:
    *   For each identified paper, run the following command (as specified in `INSTRUCTIONS.md`):
        ```bash
        python3 rss_manager.py --topic "Defect_Detection" --title "<TITLE>" --link "<LINK>" --summary "<SUMMARY>"
        ```
4.  **Verification**:
    *   Read `feeds/Defect_Detection.xml` to verify the new items have been correctly added and the file format remains valid.
