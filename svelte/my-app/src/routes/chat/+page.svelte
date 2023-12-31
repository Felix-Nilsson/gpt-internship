<script>
    import { Group, Input , Button, Center, Burger, Stack, Text, Space, Divider, ActionIcon, Flex } from '@svelteuidev/core';
    import { onMount } from 'svelte';
    import { slide } from 'svelte/transition';
    import { goto } from '$app/navigation'
    import { PaperPlane } from 'radix-icons-svelte';

    import Conversation from "./Conversation.svelte";
    import Settings from "./Settings.svelte";
    import { preventTabClose } from "./preventTabClose";

    // ID of the current chat
    let chat_id = 0;
    // Array with a 'title' for each chat (it's the first user query for that chat)
    let chats_titles = [];
    let can_create_new_chat = false;

    let opened = false;
    let input = "";

    let current_credentials = {
            'success': false,
            'login_as': 'None',
            'username': 'None'
        };

    let show_settings
    let settings = {};

    // Backend adresses
    const CREDENTIALS_URL = 'http://localhost:5001/credentials'
    const CHATS_URL = 'http://localhost:5001/all-chats';

    let get_response;
    let update_conversation;

    
    const handleSubmit = async (e) => {

        //data contains the input
        let data = new FormData(e.target);
        
        //Clear input
        input = '';
        
        await get_response(data.get('prompt'), settings);
	}

    // Ensure that the user has logged in
    async function fetchCredentials() {
        try {
            let response = await fetch(CREDENTIALS_URL);
            response = await response.json()
            
            // Check if the response was successful
            if (response['success']) {
                current_credentials = response;
            } 

        } catch (error) {
            console.error('Error:', error);
        }
    }

    onMount(fetchCredentials);

    async function logout() {
        // Logout
        await fetch(CREDENTIALS_URL, {
            method: "DELETE",
        });
        goto("/");
    }

    

    async function setup_chats() {
        const response = await fetch(CHATS_URL, {
            method: "GET"
        });
        const data = await response.json();
        chats_titles = data;

        await update_conversation();
        await check_if_can_create_new_chat(chats_titles)
    }

    // Setup the chats on page load
    onMount(setup_chats);

    async function new_chat() {
        const response = await fetch(CHATS_URL, {
            method: "POST"
        });
        const data = await response.json();
        chat_id = 0;
        chats_titles = data;

        await update_conversation();
        await check_if_can_create_new_chat(chats_titles)
    }


    async function change_current_chat(chat_index) {
        chat_id = chat_index
        const response = await fetch(CHATS_URL, {
            method: "PUT",
            body: JSON.stringify({'new_id': chat_index}),
            headers: {"Content-type": "application/json; charset=UTF-8"}
        });
        const data = await response.json();
        chats_titles = data;

        await update_conversation();
        await check_if_can_create_new_chat(chats_titles)
    }

    async function delete_chat(chat_index) {
        // If we delete the current chat, move to the latest in the history
        if (chat_index == chat_id) {
            chat_id = 0;
        }
        const response = await fetch(CHATS_URL, {
            method: "PATCH",
            body: JSON.stringify({'delete_id': chat_index}),
            headers: {"Content-type": "application/json; charset=UTF-8"}
        });
        const data = await response.json();
        chats_titles = data;

        await update_conversation();
        await check_if_can_create_new_chat(chats_titles)
    }

    async function event_update_chats(event) {
        console.log('Event, updating chats')
        const response = await fetch(CHATS_URL, {
            method: "GET"
        });
        const data = await response.json();

        await check_if_can_create_new_chat(data)

        // Trigger a reload of the chat history pane
        chats_titles = data
    }

    async function check_if_can_create_new_chat(chats_titles) {
        can_create_new_chat = true
        chats_titles.forEach(title => {
            if (title == '') {
                // Title is empty -> empty chat -> do not let user create new chat
                can_create_new_chat = false                
            }
        });
    }

    let input_placeholders = {
        'patient': 'Prova att fråga om din journal',
        'doctor': 'Prova att fråga om dina patienter',
        'intranet': 'Prova att fråga om information på intranätet',
        'internet': 'Prova att fråga om sjukdomar, mediciner och behandlingar'
    };

    let chat_history_variant = {
        true: 'outline',
        false: 'subtle'
    };

