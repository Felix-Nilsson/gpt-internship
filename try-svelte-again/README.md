#To run this svelte / flask application,

(The order of running the front/backend should not matter)

-> Open two terminals, one for the backend and one for the frontend

Backend: 
- `cd .\try-svelte-again\`
- `python server.py` (Run the Flask server)

Frontend:
- `cd .\try-svelte-again\my-app\`
- `npm install`
- `npm run dev -- --open` (Run the Svelte app)



Note:
- The frontend should run on localhost:5000 and the backend on localhost:5001.

- It might be needed to install flask-CORS `pip install flask-cors`