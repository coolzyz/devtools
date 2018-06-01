
.PHONY : ctags systags 

ctags:
	@ctags -R -h ".c.cpp.h" -o tags
	@find . -type f -name "*.lua" | xargs ltags

systags:
	@ctags -I __THROW --file-scope=yes --langmap=c:+.h  --languages=c,c++ --links=yes --c-kinds=+p -R -f ~/.vim/systags /usr/include /usr/local/include

