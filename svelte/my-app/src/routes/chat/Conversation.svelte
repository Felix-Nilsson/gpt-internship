<script>
    import { Stack, Flex, Box, Button, Text, Paper, Overlay, Title, Space, Loader, Center, Tabs, Divider, Alert } from '@svelteuidev/core';
    import UserBubble from './UserBubble.svelte';
    import AIBubble from './AIBubble.svelte';
    import { onMount, tick } from 'svelte';
    import { InfoCircled } from 'radix-icons-svelte';

    const DATA_URL = 'http://localhost:5001/chat'

    let last_fetched = 1;
    let messages = [];
    //let explanations = [];
    let show_alert = false;
    //let alert_message = null;
    let show_modal = false;
    let element;

    onMount(() => scrollToBottom(element))

    const scrollToBottom = async (node) => {
        node.scroll({ top: node.scrollHeight, behavior: 'smooth' })
    }


    //Get the conversation from the backend and update the frontend, force forces an overwrite of the current values even if the backend values are the same
    async function check_for_messages(_depth = 0) {

        console.log('Checking for response...')

        //Get the latest version of the conversation from the backend
        const response = await fetch(DATA_URL);
        const data = await response.json();
        
        let new_time = data['last_updated'];
        
        //If the conversation has been updated since we last checked, update local copy
        if (new_time > last_fetched){
            
            last_fetched = new_time;

            let conversation = data['messages'];

            loading = false;
            messages = conversation;

            //Do alert
            if (messages.length != 0) {
                if (messages.slice(-1)[0]['alert'] != null) {
                    show_alert = true;
                } else {
                    show_alert = false;
                }
                
            }

            //Scroll
            await tick();
            scrollToBottom(element);
        }
        else {
            //_depth is just to stop the function from ever falling into a never-ending recursion, only checks 5 times
            if (_depth < 5) {
                console.log('No response found, trying again...')
                check_for_messages(_depth = _depth + 1);
            }
        }
    }

    //LOADING NEW RESPONSE
    let loading = false;
    let new_temp_message = "";

    async function new_message_loading(query) {
        new_temp_message = query;
        loading = true;
        await tick();
        scrollToBottom(element);
    }

    export { check_for_messages , new_message_loading };


    //MODAL FOR EXPLANATION/SOURCES
    let modal_message;

    async function modalButtonPressed(message_id) {
        modal_message = messages[message_id]

        show_modal = true;
    }


    //CONTEXT
    let context = {};

    async function fetchContext() {
        const response = await fetch("http://localhost:5001/context");

        context = await response.json();
    }

    onMount(fetchContext);


</script>

<!-- CHAT -->
<div bind:this={element} class="chat-area">
    <Space h={100}/>
    <Stack align="center" justify="flex-start" spacing="lg">
        <div class="chat">
            {#if messages.length != 0}
                {#each messages as message, i}

                    <!--User bubble-->
                    {#if (message['user'])} 
                        <Flex justify="left">
                            <UserBubble>{message['content']}</UserBubble>
                            <div class="chat-offset"></div>
                        </Flex>

                    <!--AI bubble-->
                    {:else}
                        <Flex justify="right"> 
                            <div class="chat-offset"></div>
                            <AIBubble>
                                {message['content']}

                                <!--Responsibility text-->
                                {#if context['type'] == "doctor"}
                                    <Space h="xs" />
                                    <Center> 
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
                    <div class="chat-offset"></div>
                </Flex>
                <Flex justify="right">
                    <div class="chat-offset"></div>
                    <AIBubble><Loader variant='dots' color='orange'/></AIBubble>
                    <div style="width: 33px; "></div>
                </Flex>
            {/if}
        </div>
    </Stack>
    <Space h={120}/>
</div>


<!-- ALERT POPUP -->
{#if show_alert}
    <div class="alert-area">
        <Alert icon={InfoCircled}  title="OBS!" variant="light" color="red" withCloseButton closeButtonLabel="Stäng Varninig">
            {messages.slice(-1)[0]['alert']}
        </Alert>
    </div>
{/if}


<!-- MODAL -->
{#if show_modal}
    <Box>
        <Overlay on:click={() => (show_modal = false)} opacity={0.5} color='black' zIndex=4/>
    </Box>
    <div class="modal">
        <Paper style="position:relative; z-index: 5; max-height: 80vh; overflow:scroll;" shadow="md" color="white">
            <Tabs grow>

                <!-- SOURCES TAB -->
                <Tabs.Tab label='Källor' color='red'>
                    <!--No source-->
                    {#if modal_message['sources'] == null}
                        <Center>
                            <Text style="line-height: 1.5;">
                                Inga externa källor användes. Svaret är baserat på antingen intern data (t.ex. en patients journal) eller från chatbotens träning. Mer information om intern data kommer (nog) så småningom.
                            </Text>
                        </Center>

                    <!--String source-->
                    {:else if typeof modal_message['sources'] == 'string'}
                        <Center>
                            <Text style="line-height: 1.5;">
                                {modal_message['sources']}
                            </Text>
                        </Center>

                    <!--Formatted source with links-->
                    {:else}
                        <Stack spacing="xs">
                            {#each modal_message['sources'][1] as source}
                                <Text>
                                    <b>{source["title"]}</b> &nbsp;
                                    <a href={source["link"]} target="_blank" rel="noopener noreferrer">{source["link"]}</a>
                                </Text>
                                <Text>Utdrag: "{source["snippet"]}"</Text>
                                <Space h="sm"/>
                            {/each}
                        </Stack>
                    {/if}
                </Tabs.Tab>

                <!-- EXPLANATION TAB -->
                {#if modal_message['explanation'] != null}
                    <Tabs.Tab label='Förklarning' color='orange'>
                        <Center>
                            <Text style="line-height: 1.5;">
                                {modal_message['explanation']}
                            </Text>
                        </Center>
                    </Tabs.Tab>
                {:else}
                    <Tabs.Tab label='Förklaring' color='orange' disabled></Tabs.Tab>
                {/if}

            </Tabs>

            <!-- CURRENTLY DISCUSSED PATIENT -->
            {#if modal_message['patient'] != null}
                <Divider size='sm' color='#E9ECEF'/>
                <Center> 
                    <Text
                        size='sm'
                        weight='semibold'
                        style="line-height: 1.5;">
                            Patient: {modal_message['patient']}
                    </Text>
                </Center>
            {/if}
            
        </Paper>
    </div>
    
{/if}




<style>

    .chat-area {
        position: absolute; 
        left: 0px; 
        right: 0px; 
        top: 0px; 
        bottom: 0px; 
        overflow: auto;
    }

    .chat {
        position: relative;
        min-width: 500px;
        max-width: 1000px;
    }

    .chat-offset {
        width: 400px;
    }

    .modal {
        position: fixed; 
        top: 10vh; 
        left: 15vw; 
        width: 70vw; 
        max-height: 80vh; 
        z-index: 5; 
        padding: 25px
    }

    .alert-area {
        position: fixed;
        top: 90px;
        right: 50px;
        max-height: 200px;
        width: max-content;
    }


</style>