import pandas as pd
import plotly.graph_objects as go
import json

# ==================================== Start - Code from Jupyterlite ====================================
df = pd.read_csv('data/train.csv')

# Not all columns are relevant so we will keep those we intend to analyse
df_trimmed = df[['Pclass', 'Sex', 'Age', 'Survived', 'Name']]
df_trimmed['Sex'] = df_trimmed['Sex'].str.capitalize()

# Set up age binning
age_bins = [0,1,12,18,65,999]

# Add a new column 'AgeGroup' which takes on the age groups defined under - https://www.nih.gov/nih-style-guide/age
df_trimmed = df_trimmed.assign(
	AgeGroup = pd.cut(
		x = df_trimmed['Age'],
		bins = age_bins,
		right = True,
		include_lowest = False,
		labels = ['Infants', 'Children', 'Adolescents', 'Adults', 'Senior']
		)
	)

# Add a new category into the age bin and assign NaN to it
df_trimmed['AgeGroup'] = df_trimmed['AgeGroup'].cat.add_categories('Unknown')
df_trimmed['AgeGroup'] = df_trimmed['AgeGroup'].fillna('Unknown')

# Preparing Sankey dataframe by creating the relevant sub parts
# Part 1
df_trimmed_sankey_1 = df_trimmed.groupby(
	by = ['Pclass', 'AgeGroup']
	)['Name'].count().reset_index().rename(
	columns = {
	'Pclass': 'Source',
	'AgeGroup': 'Target',
	'Name': 'Value'
	}
	)

df_trimmed_sankey_1['Source'] = df_trimmed_sankey_1.Source.map({1: 'Pclass1', 2: 'Pclass2', 3: 'Pclass3'})

# Part 2
df_trimmed_sankey_2 = df_trimmed.groupby(
	by = ['AgeGroup', 'Sex']
	)['Name'].count().reset_index().rename(
	columns = {
	'AgeGroup': 'Source',
	'Sex': 'Target',
	'Name': 'Value'}
	)

# Part 3
df_trimmed_sankey_3 = df_trimmed.groupby(
	by = [
	'Sex', 'Survived']
	)['Name'].count().reset_index().rename(
	columns = {
	'Sex': 'Source',
	'Survived': 'Target',
	'Name': 'Value'
	}
	)

df_trimmed_sankey_3['Target'] = df_trimmed_sankey_3.Target.map({0: 'Died', 1: 'Survived'})

# Union the sub parts to form the main sankey dataframe
sankey_main = pd.concat([df_trimmed_sankey_1, df_trimmed_sankey_2, df_trimmed_sankey_3], axis = 0)

# Manipulate dataset in order for Plotly to generate the Alluvial diagram
unique_source_target = list(pd.unique(sankey_main[['Source', 'Target']].values.ravel('K')))

mapping_dict = {k:v for v, k in enumerate(unique_source_target)}

sankey_main['Source'] = sankey_main['Source'].map(mapping_dict)
sankey_main['Target'] = sankey_main['Target'].map(mapping_dict)

sankey_main_dict = sankey_main.to_dict(orient = 'list')

# ==================================== End - Code from Jupyterlite ====================================

# Begin plotting Alluvial diagram using Plotly

opacity = 0.4
rgb_color = [
	'rgba(31, 119, 180, 0.8)',
	'rgba(255, 127, 14, 0.8)',
	'rgba(44, 160, 44, 0.8)',
	'rgba(214, 39, 40, 0.8)',
	'rgba(148, 103, 189, 0.8)',
	'rgba(140, 86, 75, 0.8)',
	'rgba(227, 119, 194, 0.8)',
	'rgba(127, 127, 127, 0.8)',
	'rgba(188, 189, 34, 0.8)',
	'rgba(23, 190, 207, 0.8)',
	'rgba(31, 119, 180, 0.8)',
	'rgba(255, 127, 14, 0.8)',
	'rgba(44, 160, 44, 0.8)',
	'rgba(214, 39, 40, 0.8)',
	'rgba(148, 103, 189, 0.8)',
	'rgba(140, 86, 75, 0.8)',
	'rgba(227, 119, 194, 0.8)',
	'rgba(127, 127, 127, 0.8)',
	'rgba(188, 189, 34, 0.8)',
	'rgba(23, 190, 207, 0.8)',
	'rgba(31, 119, 180, 0.8)',
	'rgba(255, 127, 14, 0.8)',
	'rgba(44, 160, 44, 0.8)',
	'rgba(214, 39, 40, 0.8)',
	'rgba(148, 103, 189, 0.8)',
	'rgba(140, 86, 75, 0.8)',
	'rgba(227, 119, 194, 0.8)',
	'rgba(127, 127, 127, 0.8)',
	'rgba(188, 189, 34, 0.8)',
	'rgba(23, 190, 207, 0.8)',
	'rgba(255, 182, 193, 0.8)',
	'rgba(137, 207, 240, 0.8)',
	'rgba(255, 182, 193, 0.8)',
	'rgba(137, 207, 240, 0.8)'
	]

sankey_fig = go.Figure(
	data = [
	go.Sankey(
		# valueformat = '.0f', # Remove decimal point
		node = dict(
			pad = 15,
			thickness = 20,
			line = dict(color = 'black', width = 0.5),
			label = unique_source_target,
			color = 'rgb(234, 221, 202)' # Almond
			),

		link = dict(
			source = sankey_main['Source'],
			target = sankey_main['Target'],
			value = sankey_main['Value'],
			color = rgb_color
			)
		)
	]
	)

sankey_fig.update_layout(
	title_text = 'Titanic Survival Alluvial Diagram<br>Source: <a href = "https://www.kaggle.com/c/titanic/data">Titanic Passenger Survival Data Set</a>', # Add in data source here later
	autosize = True, # Scale to window boarder
	font = dict(
		family = 'Raleway',
		size = 18
		)
	)

sankey_fig.show()

