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



