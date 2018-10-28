# Building the Website

For developers who want to contribute to the website/documentation of libigl.
The website is now hosted in [its own
repository](https://github.com/libigl/libigl.github.io) separate from the main
libigl repository. You can edit directly pages of the website and create an
associated pull requests on github. For more substantial changes, you may want
to preview your changes to the website before committing them. The
instructions bellow explain how to *preview* or *deploy* the website on
github.

1. Install mkdocs and the material theme
   ```bash
   pip3 install -U --user mkdocs mkdocs-material
   ```
   Alternatively, use `pipenv` to install the dependencies:
   ```bash
   pip3 install -U --user pipenv
   pipenv install requests
   pipenv shell
   ```
2. Preview the website locally (in the root folder of the libigl project):
   ```bash
   python3 -m mkdocs serve
   ```
3. Build the website to generate the html locally (optional):
   ```bash
   python3 -m mkdocs build
   ```
4. Deploy the website directly to github (will overwrite the gh-pages branch
   of the remote repository):
   ```bash
   python3 -m mkdocs gh-deploy
   ```

!!! warning
    
    The `gh-deploy` script will overwrite the content of the `gh-pages` in the
    remote repository. Be sure of what you are doing before pushing new
    content with this command.

!!! tip

    * Be careful to not have any `<>` characters in your email in your
      `.gitconfig`, otherwise the `gh-deploy` script will fail.
    * Dead links can be checked using the
      [LinkChecker](https://wummel.github.io/linkchecker/) tool. Run the
      website locally, then run LinkChecker on it:
      ```bash
      linkchecker http://127.0.0.1:8000
      ```

The reason we are using `python -m mkdocs serve` instead of `mkdocs serve`
directly is because we are using local extensions for mkdocs. Those extensions
are located in the `scripts/` folder of libigl. Running `mkdocs` as a module
adds the current directory to the `PYTHONPATH`, allowing us to load those
extensions without installing them on the system or in a virtualenv.

## Known Issues

- Building the website with a recent version of mkdocs/Python-Markdown will
  not work. The problem is documented in libigl.github.io#8. Please let us
  know you are able to help.
- We are also working on setting up a proper python environment for building
  the website using conda/virtualenv. Right now it should work on Linux, but
  some problems may exist on macOS/Windows. We will update the documentation
  accordingly once this is resolved.

## References

- [MkDocs](http://www.mkdocs.org/)
- [Material Theme](https://squidfunk.github.io/mkdocs-material/)
