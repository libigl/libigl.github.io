<!-- Hide h3+ from toc  -->
<style>.md-nav--secondary .md-nav__list .md-nav__list { display: none }</style>

!!! danger
    On October 15, 2018, a lighter version of the libigl repository will be pushed to the master branch.
    This new version will have its history rewritten, and that will invalidate all commit SHA1 numbers pointing to previous versions of libigl.

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
git submodule add https://github.com/libigl/libigl.git
```

If you have an existing **fork** of libigl, we strongly suggest that you delete it and fork the project anew. You will not be able to create a PR with a fork that has the old history.
If you have existing changes (e.g. from a pending PR), then simply apply the same changes on the newly forked project, and submit your PR again.

If you are **new** to libigl, there is nothing to do: use the new repository normally, and enjoy the new lightness!

### What About My Old Code?

We maintain a copy of libigl with the old history in the repository [libigl-legacy](https://github.com/libigl/libigl-legacy).
If you have an old code the depends on a specific version of libigl, simply update the url (e.g. by editing the `.gitmodules` file), and it will pick up the matching commit with the SHA1 number from the old history.

### Troubleshooting

If you are getting the following error when trying to clone a repository:

```
Submodule 'libigl' (git@github.com:libigl/libigl.git) registered for path 'external/libigl'
Cloning into '/home/user/foo/libigl-example-project/external/libigl'...
error: Server does not allow request for unadvertised object 03536c4aa44a399ed7134b68f04cf3773edebc73
Fetched in submodule path 'external/libigl', but it did not contain 03536c4aa44a399ed7134b68f04cf3773edebc73. Direct fetching of that commit failed.
```

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
