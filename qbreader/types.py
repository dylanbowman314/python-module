"""Types and classes used by the library."""

from __future__ import annotations

import enum
from typing import (
    Any,
    Iterable,
    Literal,
    Optional,
    Self,
    Sequence,
    Type,
    TypeAlias,
    Union,
)


class Category(enum.StrEnum):
    """Question category enum."""

    LITERATURE = "Literature"
    HISTORY = "History"
    SCIENCE = "Science"
    FINE_ARTS = "Fine Arts"
    RELIGION = "Religion"
    MYTHOLOGY = "Mythology"
    PHILOSOPHY = "Philosophy"
    SOCIAL_SCIENCE = "Social Science"
    CURRENT_EVENTS = "Current Events"
    GEOGRAPHY = "Geography"
    OTHER_ACADEMIC = "Other Academic"
    TRASH = "Trash"


class Subcategory(enum.StrEnum):
    """Question subcategory enum."""

    AMERICAN_LITERATURE = "American Literature"
    BRITISH_LITERATURE = "British Literature"
    CLASSICAL_LITERATURE = "Classical Literature"
    EUROPEAN_LITERATURE = "European Literature"
    WORLD_LITERATURE = "World Literature"
    OTHER_LITERATURE = "Other Literature"

    AMERICAN_HISTORY = "American History"
    ANCIENT_HISTORY = "Ancient History"
    EUROPEAN_HISTORY = "European History"
    WORLD_HISTORY = "World History"
    OTHER_HISTORY = "Other History"

    BIOLOGY = "Biology"
    CHEMISTRY = "Chemistry"
    PHYSICS = "Physics"
    MATH = "Math"
    OTHER_SCIENCE = "Other Science"

    VISUAL_FINE_ARTS = "Visual Fine Arts"
    AUDITORY_FINE_ARTS = "Auditory Fine Arts"
    OTHER_FINE_ARTS = "Other Fine Arts"


class Difficulty(enum.StrEnum):
    """Question difficulty enum."""

    UNRATED = "0"
    MS = "1"
    HS_EASY = "2"
    HS_REGS = "3"
    HS_HARD = "4"
    HS_NATS = "5"
    ONE_DOT = "6"
    TWO_DOT = "7"
    THREE_DOT = "8"
    FOUR_DOT = "9"
    OPEN = "10"


class Tossup:
    """Tossup class."""

    def __init__(
        self: Self,
        question: str,
        formatted_answer: Optional[str],
        answer: str,
        category: Category,
        subcategory: Subcategory,
        set: str,
        year: int,
        packet_number: int,
        question_number: int,
        difficulty: Difficulty,
    ):
        self.question: str = question
        self.formatted_answer: str = formatted_answer if formatted_answer else answer
        self.answer: str = answer
        self.category: Category = category
        self.subcategory: Subcategory = subcategory
        self.set: str = set
        self.year: int = year
        self.packet_number: int = packet_number
        self.question_number: int = question_number
        self.difficulty: Difficulty = difficulty

    @staticmethod
    def from_json(json: dict[str, Any]) -> Tossup:
        """Create a Tossup from a JSON object.

        See https://www.qbreader.org/api-docs/schemas#tossups for schema.
        """
        return Tossup(
            question=json["question"],
            formatted_answer=json.get("formatted_answer", json["answer"]),
            answer=json["answer"],
            category=Category(json["category"]),
            subcategory=Subcategory(json["subcategory"]),
            set=json["setName"],
            year=json["setYear"],
            packet_number=json["packetNumber"],
            question_number=json["questionNumber"],
            difficulty=Difficulty(str(json["difficulty"])),
        )

    def __str__(self) -> str:
        """Return the question."""
        return self.question


class Bonus:
    """Bonus class."""

    def __init__(
        self: Self,
        leadin: str,
        parts: Sequence[str],
        formatted_answers: Optional[Sequence[str]],
        answers: Sequence[str],
        category: Category,
        subcategory: Subcategory,
        set: str,
        year: int,
        packet_number: int,
        question_number: int,
        difficulty: Difficulty,
    ):
        self.leadin: str = leadin
        self.parts: tuple[str, ...] = tuple(parts)
        self.formatted_answers: tuple[str, ...] = tuple(
            formatted_answers if formatted_answers else answers
        )
        self.answers: tuple[str, ...] = tuple(answers)
        self.category: Category = category
        self.subcategory: Subcategory = subcategory
        self.set: str = set
        self.year: int = year
        self.packet_number: int = packet_number
        self.question_number: int = question_number
        self.difficulty: Difficulty = difficulty

    @staticmethod
    def from_json(json: dict[str, Any]) -> Bonus:
        """Create a Bonus from a JSON object.

        See https://www.qbreader.org/api-docs/schemas#bonus for schema.
        """
        return Bonus(
            leadin=json["leadin"],
            parts=json["parts"],
            formatted_answers=json.get("formatted_answers", json["answers"]),
            answers=json["answers"],
            category=Category(json["category"]),
            subcategory=Subcategory(json["subcategory"]),
            set=json["setName"],
            year=json["setYear"],
            packet_number=json["packetNumber"],
            question_number=json["questionNumber"],
            difficulty=Difficulty(str(json["difficulty"])),
        )

    def __str__(self) -> str:
        """Return the parts of the bonus."""
        return "\n".join(self.parts)


QuestionType: TypeAlias = Union[
    Literal["tossup", "bonus", "all"], Type[Tossup], Type[Bonus]
]
SearchType: TypeAlias = Literal["question", "answer", "all"]

ValidDifficulties: TypeAlias = Literal[
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
]
UnnormalizedDifficulty: TypeAlias = Optional[
    Union[Difficulty, ValidDifficulties, Iterable[Union[Difficulty, ValidDifficulties]]]
]
UnnormalizedCategory: TypeAlias = Optional[
    Union[Category, str, Iterable[Union[Category, str]]]
]
UnnormalizedSubcategory: TypeAlias = Optional[
    Union[Subcategory, str, Iterable[Union[Subcategory, str]]]
]


class QueryResponse:
    """Class for responses to `api/query` requests."""

    def __init__(
        self: Self,
        tossups: list[Tossup],
        bonuses: list[Bonus],
        tossups_found: int,
        bonuses_found: int,
        query_string: str,
    ):
        self.tossups: list[Tossup] = tossups
        self.bonuses: list[Bonus] = bonuses
        self.tossups_found: int = tossups_found
        self.bonuses_found: int = bonuses_found
        self.query_string: str = query_string

    @staticmethod
    def from_json(json: dict[str, Any]) -> QueryResponse:
        """Create a QueryResponse from a JSON object.

        See https://www.qbreader.org/api-docs/query#returns for schema.
        """
        return QueryResponse(
            tossups=[
                Tossup.from_json(tossup) for tossup in json["tossups"]["questionArray"]
            ],
            bonuses=[
                Bonus.from_json(bonus) for bonus in json["bonuses"]["questionArray"]
            ],
            tossups_found=json["tossups"]["count"],
            bonuses_found=json["bonuses"]["count"],
            query_string=json["queryString"],
        )

    def __str__(self) -> str:
        return (
            "\n\n".join([str(tossup) for tossup in self.tossups])
            + "\n\n\n"
            + "\n\n".join([str(bonus) for bonus in self.bonuses])
        )
