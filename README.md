# NLP YouTube Comments

This project focuses on analyzing YouTube comments using Natural Language Processing (NLP) techniques. The goal is to extract, preprocess, and analyze comments to gain insights into viewer sentiments and opinions.

## Features

- **Data Collection**: Retrieve comments from YouTube videos.
- **Data Cleaning**: Preprocess comments by removing noise such as special characters, URLs, and excessive punctuation.
- **Sentiment Analysis**: Analyze the sentiment of comments to determine if they are positive, negative, or neutral.
- **Visualization**: Generate visual representations of sentiment distributions.

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/threaces/NLP_youtube_comments.git
   cd NLP_youtube_comments
   ```

2. **Create a Virtual Environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Data Collection**:

   - Use the `get_data.py` script to fetch comments from a specific YouTube video. Ensure you have the necessary API credentials and permissions.

2. **Data Cleaning**:

   - Run the `clean_data.py` script to preprocess the collected comments. This will remove unwanted noise and prepare the data for analysis.

3. **Sentiment Analysis**:

   - Utilize the `pipeline_video_id.py` script to perform sentiment analysis on the cleaned data. This will classify comments into positive, negative, or neutral categories.

4. **Visualization**:

   - Generate visualizations to represent the sentiment distribution of the analyzed comments. This can be done using various plotting libraries in Python.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

## License

This project is licensed under the MIT License.

