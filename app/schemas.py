from pydantic import BaseModel


class UploadDocResponse(BaseModel):
    id: int
    path: str


class DeleteDocResponse(BaseModel):
    message: str
    id: int


class DocAnalyseResponse(BaseModel):
    status: str
    id: int


class GetTextResponse(BaseModel):
    id: int
    text: str
