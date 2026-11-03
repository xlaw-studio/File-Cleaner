from src.file_cleaner.main import get_category


def test_get_category_images():
    assert get_category(".PNG") == "Images"
    assert get_category(".jpg") == "Images"


def test_get_category_documents():
    assert get_category(".pdf") == "Documents"
    assert get_category(".docx") == "Documents"


def test_get_category_unknown():
    assert get_category(".unknownext") == "Other"