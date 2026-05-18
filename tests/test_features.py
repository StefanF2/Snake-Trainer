from engine.features import FEATURE_NAMES, extract_features


def test_extract_features_length():
    snake = [(5, 5), (4, 5), (3, 5)]
    direction = (1, 0)
    food = (10, 5)

    features = extract_features(snake, direction, food, 24, 18)

    assert len(features) == len(FEATURE_NAMES)


def test_food_right_feature():
    snake = [(5, 5), (4, 5), (3, 5)]
    direction = (1, 0)
    food = (10, 5)

    features = extract_features(snake, direction, food, 24, 18)

    food_right_index = FEATURE_NAMES.index("food_right")
    assert features[food_right_index] == 1


def test_danger_front_at_wall():
    snake = [(23, 5), (22, 5), (21, 5)]
    direction = (1, 0)
    food = (10, 5)

    features = extract_features(snake, direction, food, 24, 18)

    danger_front_index = FEATURE_NAMES.index("danger_front")
    assert features[danger_front_index] == 1