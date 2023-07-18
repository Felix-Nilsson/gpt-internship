<script>
    import { Stack, Flex, Box, Button, Text, Paper, Overlay, Title, Space, Loader, Center } from '@svelteuidev/core';
    import UserBubble from './UserBubble.svelte';
    import AIBubble from './AIBubble.svelte';
    import { onMount, tick } from 'svelte';


    const DATA_URL = 'http://localhost:5001/chat'

    let last_fetched = 1;
    let messages = [];
    //let explanations = [];
    let showModal = false;
    let element;

    onMount(() => scrollToBottom(element))

    const scrollToBottom = async (node) => {
        node.scroll({ top: node.scrollHeight, behavior: 'smooth' })
    }


    //Get the conversation from the backend and update the frontend, force forces an overwrite of the current values even if the backend values are the same
    async function check_for_messages(_depth = 0) {

        console.log("Checking for updated conversation...");

        //Check
        const response = await fetch(DATA_URL);
        const data = await response.json();
        
        let new_time = data['last_updated'];
        
        //If the conversation has been updated since we last checked, update local copy
        if (new_time > last_fetched){

            console.log("Updated conversation found!");
            
            last_fetched = new_time;

            let conversation = data['messages'];
            loading = false
            messages = conversation;
            await tick();
            scrollToBottom(element);
        }
        else {
            //_depth is just to stop the function from ever falling into a never-ending recursion
            if (_depth < 30) {
                check_for_messages(_depth = _depth + 1);
            }
        }
    }

    let loading = false;
    let new_temp_message = "";

    async function new_message_loading(query) {
        new_temp_message = query;
        loading = true;
        await tick();
        scrollToBottom(element);
    }

    export { check_for_messages , new_message_loading };


    let current_modal_message_id = 0;

    async function modalButtonPressed(message_id) {

        current_modal_message_id = message_id;

        //sources = messages[message_id]["sources"];
        //explanation = messages[message_id]["explanation"]

        showModal = true;
    }


    //Context for the chat
    let context = {};

    async function fetchContext() {
        const response = await fetch("http://localhost:5001/context");

        context = await response.json();
    }

    onMount(fetchContext);


</script>


<div bind:this={element} style="position:absolute; left: 0px; right: 0px; top: 0px; bottom: 0px; overflow:auto">
    <div style="position:relative; left: 15vw; width: 70vw;">
        <Space h={100}/>
        <Stack spacing="lg">
            {#if messages.length != 0}
                {#each messages as message, i}
                    
                    {#if (message['user'])} 
                        <!--User bubble-->
                        <Flex justify="left">
                            <UserBubble>{message['content']}</UserBubble>
                            <div style="width: 35vw; "></div>
                        </Flex>
                    {:else}
                        <!--AI bubble-->
                        <Flex justify="right"> 
                            <div style="width: 35vw;"></div>
                            <AIBubble>
                                {message['content']}
                                {#if context['type'] == "doctor"}
                                <Space h="xs" />
                                <Center> <!--Responsibility text-->
                                    <Text
                                        size='sm'
                                        weight='semibold'
                                        style="line-height: 1.5;">
                                            *OBS* Du bär alltid ansvaret mot patienten
                                    </Text>
                                </Center>
                                {/if}
                            </AIBubble>

                            <!--Modal button-->
                            <Button on:click={() => modalButtonPressed(i)} variant='subtle' radius="sm" size="xs" ripple> ? </Button>
                        </Flex>
                    {/if}

                {/each}
            {/if}

            <!--Loading response-->
            {#if loading}
                <Flex justify="left">
                    <UserBubble>{new_temp_message}</UserBubble>
                    <div style="width: 35vw; "></div>
                </Flex>
                <Flex justify="right">
                    <div style="width: 35vw; "></div>
                    <AIBubble><Loader variant='dots' color='orange'/></AIBubble>
                    <div style="width: 33px; "></div>
                </Flex>
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
    <div class="modal">
        <Paper style="position:relative; z-index: 5; max-height: 80vh; overflow:scroll;" shadow="md" color="white">
            <Title variant='gradient' gradient={{from: 'red', to: 'blue', deg: 45}}><b>Källor:</b></Title>
            <Space h="xl"/>
            <Stack spacing="xs">
                {#if messages[current_modal_message_id] != "!"}
                    {#each messages[current_modal_message_id]['sources'][1] as source}
                        <Text>
                            <b>{source["title"]}</b> &nbsp;
                            <a href={source["link"]} target="_blank" rel="noopener noreferrer">{source["link"]}</a>
                        </Text>
    
                        <Text>Utdrag: "{source["snippet"]}"</Text>
                        <Space h="sm"/>
                    {/each}
                {:else}
                    <Text>
                        ChatGPT använde sin träning, svaret kan innehålla felaktig information.
                    </Text>
                {/if}
            </Stack>
        </Paper>
    </div>
    
{/if}




<style>

    .modal {
        position: fixed; 
        top: 10vh; 
        left: 15vw; 
        width: 70vw; 
        max-height: 80vh; 
        z-index: 5; 
        padding: 25px
    }



</style>