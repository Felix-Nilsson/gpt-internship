<script>

    const DATA_URL = 'http://localhost:5001/data'

    let last_fetched = 1;
    let messages = []

    // Basically a constant loop that keeps checking if the conversation has been updated in the backend

    //timer to make the while loop go slower
    const timer = ms => new Promise(res => setTimeout(res,ms))
    
    // Should be called when a query is submitted, so that it will keep checking until a new response is accessed, it will then stop until called again
    async function check_for_messages() {

        while(true) {
            //Give the server some breathing room
            await timer(5000);

            console.log('checking for updated conversation')

            //Check
            const response = await fetch(DATA_URL);
            const data = await response.json();
            
            console.log("last: " + String(last_fetched) + " conv time: " + data['time']);
            console.log(data);

            let new_time = data['time'];
            
            //Check if the conversation has been updated,
            if (new_time > last_fetched){
                
                last_fetched = (new_time + 1);

                let conversation = data['messages'];
                messages = conversation;

                break;
            }
        }
    }

    export { check_for_messages };




</script>


{#if messages.length != 0}
		<ul>
			{#each messages as message}
				<li>
					<h2>
						{message}
					</h2>
				</li>
			{/each}
		</ul>
	{/if}