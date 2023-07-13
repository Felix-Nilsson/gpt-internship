<script>
    import { Stack, Flex, Box, Button, Text, Paper, Overlay, Title, Space } from '@svelteuidev/core';
    import UserBubble from './UserBubble.svelte';
    import AIBubble from './AIBubble.svelte';
    import { onMount, tick } from 'svelte';


    const DATA_URL = 'http://localhost:5001/chat'

    let last_fetched = 1;
    let messages = [];
    let explanations = [];
    let showModal = false;
    let element;

    onMount(() => scrollToBottom(element))

    const scrollToBottom = async (node) => {
        node.scroll({ top: node.scrollHeight, behavior: 'smooth' })
    }


    //Get the conversation from the backend and update the frontend, force forces an overwrite of the current values even if the backend values are the same
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
                await tick();
                scrollToBottom(element);

                let expl = data['explanations'];

                for (let i = 0; i < expl.length; i++) {
                    explanations[i] = {
                        tool: expl[i][0]["tool"],
                        tool_input: expl[i][0]["tool_input"],
                        sources: expl[i][1]
                    }
                }

                break;
            }
        }
    }

    export { check_for_messages };

    //let curr_tool = ""
    //let curr_input = ""
    let curr_sources = []

    async function modalButtonPressed(explanation_id) {

        let id = explanation_id - 1;
        id /= 2;

        //curr_tool =  explanations[id]["tool"];
        //curr_input = explanations[id]["tool_input"];
        curr_sources = explanations[id]["sources"];

        showModal = true;
    }


</script>


<div bind:this={element} style="position:absolute; left: 0px; right: 0px; top: 0px; bottom: 0px; overflow:auto">
    <div style="position:relative; left: 15vw; width: 70vw;">
        <Space h={100}/>
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
                            <Button on:click={() => modalButtonPressed(i)} variant='subtle' radius="sm" size="xs" ripple> ? </Button>
                        </Flex>
                    {/if}
                {/each}
            {/if}
        </Stack>
        <Space h={100}/>
    </div>
</div>

<!-- SOURCE MODAL -->
{#if showModal}
    <Box>
        <Overlay on:click={() => (showModal = false)} opacity={0.5} color='black' zIndex=4/>
    </Box>
    <div style="position:fixed; top:10vh; left:15vw; width: 70vw; max-height: 80vh; z-index: 5; padding: 25px">
        <Paper style="position:relative; z-index: 5; max-height: 80vh; overflow:scroll;" shadow="md" color="white">
            <Title variant='gradient' gradient={{from: 'red', to: 'blue', deg: 45}}><b>Källor:</b></Title>
            <Space h="xl"/>
            <Stack spacing="xs">
                {#if curr_sources != "!"}
                    {#each curr_sources as source}
                        <Text>
                            <b>{source["title"]}</b> &nbsp;
                            <a href={source["link"]} target="_blank" rel="noopener noreferrer">{source["link"]}</a>
                        </Text>
    
                        <Text>Utdrag: "{source["snippet"]}"</Text>
                        <Space h="sm"/>
                    {/each}
                {:else}
                    <Text variant='gradient' gradient={{from: 'red', to: 'yellow', deg: 45}}>
                        ChatGPT använde sin träning, svaret kan innehålla felaktig information.
                    </Text>
                {/if}
            </Stack>
        </Paper>
    </div>
    
{/if}