# Attribute names
NODE_ID="node_ID"
MEASURE=""
TIMESTAMP=""
SOURCE=""
DESTINATION=""
DATASET="DATASET"

source_=""
destination_=""
measure_=""

# Control flags
flag_features_loaded=False
flag_dataset_loaded=False
flag_graph_constructed=False

# Dataframes
df_dataset = None
df_features = None

# Graph for detailed analysis
G = None

attributes_extraction=[]
columns_attributes_scatter_matrix=[]
input_file_path = None
number_datasets=1

# Figure definitions
figsize = [5, 4]
cmap = "jet"
plotly_width="100%"
plotly_height=800
