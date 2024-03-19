## functions and embeddings


#### Setup and run
- `pip install -r requirements.txt`
- `streamlit run app.py`
- Open `http://localhost:8501` in the browser


#### functions and example queries
- `What is the temperature in San Francisco/Tokyo/Paris?`: This is hardcoded so only these 3 cities are available.
- `List few animated movies` or `List movies about wars in space`: Embeddings were made and added to mongodb. mongodb api required.
- `Find flights from BLR to DEL on 2024-03-12`: Only codes work, dates must be in the `yyyy-mm-dd` format. Source, destination and departure date has to be mentioned. Uses 3rd party api, has access to live data.
- `Make me a cup of coffee`: Hardcoded, gives static response. When talking to smart home appliances.
- All other queries that donot match any of the above will be responded directly by chatgpt.