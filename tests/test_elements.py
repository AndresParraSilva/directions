from streamlit.testing.v1 import AppTest
from time import time


def test_start():
    at = AppTest.from_file("directions.py").run()
    assert not at.exception


def test_buttons():
    at = AppTest.from_file("directions.py").run()
    at.button[0].click().run()
    assert at.session_state.pressed == "above"
    at.button[1].click().run()
    assert at.session_state.pressed == "left/izquierda/before"
    at.button[2].click().run()
    assert at.session_state.pressed == "right/derecha/after"
    at.button[3].click().run()
    assert at.session_state.pressed == "below"


def test_results():
    at = AppTest.from_file("directions.py")
    at.run()
    at.session_state.start = time()
    at.session_state.streak = "✅"
    at.session_state.counter = 10
    at.session_state.progression = [10.5, 9.2]
    at.run()
    assert not at.exception
    assert len(at.markdown) == 4
    assert at.markdown[2].value.startswith("Results:")
    # assert len(at.line_chart) == 1
