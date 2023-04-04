# Author: Mirela Cazzolato
# Date: March 2023
# =======================================================================

import config
import util
import pandas as pd
import streamlit as st
from streamlit_plotly_events import plotly_events


def fextraction_tab():
    st.write("Feature extraction")

    with st.expander("Select file with the pair of EHR attributes", expanded=True):
        form_featureext_file = st.form(key='form_featureext_file')
        # file_source_extraction = form_featureext_file.text_input("Input file path:")
        file_source_extraction = form_featureext_file.file_uploader(label="Select input file",
                                                                    type=['csv', 'txt'])

        # st.write(file_source_extraction)

        use_sample_file = form_featureext_file.checkbox("Use sample file",
                                    False, help="Use in-built sample file for a demo")

        if use_sample_file:
            file_source_extraction = "data/example_EHR.csv"

        form_featureext_file.form_submit_button("Load attribute names")

        if file_source_extraction is not None and file_source_extraction != '':
            st.success("Selected file: " + str(file_source_extraction))
            print('Selected EHR file for feature extraction:', file_source_extraction)
            
            util.read_ehr_data(file_source_extraction)

    if config.flag_dataset_loaded:
        with st.expander(label="Attributes to create the weighted bipartite graph", expanded=True):
            form_feature_columns = st.form(key='form_feature_columns')

            source = form_feature_columns.selectbox(
                            "Select SOURCE (left) attribute",
                            options=config.attributes_extraction,
                            index=0)
            destination = form_feature_columns.selectbox(
                            "Select DESTINATION (right) attribute",
                            options=config.attributes_extraction,
                            index=0)        
            measure = form_feature_columns.selectbox(
                            "Select MEASURE attribute",
                            options=config.attributes_extraction,
                            index=0)
            timestamp = form_feature_columns.selectbox(
                            "Select TIMESTAMP attribute",
                            options=config.attributes_extraction,
                            index=0)

            has_dataset_attribute = form_feature_columns.checkbox("\'DATASET\' attribute")
            
            run_graph_extraction = form_feature_columns.form_submit_button("Create graph and extract features")

        if run_graph_extraction:
            with st.spinner("Creating bipartite graph and extracting features..."):
                print(file_source_extraction, source, destination, measure, timestamp)
                df_sample_extracted_features = util.setup_graph_extract_features(file_source_extraction,
                                                                                source,
                                                                                destination,
                                                                                measure,
                                                                                timestamp,
                                                                                has_dataset_attribute=has_dataset_attribute)

            st.success("Finished feature extraction. Check local file \'data/grafeda_features.csv\'")
            st.write("Top rows of generated file:", df_sample_extracted_features)

            st.write("**Tip:** You need to *reload* the features in the next step (Tab EDA)")


def input_tab():
    st.write("Load pre-extracted features from EHRs")
    with st.expander(label="Select file with extracted features", expanded=True):
        file_ehr_features = st.file_uploader(label="Select features extracted from EHRs", type=['csv', 'txt'])
        use_example_file_features = st.checkbox("Use sample file with features",
                                                False,
                                                help="Use a pre-extracted file with features from the toy data sample")
        
        if use_example_file_features and not file_ehr_features:
            file_ehr_features = "data/grafeda_features.csv"

        if file_ehr_features:
            with st.spinner('Loading features'):
                util.read_features(file_ehr_features)
        
    if config.flag_features_loaded:
        st.success("Features loaded successfully!")

        with st.expander(label="Select file with EHR data", expanded=True):
            file_ehr_dataset = st.file_uploader(label="Select file with EHRs", type=['csv', 'txt'])
            use_example_file_dataset = st.checkbox("Use sample EHR file",
                                                    False,
                                                    help="Use a pre-extracted file with features from the toy data sample")
            
            if use_example_file_dataset and not file_ehr_dataset:
                file_ehr_dataset = "data/example_EHR.csv"

            if file_ehr_dataset:
                with st.spinner('Loading EHRs'):
                    util.read_ehr_data(file_ehr_dataset)
            
                if config.flag_dataset_loaded:
                    st.success("EHRs loaded successfully!")

            st.write(label="Select attributes to create the weighted bipartite graph")
            form_graph_columns = st.form(key='form_graph_columns')

            config.source_ = form_graph_columns.selectbox(
                            "Select SOURCE (left) attribute",
                            options=config.attributes_extraction,
                            index=0)
            config.destination_ = form_graph_columns.selectbox(
                            "Select DESTINATION (right) attribute",
                            options=config.attributes_extraction,
                            index=0)        
            config.measure_ = form_graph_columns.selectbox(
                            "Select MEASURE attribute",
                            options=config.attributes_extraction,
                            index=0)
            # timestamp = form_graph_columns.selectbox(
            #                 "Select TIMESTAMP attribute",
            #                 options=config.attributes_extraction,
            #                 index=0)

            run_graph_details = form_graph_columns.form_submit_button("Create graph")
            
            if run_graph_details:
                util.construct_graph(config.source_, config.destination_, config.measure_)

                if config.flag_graph_constructed:
                    st.success("Graph constructed successfully!")


