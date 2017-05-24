.PHONY: clean
CC= g++
CFLAGS= -std=c++11 -pedantic -Wfatal-errors -Wconversion -Wredundant-decls -Wshadow -Wall -Wextra -O3

# cplex
ICPLEX = -I "../../../ibm/ILOG/CPLEX_Studio1263/cplex/include" -I "../../../ibm/ILOG/CPLEX_Studio1263/concert/include"
LCPLEX = -L "../../../ibm/ILOG/CPLEX_Studio1263/cplex/lib/x86-64_linux/static_pic" -L "../../../ibm/ILOG/CPLEX_Studio1263/concert/lib/x86-64_linux/static_pic" -lilocplex -lconcert -lcplex

OBJECTS_FILES= main.o Instance.o

bp: $(OBJECTS_FILES)
	$(CC) $(CFLAGS) $(OBJECTS_FILES) $(LCPLEX) -lm -lpthread -o bp

# Compilation des fichiers object
%.o: %.cpp %.hpp
	$(CC) $(CFLAGS) $< $(ICPLEX) -c -o $@

%.o: %.cpp
	$(CC) $(CFLAGS) $< $(ICPLEX) -c -o $@

clean:
	@rm -rf *.o cover
