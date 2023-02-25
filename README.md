# titanic-survival-sankey-visualisation

## Project Details

### Description
This project utilises Jupyter notebook for data cleaning, exploration, manipulation, and analysis before moving Sublime Text 3 to plot out the Alluvial diagram

### Libraries
1. pandas
2. plotly

### Dataset
* [Titanic Passenger Survival Data Set](https://www.kaggle.com/c/titanic/data)

### Motivation
I find Sankey and Alluvial diagrams aesthetically pleasing. Apart from the diagrams being extremely colourful, the data flow from one node to another also makes it easy to show the change in state which facilitates story telling and pattern identification. I am curious as to how to build these visualisations and also understanding more about the requirement at the data frame level. Hence, I decided to use this project as a way to learn more it. 

### Limitations
1. I am still not completely satisifed with the colour scheme of both the nodes and links. It would have been better if I am able to connect the colour of the links with the nodes as shown [here](https://d2mvzyuse3lwjc.cloudfront.net/images/WikiWeb/Origin_2020_Feature_Highlights/2020Alluvial1.png?v=10831). This particular diagram is provides even more clarity in terms of the Survival status of each node. 
2. I would have preferred my Alluvial diagram to be designed as such - Pclass -> Sex -> AgeGroup -> Survival. However, I was not able to achieve it because the output is incorrectly even though the dataframe remains accurate. I tried figuring out but couldn't do so. By using - Pclass -> AgeGroup -> Sex -> Survival did the trick.

### Credits
1. [Generating Sankey Diagrams or Alluvial Diagrams with Python's Plotly Library | Jupyter Notebook](https://www.youtube.com/watch?v=yyVwvBUFRwY&t=831s)
    - This video alone was sufficient to provide a high-level understand on building a basic Alluvial diagram using Plotly. I used this as a base reference and value added my own ideas from there.
