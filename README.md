# Apriori Algorithm Implementation with Crimes in Boston
by Anuj Deshpande and Richa Gadgil


The dataset we were interested in exploring is about crimes in Boston from the years 2015-2018. We found this dataset on Kaggle (link below) and it contains records from the new crime incident report system from the Boston Police Department. While this dataset originally consisted of many different columns, from the type of incident to when and where the incident occurred, we decided to filter out some of the columns we didn't feel were necessary, listed below:
- Incident Number
- If the crime was a shooting
- The occurrence of the crime (Day, Month, Year)
- Lattitude/Longitude

Along with dropping columns we didn't feel were important for what we were interested in, because the original dataset had about 2.6 million observations, we decided to focus in on a specific month, hence we filtered out the dataset to only include entries from **January 2017**, cutting down on the number of observations to 7,535 rows.

Link to original Kaggle dataset: https://www.kaggle.com/ankkur13/boston-crime-data/version/3#_=_
