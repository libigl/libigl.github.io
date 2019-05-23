# Building the Website

For developers who want to contribute to the website/documentation of libigl.
The website is now hosted in [its own repository](https://github.com/libigl/libigl.github.io)
separate from the main libigl repository. You can edit directly pages of the website and create an
associated pull requests on github. For more substantial changes, you may want
to preview your changes to the website before committing them. The
instructions bellow explain how to *preview* or *deploy* the website on
github.

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
3. Build the website to generate the html locally (optional):
   ```bash
   mkdocs build
   ```
4. Deploy the website directly to github (will overwrite the gh-pages branch
   of the remote repository):
   ```bash
   mkdocs gh-deploy
   ```

!!! warning
    
    The `gh-deploy` script will overwrite the content of the `gh-pages` in the
    remote repository. Be sure of what you are doing before pushing new
    content with this command.

!!! tip

    * Be careful to not have any `<>` characters in your email in your
      `.gitconfig`, otherwise the `gh-deploy` script will fail.
    * Dead links can be checked using the
      [LinkChecker](https://linkchecker.github.io/linkchecker/) tool. Run the
      website locally, then run LinkChecker on it:
      ```bash
      linkchecker http://127.0.0.1:8000
      ```

## References

- [MkDocs](http://www.mkdocs.org/)
- [Material Theme](https://squidfunk.github.io/mkdocs-material/)
