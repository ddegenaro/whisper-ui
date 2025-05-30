from setuptools import setup, find_packages

# Package metadata
NAME = 'whisper_ui'
VERSION = '1.2.16'
DESCRIPTION = 'A GUI for OpenAI\'s Whisper.'
URL = 'https://github.com/ddegenaro/whisper-ui'
AUTHOR = 'Dan DeGenaro'
AUTHOR_EMAIL = 'drd92@georgetown.edu'
LICENSE = 'MIT'
KEYWORDS = ['whisper', 'low-code', 'ASR', 'transcription']

# Read the contents of your README file
with open('README.md', 'r') as f:
    long_description = f.read()

# Define dependencies
INSTALL_REQUIRES = [
    'openai-whisper',
    'tkinterdnd2',
    'torch==2.6.0',
    'numpy==2.1.2'
    # Add other dependencies here
]

# Package configuration
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    keywords=KEYWORDS,
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
    entry_point = {
        'console_scripts': [
            'whisper_ui = whisper_ui.ui:main'
        ]
    },
    scripts=["Whisper_UI.command", "Whisper UI.cmd"]
)