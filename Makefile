all:
	g++ -o main test_cpp/main.cpp -ggdb3
install:
	touch ~/.gdbinit
	echo "source "$(shell pwd)"/scripts/gdb_plot.py" >> ~/.gdbinit
	echo "source "$(shell pwd)"/scripts/PlotPoint.py" >> ~/.gdbinit
