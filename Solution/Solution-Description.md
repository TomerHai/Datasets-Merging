# Environment pre-requisite

1. I’ve installed on my PC Anaconda python 3.11 and run everything under windows powershell from within anaconda JupyterLab. Naturally the python script can be executed using any working python 3.x environment.
2. Built a python script using the pandas library (which is good for data manipulation and processing) and the fastavro library (https://github.com/fastavro/fastavro), which is needed to "read" the binary avro.
3. For the fastavro to work, I had to import it to my env (as it does not come by default with anaconda) using pip install fastavro
4. I also downloaded the avro-tools-1.9.1.jar from https://repo1.maven.org/maven2/org/apache/avro/avro-tools/1.9.1/ and placed it on the same folder where the source files and executed python script sit.
5. Since there was no Avro schema file provided (usually an Avro schema defines the structure of the data stored in the Avro file, and it includes information about the types of the fields, their names, and the nesting structure),
   I needed to check if the fastavro library and the avro-tools JAR will be able to handle it without issues.
6. I checked the Avro file using notepad++ to see the file structure and indeed at the beginning there is avro.schema followed by 
   "type":"record","name":"record","fields":[{"name":"Name","type":"string"},{"name":"CountryCode","type":"string"},{"name":"Population","type":"long"}]".avro.codec, 
   which means it’s a standard avro and the library and avro-tools should have no problems handling it.
7. To understand how to use the pandas library correctly, I went over this site https://pandas.pydata.org/docs/user_guide/index.html
8. Same goes to the fastavro library from here: https://fastavro.readthedocs.io/en/latest/
9. Python code was commented well during the work, as I believe this is the best way to present your thinking and provide explanation to the code you write PLUS
   I find it very useful when reviewing other colleagues code, assuming they have the will and energy to document their explanations 😊

# Code execution + answers to questions #1-3

PS D:\Dropbox\Training\Python> python .\City.py
Combined and sorted data written to CombinedCityList.csv with UTF-8 encoding
Total number of rows in the result file: 2070
City with the most Population: Mumbai (Bombay)
Total population of all Cities with code name 'BRA': 55955012
PS D:\Dropbox\Training\Python>

# Question #4 – Improving the program’s performance

On a theoretical level, we can try to tackle this in different aspects (if we want to deal with larger sets of data):
1.	Optimize DataFrame Operations: 
    a.	We can try using vectorized operations and methods in Pandas to improve performance. 
    b.	These operations are optimized and can be significantly faster than using traditional loops.
2.	We can try using Chunked Reading for Large Files: 
    a.	For very large files that may not fit into memory, we can read them in chunks using parameters like chunksize in Pandas read_csv or fastavro.reader. 
    b.	This will allow us to process the data in smaller portions.
3.	We can use Parallel Processing: 
    a.	Depending on the nature of the operations, we can try performing parallel processing to perform computations concurrently. 
4.	Memory Management:
    a.	This might be another reason for using parallel processing of chunks, as large datasets in memory are not a good idea as it will impact performance.
5.	Choose Efficient Data Structures: 
    a.	Depending on the types of operations, choosing the right data structure can make a significant difference. 
    b.	For example, if we need to perform frequent lookups, I will consider using a dictionary.

# Question #5 – Scaling the solution

To scale the solution from a single node to a larger dataset (distributed computing), the following aspects can be considered:
1.	Distributed Computing Frameworks: 
    a.	As done in Hadoop or using a different computing framework like Apache Spark which can give the ability to scale the solution across multiple machines and avoid the memory limitation we have in a single node.
2.	Using MapReduce (Hadoop): 
    a.	This can assist in effectively processing the data in distributed architecture and allow further scalability growth.
3.	Data Partitioning: 
    a.	When distributing data, partitioning might improve the performance effectively, specifically if we use a clustered database and harness the power of multi-node computing.
4.	Leverage Cloud Services:   
    a.	In case we want to offer the solution in the cloud, we can leverage the cloud power in storage and computing to auto-scale dynamically.
5.	Parallel Algorithms:
    a.	We can try to change the code and algorithm to work in parallel. 
    b.	Some algorithms that work well on a single machine may need modification to take advantage of distributed computing.
6.	Fault Tolerance:
    a.	We can implement fault-tolerant strategies to overcome failures that may happen on distributed systems.
7.	Data Compression:
    a.	We should consider compressing data before storage and transmission to reduce storage and transfer costs. 
    b.	For example: unzipping file, processing, and then on-the-fly    compressing the result (gzip etc.). 
    c.	Since CSV files are text based, compressing is very fast and effective, and can reduce storage costs and transfer costs.

In general scaling solutions for large datasets often involve a trade-off between complexity and performance. 
The choice of approach depends on the specific requirements, the characteristics of the data, and the available infrastructure.
