from setuptools import setup, find_packages

setup(
        name="tsne",
        version="2020.12.12",
        packages=find_packages(),
        author="Adam Zhang",
        author_email="azhang30@jh.edu",
        description="t-SNE plugin for QIIME 2",
        license="NA",
        url="https://qiime2.org",
        entry_points={
            'qiime2.plugins':
            ['q2-tsne=q2_tsne.plugin_setup:plugin']
        },
        zip_safe=False,
)
