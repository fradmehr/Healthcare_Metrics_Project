Below is step by step process to run the pipeline:
1. Set up AWS connections using API gateway, IAM roles and policies, Lambda and S3 bucket.
2. Read files from google drive and incrementally loaded into S3 by using a python code (2. csv into S3-ELT.ipynb) and AWS credentials from step 1.
3. Upload files from S3; and run python code (3. Initial Data Analysis.ipynb) to create the visualizations.
4. Create streamlit app code (dashboard.py)
5. Save it in local directory and use below commands in the terminal:
6. cd <local directory that contains the streamlit app code>
7. Run: streamlit run dashboard.py
8. The final streamlit url will open (4. Streamlit dashboard presentation)

   <img width="488" height="194" alt="image" src="https://github.com/user-attachments/assets/1faf4f2d-0aa4-4de5-9a54-e85456cd9079" />
