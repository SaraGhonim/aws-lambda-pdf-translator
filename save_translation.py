import os
import re
def save_translation(name, text, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    match = re.search(r'pages_(\d+)-(\d+)', name)
    if not match:
        raise ValueError("Filename must match format like 'pages_11-19.txt'")
    
    start_page = int(match.group(1))
    print(start_page,"start_page start_page")
    pattern = r'(?:صفحة)\s+(\d+)'
    def replace_page(match_obj):
        old_number = int(match_obj.group(1))
        new_number = old_number + start_page - 1
        prefix = match_obj.group(0).split()[0]  # Keep original prefix ("Page" or "الصفحة")
        return f"{prefix} {new_number}"

    # Replace all matched page labels
    updated_content = re.sub(pattern, replace_page, text, flags=re.IGNORECASE)

    # Save as txt
    updated_content="\n\n" + updated_content + "\n\n"
    txt_path = os.path.join(output_folder, f"{name}")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(updated_content)