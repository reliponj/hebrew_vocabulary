from pydantic import BaseModel


class VocabularySchema(BaseModel):
    word: str
    word_u: str
    word_a: str
    words1: str

    class Config:
        orm_mode = True
        from_attributes = True
