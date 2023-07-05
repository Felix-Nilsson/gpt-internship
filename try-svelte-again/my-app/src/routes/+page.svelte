<!-- THIS IS THE STARTPAGE OF THE APP -->

<script>
    let response = '';

    const handleSubmit = e => {
        response = 'responsed';
    }

</script>
<body>
    <form action="http://localhost:5000/input" method='post'>
        <h1>Welcome to Medhelp</h1>
        <input type="text" name="prompt" placeholder="E.g. My toe hurts, what do I do?"/>
        <input type="submit" value="Send"/>
    </form>
    <h1>AI: {response}</h1>
</body>



<!--


    <script>

	let response = "";

  	const handleSubmit = e => {

		console.log("VAD FASEN")
		// getting the action url
		const ACTION_URL = e.target.action

		// get the form fields data and convert it to URLSearchParams
		const formData = new FormData(e.target)
		const data = new URLSearchParams()
		for (let field of formData) {
			const [key, value] = field
			data.append(key, value)
		}

		// check the form's method and send the fetch accordingly
		if (e.target.method.toLowerCase() == 'get') {
			print("test");
			console.log("vafan")
			fetch(`${ACTION_URL}?${data}`)
		}
		else {
			fetch(ACTION_URL, {
				method: 'POST',
				body: data
			})			
		}
		
		console.log("AASDBAJOBFBASFJABSFDKJJJJJJJJJJJJJJJJJJBDJASJDBASJDBASKJDFBLDKJBASLD");

		let new_response = "";

		fetch("./input")
			.then(d => d.text())
			.then(d => (response = d));

		while (new_response == response) {
			fetch("./input")
			.then(d => d.text())
			.then(d => (new_response = d));
		}
	
	}

  

  function getResponse() {
    fetch("./input")
      .then(d => d.text())
      .then(d => (response = d));
  }
</script>

<form action="http://localhost:5000/input" on:submit|preventDefault={handleSubmit}>
  <input name="prompt" placeholder="E.g. My toe hurts, what do I do?"/>
  <input type="submit" value="Send"/>
</form>
<h1>AI: {response}</h1>



-->
