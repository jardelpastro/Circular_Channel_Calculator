import os
import sys


def create_fake_metadata():
    metadata_content = '''Metadata-Version: 2.1
Name: streamlit
Version: 1.24.0
Summary: The fastest way to build custom web apps
Home-page: https://streamlit.io
Author: Streamlit Inc
Author-email: hello@streamlit.io
License: Apache 2
'''

    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    metadata_dir = os.path.join(base_path, 'streamlit-1.24.0.dist-info')
    os.makedirs(metadata_dir, exist_ok=True)

    with open(os.path.join(metadata_dir, 'METADATA'), 'w') as f:
        f.write(metadata_content)