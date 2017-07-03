# Table of Contents
1. [Definition of the code](README.md#definition-code)
2. [Summary of approach](README.md#summary-approach)
3. [Dependencies](README.md#dependencies)
4. [Run instructions](README.md#run-instructions)

* Link to source code documentation [link](http://htmlpreview.github.com/?https://github.com/trangel/Data-Science/blob/master/tracking-purchases/src/doc.html).
* Link to test suite documentation [link](http://htmlpreview.github.com/?https://github.com/trangel/Data-Science/blob/master/tracking-purchases/insight_testsuite/doc.html).

# Definition of the code

This code is a real-time platform to analyze purchases within a social network of users, and detect any behavior that is far from the average within that social network.
This is a solution to the project defined at the Insight GitHub site [link.](https://github.com/InsightDataScience/anomaly_detection/blob/master/README.md)

# Summary of approach
This code aa


For details on the source code, please see the
[source code documentation](http://htmlpreview.github.com/?https://github.com/trangel/Data-Science/blob/master/tracking-purchases/src/doc.html).

# Dependencies

The following packages are required:


* python 3.6
* pandas
* numpy
* json

# Run instructions

With default input/output files:

`python src/anomaly_detection.py` 

By default the input/output file names are: *batch\_log.json*, *stream\_log.json* and *flagged\_purchases.json*.
Note that input files are always in directory *input\_log* and output files are in *output\_log*.

You can define the names of input/output files:

`python src/anomaly\_detection.py -i1 <batch_log_fname> -i2 <stream_log_fname> -o <output_fname>`

