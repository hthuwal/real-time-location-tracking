## location.py

Predict coordinates using a heuristic. Plot the predicted path and actual path

## utility.py - Functions

- **heuristic_1**
	Estimate location based on circles.

    Arguments:

        circles -- list of ((x_center, y_center), radius)

    Returns:

        Centroid of Intersection of intersection of all pair of circles

- **heuristic_2**
    
    Estimate location based on circles.

    Arguments:
    	
    	circles -- list of ((x_center, y_center), radius)

    Returns:

        c = Centroid of Intersection of intersection of all pair of circles
        if c exists then c
        else Weighted centroid of all intersections where weight = 1/(r1 * r2)

- **heuristic_3**
	
	Estimate location based on circles.

	Arguments:

	    circles -- list of ((x_center, y_center), radius)

	Returns:

	    weighted average of the centers of circles where
	    weight = 1 / radius

- **fi**
	
	Find Intersection of circles.

	1. Centroid of Intersection of intersection of all pair of circles
	2. Centroid of intersction with min area among of intersection of all
	pair of circles
	3. None

	Arguments:

	    circles -- list of ((x_center, y_center), radius)

	Returns:

	    if 1 then 1 else if 2 then 2 else 3

- **rssi_to_dis**
	
	Calculate distance based on signal strength.

	Arguments:

	    signal -- Received Signal Strength

	Returns

	    dstance -- distance in inches/tile

- **signal_strength_to_distance**

	Calculate distance based on signal strength.

	Arguments:

	    signal -- Received Signal Strength
	    freq -- frequency of the signal

	Returns

	    dstance -- distance in inches/tile

- **root_mean_square_error**
	
	Give correct positions and Predicted Positions calculate the RMSQ error.

	Arguments:

	    validation [dict: key-time, value-(x,y)] -- Correct Postitions
	    test [dict: key-time, value-(x,y)] -- Predicted Postitions

	Returns:

	    RMSQ error