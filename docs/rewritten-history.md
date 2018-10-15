<!-- Hide h3+ from toc  -->
<style>.md-nav--secondary .md-nav__list .md-nav__list { display: none }</style>

!!! danger
    On October 15, 2018, a lighter version of the libigl repository has been pushed to the master branch.
    This new version has its history rewritten, which does invalidate all commit SHA1 numbers pointing to previous versions of libigl.
    See the full list of changes in the [changelog](RELEASE_HISTORY.md).

### Why Are We Doing This?

libigl was always intended as lightweight library. Over the year, the size of the git repository grew significantly for various reasons: large binary assets being committed to the main repository, optional submodules growing in size, etc. To remedy this, we have changed the way external dependencies are handled. But to truly reduce the size of the repository to something manageable, it was necessary to prune large binary files from the git history. **This means introducing breaking changes and invalidating existing commit SHA1 numbers.**

### How To Upgrade?

If you are using libigl as a **submodule**, I suggest you simply remove the submodule and add it again. To remove a submodule you can write
```
git submodule deinit external/libigl
git rm -rf external/libigl
```

And to add it again:
```
git submodule add https://github.com/libigl/libigl.git external/libigl
```

If you have an existing **fork** of libigl, we strongly suggest that you delete it and fork the project anew. You will not be able to create a PR with a fork that has the old history.
If you have existing changes (e.g. from a pending PR), then simply apply the same changes on the newly forked project, and submit your PR again.

If you are **new** to libigl, there is nothing to do: use the new repository normally, and enjoy the new lightness!

### What About My Old Code?

We maintain a copy of libigl with the old history in the repository [libigl-legacy](https://github.com/libigl/libigl-legacy).
If you have an old code the depends on a specific version of libigl, simply update the url (e.g. by editing the `.gitmodules` file), and it will pick up the matching commit with the SHA1 number from the old history.

### Troubleshooting

#### Problem 1

I have an old project with a submodule using libigl, but it is pointing to an invalid commit number:

```
Submodule 'libigl' (git@github.com:libigl/libigl.git) registered for path 'external/libigl'
Cloning into '/home/user/foo/libigl-example-project/external/libigl'...
error: Server does not allow request for unadvertised object 03536c4aa44a399ed7134b68f04cf3773edebc73
Fetched in submodule path 'external/libigl', but it did not contain 03536c4aa44a399ed7134b68f04cf3773edebc73. Direct fetching of that commit failed.
```

??? faq "How to fix"

    #### Steps to reproduce the problem:

    1. Suppose we have a parent project with libigl submodule in `external/libigl/`.
    2. Clone the parent repository
        ```
        git clone git@github.com:gabuzome/libigl-example-project.git
        ```
    3. Try to initialize the submodules with the command
        ```
        git submodule update --init --recursive
        ```
       this should produces the error you see above.

    #### Steps to fix the problem (execute *in that order*):

    1. Delete the local folder that contained the submodule
       ```
       rm -rf external/libigl/
       ```
    2. Delete the corrupted copy in the `.git/` folder
       ```
       rm -rf .git/modules/external/libigl/
       ```
    3. Change the `libigl/libigl.git` to `libigl/libigl-legacy.git` in the `.gitmodules` file. 
    > Or issue, on Linux
    >    ```
    >    sed -i 's|libigl/libigl.git|libigl/libigl-legacy.git|' .gitmodules
    >    ```
    > Or issue, on Mac OS X
    >    ```
    >    sed -i '' 's|libigl/libigl.git|libigl/libigl-legacy.git|' .gitmodules
    >    ```
    > 
    4. Update local configuration of your submodule repos with the new URL
        ```
        git submodule sync
        ```
    5. Clone the submodule with the new address
        ```
        git submodule update --init --recursive
        ```

#### Problem 2

I have a problem with my current project that I want to update to the latest version, but I messed up my submodule and somehow get this error message:

```
A git directory for 'external/libigl' is found locally with remote(s):
  origin  https://github.com/libigl/libigl.git
If you want to reuse this local git directory instead of cloning again from
  https://github.com/libigl/libigl.git
use the '--force' option. If the local git directory is not the correct repo
or you are unsure what this means choose another name with the '--name' option.
```

??? faq "How to fix"

    #### Steps to fix the problem (execute *in that order*):

    1. Delete the local folder that contained the submodule
       ```
       rm -rf external/libigl/
       ```
    2. Delete the corrupted copy in the `.git/` folder
       ```
       rm -rf .git/modules/external/libigl/
       ```
    3. Update local configuration of your submodule repos with the new URL
        ```
        git submodule sync
        ```
    4. Clone the submodule to the current tip of the repository
        ```
        git submodule update --init --recursive
        ```

#### Problem 3

I have updated my submodule to the latest version of libigl, but the CMake script is complaining about missing targets.

??? faq "How to fix"

    The files in the libigl repository have been restructured a little bit.
    The CMake build script are now located under `cmake/` instead of `shared/cmake/`.
    Please check out the latest version of the [FindLIBIGL.cmake](https://github.com/libigl/libigl-example-project/blob/master/cmake/FindLIBIGL.cmake) from the `libigl-example-project`.

### Problem 4

I have an existing fork with some changes, how do I update it to the latest version of libigl?

??? faq "How to fix"

    For now we advise that you keep a copy of your legacy fork (you can rename/archive your existing fork, etc.),
    and create a new fork from the current libigl repository. If you have existing changes that you would like
    to merge, you can also try to `cherry-pick` the individual commits, but the simplest solution might to recreate
    new commits with the desired changes.

#### Other Problems

Please check out the [changelog](RELEASE_HISTORY.md) page for the list of changes that have been merged into the main branch.
