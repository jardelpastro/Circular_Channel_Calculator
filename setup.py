import os
import streamlit


def get_streamlit_data_files():
    streamlit_path = os.path.dirname(streamlit.__file__)
    static_path = os.path.join(streamlit_path, 'static')

    files = []
    for root, dirs, filenames in os.walk(static_path):
        for filename in filenames:
            source_path = os.path.join(root, filename)
            dest_path = os.path.join('streamlit', 'static', os.path.relpath(source_path, static_path))
            files.append((source_path, dest_path))

    return files


def get_assets_files():
    assets_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
    files = []

    if os.path.exists(assets_path):
        for root, dirs, filenames in os.walk(assets_path):
            for filename in filenames:
                source_path = os.path.join(root, filename)
                dest_path = os.path.join('assets', filename)
                files.append((source_path, dest_path))

    return files