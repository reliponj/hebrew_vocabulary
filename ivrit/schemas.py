from pydantic import BaseModel


class KluchSchema(BaseModel):
    value: str
    value_ru: str
    value_ua: str
    value_en: str

    class Config:
        orm_mode = True
        from_attributes = True


class RootSchema(BaseModel):
    root: str


class VocabularySchema(BaseModel):
    word: str
    word_u: str
    word_a: str
    words1: str

    class Config:
        orm_mode = True
        from_attributes = True


class SettingsSchema(BaseModel):
    app_about_ru: str
    app_about_ua: str
    app_about_en: str
    app_about_il: str

    class Config:
        orm_mode = True
        from_attributes = True
