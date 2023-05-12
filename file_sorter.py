from pathlib import Path
import os

CATEGORIES = {
    'images': ['.jpeg', '.png', '.jpg', '.svg'],
    'documents': ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'],
    'audio': ['.mp3', '.ogg', '.wav', '.amr'],
    'video': ['.avi', '.mp4', '.mov', '.mkv'],
    'archives': ['.zip', '.gz', '.tar']
}


def get_categories(file: Path):
    extension = file.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category
    return None


def file_sorter(path_str: str):
    path = Path(path_str)
    if not path.exists():
        raise ValueError("Folder does not exist")
    for file in path.glob('*.*'):
        category = get_categories(file)
        if not category:
            continue
        target_dir = path.joinpath(category)
        if not target_dir.exists():
            target_dir.mkdir()
        filename = os.path.split(file)[1]
        dst_file = target_dir.joinpath(filename)
        file.rename(dst_file)
    return f'Files have been sorted'


if __name__ == '__main__':
    path1 = 'C:\\Users\\Surface\\Downloads'
    print(file_sorter(path1))
