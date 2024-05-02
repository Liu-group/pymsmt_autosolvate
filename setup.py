from setuptools import setup, find_packages


setup(
    name='pymsmt_orca',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'MCPB_orca=MCPB_orca.__main__:main',
        ],
    },
    author='Sangni',
    description='A brief description of your program',
    install_requires=[
        # 任何依赖项，例如：'numpy>=1.18.0',
    ],
)
