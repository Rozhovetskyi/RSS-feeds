# Defect Detection Research Strategy

This document outlines a search-query-based RSS configuration to track state-of-the-art algorithms for Defect Detection in Computer Vision, specifically for Industrial Inspection.

## Search Logic

**Intersection:** 'Computer Vision' AND 'Industrial Inspection'

**Boolean Logic:**
```
(Title OR Abstract matches: 'Defect Detection' OR 'Anomaly Detection' OR 'Surface Inspection' OR 'Optical Inspection')
AND
(Context matches: 'Industrial' OR 'Manufacturing' OR 'Unsupervised' OR 'Fabric' OR 'Metal' OR 'PCB')
```

## Data Sources & Configuration

### 1. arXiv.org (cs.CV)

arXiv provides an API that returns results in Atom format, which can be used as an RSS feed.

*   **Category:** Computer Vision (`cs.CV`)
*   **Search Query:**
    ```
    cat:cs.CV AND (ti:"Defect Detection" OR abs:"Defect Detection" OR ti:"Anomaly Detection" OR abs:"Anomaly Detection" OR ti:"Surface Inspection" OR abs:"Surface Inspection" OR ti:"Optical Inspection" OR abs:"Optical Inspection") AND (all:"Industrial" OR all:"Manufacturing" OR all:"Unsupervised" OR all:"Fabric" OR all:"Metal" OR all:"PCB")
    ```
*   **RSS/Atom Feed URL:**
    [Link to arXiv Feed](http://export.arxiv.org/api/query?search_query=cat:cs.CV+AND+(ti:%22Defect+Detection%22+OR+abs:%22Defect+Detection%22+OR+ti:%22Anomaly+Detection%22+OR+abs:%22Anomaly+Detection%22+OR+ti:%22Surface+Inspection%22+OR+abs:%22Surface+Inspection%22+OR+ti:%22Optical+Inspection%22+OR+abs:%22Optical+Inspection%22)+AND+(all:%22Industrial%22+OR+all:%22Manufacturing%22+OR+all:%22Unsupervised%22+OR+all:%22Fabric%22+OR+all:%22Metal%22+OR+all:%22PCB%22)&sortBy=submittedDate&sortOrder=descending)

### 2. Papers With Code

Papers With Code does not have a direct RSS feed for complex search queries, but you can bookmark the following search URL.

*   **Search Query:**
    ```
    ("Defect Detection" OR "Anomaly Detection" OR "Surface Inspection" OR "Optical Inspection") AND ("Industrial" OR "Manufacturing" OR "Unsupervised" OR "Fabric" OR "Metal" OR "PCB")
    ```
*   **Search URL:**
    [Link to Papers With Code Search](https://paperswithcode.com/search?q_meta=&q_type=&q=%28%22Defect+Detection%22+OR+%22Anomaly+Detection%22+OR+%22Surface+Inspection%22+OR+%22Optical+Inspection%22%29+AND+%28%22Industrial%22+OR+%22Manufacturing%22+OR+%22Unsupervised%22+OR+%22Fabric%22+OR+%22Metal%22+OR+%22PCB%22%29)

## Jules Automation

The local feed `feeds/Defect_Detection.xml` is populated using the arXiv query above.
