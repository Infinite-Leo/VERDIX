import json
import os
from typing import Any, Dict
from pydantic import BaseModel
from ..locus.config import USER_MEMORY_FILE

class UserMemory(BaseModel):
    past_purchases: list[Dict[str, Any]] = []
    preferences: list[str] = []
    avoid: list[str] = []
    budget_patterns: Dict[str, float] = {}
    tx_history: list[str] = []

class MemoryAgent:
    def __init__(self, path: str = USER_MEMORY_FILE) -> None:
        self.path = os.path.abspath(path)
        self._ensure_memory_file()

    def _ensure_memory_file(self) -> None:
        directory = os.path.dirname(self.path)
        os.makedirs(directory, exist_ok=True)
        if not os.path.exists(self.path):
            with open(self.path, "w", encoding="utf-8") as file:
                json.dump({
                    "past_purchases": [],
                    "preferences": [],
                    "avoid": [],
                    "budget_patterns": {},
                    "tx_history": [],
                }, file, indent=2)

    def load_memory(self, user_id: str = "default") -> UserMemory:
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                data = json.load(file)
            return UserMemory(**data)
        except Exception:
            return UserMemory()

    def save_memory(self, memory: UserMemory) -> None:
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(memory.model_dump(), file, indent=2)

    def record_transaction(self, tx_id: str, product_name: str, price: float, rating: int = 0) -> None:
        memory = self.load_memory()
        memory.tx_history.append(tx_id)
        memory.past_purchases.append({
            "product": product_name,
            "price": price,
            "rating": rating,
            "note": "auto-recorded by VERDIX",
        })
        self.save_memory(memory)