def eda_tab():
    selected_points_mouse = []
    fig_scatter_matrix=None

    if config.flag_graph_constructed:

        form_featureext_file = st.form(key='form_dataset_view')
        st.write("Exploratory Data Analysis")

        form_hexbin_feature_selection = st.form(key="form_hexbin_feature_selection")

        config.feature1_hexbin = form_hexbin_feature_selection.selectbox("Select first feature",
                                    options=config.df_features.columns[1:],
                                    index=0)
        config.feature2_hexbin = form_hexbin_feature_selection.selectbox("Select second feature",
                                    options=config.df_features.columns[1:],
                                    index=1)

        submit_form_hexbin = form_hexbin_feature_selection.form_submit_button("Plot HexBin")

        if submit_form_hexbin:
            with st.expander(label="2-d HexBin", expanded=True):
                fig_hexbin = util.plot_hexbin()
                _, col_hexbin, _ = st.columns([1, 5, 1])
                with col_hexbin:
                    st.pyplot(fig_hexbin)
        
        form_scatter_matrix_feature_selection = st.form(key="form_scatter_matrix_feature_selection")

        config.columns_attributes_scatter_matrix = form_scatter_matrix_feature_selection.multiselect("Select features to visualize",
                                                        config.df_features.columns[1:])

        submit_form_scatter_matrix = form_scatter_matrix_feature_selection.form_submit_button("Plot Features")

        with st.expander(label="1-d Histograms", expanded=True):
            st.write("1-d Hists")

            figs_hist = [None] * len(config.columns_attributes_scatter_matrix)
            for i, feature in enumerate(config.columns_attributes_scatter_matrix):
                figs_hist[i] = util.plot_histogram(feature)
                st.pyplot(figs_hist[i])

        if config.flag_graph_constructed:
            with st.expander(label="Further details", expanded=True):
                st.success("EgoNet created successfully.")
                
                # if submit_form_scatter_matrix:
                fig_scatter_matrix = util.plot_scatter_plot_matrix()

                selected_points_mouse = plotly_events(fig_scatter_matrix, select_event=True,
                                                        override_height=config.plotly_height,
                                                        override_width=config.plotly_width,
                                                    )

                if len(selected_points_mouse) > 0:
                    st.write("Selected nodes:", len(selected_points_mouse))
                    df_selected = pd.DataFrame(selected_points_mouse)
                    st.dataframe(config.df_features.loc[df_selected["pointNumber"].values])
            
            with st.expander(label="EgoNet of selected points", expanded=True):
                if len(selected_points_mouse) > 0:
                    st.write("Heatmap-based adjacency matrix")

                    with st.spinner("Generating EgoNet of selected points"):

                        fig_adj_matrix, egonet_nodes = util.plot_interactive_scatter_selected_nodes(config.df_features.loc[df_selected["pointNumber"].values][config.NODE_ID])
                        selected_points_mouse = plotly_events(fig_adj_matrix, select_event=True,
                                                            #   override_height=config.plotly_height,
                                                            override_width=config.plotly_width,
                                                            )
                        st.dataframe(config.df_features[config.df_features[config.NODE_ID].isin(egonet_nodes)])
    else:
        st.write("Please, select EHR file and create graph in the \'Input Data\' tab to continue.")


def update_sidebar():
    """
    Add options to the sidebar
    """
    pass

    # with st.sidebar:
        # form_sidebar = st.form(key='form_sidebar')
        # config.number_datasets = form_sidebar.number_input("Number of datasets",
        #                                                    min_value=1, step=1)
        
        # form_sidebar.form_submit_button("Set settings")
    

def launch_dashboard():
    """
    Launch main window load specific tabs
    """
    
    update_sidebar()

    tab_feature_extraction, tab_input, tab_eda = st.tabs(["Feature Extraction",
                                                          "Input Data",
                                                          "EDA"])

    with tab_feature_extraction:
        fextraction_tab()
    with tab_input:
        input_tab()
    with tab_eda:
        eda_tab()

    