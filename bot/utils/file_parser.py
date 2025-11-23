# -*- coding: utf-8 -*-
from typing import Optional
import os
from pdfminer.high_level import extract_text
import docx
import magic

def parse_resume_file(file_path: str) -> Optional[str]:
    """Парсинг PDF и DOCX резюме"""
    if not os.path.exists(file_path):
        return None

    try:
        mime = magic.from_file(file_path, mime=True)
        
        if mime == "application/pdf":
            return extract_text(file_path)
        elif mime in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            doc = docx.Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        else:
            # Попробуем как текст
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
    except Exception as e:
        print(f"❌ Ошибка парсинга: {e}")
        return None