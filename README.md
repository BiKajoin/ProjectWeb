# Project: Deep Learning Model for Photovoltaic Nowcasting and Web Application

Earth is facing with energy crisis since energy demand is higher than production. 
Most energy sources are from non-renewable resources such as oil, natural gas, and coal, which are depleting.
These resources are all from fossils which cannot be replaced. They also require combustion which causes various negative effects on the environment. 
At the same time, There have been estimation that the Earth receives more than enough energy from the sun for the energy consumption on Earth. 
One of the main mechanisms used to produce energy from the sun is Photovoltaic Cell (PV Cell) which can convert sunlight directly into electricity. 
However, one of the critical problems that prevent PV Cell from becoming the main source of electricity production, is the fluctuation of electricity production, which depends on the weather. 
In this project, we study the relationship between electrical and environmental data and electricity production. 
Then we develop Deep Learning Nowcasting models that can predict electricity production and get the best model from the experiment 
as LSTM6x64_cloud_cover model with RMSE of 0.07065 and MAE of 0.04297. We also found that having cloud cover data helps the model to predict electricity production more accurately than without it. 
Moreover, the LSTM model works better than the MLP model. And using the model to convert cloud cover image data into variables for prediction still needs further specific development. 
After the model is finished, we have developed a web application for users to utilise the model easily. The web application also has a user system and a database management system for convenience. 
The web application is developed with Django Web Framework and MongoDB Cloud Database as specified above.
