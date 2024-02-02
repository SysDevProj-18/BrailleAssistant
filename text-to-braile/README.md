- Install Bear for LSP support [https://github.com/rizsotto/Bear] 
- 
```
cd liblouis 
bear -- ./configure
bear -- make
make install
mv compile_commands.json ../
```
- Now you can open main.cpp in your favourite editor and enjoy LSP support :P
- To actually run the program, the following can be done 
```
gcc main.cpp -Wall -Wextra -pedantic -std=c++20 -I./liblouis/liblouis -llouis -o main && ./main
```
(Don't ask me at this time how I managed to pull this off, I don't know either :P)

The program as it stands isn't very helpful because it's not printing the unicode characters to the console. 

If you ran `make install`, it should move a bunch of executables to `/usr/local/bin`. One of them is called `lou_translate`.
So you should be able to run 
```
echo "apple" | lou_translate unicode.dis,en-us-g2.ctb
```
and get `⠁⠏⠏⠇⠑` as output.

Now I think it'd be good to be able to do this directly in C without interfacing with system calls. But if we fail to do that, we can do just that.

Another thing is how do we want to go forward with this project? Should we make a library so it's easier to work
with libloius because it's very fiddly to work with it directly. Or create some HTTP GET requests that 
can be used to translate text to braille. 

### Installing python bindings:
- Build liblouis as normal
- enter `liblouis/python` and run `sudo python3 setup.py install`
NB: alternatively you can use `python3 setup.py sdist` to get a tarball you can install via `pip install` which might be more portable?
- cython doesn't read libraries from `/usr/local/lib` by default, so run `export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/lib`
trying to find an alternative to doing this manually but coming up blank. maybe figure out how to generate a portable .so file or something? we can probably just throw a bash script wrapper on our python or something but thats depressing
- `import louis` in your python and use it as normal. docstrings are provided / readable on the liblouis gh
