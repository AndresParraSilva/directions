import pandas as pd
import random
import streamlit as st
from time import time


def on_click(direction):
    if not state.start:
        state.start = time()

    state.pressed = direction
    if state.answer in state.pressed:
        state.streak += "✅"
    else:
        state.streak += "❌"


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

if "counter" not in state:
    state.counter = 0
    state.answer = ""
    state.pressed = ""
    state.streak = ""
    state.start = None
    state.taken = False

if state.streak:
    st.markdown(f"Streak: {state.streak}")

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
        st.line_chart(df)
    if st.button("Play again"):
        del state.counter
        st.rerun()
    st.page_link(
        "https://github.com/AndresParraSilva/directions", label="© Andrés Parra"
    )
