# main.py
import argparse
import os
from utils.ocr import image_to_text
from utils.llm import answer_question_with_llm
from utils.notion import upload_question
from datetime import datetime

def save_markdown(content: str, out_dir="outputs"):
    os.makedirs(out_dir, exist_ok=True)
    fname = f"answer_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.md"
    path = os.path.join(out_dir, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path

def main(image_path: str, lang="en", use_gpu: bool = True, notion_upload: bool = True):
    print("Running OCR...")
    text = image_to_text(image_path, lang_list=[lang], gpu=use_gpu)
    if not text.strip():
        print("No text extracted from image.")
        return

    print("Question text extracted:")
    print(text[:500], "...\n")

    print("Asking local LLM (Ollama) to answer...")
    answer = answer_question_with_llm(text)
    md = f"# Question\n\n{text}\n\n# Answer\n\n{answer}\n"

    saved = save_markdown(md)
    print("Saved markdown to:", saved)

    if notion_upload:
        print("Uploading to Notion...")
        page = upload_question(md, title=os.path.basename(saved))
        print("Uploaded page:", page.get("id"))

if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument("image", help="Path to question image")
    # parser.add_argument("--lang", default="en")
    # parser.add_argument("--no-gpu", action="store_true", help="Disable GPU for OCR")
    # parser.add_argument("--no-notion", action="store_true", help="Skip Notion upload")
    # args = parser.parse_args()
    # main(args.image, lang=args.lang, use_gpu=not args.no_gpu, notion_upload=not args.no_notion)
    print(image_to_text("images/Example.png"))