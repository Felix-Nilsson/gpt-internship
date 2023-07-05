<script>
  const handleSubmit = e => {
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
		if (e.target.method.toLowerCase() == 'get') fetch(`${ACTION_URL}?${data}`)
		else {
			fetch(ACTION_URL, {
				method: 'POST',
				body: data
			})			
		}
    getResponse()
	}

  let response = "";

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

<!--- 
<button on:click={getRand}>Get a random number</button>
-->

