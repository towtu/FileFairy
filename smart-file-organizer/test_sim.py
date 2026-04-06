import time
from pathlib import Path

downloads = Path.home() / "Downloads"
downloads.mkdir(exist_ok=True)

files_to_create = [
    "lecture_week3_slides.pdf",
    "assignment_1_submission.docx",
    "research_paper_2024.pdf",
    "cat_photo.jpg",
    "random_data.csv",
    "my_test_script.py"
]

data_11kb = "0" * 11 * 1024

for i, f in enumerate(files_to_create):
    filepath = downloads / f
    with open(filepath, "w") as file:
        # Give each file a unique prefix so the hash is unique, but still pad to 11KB
        unique_content = f"Unique {i}: {f}\n" + data_11kb
        file.write(unique_content)
    time.sleep(0.5)

print("Dummy files created in Downloads.")
