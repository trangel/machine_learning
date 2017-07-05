# Test suite

## Notes:

* To test that the purchases database is sorted correctly (by timestamp and event order), set *debug=True* in the sources. 
This will write down the database into a file named *df.cvs*, which can be checked externally.

* To verify that user networks of degree *D* are correct, set *debug=True* and the network for each user will be printed out.

## Test suite

Here I detail the test suite:

*  **Test 1** 
Test provided by insights.

* **Test 2**
A network of 4 users and 1000 random purchases is given in the *batch_log* file.
Initially all purchases amounts range between 1 and 10.
In *stream_log*, I add first 100 purchases with amounts in the same range, and 4 other purchases with amounts deliberately above this range. 
If the code is correct, the latter should be tagged as *anomalous*.
This shows that the code can deal with larger databases, and verifies that statistics are correct. 

* **Test 3**
This test is similar to Test 2, but here the value of *timestamp* is equal for all purchases.
If *debug=True* in the sources, the history of purchase database is printed out into a file. 
This is useful to verify that purchases with same timestamp are indeed ordered by event index (order of event in input files), as required.

* **Test 4**
I divide users in two classes: *ID=* *a1*, *a2*, *a3* and *a4* belong to the first class, while *ID=* *b1* to *b4* to the second class.
The user-network degree is high (*D=4*).
Users of the each class are friends only to themselves, i.e., no friends belong to different classes.
I feed a database of around 2000 purchase records. 
For class 1, purchase amounts range from 1 to 10, while for class 2, amounts are substantially higher ranging from 100 to 1000.
Later, I add 1 purchase for each user with amount in the range of 100 to 1000.
The latter purchases are to be flagged as anomalous only for users of class 1.
If the above holds true, then this test shows that user networks are working correctly.

* **Test 5**
This is a larger dataset with 1200 entries.
This is to test the performance in a larger dataset.
For example, to improve the performance, I intentionally reduce the size of the history-of-purchases dataset constantly, so that it never gets too big.
This is done in the routine *db\_add\_entry.py* (see source doc.).
By keeping the dataset small, the total execution time was reduced by a factor of 4.

