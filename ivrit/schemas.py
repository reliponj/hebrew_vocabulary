from typing import Optional

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

    class Config:
        orm_mode = True
        from_attributes = True


class VocabularySchema(BaseModel):
    word: str
    word_u: str
    word_a: str
    words1: str
    link: str
    root: str
    infinitive: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True


class SettingsSchema(BaseModel):
    app_about_ru: str
    app_about_ua: str
    app_about_en: str
    app_about_il: str

    app_verb_about_ru: str
    app_verb_about_ua: str
    app_verb_about_en: str
    app_verb_about_il: str

    app_binyan_about_ru: str
    app_binyan_about_ua: str
    app_binyan_about_en: str
    app_binyan_about_il: str

    class Config:
        orm_mode = True
        from_attributes = True


class BinyanSchema(BaseModel):
    binyan: str

    class Config:
        orm_mode = True
        from_attributes = True


class RCategorySchema(BaseModel):
    word: str
    description: str

    class Config:
        orm_mode = True
        from_attributes = True


class VerbSchema(BaseModel):
    binyans: list[BinyanSchema]
    chosen_binyan: BinyanSchema
    infinitives: list[str]

    main_form: RCategorySchema
    present: list[RCategorySchema]
    past: list[RCategorySchema]
    future: list[RCategorySchema]
    naklon: list[RCategorySchema]

    class Config:
        orm_mode = True
        from_attributes = True
