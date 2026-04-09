# Annotation Instructions for POLAR Lab Meeting (04/09)

Thanks for helping annotate! This is a small Flask app that shows you pairs of rulesets (an original and a revised version) and asks you to judge whether the
revision preserves the intent of the original ruleset.

## Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/nimra-nadeem/cai_annotations.git
   cd cai_annotations/intent_neurips
   ```
2. Install the one dependency (Flask):
   ```bash
   pip install flask
   ```

## Running the app

From the `intent_neurips/` directory:

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
stop and restart the app, it will start over from the first pair — there's
currently no resume support, so it's best to do all your annotations in one
sitting. 
(If you do need to restart partway, re-annotating a pair under the
same name will append a new line rather than overwrite the old one, so you
can de-duplicate later by keeping the latest entry per pair.)

## Uploading your results

When you're done, please upload your
`annotations/annotations_<your-name>.jsonl` file to this Google Drive folder:

https://drive.google.com/drive/folders/1nMsvnmyiZlH2uR1JQ3nREHcxpltgpAlw?usp=sharing

Thank you!
