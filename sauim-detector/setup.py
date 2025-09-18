from setuptools import setup, find_packages

setup(
    name="sauim-detector",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "librosa",
        "numpy",
        "scipy",
        "tensorflow",
        "tensorflow-hub",
        "joblib",
        "tqdm",
        "soundfile"
    ],
    entry_points={
        "console_scripts": [
            "sauim-detector=sauim_detector.cli:main"
        ]
    },
    include_package_data=True,  # garante que arquivos extra sejam incluídos
    package_data={
        "sauim_detector": ["models/*.joblib"],  # inclui os modelos
    },
)
