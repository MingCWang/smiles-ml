
### What I have done
1. Create and deployed the web application on render.com https://smiles-ml-web.onrender.com
2. Created a database on MongoDB atlas 
3. Created a docker image that serves the transformer model using FastAPI to perform inference and deployed it on render.com
4. Generated over 20 molecular images with the predicted plot and stored them in the database 

I chose to deploy the model on render.com and MongoDB atlas because it is free and easy to use, abstracting away the complexities of managing the infrastructure, while providing a scalable solution. The current application includes the following features
- User input SMILE string and generate a molecular image with the predicted plot. 
- Button when clicked will query 5 random SMILE strings from the database and display the molecular images with the predicted plot.

### Improvements
- Allow user to download the predicted image and plot
- Allow user to upload a file with multiple SMILE strings and generate the molecular images with the predicted plot
- Include error handling for invalid SMILE strings and other errors from the server

### Hosting: Assuming we will be given a pretrained model
- Static website (render.com): free
- Database (MongoDB atlas): free
  - storage: 512 MB 
- Server (render.com): free
  - bandwith: 100 GB
  - RAM: 512 MB
  - CPU: 0.1
### GPU usage
- Not required, unless you will be training the model actively
### Scaling:
The above is sufficent for the current application assuming a transformer model that has 
- 14 million parameters, and each parameter is a float32 (4 bytes)
- batch size of 2
- sequence length of 40
will only require around 62 MB of memory to perform inference on a single CPU.

However, due to the size of 512 MB, the server will not be able to return a large number of molecular images at once. Therefore, the current application is limited to 5 random SMILE strings from the database.

However, below is the scaling options for render.com for reference
- Server: $7 month
  - ![Screen Shot 2024-11-03 at 11 12 57 PM](https://github.com/user-attachments/assets/f76b51d7-3949-4020-a830-bc6b259f36d8)

