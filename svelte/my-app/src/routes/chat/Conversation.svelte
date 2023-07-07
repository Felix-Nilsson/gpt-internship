<script>
    import { Stack, Container, Flex, Group, Title, Paper, ThemeIcon,
        Input , Button, Center, Burger, Navbar, Header,} from '@svelteuidev/core';
    import UserBubble from './UserBubble.svelte';
    import AIBubble from './AIBubble.svelte';


    const DATA_URL = 'http://localhost:5001/data/get'

    let last_fetched = 1;
    let messages = [];
    let m_count = 0;

    // Basically a constant loop that keeps checking if the conversation has been updated in the backend

    //timer to make the while loop go slower
    const timer = ms => new Promise(res => setTimeout(res,ms))
    
    // Should be called when a query is submitted, so that it will keep checking until a new response is accessed, it will then stop until called again
    async function check_for_messages() {

        while(true) {
            //Give the server some breathing room
            await timer(1000);

            console.log('checking for updated conversation')

            //Check
            const response = await fetch(DATA_URL);
            const data = await response.json();
            
            console.log("last: " + String(last_fetched) + " conv time: " + data['time']);

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


<Stack align="center" spacing="lg" direction="column">
    
    <div style="padding-top: 100px; padding-bottom: 100px">
        {#if messages.length != 0}
            {#each messages as message}
                {#if (messages.indexOf(message) % 2 == 0)}
                    <Flex>
                        <UserBubble>{message}</UserBubble>
                        <div style="width: 20vw;"></div>
                    </Flex>
                {:else}
                    <Flex justify="right">
                        <div style="width: 20vw;"></div>
                        <AIBubble>{message}</AIBubble>
                    </Flex>
                {/if}
            {/each}
        {/if}
    </div>
    
    
</Stack>