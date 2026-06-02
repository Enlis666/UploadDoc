class DocumentNotFound(Exception):
    def __init__(self, doc_id: int) -> None:
        self.doc_id = doc_id
        super().__init__(f"Документ {doc_id} не найден")


class TextNotReady(Exception):
    def __init__(self, doc_id: int) -> None:
        self.doc_id = doc_id
        super().__init__(f"Текст для документа {doc_id} ещё не готов")
