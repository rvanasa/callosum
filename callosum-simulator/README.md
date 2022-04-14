# C A L L O S U M
## Visualizer

### Setup:

- Install the latest [Python](https://www.python.org/) or [Anaconda](https://www.anaconda.com/) distribution
- (Optionally)
  [set up a virtual environment](https://www.geeksforgeeks.org/set-up-virtual-environment-for-python-using-anaconda/)
  for this project
- Run the following command to install the required dependencies:
    - `pip install -r requirements.txt`

### Scripts:

- `python server.py`
    - Start a room-relay server which listens for 
    - 
- `python visualizer.py [song_name] [start_time_seconds]`
    - Simulate the main visualizer using the selected song and start time.
    - Example: `python visualizer.py Abba 10` plays `music/Abba.ogg` starting 10 seconds into the track.
- `python wordsearch.py`
    - Solve the word search for the given `wordsearch.txt` and `words.txt` files.
    - Overwrites `wordsearch_solution.py`.
- `python speech.py`
    - Attempt speech-to-text for the given song using Google Speech Recognition.
    - Requires a JSON service key named `google_cloud_key.json` in the root directory.
