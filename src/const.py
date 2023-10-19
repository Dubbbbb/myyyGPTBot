from dataclasses import dataclass



@dataclass(frozen=True)
class ButtonNames:
    ACTIVE_DIALOG: str = "Активный диалог ☑️"
    NEW_DIALOG: str = "Новый диалог 🆕"
    HISTORY_DIALOG: str = "История диалогов 📋"


@dataclass(frozen=True)
class Result:
    OK: int = 1
    ERROR: None = None

