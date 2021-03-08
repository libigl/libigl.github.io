# Building the Website

For developers who want to contribute to the website/documentation of libigl.
The website is now hosted in [its own repository](https://github.com/libigl/libigl.github.io)
separate from the main libigl repository.

## Simple Workflow

1. For simple edits to the website, you can directly edit the pages online:
  ![](images/readme/edit-website.png)

2. Write your changes to the markdown file on github:
  ![](images/readme/edit-markdown.png)

3. Preview the modified page on github:
  ![](images/readme/edit-preview.png)

4. Finally, commit the changes to a new branch/fork and let github create a pull request with your changes:
  ![](images/readme/edit-commit.png)

Feel free to make your changes locally, and use something like dynamic previews in [VS Code](https://code.visualstudio.com/docs/languages/markdown) to preview your changes.
The files are just markdown so anything should work! For more complicated changes (e.g. to render math equations), you may want to run [mkdocs](https://www.mkdocs.org/) to preview the final website.

## Final Website Preview 

For more complicated changes, you may want to preview the website locally on your machine while editing its content.
You will need to run [mkdocs](https://www.mkdocs.org/) to do this. 
If you want to preview the website locally on your machine, you will need to run [mkdocs](https://www.mkdocs.org/)

### Prerequisites

#### Install Conda

If you do not already have it, install [miniconda](https://docs.conda.io/en/latest/miniconda.html) on your machine.

??? info "Instructions for Windows"

    - Option 1: Using [Chocolatey](https://chocolatey.org/):
      ```
      choco install -y miniconda3
      ```

    - Option 2: Using [Scoop](https://scoop.sh/):
      ```bash
      # Add the extras bucket
      scoop bucket add extras
      scoop install miniconda3
      ```
      
    - Option 3: [Manual Installation](https://conda.io/projects/conda/en/latest/user-guide/install/windows.html)

??? info "Instructions for macOS"

    - Option 1: Using Homebrew Cask:
      ```bash
      brew cask install miniconda
      ```

    - Option 2: [Manual Installation](https://conda.io/projects/conda/en/latest/user-guide/install/macos.html)
    ```bash
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
    bash Miniconda3-latest-MacOSX-x86_64.sh
    ```

??? info "Instructions for Ubuntu/Debian"

    1. Download the public GPG key and add the conda repository to the sources list
        ```bash
        # Install our public GPG key to trusted store
        curl https://repo.anaconda.com/pkgs/misc/gpgkeys/anaconda.asc | gpg --dearmor > conda.gpg
        install -o root -g root -m 644 conda.gpg /usr/share/keyrings/conda-archive-keyring.gpg

        # Check whether fingerprint is correct (will output an error message otherwise)
        gpg --keyring /usr/share/keyrings/conda-archive-keyring.gpg --no-default-keyring --fingerprint 34161F5BF5EB1D4BFBBB8F0A8AEB4F8B29D82806

        # Add our Debian repo
        echo "deb [arch=amd64 signed-by=/usr/share/keyrings/conda-archive-keyring.gpg] https://repo.anaconda.com/pkgs/misc/debrepo/conda stable main" > /etc/apt/sources.list.d/conda.list

        **NB:** If you receive a Permission denied error when trying to run the above command (because `/etc/apt/sources.list.d/conda.list` is write protected), try using the following command instead:
        echo "deb [arch=amd64 signed-by=/usr/share/keyrings/conda-archive-keyring.gpg] https://repo.anaconda.com/pkgs/misc/debrepo/conda stable main" | sudo tee -a /etc/apt/sources.list.d/conda.list
        ```

    2. Install the conda package manager:
        ```bash
        # Install it!
        apt update
        apt install conda
        ```

??? info "Instructions for RedHat/CentOS/Fedora"

    1. Download the GPG key and add a repository configuration file for conda
        ```bash
        # Import our GPG public key
        rpm --import https://repo.anaconda.com/pkgs/misc/gpgkeys/anaconda.asc

        # Add the Anaconda repository
        cat <<EOF > /etc/yum/repos.d/conda.repo
        [conda]
        name=Conda
        baseurl=https://repo.anaconda.com/pkgs/misc/rpmrepo/conda
        enabled=1
        gpgcheck=1
        gpgkey=https://repo.anaconda.com/pkgs/misc/gpgkeys/anaconda.asc
        EOF
        ```

    2. Install the conda package manager:
        ```
        yum install conda
        ```

??? info "Instructions for generic Linux"

    - [Manual installation](https://conda.io/projects/conda/en/latest/user-guide/install/linux.html):
      ```bash
      wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
      bash Miniconda3-latest-Linux-x86_64.sh
      ```

#### Create/Update Conda Environment

```
conda env update -f conda.yml
```


### Render the Website

1. Activate the conda environment installed on the previous step:
   ```bash
   conda activate libigl-website
   ```

2. Preview the website locally (run this command in the root folder of the libigl project):
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

- [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- [MkDocs](http://www.mkdocs.org/)
- [Material Theme](https://squidfunk.github.io/mkdocs-material/)
