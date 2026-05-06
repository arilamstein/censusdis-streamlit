"""
Helpers for building Streamlit UI elements that appear across multiple tabs.

Streamlit does not natively support using the same widget instance in more than
one tab. This module works around that by creating duplicate widgets—one per tab—
and keeping them synchronized via `st.session_state`.

Each widget is given a unique key of the form `<tab>_<element>`. When a widget
changes, `update_keys()` propagates the new value to the corresponding widgets
in all other tabs. UI functions only need to declare which tab they belong to;
the synchronization logic is handled centrally.
"""

import streamlit as st

import backend as be

VALID_TABS = ["trend", "compare", "ranking"]


def validate_tab(tab: str) -> None:
    if tab not in VALID_TABS:
        raise ValueError(f"tab must one of {VALID_TABS}. {tab} given")


def gen_key(tab: str, ui_element: str) -> str:
    return f"{tab}_{ui_element}"


def update_keys(updated_key: str) -> None:
    """
    Propagate the updated value of a UI element to the same element
    across all tabs. Ensures synchronized state for shared selectors.
    """

    new_value = st.session_state[updated_key]

    ui_element = updated_key.partition("_")[2]
    for one_tab in VALID_TABS:
        key_to_update = gen_key(one_tab, ui_element)
        if key_to_update != updated_key:
            st.session_state[key_to_update] = new_value


def demographic_selector(tab: str) -> str:
    validate_tab(tab)

    options = be.get_demographic_statistics()

    key = gen_key(tab, "demographic_selector")
    column = st.selectbox(
        "Demographic:",
        options=options,
        key=key,
        on_change=lambda: update_keys(key),
    )
    return column


def location_selector(tab: str) -> str:
    validate_tab(tab)

    location_options = be.get_all_names()
    key = gen_key(tab, "location_selector")
    location = st.selectbox(
        "Location:",
        options=location_options,
        placeholder="Search for a place...",
        index=None,
        key=key,
        on_change=lambda: update_keys(key),
    )
    if location is None:
        location = "United States"
    return location


def location_and_demographic_block(tab: str) -> tuple[str, str]:
    st.markdown(
        "**Start typing** the name of a State, County, or City to search for it. "
        "Leave blank to view national totals."
    )
    col1, col2 = st.columns(2)

    with col1:
        location = location_selector(tab)

    with col2:
        column = demographic_selector(tab)

    return location, column
