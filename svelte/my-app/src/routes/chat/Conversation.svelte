<script>
    import { Stack, Flex, Box, Button, Text, Paper, Overlay, Title, Space, Loader, Center, Tabs, Divider, Alert, exception } from '@svelteuidev/core';
    import UserBubble from './UserBubble.svelte';
    import AIBubble from './AIBubble.svelte';
    import { onMount, tick } from 'svelte';
    import { InfoCircled } from 'radix-icons-svelte';
    import { scale } from 'svelte/transition';

    const DATA_URL = 'http://localhost:5001/chat'

    export let messages = [];
    //let explanations = [];
    let show_alert = false;
    let show_modal = false;
    let element;

    let current_query = '';

    // Timer
    const timer = ms => new Promise(res => setTimeout(res,ms))

    // Get a generated response to the query
    export async function get_response(query, settings) {
        current_query = query;

        new_message_loading(query);

        //Send a update request. The backend will generate a response and update the conversation.
        const response = await fetch(DATA_URL, {
            method: "PUT",
            body: JSON.stringify({'query': query, 'settings': settings}),
            headers: {"Content-type": "application/json; charset=UTF-8"}
        });
        const data = await response.json();
        let conversation = data['messages'].slice();

        await manage_response(conversation);
    }

    // Update the front-end conversation to match the one in the backend
    // (is also used when the internet-bot wants to call a function)
    export async function get_conversation() {

        // Send a get request
        const response = await fetch(DATA_URL, {
            method: "GET",
        });
        const data = await response.json();

        let conversation = []
        conversation = data['messages'].slice();

        await manage_response(conversation);
    }

    // This function manages the conversation after a generation or get request to the backend
    async function manage_response(conversation) {

        if (conversation.length == 0) {
            messages = [];

            //Scroll
            await tick();
            scrollToBottom(element);
            return
        }

        if (conversation[conversation.length - 1]['additional_info']['final'] == false) {
            // wants to call function, continue


            // Show progress in loading message
            let function_call = conversation[conversation.length - 1]['function_call']
            let function_to_call = function_call['name']
            let function_arguments = function_call['arguments']
            new_message_loading(current_query, 
                "" + function_arguments['explanation'] + "\nSöker efter " + function_arguments['search_query'] + " på " + function_to_call + ".se")

            // let ai continue
            await get_conversation();

        } else {
            // Final response to the query

            //Remove loading message and update displayed conversation (messages)
            loading = false;
            temp_query = "";
            temp_response = "";
            messages = conversation;

            //Scroll
            await tick();
            scrollToBottom(element);

            //Do alert
            if (messages.length != 0) {
                if (messages[messages.length - 1]['additional_info']['alert'] != null) {
                    // Show alert, wait a few seconds, hide it again
                    show_alert = true;
                    await timer(5000);
                    show_alert = false;
                } else {
                    show_alert = false;
                }
            }
        }
    }

    // Auto scroll on load
    onMount(() => scrollToBottom(element))

    // SCROLL TO THE BOTTOM OF THE CONVERSATION
    const scrollToBottom = async (node) => {
        node.scroll({ top: node.scrollHeight, behavior: 'smooth' })
    }

    //LOADING NEW RESPONSE
    let loading = false;
    let temp_query = "";
    let temp_response = "";

    async function new_message_loading(query, loading_response="") {
        if (query != "") {
            temp_query = query;
        }
        if (loading_response != "") {
            temp_response = loading_response;
        }
        loading = true;
        await tick();
        scrollToBottom(element);
    }

    //MODAL FOR EXPLANATION/SOURCES
    let modal_message;
    let modal_sources;

    async function modalButtonPressed(message_id) {
        modal_sources = [];
        modal_message = messages[message_id];
        
        if (modal_message['additional_info']['chat_type'] == 'internet') {
            // Go through and add all sources
            modal_message['additional_info']['sources'].forEach(source => {
                modal_sources.push(source)
            });
        } else {
            modal_sources = modal_message['additional_info']['sources']
        }

        show_modal = true;
    }


    // This function splits text into text and links
    function splitTextWithLinks(text) {
        const regex = /\[(.*?)\]\((.*?)\)/;
        const resultArray = [];
        let startIndex = 0;
        let match;

        while ((match = text.slice(startIndex).match(regex)) !== null) {
            const fullMatch = match[0];
            const linkText = match[1];
            const linkURL = match[2];

            const textBeforeLink = text.slice(startIndex, startIndex + match.index);
            if (textBeforeLink) {
            resultArray.push({'type': 'text', 'content': textBeforeLink});
            }

            resultArray.push({'type': 'link', 'linktext': linkText, 'linkurl': linkURL})

            startIndex += match.index + fullMatch.length;
        }

        const remainingText = text.slice(startIndex);
        if (remainingText) {
            resultArray.push({'type': 'text', 'content': remainingText});
        }

        return resultArray;
    }


</script>

