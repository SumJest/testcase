import typing
from datetime import datetime

import pydantic


class UpdatableBaseModel(pydantic.BaseModel):


    def update(self, model: "UpdatableBaseModel" | dict):
        print("Обновляем модель на ", type(model))
        update = model.dict() if model is not dict else model
        updatedAt = None
        for k, v in update.items():
            original_value = getattr(self, k, None)
            if callable(getattr(original_value, "update", None)):
                setattr(self, k, getattr(self, k).update(v))
            else:
                if not hasattr(self, k) or getattr(self, k) != v:
                    updatedAt = datetime.now()
                    setattr(self, k, v)
                    print(f"Rec: Updating {k} na ({type(v)}){v}")
        if updatedAt and "updatedAt" in self.dict().keys():
            return self.model_copy(update={"updatedAt": updatedAt})
        return self

    class Config:
        validate_assignment = True