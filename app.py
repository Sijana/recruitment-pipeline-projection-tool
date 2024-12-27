import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import io

class FlexibleRecruitmentPipelineTool:
    def __init__(self):
        # Initialize session state for historical data and stages
        if 'historical_data' not in st.session_state:
            st.session_state.historical_data = None
        
        # Default stages if none are specified
        if 'interview_stages' not in st.session_state:
            st.session_state.interview_stages = [
                'Applications', 
                'Phone Screen', 
                'Technical Interview', 
                'Onsite Interview', 
                'Offers', 
                'Hires'
            ]
        
        # Initialize session state for projection results
        if 'projection_results' not in st.session_state:
            st.session_state.projection_results = None
    
    def configure_stages(self):
        """Allow user to configure interview stages"""
        st.sidebar.header("Configure Recruitment Stages")
        
        # Allow adding and removing stages
        num_stages = st.sidebar.number_input(
            "Number of Stages", 
            min_value=3, 
            max_value=10, 
            value=len(st.session_state.interview_stages),
            key="stage_count"
        )
        
        # Dynamic stage name inputs
        new_stages = []
        for i in range(num_stages):
            default_stage = (st.session_state.interview_stages[i] 
                             if i < len(st.session_state.interview_stages) 
                             else f"Stage {i+1}")
            stage_name = st.sidebar.text_input(
                f"Name for Stage {i+1}", 
                value=default_stage,
                key=f"stage_input_{i}"
            )
            new_stages.append(stage_name)
        
        # Save updated stages
        st.session_state.interview_stages = new_stages
        
        return new_stages
    
    def load_data(self, stages):
        """Allow users to upload historical recruitment data"""
        st.sidebar.header("Upload Historical Data")
        uploaded_file = st.sidebar.file_uploader(
            "Choose a CSV file", 
            type="csv"
        )
        
        if uploaded_file is not None:
            try:
                # Read the CSV file
                df = pd.read_csv(uploaded_file)
                
                # Validate DataFrame columns
                required_columns = ['Year'] + stages
                
                # Check if all required columns exist
                if all(col in df.columns for col in required_columns):
                    # Select only the relevant columns
                    df = df[required_columns]
                    st.session_state.historical_data = df
                    st.sidebar.success("Data successfully uploaded!")
                    return df
                else:
                    missing_cols = [col for col in required_columns if col not in df.columns]
                    st.sidebar.error(f"Missing columns: {', '.join(missing_cols)}")
                    return None
            except Exception as e:
                st.sidebar.error(f"Error loading file: {e}")
                return None
        
        return None
    
    def calculate_conversion_rates(self, df, stages):
        """Calculate conversion rates between recruitment stages"""
        if df is None or len(stages) < 2:
            return {}
        
        rates = {}
        for i in range(len(stages) - 1):
            from_stage = stages[i]
            to_stage = stages[i+1]
            
            try:
                conversion_rate = (df[to_stage].mean() / df[from_stage].mean()) * 100
                rates[f"{from_stage} to {to_stage}"] = conversion_rate
            except ZeroDivisionError:
                rates[f"{from_stage} to {to_stage}"] = 0
        
        return rates
    
    def project_pipeline(self, df, target_final_stage, stages):
        """Project pipeline volumes based on historical conversion rates"""
        # Calculate conversion rates
        rates = self.calculate_conversion_rates(df, stages)
        
        # Start from the target and work backwards
        projection = {stages[-1]: target_final_stage}
        
        # Reverse calculate required volumes through stages
        for i in range(len(stages) - 1, 0, -1):
            from_stage = stages[i-1]
            to_stage = stages[i]
            
            rate_key = f"{from_stage} to {to_stage}"
            if rate_key in rates and rates[rate_key] > 0:
                required_volume = projection[to_stage] / (rates[rate_key] / 100)
                projection[from_stage] = required_volume
        
        # Add conversion rates to projection
        projection['Conversion Rates'] = rates
        
        return projection
    
    def generate_projection_csv(self, projection, stages):
        """Generate a CSV file for download with projection data"""
        # Create DataFrame from projection
        projection_df = pd.DataFrame([projection])
        
        # Separate conversion rates
        conversion_rates = projection_df['Conversion Rates'].iloc[0]
        projection_df = projection_df.drop('Conversion Rates', axis=1)
        
        # Add conversion rates as additional columns
        for rate_name, rate_value in conversion_rates.items():
            projection_df[f'Conversion Rate - {rate_name}'] = rate_value
        
        # Create a buffer to store our CSV
        csv_buffer = io.StringIO()
        projection_df.to_csv(csv_buffer, index=False)
        
        # Create download button
        st.download_button(
            label="Download Projection as CSV",
            data=csv_buffer.getvalue(),
            file_name="recruitment_pipeline_projection.csv",
            mime="text/csv",
            key="download_projection_csv"
        )
    
    def visualize_pipeline(self, historical_df, projection, stages):
        """Create interactive visualizations of historical and projected data"""
        # Historical Data Line Chart
        historical_fig = px.line(
            historical_df, 
            x='Year', 
            y=stages,
            title='Recruitment Pipeline Changes Over Time',
            labels={'value': 'Number of Candidates', 'variable': 'Stage'}
        )
        
        # Update x-axis to show every 1 year
        historical_fig.update_xaxes(
            tick0=historical_df['Year'].min(), # Starting point for the ticks
            dtick=1 # Interval between ticks (1 year)
            )

        historical_fig.update_yaxes(
            dtick=200,
            tickcolor="white",
            gridcolor = "grey"
            )
        # Projection Bar Chart
        projection_df = pd.DataFrame([projection])
        projection_df = projection_df.drop('Conversion Rates', axis=1)
        
        projection_long = projection_df.melt(
            var_name='Stage', 
            value_name='Candidates',
            value_vars=list(projection_df.columns)
        )
        
        projection_fig = px.bar(
            projection_long, 
            x='Stage', 
            y='Candidates',
            title='Projected Recruitment Pipeline',
            labels={'Candidates': 'Number of Candidates'}
        )
        
        projection_fig.update_yaxes(
            tickcolor="white",
            gridcolor = "grey"
            )

        return historical_fig, projection_fig
    
    def run(self):
        """Main application runner"""
        st.title("Recruitment Pipeline Projection Tool")
        
        # Configure stages
        stages = self.configure_stages()
        
        # Load historical data
        historical_df = self.load_data(stages)
        
        if historical_df is not None:
            # Conversion Rates Display
            st.sidebar.header("Conversion Rates")
            rates = self.calculate_conversion_rates(historical_df, stages)
            for stage, rate in rates.items():
                st.sidebar.metric(stage, f"{rate:.2f}%")
            
            # Projection Inputs
            st.sidebar.header("Projection Parameters")
            target_final_stage = st.sidebar.number_input(
                f"Target Number of {stages[-1]}", 
                min_value=1, 
                value=10
            )
            
            # Generate Projection
            if st.sidebar.button("Generate Projection"):
                # Project pipeline
                projection = self.project_pipeline(
                    historical_df, target_final_stage, stages
                )
                
                # Store projection in session state
                st.session_state.projection_results = projection
                
                # Visualizations
                historical_fig, projection_fig = self.visualize_pipeline(
                    historical_df, projection, stages
                )
                
                st.plotly_chart(historical_fig)
                st.plotly_chart(projection_fig)
                
                # Display Projection Details
                st.write("### Projection Details")
                st.json({k:v for k,v in projection.items() if k != 'Conversion Rates'})
                
                # Conversion Rates Details
                st.write("### Conversion Rates")
                st.json(projection['Conversion Rates'])
                
                # Generate and display CSV download button
                self.generate_projection_csv(projection, stages)

def main():
    tool = FlexibleRecruitmentPipelineTool()
    tool.run()

if __name__ == "__main__":
    main()