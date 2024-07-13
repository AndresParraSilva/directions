import pandas as pd
import random
import streamlit as st
from streamlit_js_eval import streamlit_js_eval
from streamlit_shortcuts import add_keyboard_shortcuts
from time import time


def on_click(direction: str) -> None:
    if not state.start:
        state.start = time()

    state.pressed = direction
    if state.answer in state.pressed:
        state.streak += "✅"
    else:
        state.streak += "❌"


def has_consecutive_not_nulls(l: list) -> bool:
    ans = False
    for i in range(len(l) - 1):
        if l[i] and l[i + 1]:
            ans = True
            break
    return ans


state = st.session_state
st.header("Directions")
st.subheader("Press the correct button according to the indication in the center")

st.write(
    """<style>
[data-testid="column"] {
    width: calc(33.3333% - 1rem) !important;
    flex: 1 1 calc(33.3333% - 1rem) !important;
    min-width: calc(33% - 1rem) !important;
}
</style>""",
    unsafe_allow_html=True,
)

if "progression" not in state:
    state.progression = []

state.width = streamlit_js_eval(
    js_expressions="window.innerWidth",
    key="WIDTH",
    want_output=True,
)

if "counter" not in state:
    state.counter = 0
    state.answer = ""
    state.pressed = ""
    state.streak = ""
    state.start = None
    state.taken = False

if state.streak:
    st.markdown(f"Streak:<br/>{state.streak}", unsafe_allow_html=True)
else:
    if state.width > 300:
        st.markdown(
            "Time starts when the first button is pressed<br />You can use the arrow keys",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "Time starts when<br />the first button is pressed", unsafe_allow_html=True
        )

if state.counter < 10:
    c1, c2, c3 = st.columns(3)
    with c2:
        st.button("⬆️", on_click=on_click, args=("above",), use_container_width=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.button(
            "⬅️⏰",
            on_click=on_click,
            args=("left/izquierda/before",),
            use_container_width=True,
        )
    with c2:
        state.answer = random.choice(
            [
                "above",
                "left",
                "izquierda",
                "before",
                "right",
                "derecha",
                "after",
                "below",
            ]
        )
        st.markdown(
            f"<p style='text-align: center; font-size:20px;'>{state.answer}</h5>",
            unsafe_allow_html=True,
        )
    with c3:
        st.button(
            "⏰➡️",
            on_click=on_click,
            args=("right/derecha/after",),
            use_container_width=True,
        )
    c1, c2, c3 = st.columns(3)
    with c2:
        st.button("⬇️", on_click=on_click, args=("below",), use_container_width=True)
    add_keyboard_shortcuts(
        {
            "ArrowUp": "⬆️",
            "ArrowLeft": "⬅️⏰",
            "ArrowRight": "⏰➡️",
            "ArrowDown": "⬇️",
        }
    )
    state.counter += 1
else:
    ok = state.streak.count("✅")
    total = len(state.streak)
    if not state.taken:
        state.end = time()
        if ok == total:
            state.progression.append(round(state.end - state.start, 2))
        else:
            state.progression.append(None)
        state.taken = True
    st.write(
        f"Results: {ok}/{total} ({ok / total * 100:.1f}%) in {state.end - state.start:.2f} seconds"
    )
    if state.progression:
        st.write("Progression:")
        df = pd.DataFrame({"Seconds": state.progression})
        st.dataframe(df, hide_index=True)
        if has_consecutive_not_nulls(state.progression):
            st.line_chart(df)
        else:
            st.scatter_chart(df)
    if st.button("Play again" + (" (Home key)" if state.width > 300 else "")):
        del state.counter
        st.rerun()
    st.page_link(
        "https://github.com/AndresParraSilva/directions", label="© Andrés Parra"
    )
    add_keyboard_shortcuts(
        {
            "Home": "Play again (Home key)",
        }
    )
