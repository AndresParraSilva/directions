from streamlit.testing.v1 import AppTest
from time import time
from unittest.mock import patch


@patch("random.choice")
def test_one_good_click(random_choice):
    random_choice.return_value = "above"
    at = AppTest.from_file("directions.py").run()
    at.button[0].click().run()
    assert at.session_state.counter == 2
    assert at.session_state.answer == "above"
    assert at.session_state.streak == "✅"
    assert at.session_state.pressed == "above"


@patch("random.choice")
def test_one_bad_click(random_choice):
    random_choice.return_value = "above"
    at = AppTest.from_file("directions.py").run()
    at.button[3].click().run()
    assert at.session_state.counter == 2
    assert at.session_state.answer == "above"
    assert at.session_state.streak == "❌"
    assert at.session_state.pressed == "below"


@patch("random.choice")
@patch("time.time")
def test_ten_clicks(test_time, random_choice):
    test_time.return_value = time()
    random_choice.return_value = "above"
    at = AppTest.from_file("directions.py").run()
    at.button[0].click().run()
    at.button[1].click().run()
    at.button[2].click().run()
    at.button[3].click().run()
    random_choice.return_value = "before"
    at.button[0].click().run()
    at.button[1].click().run()
    at.button[2].click().run()
    at.button[3].click().run()
    at.button[0].click().run()
    test_time.return_value = test_time.return_value + 1
    at.button[1].click().run()
    assert at.session_state.counter == 10
    assert at.session_state.streak == "✅❌❌❌✅✅❌❌❌✅"
    assert not at.exception
    assert len(at.markdown) == 4
    assert (
        at.markdown[2].value
        == f"Results: {4}/{10} ({4 / 10 * 100:.1f}%) in 1.00 seconds"
    )
