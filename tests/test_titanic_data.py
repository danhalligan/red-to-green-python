"""Integrity checks for the Titanic passenger data."""

from exercises.data_analysis.titanic.loaders import load_titanic_data


def test_titanic_data_preserves_labels_identifiers_and_missingness():
    passengers = load_titanic_data()

    assert len(passengers) == 1309
    assert list(passengers[0]) == [
        "PassengerId",
        "Survived",
        "Pclass",
        "Name",
        "Sex",
        "Age",
        "SibSp",
        "Parch",
        "Ticket",
        "Fare",
        "Cabin",
        "Embarked",
    ]
    assert [row["PassengerId"] for row in passengers] == [
        str(number) for number in range(1, 1310)
    ]
    assert {row["Survived"] for row in passengers} == {"0", "1"}
    assert sum(row["Age"] is None for row in passengers) == 263
    assert sum(row["Fare"] is None for row in passengers) == 1
    assert sum(row["Cabin"] is None for row in passengers) == 1014
    assert sum(row["Embarked"] is None for row in passengers) == 2
    assert passengers[0]["Age"] == "29"
    assert passengers[0]["Ticket"] == "24160"
    assert sum(row["Survived"] == "1" for row in passengers) == 500
    assert all(not {"boat", "body", "home.dest"} & row.keys() for row in passengers)
