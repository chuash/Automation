> [!NOTE]
> The `requirements.txt` file in this repository was generated using a Python 3.13 environment.

# Ecommerce Product Listing Extraction - Proof of Concept

## Problem Statement

Imagine having a list of ecommerce product listing URLs that need to be:
- accessed,
- scraped for relevant information,
- and captured as screenshots.

A straightforward approach would be to use browser automation frameworks such as Selenium or Playwright to:
1. launch a browser,
2. navigate to the target URLs,
3. locate and extract the required web elements,
4. and capture screenshots of the webpages.

While this approach is technically feasible, modern ecommerce platforms often deploy sophisticated anti-botting and anti-automation mechanisms. One possible response is to continuously improve and adapt automation techniques to bypass these defences, but this quickly becomes an ongoing cat-and-mouse game.

Another alternative is to consume official platform APIs, if available. However, API access is often rate-limited, restricted, or tied to paid subscription tiers.

---

# Proof of Concept

This project explores a scraping-independent and potentially freemium approach for extracting information and screenshots from ecommerce product listing URLs.

## Approach Overview

Instead of automating a browser session directly through Selenium or Playwright, this approach leverages the host machine's native web browser and existing authenticated user session.

The core idea is:
1. Manually open the ecommerce platform in a native browser.
2. Log into the platform normally so that authentication cookies and session data are established.
3. Keep the browser window open.
4. Execute the automation scripts separately.

By operating on top of an already-authenticated browser session, the workflow attempts to reduce the likelihood of triggering anti-botting mechanisms commonly associated with fully automated browser environments.

---

## Workflow

### Step 1 - Capture Screenshots

Run:

```bash
python main.py
```

The script performs the following actions for each product listing URL:

- Uses Python's `webbrowser` library to open the URL in a separate browser tab within the existing authenticated browser window.
- Uses Python's `pyautogui` library to simulate human interactions with the webpage.
- Captures screenshots of the relevant webpage sections.

---

### Step 2 - Extract Information from Images

Run:

```bash
python data_from_images.py
```

This script:
- crops and preprocesses the captured screenshots,
- prepares the corresponding prompts,
- and sends the images to a Vision Language Model (VLM) for structured information extraction.

For this project, the following model setup is used:

| Component | Value |
|---|---|
| Model | `meta-llama/llama-4-scout-17b-16e-instruct` |
| Hosting Provider | Groq |
| Reason for Selection | Free usage within specified rate limits |

---

# Key Libraries Used

| Library | Purpose |
|---|---|
| `webbrowser` | Opens URLs using the system's native browser |
| `pyautogui` | Simulates mouse and keyboard interactions |
| `PIL` | Crops and preprocesses images |
| `groq` | Provides the API client to access VLM |

---

# Limitations

- Screenshot-based extraction is generally slower compared to direct API access.
- Accuracy of extracted information depends on screenshot quality and VLM performance.
- Some platforms may still implement protections against automated interactions.

---

# Further Work

Potential future improvements include:

- Fine-tuning and adapting the workflow for specific ecommerce platforms.
- Improving screenshot preprocessing and cropping logic.
- Enhancing automation robustness across different screen resolutions and browser configurations.
- Benchmarking different Vision Language Models for extraction accuracy and cost efficiency.