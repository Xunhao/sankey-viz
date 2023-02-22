import pandas as pd
import plotly.graph_objects as go

# ==================================== Start - Code from Jupyterlite ====================================
df = pd.read_csv('data/train.csv')

# Not all columns are relevant so we will keep those we intend to analyse
df_trimmed = df[['Pclass', 'Sex', 'Age', 'Survived']]

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
	by = ['Pclass', 'Sex']
	)['Survived'].count().reset_index().rename(
	columns = {
	'Pclass': 'Source',
	'Sex': 'Target',
	'Survived': 'Value'
	},
	inplace = False
	)

df_trimmed_sankey_1['Source'] = df_trimmed_sankey_1.Source.map({1: 'Pclass1', 2: 'Pclass2', 3: 'Pclass3'})

# Part 2
df_trimmed_sankey_2 = df_trimmed.groupby(
	by = ['Sex', 'AgeGroup']
	)['Survived'].count().reset_index().rename(
	columns = {
	'Sex': 'Source',
	'AgeGroup': 'Target',
	'Survived': 'Value'},
	inplace = False
	)

# Part 3
df_trimmed_sankey_3 = df_trimmed.groupby(
	by = ['AgeGroup', 'Survived']
	)['Pclass'].count().reset_index().rename(
	columns = {
	'AgeGroup': 'Source',
	'Survived': 'Target',
	'Pclass': 'Value'
	},
	inplace = False
	)

df_trimmed_sankey_3['Target'] = df_trimmed_sankey_3.Target.map({0: 'Died', 1: 'Survived'})

# Union the sub parts to form the main sankey dataframe
sankey_main = pd.concat([df_trimmed_sankey_1, df_trimmed_sankey_2, df_trimmed_sankey_3], axis = 0)

# Manipulate dataset in order for Plotly to generate the Alluvial diagram
unique_source_target = list(pd.unique(list(sankey_main[['Source', 'Target']].values.ravel('K'))))

mapping_dict = {k:v for v, k in enumerate(unique_source_target)}

sankey_main['Source'] = sankey_main['Source'].map(mapping_dict)
sankey_main['Target'] = sankey_main['Target'].map(mapping_dict)

sankey_main = sankey_main.to_dict(orient = 'list')

# ==================================== End - Code from Jupyterlite ====================================

# Begin plotting Alluvial diagram using Plotly
sankey_fig = go.Figure(
	data = [
	go.Sankey(
		node = dict(
			pad = 15,
			thickness = 20,
			line = dict(color = 'black', width = 0.5),
			label = unique_source_target,
			color = 'blue'
			),

		link = dict(
			source = sankey_main['Source'],
			target = sankey_main['Target'],
			value = sankey_main['Value']
			)
		)
	]
	)

sankey_fig.update_layout(title_text = 'Titanic Survival Alluvial Diagram', font_size = 10)
sankey_fig.show()




