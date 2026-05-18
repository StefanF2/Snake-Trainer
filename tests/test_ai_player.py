from engine.ai_player import load_model, predict_action
from engine.snake_logic import ACTION_STRAIGHT


class FakeModel:
    """
    Einfaches Testmodell.

    Es gibt immer die Aktion 2 zurück.
    """

    def predict(self, rows):
        return [2]


class BadFakeModel:
    """
    Fehlerhaftes Testmodell.

    Es gibt absichtlich eine ungültige Aktion zurück.
    """

    def predict(self, rows):
        return [99]


def test_load_model_missing_file(tmp_path):
    model_path = tmp_path / "missing_model.joblib"

    model = load_model(str(model_path))

    assert model is None


def test_predict_action_without_model():
    features = [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]

    action = predict_action(None, features)

    assert action == ACTION_STRAIGHT


def test_predict_action_with_fake_model():
    model = FakeModel()
    features = [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]

    action = predict_action(model, features)

    assert action == 2


def test_predict_action_invalid_model_output():
    model = BadFakeModel()
    features = [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]

    action = predict_action(model, features)

    assert action == ACTION_STRAIGHT