# cocus_challenge_2024
A code challenge for COCUS.

### Requirements are as follows:
Please implement the challenge below with Python. 
<br>It is not necessary to fulfil all below objectives.
<br>Consider any best coding practices you would use in your daily work.

1. **Web-Service**
<br>Develop a Web service with following functionality.

2. **File upload**
<br>Upload a text file and store it.

3. **one random line**
<br>Return one random line of a previously uploaded file via http as text/plain, application/json or application/xml depending on the request accept header. All three headers must be supported.
If the request is application/* please include following details in the response:
<br>• line number
<br>• file name
<br>• the letter which occurs most often in this line

4. **one random line backwards**
<br>Return the requested random line backwards (choose all files)

5. **longest 100 lines**
<br>Return the 100 longest lines of all files uploaded

6. **20 longest line of one file**
<br>Return the 20 longest lines of one file uploaded (choose file randomly or choose latest file)