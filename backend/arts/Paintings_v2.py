# flake8:noqa
from dataclasses import dataclass

import numpy as np
from catboost import CatBoostRegressor
from django.conf import settings


@dataclass
class ArtObject:
    category: str
    year: int
    height: float
    width: float
    work_material: str
    pad_material: str
    country: str
    sex: str
    solo_shows: str
    group_shows: str
    age: int
    is_alive: float = np.NaN
    count_title: float = np.NaN
    count_artist: float = np.NaN

    def get_data(self) -> np.ndarray:
        return np.array(
            [
                self.category,
                self.year,
                self.height,
                self.width,
                self.work_material,
                self.pad_material,
                self.count_title,
                self.count_artist,
                self.country,
                self.sex,
                make_shows_authority_from_shows(self.solo_shows),
                make_shows_authority_from_shows(self.group_shows),
                self.age,
                self.is_alive,
            ]
        )


def make_shows_authority_from_shows(shows: str) -> float:
    """
    Функция для преобразования строки(полей solo_shows и group_shows), содержащей информацию о выставках автора(будь то индивидуальных или групповых) в число - эквивалент суммарного посещения выставок
    с весами authorities(пока они все одинаковы). All shows - все выставки, имеющиеся у меня на данный момент, в дальнейшем будет пополняться.
    """
    all_shows = [
        "centre pompidou",
        "whitney museum of american art",
        "the metropolitan museum of art",
        "los angeles county museum of art (lacma)",
        "guggenheim museum bilbao",
        "louisiana museum of art",
        "hirshhorn museum and sculpture garden",
        "museum of contemporary art",
        "los angeles (moca)",
        "tate britain",
        "museum ludwig",
        "national gallery of victoria",
        "hamburger bahnhof",
        "neue nationalgalerie",
        "national portrait gallery - london",
        "art institute of chicago",
        "national museum of modern and contemporary art - korea (mmca)",
        "museo tamayo",
        "tel aviv museum of art",
        "tate liverpool",
        "international center of photography (icp)",
        "mca chicago",
        "new museum",
        "dallas museum of art",
        "brooklyn museum",
        "museum of modern art (moma)",
        "tate modern",
        "solomon r. guggenheim museum",
        "national gallery of art",
        "washington",
        "d.c.",
        "ullens center for contemporary art (ucca)",
        "san francisco museum of modern art (sfmoma)",
        "perez art museum miami (pamm)",
        "mass moca",
        "museo reina sofia",
        "moma ps1",
        "serpentine galleries",
        "museu d'art contemporani de barcelona (macba)",
        "jewish museum",
        "k20 grabbeplatz",
        "dia:beacon",
        "museum fur moderne kunst",
        "frankfurt (mmk)",
        "museum of contemporary art australia (mca)",
        "institute of contemporary art",
        "miami (ica miami)",
        "aspen art museum",
        "schirn kunsthalle frankfurt",
        "dallas contemporary",
        "hammer museum",
        "garage museum of contemporary art",
        "deichtorhallen hamburg",
        "yuz museum shanghai",
        "mori art museum",
        "the broad",
        "tai kwun",
        "fondation beyeler",
        "malba",
        "boston",
        "stedelijk museum amsterdam",
        "castello di rivoli",
        "leeum - samsung museum of art",
        "dia:chelsea",
        "kunstmuseum basel",
        "power station of art",
        "museo jumex",
        "met breuer",
        "lenbachhaus",
        "palazzo grassi - punta della dogana",
        "nasher sculpture center",
        "haus der kunst",
        "institute of contemporary arts",
        "london",
        "whitechapel gallery",
        "secession",
        "kunsthalle basel",
        "m+",
        "museo d'arte contemporanea di roma (macro)",
        "kroller-muller museum",
        "fondazione prada",
        "martin-gropius-bau",
        "the bass museum of art",
        "palais de tokyo",
        "rockbund art museum",
        "studio museum in harlem",
        "national gallery singapore",
        "k21 standehaus",
        "kw institute for contemporary art",
        "jeu de paume",
        "zeitz mocaa",
        "museum of old and new art",
        "musée du louvre",
        "museu de arte moderna de sao paulo (mam)",
        "museu de arte moderna (mam rio)",
    ]
    n = len(all_shows)
    authorities = [0.5 for i in range(n)]
    vector = [0 for i in range(n)]
    if not isinstance(shows, float):
        shows = set([k.strip().lower() for k in shows.split(",")])
        for i in range(n):
            if all_shows[i] in shows:
                vector[i] = 1
    return sum([vector[i] * authorities[i] for i in range(n)])


def predict(art_object: ArtObject) -> float:
    model = CatBoostRegressor().load_model(
        settings.BASE_DIR / "data/catboost_v1.json",
        format="json",
    )
    return np.clip(model.predict(art_object.get_data()), 1000, np.inf)


if __name__ == "__main__":
    data = ArtObject(
        category="Печать",
        year=1983,
        height=60.5,
        width=91.0,
        work_material="Цветная литография",
        pad_material="Сотканная бумага",
        country="Россия",
        sex="М",
        solo_shows="centre pompidou, whitney museum of american art, the metropolitan museum of art, los angeles county museum of art (lacma)",
        group_shows="whitney museum of american art, the metropolitan museum of art, los angeles county museum of art (lacma)",
        age=80,
    )
    print(predict(data))
