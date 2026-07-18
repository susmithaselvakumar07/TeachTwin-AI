import streamlit as st


def apply_theme():

    st.markdown(
        """
        <style>

        /* -----------------------------
           Global Font
        ----------------------------- */

        @import url(
            'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap'
        );

        html,
        body,
        [class*="css"] {
            font-family: 'Inter', sans-serif;
        }


       /* -----------------------------
          Clearly Visible Input Boxes
          ----------------------------- */

        div[data-testid="stTextInput"] div[data-baseweb="base-input"] {

            border: 2px solid #64748B !important;

            background-color: white !important;

            border-radius: 0px !important;
}
div[data-testid="stTextInput"] div[data-baseweb="base-input"]:focus-within {

    border: 2px solid #2563EB !important;

}

        /* -----------------------------
           Text Area
        ----------------------------- */
         div[data-testid="stTextArea"] div[data-baseweb="base-input"] {

            border: 2px solid #64748B !important;

            background-color: white !important;

}
        
        div[data-baseweb="textarea"]:focus-within {

            border: 2px solid #2563EB !important;

        }


        /* -----------------------------
           Buttons
        ----------------------------- */

        .stButton > button {

            border-radius: 0px !important;

            font-weight: 600;

            padding: 10px;

        }


        /* -----------------------------
           Select Boxes
        ----------------------------- */

        div[data-baseweb="select"] {

            border: 2px solid #94A3B8 !important;

            border-radius: 6px !important;

        }


        /* -----------------------------
           Page Spacing
        ----------------------------- */

        .block-container {

            padding-top: 2rem;

            padding-bottom: 2rem;

        }

        </style>
        """,
        unsafe_allow_html=True
    )
