### SMILES prediction generator
A React based web application that integrates a transformer model, visualizing predicted molecular structure from SMILE strings as inputs. This project serves as a basis to learn about basic ML infra & Ops.

### What I did
1. Deployed the web application on render.com https://smiles-ml-web.onrender.com
2. Created a MongoDB atlas database to store prediction results and perform caching.
3. Created a docker image that serves the transformer model.
4. Developed 4 REST API end points using FastAPI to perform inference https://ml-latest-zsx7.onrender.com/docs
5. Generated over 30 molecular images with the predicted plot and stored them in the database 

I chose to deploy the model on render.com and MongoDB atlas because it is free and easy to use, abstracting away the complexities of managing the infrastructure, while providing a scalable solution. The current application includes the following features
- User input SMILE string and generate a molecular image with the predicted plot. 
- Button when clicked will query 1 random SMILE strings from the database and display the molecular images with the predicted plot.

DEMO:

CPU is 0.1 with free tier, so the loading time is long.

https://github.com/user-attachments/assets/ec07de49-f2ec-4cad-9802-bbeb1fa1d486

### Web Improvements
- Allow user to download the predicted image and plot
- Allow user to upload a file with multiple SMILE strings and generate the molecular images with the predicted plot
- Include error handling for invalid SMILE strings and other errors from the server
- Implement a pagination system to allow the user to query multiple SMILE strings from the database

### Hosting: Assuming we will be given a pretrained model
- Static website (render.com): free
- Database (MongoDB atlas): free
  - storage: 512 MB 
- Server (render.com): free
  - bandwith: 100 GB
  - RAM: 512 MB
  - CPU: 0.1

### Scaling:
However, due to the size of 512 MB RAM, the server will not be able to return 10 molecular images at once. Therefore, without the data of the size of running an inference, the current application is set to generating single random results. 

To minimize the cost of scaling, I need to calculate the FLOPS of the model to obtain how much GPU the model needs to generate a response within a given time. 

Here are the articles that I'm referring to. 

1. [GPU estimation](https://medium.com/@samuel-taiwo/a-comprehensive-guide-to-selecting-and-estimating-gpus-for-serving-ml-models-23d2874dcbd8)
2. [Calculating FLOPS](https://www.adamcasson.com/posts/transformer-flops)

If I were to proceed with this deployment, I would migrate to AWS EC2 given the size of the target user base. For t2.medium instance with 2 CPU is around 406 USD a year. I don't have the exact time that it will take for a single prediction, but I can see it being around 10 seconds or below. Given the current one we're using is around 0.1 CPU. This is one of the cheapest options on the market which is around 0.0464 USD per Hour for performing model inference, as if I were to use AWS Sagemaker that is specialized for MLops, it would be around 24% more expensive than EC2. 



