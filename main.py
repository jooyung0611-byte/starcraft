import streamlit as st
import random

st.set_page_config(
    page_title="StarCraft Mini",
    page_icon="🚀",
    layout="wide"
)

# -----------------------------
# 게임 초기화
# -----------------------------
if "game_started" not in st.session_state:
    st.session_state.game_started = False

if "race" not in st.session_state:
    st.session_state.race = None

if "minerals" not in st.session_state:
    st.session_state.minerals = 50

if "scv_count" not in st.session_state:
    st.session_state.scv_count = 5

if "scv_mining" not in st.session_state:
    st.session_state.scv_mining = 0


# -----------------------------
# 시작 화면
# -----------------------------
if not st.session_state.game_started:

    st.title("⚔️ STARCRAFT MINI")
    st.subheader("종족을 선택하세요")

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔵 테란", use_container_width=True):
            st.session_state.race = "Terran"
            st.session_state.game_started = True
            st.rerun()

    with col2:
        st.button("🟣 프로토스", disabled=True, use_container_width=True)

    with col3:
        st.button("🟢 저그", disabled=True, use_container_width=True)

    st.info("현재는 테란만 플레이할 수 있습니다.")


# -----------------------------
# 테란 게임 화면
# -----------------------------
else:

    st.title("🔵 STARCRAFT MINI - TERRAN")

    # 상단 자원 표시
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("💎 미네랄", st.session_state.minerals)

    with col2:
        st.metric("👨‍🚀 SCV", st.session_state.scv_count)

    with col3:
        st.metric(
            "⛏️ 채취 중",
            st.session_state.scv_mining
        )

    with col4:
        if st.button("🔄 게임 재시작"):
            st.session_state.clear()
            st.rerun()

    st.divider()

    # -----------------------------
    # 맵
    # -----------------------------
    st.subheader("🗺️ 테란 기지")

    # 맵을 여러 구역으로 나눔
    map_cols = st.columns(5)

    mineral_positions = [
        0, 1, 2,
        5, 6, 7,
        10, 11, 12,
        15, 16, 17,
        20, 21, 22,
        3, 8, 13, 18, 23
    ]

    for i in range(25):

        column = map_cols[i % 5]

        with column:

            # 사령부
            if i == 12:
                st.button(
                    "🏢\n\n사령부",
                    disabled=True,
                    use_container_width=True
                )

            # 미네랄
            elif i in mineral_positions:
                if st.button(
                    "💎 미네랄",
                    key=f"mineral_{i}",
                    use_container_width=True
                ):

                    if st.session_state.scv_count > 0:

                        st.session_state.scv_mining += 1

                        # 미네랄 채취
                        st.session_state.minerals += 5

                        # SCV가 채취 중인 상태를 잠깐 표시
                        st.toast("⛏️ SCV가 미네랄을 채취했습니다!")

                        st.session_state.scv_mining -= 1

                        st.rerun()

            # 일반 지형
            else:
                st.button(
                    "🌑",
                    key=f"ground_{i}",
                    use_container_width=True
                )

    st.divider()

    # -----------------------------
    # SCV 관리
    # -----------------------------
    st.subheader("👨‍🚀 SCV")

    scv_cols = st.columns(5)

    for i in range(st.session_state.scv_count):

        with scv_cols[i % 5]:

            if st.button(
                f"SCV {i + 1}",
                key=f"scv_{i}",
                use_container_width=True
            ):

                st.session_state.minerals += 5

                st.toast(
                    f"SCV {i + 1}이 미네랄을 채취했습니다! +5"
                )

                st.rerun()

    st.divider()

    # -----------------------------
    # 설명
    # -----------------------------
    st.subheader("📋 현재 상황")

    st.write(
        "테란 기지가 건설되었습니다. "
        "SCV 5기가 지급되었습니다."
    )

    st.write(
        "💎 미네랄을 클릭하거나 SCV를 클릭해서 "
        "미네랄을 채취하세요."
    )
