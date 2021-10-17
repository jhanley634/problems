
ACTIVATE = source activate problems

all:
	@echo Hello, world!

perc:
	$(ACTIVATE) && percolate/bin/viz.py

# After `make jupyter`,
# navigate down to: percolate/notebooks/percolation_visualization.ipynb
jupyter:
	$(ACTIVATE) && env PYTHONPATH=../.. jupyter notebook
