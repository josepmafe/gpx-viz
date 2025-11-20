# GPX Visualization

`gpx-viz` is a Streamlit application that allows you to explore and analyze a given GPX file.


## How-to

### Chech out the app
You can test the app remotely in the Streamlit Cloud: check [gpx-viz](https://josepmafe-gpx-viz-srcappstreamlit-app-zyr9hb.streamlit.app)

### Deep dive
To run it locally, you need to install the project as
```bash
poetry install
```

Then run the app as
```bash
poetry run streamlit run src/app/streamlit_app.py 
```

If you modify the source code, you can check your sources as
```bash
poetry run ruff check src
````

