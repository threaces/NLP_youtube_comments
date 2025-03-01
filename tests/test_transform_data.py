from src.transform_data import parse_views

def test_parse_views():

    example_text = 'dsafdwewww'
    expected_text = 100000

    result = parse_views(example_text)

    assert result == expected_text