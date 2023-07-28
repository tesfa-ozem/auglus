# -*- coding: utf-8 -*-
from pydantic import BaseModel


class ExceptionResponseSchema(BaseModel):
    error: str
