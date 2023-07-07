<h2> To run this svelte / flask application, </h1>

(The order of running the front/backend should not matter)

-> Open two terminals, one for the backend and one for the frontend

To run the backend,
- `cd ./svelte/`
- `python server.py`


To run the frontend,
- `cd ./svelte/my-app/`
- `npm install`
- `npm run dev -- --open` (Run the Svelte app)

    (`--open` opens the page in the browser automatically and can be ommitted.)

Note:
- The frontend should run on localhost:5000 and the backend on localhost:5001.

- It might be needed to install flask-CORS `pip install flask-cors`
  - (At this point there are probably many more packages that you might need to install)