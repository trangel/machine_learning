# Test suite

## Notes:

* To test that the purchases database is sorted correctly (by timestamp and event order), set *debug=True* in the sources. This will write down the database in a file *df.cvs*, which can be checked externally.

* To verify that user networks of degree *D* are correct, set *debug=True* and the network for each user will be printed out.

## Test suite

Here I detail the test suite:

*  **Test 1** 
Test provided by insights.

* **Test 2**
A network of 4 users and 1000 random purchases is given in the *batch_log* file.
Initially all purchases amounts range between 1 and 10.
In *batch_stream*, I add first 100 purchases with amounts in the same range, and 4 other purchases with amounts clearly above this range. The latter should be tagged as *anomalous*.
This shows that the algorithm can deal with larger databases, and verifies that statistics are correct. 

* **Test 3**
This test is similar to Test 2, but here the value of *timestamp* is set to the same for all purchases.
If *debug=True* in the sources, the history of purchase database is printed into a file. 
This is useful to verify that purchases with same timestamp are indeed ordered by event index (order of event in input files), as required.

* **Test 4**
I divide users in two classes: *ID=* *a1*, *a2*, *a3* and *a4* belong to the first class, and *ID=* *b1* to *b4* to the second class.
User network degree is high *D=4*.
Users of the each class are friends only to themselves, i.e., there are no friends belonging to different classes.
I feed a database of around 2000 records with purchases. 
For class 1, amounts range from 1 to 10, while for class 2, amounts are substantially higher ranging from 100 to 1000.
I then add 1 purchase for each user in the range of 100 to 1000.
The latter purchases are to be flagged only for users of class 1.
This test shows that user networks are working correctly.

<!------
#  <li> <b>Test 2.</b> Test for command line arguments.
#  Input/Output file names are passed as command line arguments.
#  This tests that command line arguments work correctly.
#  <li> <b>Test 3.</b> Test for user network.
#  For a network of degree 2 (D=2), the algorithm prints out the user network.
#  Only "befriend" and "unfriend" events appear. 
#  This tests the functions for adding and removing users/friends from the network.
#  </li>
#  <li> <b>Test 4.</b> Test for history-of-purchases database.
#  A small database of purchases is constructed and printed out at the end.
#  This tests that the database is correctly built and sorted, i.e., at end entries should be ordered by timeframe and order of appearance. 
#  </li>
#  <li> <b>Test 5.</b> Test for purchase statistics.
#  A small database is constructed. 
#  At the end, for a given set of purchases, the mean and standard deviation are printed out.
#  This checks that statistics correct, i.e., it tests routines to evaluate purchase statistics.
#  </li>
#  <li> <b>Test 6.</b> Tests for performance in a larger database.
#  A database of few thousands of records is built.
#  This test can serve to check performance of the algorigthm. 
#  Execution time is output for these means.
#  </li>
#</ul>  
#</body>
#</html>
#
--!>
