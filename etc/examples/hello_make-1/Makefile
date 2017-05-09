.PHONY: all
all: hello

.PHONY: clean
clean:
	rm -f *.o hello

hello: hello.o
	$(CXX) $(CXXFLAGS) -o $@ $^