<!-- CHAT -->
<div bind:this={element} class="chat-area">
    <Space h={100}/>
    <Stack align="center" justify="flex-start" spacing="lg">
        <div class="chat">
            {#if messages.length != 0}
                {#each messages as message, i}

                    <!--User bubble-->
                    {#if (message['role'] == 'user')} 
                        <Flex justify="right">
                            <div class="chat-offset"></div>
                            <UserBubble>{message['content']}</UserBubble>
                        </Flex>

                    <!--AI bubble-->
                    {:else}
                        {#if (message['content'] != null)}
                        <Flex justify="left"> 

                            <!--Modal button-->
                            <Button on:click={() => modalButtonPressed(i)} variant='subtle' radius="sm" size="xs" ripple> ? </Button>

                            <AIBubble>
                                <Text
                                    size='md'
                                    weight='semibold'
                                    style="line-height: 1.5;">
                                        {#if message['additional_info']['chat_type'] == 'doctor'}
                                        Läkarassistent:
                                        {:else if message['additional_info']['chat_type'] == 'patient'}
                                        Patientassistent:
                                        {:else if message['additional_info']['chat_type'] == 'intranet'}
                                        Intranätsassistent:
                                        {:else if message['additional_info']['chat_type'] == 'internet'}
                                        Internetassistent:
                                        {/if}
                                </Text>

                                <!--Manages links in text-->
                                {#each splitTextWithLinks(message['content']) as message_part, i}
                                    {#if message_part['type'] == 'text'}
                                        {message_part['content']}
                                    {:else}
                                        <a href={message_part['linkurl']} target="_blank" rel="noopener noreferrer">{message_part["linktext"]}</a>
                                    {/if}
                                {/each}
                                    

                                <!--Responsibility text-->
                                {#if message['additional_info']['chat_type'] == 'doctor'}
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
                            <div class="chat-offset"></div>
                        </Flex>
                        {/if}
                    {/if}
                    <Space h="lg"/>
                {/each}
            {/if}

            <!--Loading response-->
            {#if loading}
                <Flex justify="right">
                    <div class="chat-offset"></div>
                    <UserBubble>{temp_query}</UserBubble>
                </Flex>
                <Space h="lg"/>
                <Flex justify="left">
                    <div style="width: 33px; "></div>
                    <AIBubble>
                        {#if temp_response != ""}
                            <Loader variant='dots' color='orange'/>    
                            <Space h="xs" />
                            <Center> 
                                {temp_response}
                            </Center>
                            
                        {:else}
                            <Loader variant='dots' color='orange'/>
                        {/if}
                    </AIBubble>
                    <div class="chat-offset"></div>
                </Flex>
                <Space h="lg"/>
            {/if}
        </div>
    </Stack>
    <Space h={120}/>
</div>


<!-- ALERT POPUP -->
{#if show_alert}
    <div class="alert-area">
        <Alert icon={InfoCircled}  title="OBS!" variant="light" color="red">
            {messages[messages.length - 1]['additional_info']['alert']}
        </Alert>
    </div>
{/if}


<!-- MODAL -->
{#if show_modal}
    <Box>
        <Overlay on:click={() => (show_modal = false)} opacity={0.5} color='black' zIndex=100/>
    </Box>
    <div class="modal" transition:scale={{ duration: 350 }}>
        <Paper style="position:relative; z-index: 5; max-height: 80vh; overflow:scroll;" shadow="md" color="white">
            <Tabs grow>

                <!-- SOURCES TAB -->
                <Tabs.Tab label='Källor' color='red'>
                    <!--No source-->
                    {#if modal_sources == null}
                        <Center>
                            <Text style="line-height: 1.5;">
                                Inga externa källor användes. Svaret är baserat på antingen intern data (t.ex. en patients journal) eller från chatbotens träning. Mer information om intern data kommer (nog) så småningom.
                            </Text>
                        </Center>

                    <!--String source-->
                    {:else if typeof modal_sources == 'string'}
                        <Center>
                            <Text style="line-height: 1.5;">
                                {modal_sources}
                            </Text>
                        </Center>

                    <!--Formatted source with links-->
                    {:else}
                        <Stack spacing="xs">
                            {#each modal_sources as source}
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
                {#if modal_message['additional_info']['explanation'] != null}
                    <Tabs.Tab label='Förklarning' color='orange'>
                        <Center>
                            <Text style="line-height: 1.5;">
                                {modal_message['additional_info']['explanation']}
                            </Text>
                        </Center>
                    </Tabs.Tab>
                {:else}
                    <Tabs.Tab label='Förklaring' color='orange' disabled></Tabs.Tab>
                {/if}

            </Tabs>

            <!-- CURRENTLY DISCUSSED PATIENT -->
            {#if modal_message['additional_info']['patient'] != null}
                <Divider size='sm' color='#E9ECEF'/>
                <Center> 
                    <Text
                        size='sm'
                        weight='semibold'
                        style="line-height: 1.5;">
                            Patient: {modal_message['additional_info']['patient']}
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
        width: 1000px;
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
        z-index: 101; 
        padding: 25px
    }

    .alert-area {
        position: fixed;
        bottom: 90px;
        left: 220px;
        max-height: 200px;
        width: max-content;
        z-index: 1000;
    }


</style>