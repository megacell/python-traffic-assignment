# python-traffic-assignment
This is a Python implementation of the equilibrium assignment using the traditional Frank-Wolfe algorithm. At its heart, it relies on a All-or-Nothing assignment module which original Cython implementation is from: http://www.xl-optim.com/python-traffic-assignment/. 

Our Python implementation has been tested against Matthew Steel's C++ implementation of Bar-Gera's and Dial's origin-based solver: http://www.repsilat.com/EquilibriumSolver.html. Both yield same edge flow assignment on some of the test problems in: http://www.bgu.ac.il/~bargera/tntp/

Setup
-----
Compile the Cython code with the following command:

	python setup_Assignment.py build_ext --inplace

Test the compiled code with:

	python -m unittest discover


Run on Chicago sketch network
-----

The Chicago sketch network (387 zones; 933 nodes; 2950 links) can be found in: http://www.bgu.ac.il/~bargera/tntp/. The .txt files have to be converted into .csv files compatible with our algorithm:

	python process_data.py
	python visualization/to_geojson.py

Then Frank-Wolfe can be runned:

	python tests/frank_wolfe_large_networks.py

