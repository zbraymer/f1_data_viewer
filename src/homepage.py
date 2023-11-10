import streamlit as st
import os

png_dir = os.path.dirname(os.path.dirname(__file__))


def write():

    st.image(os.path.join(png_dir, 'pngs/f1_logo.png'))

    st.write()
    return


if __name__ == "__main__":
    write()
