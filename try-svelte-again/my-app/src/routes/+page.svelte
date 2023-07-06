<!-- THIS IS THE STARTPAGE OF THE APP -->
<script>
	import Conversation from './Conversation.svelte';


    const DATA_URL = 'http://localhost:5001/data'

    const handleSubmit = e => {

        // get the form fields data and convert it to URLSearchParams
        const formData = new FormData(e.target);

        const data = new URLSearchParams()
        for (let field of formData) {
            const [key, value] = field;
            data.append(key, value);
        }
		fetch(`${DATA_URL}?${data}`);

		//Start looking for a response
		get_response();
	}

	let check;

    async function get_response() {
		check();
	}

</script>


<body>
	<!-- WE USE PORT 5001 FOR OUR PYTHON "BACKEND" -->
    <form on:submit|preventDefault={handleSubmit}>
        <h1>Welcome to Medhelp</h1>
        <input type="text" name="prompt" placeholder="E.g. My toe hurts, what do I do?"/>
        <input type="submit" value="Send"/>
    </form>

    <div/>

    <!--<button on:click={get_response}>Get Response</button>-->

	<h1>MESSAGES:</h1>
	<Conversation bind:check_for_messages={check}></Conversation>
    
</body>


<style>

	div {
		height: 40px;
	}

</style>