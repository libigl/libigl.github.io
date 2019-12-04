# Building the Website

For developers who want to contribute to the website/documentation of libigl.
The website is now hosted in [its own repository](https://github.com/libigl/libigl.github.io)
separate from the main libigl repository. You can edit directly pages of the website and create an
associated pull requests on github. For more substantial changes, you may want
to preview your changes to the website before committing them. The
instructions bellow explain how to *preview* the website on your local machine.

### Prerequisites

1. If you do not already have it, install conda on your machine. We recommend using [miniconda3](https://docs.conda.io/en/latest/miniconda.html). On Linux you can run:
    ```bash
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    bash Miniconda3-latest-Linux-x86_64.sh
    ```
2. Install the conda environment for the website:
   ```
   conda env create -f libigl-website.yml
   ```

### Using mkdocs

1. Activate the conda environment installed on the previous step:
   ```bash
   conda activate libigl-website
   ```
2. Preview the website locally
   (run this command in the root folder of the libigl project):
   ```bash
   mkdocs serve
   ```

!!! tip

    Dead links can be checked using the [LinkChecker](https://linkchecker.github.io/linkchecker/)
    tool. Run the website locally, then run LinkChecker on it:
    ```bash
    linkchecker http://127.0.0.1:8000
    ```

### Deployment

Deployment has been automated through the use of GitHub Actions. The configuration file is located [here](https://github.com/libigl/libigl.github.io/blob/docs/.github/workflows/gh-pages.yml).

## References

- [MkDocs](http://www.mkdocs.org/)
- [Material Theme](https://squidfunk.github.io/mkdocs-material/)
