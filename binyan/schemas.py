from pydantic import BaseModel


class BinyanInAppSchema(BaseModel):
    binyan: str
    text_ru: str
    text_ua: str
    text_en: str

    class Config:
        orm_mode = True
        from_attributes = True