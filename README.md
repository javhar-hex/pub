## Condorcet Ranking Utilities

This repository explores algorithms and data structures for constructing and analysing Condorcet-style rankings in pairwise comparison settings.

The core focus is on modelling tournaments as directed graphs and computing rankings under Condorcet and Kemeny-style optimisation criteria, including support for Condorcet splits.
A split is a partitioning into two subsets, where the aim is to minimize the Kemeny violation score between the two subsets. 
It determines the optimal choice for picking a subset of a given size, regardless of the ranking of the items.

# Design Philosophy

The codebase emphasises:

- Explicit modelling of graph structures: directed graphs, hypergraphs, tournaments.
- Separation of data representation from algorithmic logic.
- Deterministic and reproducible ranking procedures.
- Composable abstractions for experimentation with alternative scoring schemes.
- Clear semantic data types rather than loosely structured arrays, tuples, or dicts.

The implementation is written in Python and structured to support experimentation with ranking procedures under noisy or partially inconsistent preference data.

# Open Directions

- Probabilistic ranking under noisy duel scores.
- Heuristic approximations for large Condorcet matrices. Possible approaches:
  - Merge-Condorcet: mergesort analogue for Concorcet ranking.
  - Pointwise optimisation: Assuming a fixed ranking of n-1 items, the optimal position for the n-th element can be found in linear time. Iterate with stochastic descent.

## License
This project is licensed under the [Apache License 2.0](LICENSE).
