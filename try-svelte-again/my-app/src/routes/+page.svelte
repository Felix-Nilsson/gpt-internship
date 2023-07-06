<!-- THIS IS THE STARTPAGE OF THE APP -->
<script>
	import Conversation from "./conversation.svelte";

    //Backend should be running on port 5001
    const DATA_URL = 'http://localhost:5001/data';

    let check;

    async function get_response() {
        check();
    }

    const handleSubmit = e => {

        //data contains the input
        let data = new FormData(e.target);

        fetch(DATA_URL, {
            method: "POST",
            body: JSON.stringify({'prompt': data.get('prompt')}),
            headers: {"Content-type": "application/json; charset=UTF-8"}
        });

		//Start looking for a response
		get_response();
	}

</script>


<body>
    <form on:submit|preventDefault={handleSubmit}>
        <h1>Welcome to Medhelp</h1>
        <input type="text" name="prompt" placeholder="E.g. My toe hurts, what do I do?"/>
        <input type="submit" value="Send"/>
    </form>

    <div/>

	<h1>MESSAGES:</h1>
	<Conversation bind:check_for_messages={check}></Conversation>
    
</body>


<style>

	div {
		height: 40px;
	}

</style>