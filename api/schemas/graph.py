from pydantic import BaseModel, Field
from typing import Optional, List


class GraphRead(BaseModel):
    id: int
    title: str

    image_url: str
    error_url: str

    approximation_id: int
