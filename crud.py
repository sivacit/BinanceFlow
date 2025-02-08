from pydantic import BaseModel
from typing import Optional

class ToDoItem(BaseModel):
    id: Optional[int]
    task: str
    completed: bool

class BTCData(BaseModel):
    timestamp: str
    price: float
