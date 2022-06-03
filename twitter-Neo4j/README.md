1. Make sure to download Neo4j Desktop. This is important if you want to create and see a
graph of the tweets you're going to mine.
2. Once you have it downloaded and opened, create a Project and name it whatever you want.
3. From there, create a database
4. Create a user and password for the database and make sure to take note of them for
reference.
5. Next, you will need to start the database and note which Bolt port it is running on localhost.
This will be important for later.
6. Now, you will need to go into the Final_Deliverable.ipynb file and insert the port number into
bolt://localhost:{xxxx} so that py2neo will create a connection with your Neo4j graph database.
7. After that, fill in the user and password parameters with the corresponding credentials for
your database. This will give you access to read and write controls for the database.
8. Now that we have our graph database connection set up, turn your attention to the second
cell containing all the tokens. This file gets all the secrets, tokens and keys information from
creds.py which
is located in the same directory.
9. Go to creds.py and fill in all of your credentials. Double check to see if you have the access
that you think you have to Twitter's API.
10. After all this information is inputted, you are ready to go!

View the [full report](./Social_Media_Research_Report_Nallamotu_Sumanth.pdf).