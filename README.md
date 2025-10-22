# Streamlit OpenLineage visualization

This is a sample lightweight repo, to generate / emit events to file-system, and then render via streamlit.

Advised to use pyenv with python 3.12

## Setup
```
python -m venv venv
. venv/bin/activate
pip install streamlit pyvis openlineage-python uuid-extension attr watchdog
```

## Running

### Emit events (uses filesystem, needs read-write file-system)
```
python emit_events.py
```

### Run streamlit

```
python -m streamlit run app.py
```

### Cleanup

```
rm -rf openlineage_events*
```
