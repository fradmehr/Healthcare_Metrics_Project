Below is step by step process to run the pipeline:
1. Set up AWS connections using API gateway, IAM roles and policies, Lambda and S3 bucket.
2. Read files from google drive and incrementally loaded into S3 by using a python code (2. csv into S3-ELT.ipynb) and AWS credentials from step 1.
3. Upload files from S3; and run python code (3. Initial Data Analysis.ipynb) to create the visualizations.
4. Create streamlit app code (dashboard.py)
5. Save it in local directory and use below commands in the terminal:
6. cd <local_directory_that_contains_the_streamlit_app_code>
7. Run: streamlit run dashboard.py
8. The final streamlit url will open (4. Streamlit dashboard presentation)

  <img width="496" height="190" alt="image" src="https://github.com/user-attachments/assets/f598514b-3fb0-415c-91a8-d39994d57480" />

