## data_summarization.py

Extract data corresponding to validation paths from the entire logs into inputs_path1.csv and inputs_path2.csv

## learn.py

Learn the optimal values of the parameters ε and P<sub>0</sub> for each of the access points using

- Linear Regression
- Validation Data Path1 or Path2

## predict.py

Apply the Downhill Simplex Algorithm on to find the coordinate of the mobile device (instead of finding it geometrically).

## utility.py: Functions

- **jitter_error**

	Angle of deviation from original Path.
	Can be used as a part of target function to be optimized.
	But, downhill fails to optimize if this is included. Can try other optimization algorithms.

	Arguments: *x, y, x1, y1, x2, y2*

	Original Direction:

	    x1,y1 -> x2,y2

	New Direction:

	    x2,y2 -> x,y

- **dell_jitter_error**

    Gradient of Angle of Deviaton from original path.
    May be needed by some optimization technique.

- **fs**

	Function **f** to be optimized

	Arguments:

		z: (x, y) [to be estimated]
		args: Other args required

	Returns:

		f(z, *args)

- **optimum**

    Optimize fs using Downhill simplex algorthm.

    Arguments:

    	cids: list of AP numbers e.g [1,2,3,4]
    	powers: list of powers corresponding to each AP
    	params: value of epsilon and P0 for each AP
    	zinit: initial estimate of the coordinate(x,y)
    	x1: x coordinate of second last position
    	y1: y coordinate of second last position
    	x2: x coordinate of last position
    	y2: y coordinate of last position