</script>


<svelte:head>
    <title>Medicinsk AI-Hjälp</title> 
</svelte:head>

<!--Warn user about closing the tab-->
<div use:preventTabClose={true}/>


<!--Conversation-->
<Conversation on:update={event_update_chats} bind:get_response={get_response} bind:get_conversation={update_conversation} show_settings={show_settings} user_type={current_credentials['login_as']}/>

<!--Burger button-->
<div class="burger-button">
    <ActionIcon size={60} on:click={() => (opened = !opened)}> 
        <Burger color="cyan" {opened}/>
    </ActionIcon>
</div>


<!--Burger menu-->
{#if opened}
<div class="burger-menu" transition:slide={{ duration: 350, axis: 'x' }}> 

    <div style="position:absolute; top:0; right:0; height:100vh">
        <Divider orientation='vertical'/>
    </div>

    <Stack align="center" spacing="md">
        <!-- Leave room for the burger button -->
        <Space h={70}/>

        <!-- Create new chat button-->
        <Button fullSize on:click={new_chat} disabled={!can_create_new_chat} ripple
        style="overflow:hidden; width:200px;"
        >💬 Ny chatt</Button>
        
        <!-- Chat history -->
        <div style="height: calc(100vh - 300px); overflow: auto;">
        {#if chats_titles.length != 0}
            {#each chats_titles as title, i}
            <Flex gap={0} style="align: center;">
                <Button on:click={() => change_current_chat(i)} 
                    size={40} 
                    variant={chat_history_variant[(i == chat_id)]}
                    color='cyan'
                    style="width: 160px; padding: 5px; overflow: hidden; justify-content:left"
                    ripple>
                    {#if title == ''}
                        🗒️ (Ny chatt)
                    {:else if title.length > 12}
                        🗒️ {String(title).slice(0, 9) + ' ...'}
                    {:else}
                        🗒️ {title}
                    {/if}
                </Button>
                
                <ActionIcon on:click={() => delete_chat(i)} color='red' size={40}>
                    🗑️
                </ActionIcon>
            </Flex>
            {/each}
        {/if}
        </div>



        <!-- Logout button -->
        {#if current_credentials['success']}
            <Text
                style="line-height:1.5; position: absolute; bottom: 100px"
                color="#c0c0c0"
                size="md">
                    {current_credentials.username}
            </Text>
            <div style="position: absolute; bottom: 40px">
                <Button type="button" on:click={logout} color='red' ripple 
                style="overflow:hidden;width: 200px;">
                    👋 Logga ut
                </Button>
            </div>
        {/if}
    </Stack>
</div>
{/if}

<!--Input area-->
<div class="gradient-strip-bottom">
    <Center style="padding:20px">  
        <Group spacing="lg" direction="row">
                <form autocomplete="off" on:submit|preventDefault={handleSubmit}>
                    <Center>
                        <Group spacing="lg" direction="row">
                            <Input 
                                name="prompt"
                                bind:value={input}
                                variant="filled"
                                placeholder={input_placeholders[settings['chatbot_type']]}
                                radius="lg"
                                size="l"
                                style="width: calc(100vw - 680px);box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.07); border-radius: 8px;"   
                                >
                            </Input>
                            <Button color="teal" style="z-index:50000; position=relative; right:5px" ripple> <PaperPlane/> </Button>
                        </Group>
                    </Center>
                </form>
        </Group>
    </Center>
</div>


<!--Settings-->
<Settings bind:show_settings={show_settings} bind:settings={settings} bind:login_as={current_credentials['login_as']}></Settings>


<style>

    .burger-button {
        position: fixed;
        left: 20px;
        top: 20px;
        z-index: 13;
    }

    .burger-button:hover {
        background-color: #d2d2d2;
        border-radius: 5px;
    }

    .gradient-strip-bottom {
        background: white;
        position: fixed; 
        bottom: 0; 
        left: 0; 
        right: 0; 
        height: 80px;
        z-index: 11;
        box-shadow:0 -20px 30px 8px white
    }

    .burger-menu {
        background: white;
        position: fixed; 
        top: 0; 
        left: 0;  
        bottom: 0;
        padding: 20px;
        width: 200px;
        overflow: hidden;
        z-index: 12;
    }



</style>