Telephone: An Information Network Simulation
======================================
This project aims to explore the throughput of an information network 
composed of a virtual population's aggregate social networks, wherein 
individuals seek to use those they know in search of "knowledge" in the form 
of a piece of boolean data.

Background
----------
A simulation begins with two groups of individuals: those who are searching 
for the answer (a bit of boolean data) and those who already know.  Each 
step, those who do not know choose a random contact from their social 
networks to "call" and ask; if successful, then their search ceases otherwise
they continue with the additional efforts of the person contacted.  In this 
way, the search network expands as the simulation progresses.  Individuals 
that find the data then seek to "report" it back to those who first caused 
them to begin searching.  Eventually, either everyone who was searching will
find the data or the simulation will grind to a halt.  Finally, certain 
agents may be designated as "malicious" and, regardless of their own 
knowledge of the data, will never prove helpful to anyone but themselves and 
act as artificial barriers to information flow through the network.

Individuals that call one another are considered "busy" for a single time 
step; thus, only one call may be placed or received per person per step.  In 
addition, the following rules apply:

 * Individuals may not call the same person twice in a row (configurable).
 * Individuals may not call the person who initially caused them to begin 
 searching.  This is to ensure that information flows in a hierarchical manner.

There are a number of configurable parameters that a user may utilize to 
customize this project.  Aside from the standard initialization parameters 
related to demography, the distribution of social contacts 
may be either a maximum threshold or follow a normal distribution as desired.
In addition, the degree to which the resultant networks are reciprocal
may also be chosen.  Finally, whether or not individuals may (eventually) 
call the same person twice may also be selected; this is an important 
consideration for smaller network sizes.

Building and Running
--------------------
This project's dependencies are specified in `requirements.txt` and can be 
installed in whatever manner is considered best.  The easiest, if you do not 
mind user-level packages, is to run:
```shell
pip3 install requirements.txt --user
```
otherwise the usual chicanery with `virtualenv` works fine.

To build and run this project, execute the following:
```shell
python3 -m telephone.main
```
from the command line.  To view the simulation, point a web browser to
`127.0.0.1` port `:8521`.

To run the included tests:
```shell
python3 -m nose2
```

Screenshots
-----------
An example of this project in action is shown below:
![Running an example simulation.](screenshots/simulation-example.png "Action 
shot!")

The charts, in order of appearance, correspond to the following:

 * The first chart is a knowledge chart that tracks how many people have 
 discovered (through their networks) the piece of data.
   * Those with knowledge are in <span style="color:blue">blue</span>.
   * Those without knowledge are in <span style="color:red">red</span>.
 * The second is a state chart that reports how many people are in which 
 state.  The colors for these states are:

   * Reporting (<span style="color:green">green</span>).
   * Searching (<span style="color:red">red</span>).
   * Waiting (<span style="color:gray">gray</span>).

Dependencies
------------
This project is written in Python 3 and requires the following libraries:

 * [Mesa](https://mesa.readthedocs.io/en/latest/index.html), an agent-based 
 modeleing toolkit.
 * [NumPy](http://www.numpy.org/), a scientific computing library.
 * [Nose 2](https://nose2.readthedocs.io/en/latest/), a unit testing library.

License
-------
This project is released under the
[Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) license as specified
 in [License.txt](License.txt).
