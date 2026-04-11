# Annotation Instructions for POLAR Lab Meeting (04/09)

Thanks for helping annotate! This is a small Flask app that shows you pairs of rulesets (an original and a revised version) and asks you to judge whether the
revision preserves the intent of the original ruleset.

## Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/nimra-nadeem/cai_annotations.git
   cd cai_annotations/interface
   ```
2. Install the one dependency (Flask):
   ```bash
   pip install flask
   ```
   **If you have uv on your computer, just run `uv sync`**


## Running the app

From the `interface/` directory:

```bash
python app.py
```

Then open <http://127.0.0.1:5000> in your browser.

## Annotating

1. Enter your name and click **Start**.
2. For each pair, read the ruleset description at the top, then compare the
   original and revised rules side-by-side. Differences are highlighted inline
   by default but you can toggle it off by clicking the "Show inline diff 
   highlighting" checkbox.
3. Use the slider to score how well the revision preserves the original
   intent (`-1` = no, `0` = unsure, `+1` = yes).
4. Optionally leave a note in the **Feedback** box.
5. Click **Submit & Next**. Your annotation is saved immediately.
6. Repeat until you see the "All done" screen.

Your annotations are appended to
`annotations/annotations_<your-name>.jsonl` after every submission. If you
stop and restart the app, just enter the same name and click **Start** —
it will automatically resume from the first unannotated pair. You can also
use the **Back** and **Skip** buttons to navigate between pairs.

## Uploading your results

When you're done, please upload your
`annotations/annotations_<your-name>.jsonl` file to this Google Drive folder:

https://drive.google.com/drive/folders/1nMsvnmyiZlH2uR1JQ3nREHcxpltgpAlw?usp=sharing

Thank you!
