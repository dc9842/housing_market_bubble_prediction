# OMSCS_CSE_6242_Project
## Team 012: BubbleWarn  
Derek Cheng, Mahaveer Jain, Micah Jeng, Peter Hernandez, Victor Cerabone

## DESCRIPTION

BubbleWarn is a visual analytics system that combines predictive model algorithms with fundamental housing market factors to provide insights into housing market volatilities, risks, and rewards. This allows potential home buyers, investors, and policy makers to make pragmatic decisions by combining various predictive variables and public sentiment through Google search indices. The BubbleWarn model is also validated against 2006-07 U.S. housing market crisis data, where it has successfully identified the set of all benchmark states as being in a bubble period ahead of the crisis by 4 quarters. BubbleWarn also provides housing affordability scores by occupation which allows users to visually note where the most affordable homes exist. With both metrics, users can interactively explore various affordable housing markets and determine the market condition using two very intuitive ratios.​ 

## INSTALLATION

We have hosted our visualization on the Tableau public server. Simply navigate to: https://tinyurl.com/BubbleWarn 
If tinyurl link does not work, please try public Tableau link: 
https://public.tableau.com/app/profile/victor.cerabone6321/viz/BubbleWarn_16381386293050/HousingBubble

In our analysis we used Python and R for data gathering, cleaning, model selection, and performance evaluation. The libraries used are:
Python - Pandas, Numpy, Matplotlib, Seaborn, Statsmodels, Pytrends, Tabulate, CPI  
R - glmnet, tidyverse, lubridate  

## EXECUTION

BubbleWarn has two tabs to switch back and forth from: Housing Bubble and Housing Affordability. For the first tab "Housing Bubble", the user may interact with the slider to select a year and quarter to see the housing bubble score for each state in the U.S. Sliding the element from beginning to end lets the user visualize the bubble period for each state over time.

For the second tab "Housing Affordability", the housing affordability score (as defined in our final report and poster) is plotted for each CBSA metropolitan region in the U.S. On the right side, the user is given three inputs: year, alpha (ratio of income to spending budget), and job description. Once these interactive elements are selected, the personalized results are shown on the choropleth map.