<script>
    import { Stack, Flex, Box, Button, Text, Paper, Center } from '@svelteuidev/core';
    import UserBubble from './UserBubble.svelte';
    import AIBubble from './AIBubble.svelte';


    const DATA_URL = 'http://localhost:5001/data/get'

    let last_fetched = 1;
    let messages = [];
    let explanations = [];

    // Basically a constant loop that keeps checking if the conversation has been updated in the backend

    //timer to make the while loop go slower
    const timer = ms => new Promise(res => setTimeout(res,ms))
    
    // Should be called when a query is submitted, so that it will keep checking until a new response is accessed, it will then stop until called again
    async function check_for_messages(max_iterations=30, force=false) {

        for (let i = 0; i < max_iterations; i++) {

            console.log('checking for updated conversation')

            //Check
            const response = await fetch(DATA_URL);
            const data = await response.json();
            
            console.log("last: " + String(last_fetched) + " conv time: " + data['time']);

            let new_time = data['time'];
            
            //Check if the conversation has been updated,
            if (new_time > last_fetched || force){
                
                last_fetched = new_time;

                let conversation = data['messages'];
                messages = conversation;

                let expl = data['explanations'];
                explanations = expl;

                break;
            }

            //Give the server some breathing room
            //await timer(1000);
        }
    }

    export { check_for_messages };

    let showModal = false;

    const modalButtonPressed = (e) => {
        console.log(showModal)
        showModal = true
        console.log(showModal)
    }

    let explanation = "BLa bla bla blblablblbalba bl bl b abalba lbalbalb alb alba l balbal bal bal ba ba bal abl bal bal bal balbal babal lba lab baballbal balba balalbalba bal bal bla bal bal lba lba lba bal ba ballablba lba lba bl blba blba lba bal "

    async function get_explanation() {
        
    }


</script>


<div style="padding-top: 100px; padding-bottom: 100px; width: 70vw;">
    <Stack spacing="lg">
        {#if messages.length != 0}
            {#each messages as message, i}
                {#if (i % 2 == 0)}
                    <Flex justify="left">
                        <UserBubble>{message}</UserBubble>
                        <div style="width: 35vw; "></div>
                    </Flex>
                {:else}
                    <Flex justify="right">
                        <div style="width: 35vw; "></div>
                        <AIBubble>{message}</AIBubble>
                        <Button on:click={modalButtonPressed} variant='subtle' radius="sm" size="xs" ripple> ? </Button>
                    </Flex>
                {/if}
            {/each}
        {/if}
    </Stack>
</div>

{#if showModal}
    <Box on:click={() => showModal = false} css={{
        position: 'fixed',
        backgroundColor: 'black',
        opacity: 0.5,
        top: 0,
        left: 0,
        width: '100vw',
        height: '100vh',
        zIndex: 1
    }}/>
    <Paper style="position:fixed; z-index: 1; width: 60vw; height: 60vh;" shadow="md" color="white">
        {explanation}
    </Paper>
{/if}